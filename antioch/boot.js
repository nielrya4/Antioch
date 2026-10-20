/*
 * Antioch boot loader.
 *
 * index.html carries only a JSON config block (#antioch-boot) and this script.
 * Everything that happens between "the page opened" and "main.py is running"
 * lives here, so it is written once rather than pasted into every page shell.
 *
 * The slow parts overlap instead of queueing:
 *
 *   interpreter + Pyodide packages ─┐
 *   Python source bundles ──────────┼─> write the filesystem -> main.py
 *   assets ─────────────────────────┘
 *
 * With `snapshot` enabled, the interpreter is restored from a memory snapshot
 * kept in IndexedDB instead of being booted from scratch. The snapshot is of a
 * bare interpreter (no packages, no app code), so it depends only on the
 * Pyodide build and is shared by every Antioch app on the origin. Packages
 * still load after the restore, in parallel with the source download.
 */
(function () {
    "use strict";

    const cfg = JSON.parse(document.getElementById("antioch-boot").textContent);
    const started = performance.now();
    const elapsed = () => Math.round(performance.now() - started) + "ms";

    const domReady = new Promise((resolve) => {
        if (document.readyState === "loading") {
            document.addEventListener("DOMContentLoaded", resolve, { once: true });
        } else {
            resolve();
        }
    });

    // ---- Downloads ---------------------------------------------------------

    async function fetchBundle(bundle) {
        const response = await fetch(bundle.url);
        if (!response.ok) throw new Error("HTTP " + response.status + " for " + bundle.url);
        return response.json();
    }

    // Assets are fetched as bytes: they are not all text, and a UTF-8 string
    // round trip corrupts anything that is not.
    async function fetchAssets() {
        const paths = Object.keys(cfg.assets);
        const results = [];
        const CONCURRENCY = 12;
        for (let start = 0; start < paths.length; start += CONCURRENCY) {
            const batch = paths.slice(start, start + CONCURRENCY);
            results.push(...await Promise.all(batch.map(async (path) => {
                try {
                    const response = await fetch(path + "?v=" + cfg.assets[path]);
                    if (!response.ok) throw new Error("HTTP " + response.status);
                    return [path, new Uint8Array(await response.arrayBuffer())];
                } catch (e) {
                    console.warn("✗ Failed to load " + path + ":", e);
                    return null;
                }
            })));
        }
        return results.filter(Boolean);
    }

    // ---- Snapshot storage --------------------------------------------------

    const snapshots = (() => {
        const run = async (mode, operation) => {
            const db = await new Promise((resolve, reject) => {
                const request = indexedDB.open("antioch-boot", 1);
                request.onupgradeneeded = () => request.result.createObjectStore("snapshots");
                request.onsuccess = () => resolve(request.result);
                request.onerror = () => reject(request.error);
            });
            try {
                return await new Promise((resolve, reject) => {
                    const tx = db.transaction("snapshots", mode);
                    const request = operation(tx.objectStore("snapshots"));
                    tx.oncomplete = () => resolve(request.result);
                    tx.onerror = tx.onabort = () => reject(tx.error);
                });
            } finally {
                db.close();
            }
        };
        // Storage can be missing, blocked or full (private windows, quotas).
        // None of that may stop the app, so reads fail to "no snapshot".
        return {
            get: (key) => run("readonly", (s) => s.get(key)).catch(() => undefined),
            put: (key, value) => run("readwrite", (s) => s.put(value, key)),
            delete: (key) => run("readwrite", (s) => s.delete(key)).catch(() => {}),
        };
    })();

    const snapshotKey = "pyodide:" + cfg.pyodide.id;

    // Building a snapshot means booting a second interpreter. On the main
    // thread that is over a second of frozen page, so it happens in a worker,
    // after the app is up. The files it needs are already in the HTTP cache.
    function buildSnapshotInBackground() {
        const absolute = (url) => new URL(url, document.baseURI).href;
        const source = `
            self.onmessage = async (event) => {
                try {
                    importScripts(event.data.jsURL);
                    const py = await loadPyodide({ indexURL: event.data.indexURL, _makeSnapshot: true });
                    self.postMessage({ snapshot: py.makeMemorySnapshot() });
                } catch (e) {
                    self.postMessage({ error: String(e) });
                }
            };`;
        const url = URL.createObjectURL(new Blob([source], { type: "text/javascript" }));
        const worker = new Worker(url);
        const finish = () => { worker.terminate(); URL.revokeObjectURL(url); };
        worker.onmessage = async (event) => {
            finish();
            if (!event.data.snapshot) {
                console.warn("Snapshot not created:", event.data.error);
                return;
            }
            try {
                await snapshots.put(snapshotKey, event.data.snapshot);
                console.log("Saved interpreter snapshot for faster startup (" +
                    (event.data.snapshot.byteLength / 1e6).toFixed(0) + " MB)");
            } catch (e) {
                console.warn("Snapshot not saved:", e);
            }
        };
        worker.onerror = (event) => { finish(); console.warn("Snapshot worker failed:", event.message); };
        worker.postMessage({ jsURL: absolute(cfg.pyodide.jsURL), indexURL: absolute(cfg.pyodide.indexURL) });
    }

    // ---- Interpreter -------------------------------------------------------

    function withTimeout(promise, ms, what) {
        let timer;
        const timeout = new Promise((_, reject) => {
            timer = setTimeout(() => reject(new Error(what + " timed out after " + ms + "ms")), ms);
        });
        return Promise.race([promise, timeout]).finally(() => clearTimeout(timer));
    }

    async function bootInterpreter() {
        const indexURL = cfg.pyodide.indexURL;
        const packages = cfg.pyodide.packages;

        if (cfg.snapshot && "indexedDB" in window && typeof Worker !== "undefined") {
            const snapshot = await snapshots.get(snapshotKey);
            if (snapshot) {
                try {
                    // A snapshot the runtime cannot load does not always reject;
                    // Emscripten can fail and leave the promise pending forever.
                    // A healthy restore takes a fraction of a second, so the
                    // timeout only ever fires on a snapshot that is not coming.
                    const py = await withTimeout(
                        loadPyodide({ indexURL, _loadSnapshot: snapshot }), 10000, "Snapshot restore");
                    py.runPython("1 + 1");  // a damaged snapshot should fail here, not in the app
                    return { py, mode: "snapshot" };
                } catch (e) {
                    console.warn("Interpreter snapshot unusable, booting normally:", e);
                    await snapshots.delete(snapshotKey);
                }
            }
            // `packages` loads alongside the interpreter download.
            const py = await loadPyodide({ indexURL, packages });
            return { py, mode: "plain", wantsSnapshot: true };
        }
        return { py: await loadPyodide({ indexURL, packages }), mode: "plain" };
    }

    // ---- Filesystem --------------------------------------------------------

    function writeFiles(py, files) {
        const made = new Set();
        for (const [path, data] of files) {
            if (path.includes("..")) continue;
            const dir = "/" + path.split("/").slice(0, -1).join("/");
            if (dir.length > 1 && !made.has(dir)) {
                py.FS.mkdirTree(dir);
                made.add(dir);
            }
            try {
                py.FS.writeFile("/" + path, data);
            } catch (e) {
                console.warn("✗ Failed to write " + path + ":", e);
            }
        }
    }

    // ---- Packages ----------------------------------------------------------

    async function micropipInstall(py, names) {
        const globals = py.toPy({ names });
        try {
            await py.runPythonAsync("import micropip\nawait micropip.install(names)", { globals });
        } finally {
            globals.destroy();
        }
    }

    async function installPackages(py, names, label) {
        if (!names.length) return;
        console.log("Installing " + label + " packages:", names);
        try {
            await micropipInstall(py, names);  // one resolution for the lot
        } catch (e) {
            // One bad package should not take the others down with it.
            console.warn("Batch install failed, trying packages one at a time:", e);
            for (const name of names) {
                try {
                    await micropipInstall(py, [name]);
                } catch (err) {
                    console.warn("✗ Failed to install " + label + " package " + name + ":", err);
                }
            }
        }
    }

    // ---- Errors ------------------------------------------------------------

    function showError(err) {
        const html = `<div style="color:red; padding:20px;">
            <h3>Error loading application</h3>
            <p></p>
            <details><summary>Stack trace</summary><pre></pre></details>
        </div>`;
        const holder = document.getElementById("loading") || document.body.appendChild(document.createElement("div"));
        holder.innerHTML = html;
        holder.querySelector("p").textContent = err.message;
        holder.querySelector("pre").textContent = err.stack || "";
    }

    // ---- Boot --------------------------------------------------------------

    async function start() {
        // Start every download before waiting on any of them.
        const bundles = Promise.all(cfg.bundles.map(fetchBundle));
        const assets = fetchAssets();
        bundles.catch(() => {});  // reported where awaited; avoid a second, unhandled report

        const { py, mode, wantsSnapshot } = await bootInterpreter();

        const missing = cfg.pyodide.packages.filter((name) => !(name in py.loadedPackages));
        if (missing.length) {
            console.log("Loading Pyodide packages:", missing);
            await py.loadPackage(missing);
        }

        const sources = Object.assign({}, ...await bundles);
        py.FS.mkdirTree("/antioch/macros");
        py.FS.mkdirTree("/scripts");
        py.FS.mkdirTree("/assets");
        for (const dir of cfg.extraDirs) {
            try { py.FS.mkdirTree(dir); } catch (e) { console.warn("Could not create directory " + dir + ":", e); }
        }
        writeFiles(py, Object.entries(sources));
        writeFiles(py, await assets);

        let pythonPath = "import sys\n" + [
            "/", "/antioch", "/antioch/macros", "/antioch/macros/canvas_macros", "/scripts", ...cfg.extraDirs,
        ].map((dir) => "sys.path.insert(0, " + JSON.stringify(dir) + ")").join("\n");
        py.runPython(pythonPath);

        if ((cfg.localPackages.length || cfg.pypiPackages.length) && !("micropip" in py.loadedPackages)) {
            await py.loadPackage("micropip");
        }
        await installPackages(py, cfg.localPackages, "local");
        await installPackages(py, cfg.pypiPackages, "PyPI");

        // The app talks to the DOM, so it waits for the page even though
        // everything above did not.
        await domReady;

        if (cfg.mainScript) {
            let code = sources[cfg.mainScript];
            if (code === undefined) {
                code = await (await fetch(cfg.mainScript)).text();
            }
            console.log("Executing main script: " + cfg.mainScript);
            await py.runPythonAsync(code);
        } else {
            console.log("No main.py found, skipping execution");
        }

        const loading = document.getElementById("loading");
        const content = document.getElementById("content");
        if (loading) loading.style.display = "none";
        if (content) content.style.display = "block";
        console.log("🎉 Application loaded successfully! (" + elapsed() + ", interpreter: " + mode + ")");

        if (wantsSnapshot) {
            const idle = window.requestIdleCallback || ((callback) => setTimeout(callback, 1000));
            idle(() => buildSnapshotInBackground());
        }
    }

    start().catch(async (err) => {
        console.error("💥 Error loading application:", err);
        await domReady;
        showError(err);
    });
})();
