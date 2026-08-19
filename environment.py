def init_environment(output_folder: str, scripts_folder: str = "scripts", use_cdn_pyodide: bool = False, antioch_source: str = None) -> str:
    """Setup antioch environment by copying necessary files to output folder.

    Args:
        output_folder: Destination folder for build output
        scripts_folder: Source folder containing Python scripts
        use_cdn_pyodide: If True, skip copying pyodide (will load from CDN)
        antioch_source: Path to antioch library (if not in current directory)
    """
    import os
    import shutil
    from pathlib import Path

    output_path = Path(output_folder)

    # Create output directory
    output_path.mkdir(parents=True, exist_ok=True)
    print(f"Created output directory: {output_path}")

    # Copy pyodide folder if using local (not CDN)
    if not use_cdn_pyodide:
        pyodide_sources = ["./pyodide", "../pyodide", "pyodide"]
        for pyodide_src in pyodide_sources:
            if os.path.exists(pyodide_src):
                pyodide_dest = output_path / "pyodide"
                if pyodide_dest.exists():
                    shutil.rmtree(pyodide_dest)
                shutil.copytree(pyodide_src, pyodide_dest)
                print(f"Copied pyodide folder from {pyodide_src} to {pyodide_dest}")
                break
        else:
            print("Warning: pyodide folder not found - run download_pyodide.py first")
    else:
        print("Using CDN for Pyodide (skipping local copy)")

    # Copy antioch library
    # Use provided source, or look in current directory
    antioch_src = None
    if antioch_source and os.path.exists(antioch_source):
        antioch_src = antioch_source
    elif os.path.exists("antioch"):
        antioch_src = "antioch"

    if antioch_src:
        antioch_dest = output_path / "antioch"
        if antioch_dest.exists():
            shutil.rmtree(antioch_dest)
        shutil.copytree(antioch_src, antioch_dest)
        print(f"Copied antioch library to {antioch_dest}")
    else:
        print("Warning: antioch library not found")

    # Copy scripts folder
    if os.path.exists(scripts_folder):
        scripts_dest = output_path / "scripts"
        if scripts_dest.exists():
            shutil.rmtree(scripts_dest)
        shutil.copytree(scripts_folder, scripts_dest)
        print(f"Copied {scripts_folder} folder to {scripts_dest}")

    # Copy assets folder
    if os.path.exists("assets"):
        assets_dest = output_path / "assets"
        if assets_dest.exists():
            shutil.rmtree(assets_dest)
        shutil.copytree("assets", assets_dest)
        print(f"Copied assets folder to {assets_dest}")

    return f"Environment setup complete in {output_path}"


DEFAULT_PAGE_TITLE = "Antioch App"

FAVICON_MIME_TYPES = {
    ".png": "image/png",
    ".svg": "image/svg+xml",
    ".ico": "image/x-icon",
    ".gif": "image/gif",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
}


def _escape_html_text(text: str) -> str:
    """Escape text for use in element content or an attribute value."""
    return (str(text)
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;"))


def _extract_title(html: str):
    """The contents of a splash page's <title>, if it declares one."""
    import re

    match = re.search(r"<title[^>]*>(.*?)</title>", html, flags=re.DOTALL | re.IGNORECASE)
    if not match:
        return None
    title = match.group(1).strip()
    return title or None


def _emoji_favicon_href(emoji: str) -> str:
    """An emoji rendered as an inline SVG data URI, so no image file is needed."""
    from urllib.parse import quote

    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">'
           f'<text x="50%" y="50%" dy=".35em" text-anchor="middle" '
           f'font-size="80">{_escape_html_text(emoji)}</text></svg>')
    return "data:image/svg+xml," + quote(svg)


def _looks_like_emoji(favicon: str) -> bool:
    """Distinguish a literal emoji from a path or URL."""
    if len(favicon) > 8 or not favicon.strip():
        return False
    return not any(c in favicon for c in "/\\.:")


def _resolve_favicon(favicon: str, output_dir: str, scripts_folder: str):
    """
    Turn a favicon setting into (href, mime_type).

    Accepts an emoji, an absolute URL or data URI, or a path to an image file.
    Files that do not already live somewhere init_environment copies (assets/,
    the scripts folder) are copied next to the generated HTML, so the built
    output stays self-contained.
    """
    import os
    import shutil

    favicon = str(favicon).strip()
    if not favicon:
        return None, None

    if _looks_like_emoji(favicon):
        return _emoji_favicon_href(favicon), "image/svg+xml"

    lowered = favicon.lower()
    if lowered.startswith(("http://", "https://", "//", "data:")):
        mime = FAVICON_MIME_TYPES.get(os.path.splitext(lowered)[1])
        return favicon, mime

    mime = FAVICON_MIME_TYPES.get(os.path.splitext(lowered)[1])

    if not os.path.exists(favicon):
        print(f"Warning: favicon not found: {favicon}")
        return favicon.replace(os.sep, "/"), mime

    # Already inside a directory the build copies verbatim, so the relative
    # path stays correct in the output.
    normalized = os.path.normpath(favicon)
    copied_roots = [os.path.normpath("assets"), os.path.normpath(scripts_folder)]
    if any(normalized.startswith(root + os.sep) for root in copied_roots):
        return normalized.replace(os.sep, "/"), mime

    destination = os.path.join(output_dir, os.path.basename(favicon))
    try:
        os.makedirs(output_dir, exist_ok=True)
        if os.path.abspath(destination) != os.path.abspath(favicon):
            shutil.copyfile(favicon, destination)
        print(f"Copied favicon to {destination}")
    except Exception as e:
        print(f"Warning: could not copy favicon: {e}")

    return os.path.basename(favicon), mime


def _favicon_tags(href: str, mime: str) -> str:
    """The <link> tags for a resolved favicon, or an empty string."""
    if not href:
        return ""
    type_attr = f' type="{mime}"' if mime else ""
    escaped = _escape_html_text(href)
    return (f'<link rel="icon"{type_attr} href="{escaped}">\n'
            f'<link rel="apple-touch-icon" href="{escaped}">\n')


def _strip_icon_links(head_html: str) -> str:
    """Drop a splash page's icon links when the build supplies its own."""
    import re

    return re.sub(
        r'<link[^>]*rel=["\'][^"\']*\b(?:icon|apple-touch-icon)\b[^"\']*["\'][^>]*>',
        "", head_html, flags=re.IGNORECASE)


def build_page(
        filename: str,
        scripts_folder: str = "scripts",
        additional_directories: list = None,
        pyodide_packages: list = None,
        local_packages: list = None,
        pypi_packages: list = None,
        use_cdn_pyodide: bool = False,
        pyodide_version: str = "0.24.1",
        splash_html: str = None,
        splash_file: str = None,
        title: str = None,
        default_title: str = DEFAULT_PAGE_TITLE,
        favicon: str = None
) -> str:
    """
    Generate Pyodide-powered HTML app for antioch library.

    Args:
        filename: Output HTML filename
        scripts_folder: Source folder for Python scripts
        additional_directories: Extra directories to create in VFS
        pyodide_packages: list of packages to load from Pyodide (numpy, matplotlib, etc.)
        local_packages: list of local packages/directories to include as modules
        pypi_packages: list of packages to install from PyPI via micropip
        use_cdn_pyodide: If True, load Pyodide from CDN instead of local folder
        pyodide_version: Pyodide version to use when loading from CDN
        splash_html: Custom HTML for splash screen (overrides splash_file)
        splash_file: Path to .html or .py file for splash screen
                     - .html files are loaded directly
                     - .py files must define generate_splash() or main() function
        title: Page title. Overrides a title set by the splash screen.
        default_title: Used when neither `title` nor the splash screen sets one.
        favicon: Emoji, URL/data URI, or path to an image file. Overrides an
                 icon set by the splash screen.

    The page title is taken from the first of: `title`, the splash screen's
    <title>, `default_title`.
    """
    import os
    import glob
    import time
    from pathlib import Path

    # Generate cache-busting timestamp
    cache_buster = int(time.time() * 1000)  # milliseconds since epoch

    # Generate splash screen HTML
    body_content = None
    if splash_html:
        # Use provided splash HTML directly
        body_content = splash_html
        print("Using custom splash HTML")
    elif splash_file and os.path.exists(splash_file):
        # Check if it's an HTML file or Python file
        if splash_file.endswith('.html'):
            # Read HTML file directly
            print(f"Loading splash screen from {splash_file}")
            try:
                with open(splash_file, 'r', encoding='utf-8') as f:
                    body_content = f.read()
            except Exception as e:
                print(f"Error reading splash HTML file: {e}")
                body_content = None
        elif splash_file.endswith('.py'):
            # Execute Python splash file to generate HTML
            print(f"Generating splash screen from {splash_file}")
            try:
                import sys
                import importlib.util

                # Add antioch directory to sys.path so splash file can import antioch.static
                # Try to find antioch directory in common locations
                # Prioritize current working directory over installed version
                antioch_paths = [
                    Path.cwd() / "antioch",  # Current working directory (project's antioch)
                    Path(__file__).parent / "antioch",  # Same directory as environment.py (installed antioch)
                ]

                # CRITICAL: Remove any cached antioch imports so Python re-imports from the correct path
                # This ensures we use the local project's antioch, not the installed version
                antioch_modules = [key for key in sys.modules.keys() if key == 'antioch' or key.startswith('antioch.')]
                for mod in antioch_modules:
                    del sys.modules[mod]

                antioch_path_added = None
                for p in antioch_paths:
                    if p.exists() and p.is_dir():
                        antioch_path_str = str(p.parent)
                        if antioch_path_str not in sys.path:
                            sys.path.insert(0, antioch_path_str)
                            antioch_path_added = antioch_path_str
                        break

                # Load the splash module
                spec = importlib.util.spec_from_file_location("splash_module", splash_file)
                splash_module = importlib.util.module_from_spec(spec)
                sys.modules["splash_module"] = splash_module
                spec.loader.exec_module(splash_module)

                # Check for generate_splash() or main() function
                if hasattr(splash_module, 'generate_splash'):
                    result = splash_module.generate_splash()
                    if hasattr(result, 'render'):
                        body_content = result.render()
                    else:
                        body_content = str(result)
                elif hasattr(splash_module, 'main'):
                    result = splash_module.main()
                    if hasattr(result, 'render'):
                        body_content = result.render()
                    else:
                        body_content = str(result)
                else:
                    print(f"Warning: {splash_file} must define generate_splash() or main() function")

                # Clean up sys.path
                if antioch_path_added and antioch_path_added in sys.path:
                    sys.path.remove(antioch_path_added)

            except Exception as e:
                print(f"Error generating splash screen: {e}")
                import traceback
                traceback.print_exc()
                body_content = None
        else:
            print(f"Warning: splash_file must be .html or .py file, got: {splash_file}")
            body_content = None

    # Resolve the page title: explicit argument, then whatever the splash
    # screen declared, then the fallback.
    splash_title = _extract_title(body_content) if body_content else None
    page_title = _escape_html_text(title or splash_title or default_title
                                   or DEFAULT_PAGE_TITLE)

    output_dir = os.path.dirname(filename) or "."
    favicon_href, favicon_mime = _resolve_favicon(favicon, output_dir, scripts_folder) \
        if favicon else (None, None)
    favicon_html = _favicon_tags(favicon_href, favicon_mime)

    # Get all Python files from scripts folder
    python_files = []
    if os.path.exists(scripts_folder):
        for root, dirs, files in os.walk(scripts_folder):
            for file in files:
                if file.endswith(".py"):
                    rel_path = os.path.relpath(os.path.join(root, file), ".")
                    python_files.append(rel_path)
    else:
        # Fall back to current directory if scripts folder doesn't exist
        python_files = glob.glob("*.py")

    # Get all Python files from antioch library
    antioch_files = []
    if os.path.exists("antioch"):
        for root, dirs, files in os.walk("antioch"):
            for file in files:
                if file.endswith(".py"):
                    rel_path = os.path.relpath(os.path.join(root, file), ".")
                    antioch_files.append(rel_path)

    asset_files = []
    if os.path.exists("assets"):
        for root, dirs, files in os.walk("assets"):
            for file in files:
                rel_path = os.path.relpath(os.path.join(root, file), ".")
                asset_files.append(rel_path)

    # Determine Pyodide source URLs
    if use_cdn_pyodide:
        pyodide_js_url = f"https://cdn.jsdelivr.net/pyodide/v{pyodide_version}/full/pyodide.js"
        pyodide_index_url = f"https://cdn.jsdelivr.net/pyodide/v{pyodide_version}/full/"
    else:
        pyodide_js_url = "pyodide/pyodide.js"
        pyodide_index_url = "./pyodide/"

    # Build the body content
    if body_content:
        # Use custom splash screen (it's a full HTML page)
        # Extract just the body content and head extras if present
        if '<body' in body_content and '</body>' in body_content:
            # Extract head extras (styles, scripts, meta tags)
            head_extras = ""
            if '<head' in body_content and '</head>' in body_content:
                head_start = body_content.find('<head')
                head_start = body_content.find('>', head_start) + 1
                head_end = body_content.find('</head>')
                head_content = body_content[head_start:head_end]
                # Remove default tags we'll add ourselves
                import re
                head_content = re.sub(r'<meta charset[^>]*>', '', head_content)
                head_content = re.sub(r'<meta name="viewport"[^>]*>', '', head_content)
                head_content = re.sub(r'<title[^>]*>.*?</title>', '', head_content,
                                      flags=re.DOTALL | re.IGNORECASE)
                if favicon_html:
                    # The build's favicon wins; keeping both would emit two
                    # competing <link rel="icon"> tags.
                    head_content = _strip_icon_links(head_content)
                head_extras = head_content.strip()

            # Extract body and its attributes
            body_start = body_content.find('<body')
            body_tag_end = body_content.find('>', body_start)
            body_tag = body_content[body_start:body_tag_end+1]
            body_end = body_content.find('</body>')
            custom_body_content = body_content[body_tag_end+1:body_end].strip()

            # Generate the HTML template with custom splash
            html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{page_title}</title>
{favicon_html}<script src="{pyodide_js_url}"></script>
{head_extras}
</head>
{body_tag}
{custom_body_content}
<script>
async function initializeApp() {{
    try {{
        // Cache-busting timestamp - prevents browser from serving stale files
        const cacheBuster = {cache_buster};

        // Initialize Pyodide
        const pyodide = await loadPyodide({{ indexURL: "{pyodide_index_url}" }});

        // Load Pyodide packages first
        const pyodidePackages = {pyodide_packages or ['micropip']};
        console.log('Loading Pyodide packages:', pyodidePackages);
        await pyodide.loadPackage(pyodidePackages);

        const pythonFiles = {python_files};
        const assetFiles = {asset_files};
        const antiochFiles = {antioch_files};
        const extraDirs = {additional_directories or []};
        const localPkgs = {local_packages or []};
        const pypiPkgs = {pypi_packages or []};

        // --- Create directories in Pyodide FS ---
        console.log('Creating directories in Pyodide filesystem...');

        // Helper function to create directories recursively
        function createDirectoryRecursive(path) {{
            const parts = path.split('/').filter(p => p);
            let currentPath = '';
            for (const part of parts) {{
                currentPath += '/' + part;
                try {{
                    pyodide.FS.mkdir(currentPath);
                    console.log(`Created directory: ${{currentPath}}`);
                }} catch (e) {{
                    // Directory already exists, ignore
                }}
            }}
        }}

        // Create base directories
        createDirectoryRecursive("/antioch");
        createDirectoryRecursive("/antioch/macros");
        createDirectoryRecursive("/scripts");
        createDirectoryRecursive("/assets");

        // Create all needed directories from Python files
        const allFiles = [...pythonFiles, ...antiochFiles, ...assetFiles];
        for (const file of allFiles) {{
            const dirPath = file.substring(0, file.lastIndexOf('/'));
            if (dirPath && !dirPath.includes('..')) {{
                createDirectoryRecursive('/' + dirPath);
            }}
        }}

        // Create additional directories
        for(const d of extraDirs){{
            try{{
                pyodide.FS.mkdir(d);
                console.log(`Created directory: ${{d}}`);
            }}catch(e){{
                console.warn(`Directory ${{d}} already exists or could not be created`);
            }}
        }}

        // --- Load files into FS ---
        async function loadFiles(list, label){{
            console.log(`Loading ${{label}} files:`, list);
            for(const f of list){{
                try {{
                    const content = await fetch(f + '?v=' + cacheBuster).then(r=>r.text());
                    pyodide.FS.writeFile("/"+f, content);
                    console.log(`✓ Loaded ${{f}}`);
                }} catch(e){{
                    console.warn(`✗ Failed to load ${{f}}:`, e);
                }}
            }}
        }}

        // Load all Python files
        await loadFiles(antiochFiles, 'antioch');
        await loadFiles(pythonFiles, 'scripts');
        await loadFiles(assetFiles, 'assets');

        // --- Setup Python path ---
        console.log('Setting up Python path...');
        let pythonPathSetup = `
import sys
# Add core directories to Python path
sys.path.insert(0, '/')
sys.path.insert(0, '/antioch')
sys.path.insert(0, '/antioch/macros')
sys.path.insert(0, '/antioch/macros/canvas_macros')
sys.path.insert(0, '/scripts')`;

        // Add additional directories to Python path
        for(const d of extraDirs){{
            pythonPathSetup += `\\nsys.path.insert(0, '${{d}}')`;
        }}

        pythonPathSetup += `\\nprint('Python path updated with:', sys.path[:8])`;
        await pyodide.runPython(pythonPathSetup);

        // --- Install local packages ---
        if(localPkgs.length > 0) {{
            console.log('Installing local packages:', localPkgs);
            for(const pkg of localPkgs){{
                try {{
                    await pyodide.runPythonAsync(`import micropip; await micropip.install("${{pkg}}")`);
                    console.log(`✓ Installed local package: ${{pkg}}`);
                }} catch(e) {{
                    console.warn(`✗ Failed to install local package ${{pkg}}:`, e);
                }}
            }}
        }}

        // --- Install PyPI packages ---
        if(pypiPkgs.length > 0) {{
            console.log('Installing PyPI packages:', pypiPkgs);
            for(const pkg of pypiPkgs){{
                try {{
                    await pyodide.runPythonAsync(`import micropip; await micropip.install("${{pkg}}")`);
                    console.log(`✓ Installed PyPI package: ${{pkg}}`);
                }} catch(e) {{
                    console.warn(`✗ Failed to install PyPI package ${{pkg}}:`, e);
                }}
            }}
        }}

        // --- Execute main.py if exists ---
        let mainScript = pythonFiles.includes('{scripts_folder}/main.py')
                        ? '{scripts_folder}/main.py'
                        : (pythonFiles.includes('main.py') ? 'main.py' : null);

        if(mainScript){{
            console.log(`Executing main script: ${{mainScript}}`);
            const code = await fetch(mainScript + '?v=' + cacheBuster).then(r=>r.text());
            await pyodide.runPythonAsync(code);
            console.log(`✓ Executed ${{mainScript}}`);
        }} else {{
            console.log('No main.py found, skipping execution');
        }}

        // Hide loading and show content (if elements still exist)
        const loadingEl = document.getElementById("loading");
        const contentEl = document.getElementById("content");

        if (loadingEl) {{
            loadingEl.style.display = "none";
        }}
        if (contentEl) {{
            contentEl.style.display = "block";
        }}
        console.log('🎉 Application loaded successfully!');

    }} catch(err) {{
        console.error('💥 Error loading application:', err);
        const loadingEl = document.getElementById("loading");
        if (loadingEl) {{
            loadingEl.innerHTML =
                `<div style="color:red; padding:20px;">
                    <h3>Error loading application</h3>
                    <p>${{err.message}}</p>
                    <details><summary>Stack trace</summary><pre>${{err.stack}}</pre></details>
                </div>`;
        }} else {{
            // If loading element doesn't exist, create error display in body
            const errorDiv = document.createElement('div');
            errorDiv.innerHTML =
                `<div style="color:red; padding:20px;">
                    <h3>Error loading application</h3>
                    <p>${{err.message}}</p>
                    <details><summary>Stack trace</summary><pre>${{err.stack}}</pre></details>
                </div>`;
            document.body.appendChild(errorDiv);
        }}
    }}
}}

// Start loading when page is ready
window.addEventListener("DOMContentLoaded", initializeApp);
</script>
</body>
</html>'''
        else:
            # Custom splash didn't have proper HTML structure, use it as-is in body
            html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{page_title}</title>
{favicon_html}<script src="{pyodide_js_url}"></script>
</head>
<body>
{body_content}
<script>
async function initializeApp() {{
    try {{
        // Cache-busting timestamp - prevents browser from serving stale files
        const cacheBuster = {cache_buster};

        // Initialize Pyodide
        const pyodide = await loadPyodide({{ indexURL: "{pyodide_index_url}" }});

        // Load Pyodide packages first
        const pyodidePackages = {pyodide_packages or ['micropip']};
        console.log('Loading Pyodide packages:', pyodidePackages);
        await pyodide.loadPackage(pyodidePackages);

        const pythonFiles = {python_files};
        const assetFiles = {asset_files};
        const antiochFiles = {antioch_files};
        const extraDirs = {additional_directories or []};
        const localPkgs = {local_packages or []};
        const pypiPkgs = {pypi_packages or []};

        // --- Create directories in Pyodide FS ---
        console.log('Creating directories in Pyodide filesystem...');
        
        // Helper function to create directories recursively
        function createDirectoryRecursive(path) {{
            const parts = path.split('/').filter(p => p);
            let currentPath = '';
            for (const part of parts) {{
                currentPath += '/' + part;
                try {{
                    pyodide.FS.mkdir(currentPath);
                    console.log(`Created directory: ${{currentPath}}`);
                }} catch (e) {{
                    // Directory already exists, ignore
                }}
            }}
        }}
        
        // Create base directories
        createDirectoryRecursive("/antioch");
        createDirectoryRecursive("/antioch/macros");
        createDirectoryRecursive("/scripts");
        createDirectoryRecursive("/assets");
        
        // Create all needed directories from Python files
        const allFiles = [...pythonFiles, ...antiochFiles, ...assetFiles];
        for (const file of allFiles) {{
            const dirPath = file.substring(0, file.lastIndexOf('/'));
            if (dirPath && !dirPath.includes('..')) {{
                createDirectoryRecursive('/' + dirPath);
            }}
        }}

        // Create additional directories
        for(const d of extraDirs){{
            try{{ 
                pyodide.FS.mkdir(d); 
                console.log(`Created directory: ${{d}}`);
            }}catch(e){{ 
                console.warn(`Directory ${{d}} already exists or could not be created`);
            }}
        }}

        // --- Load files into FS ---
        async function loadFiles(list, label){{
            console.log(`Loading ${{label}} files:`, list);
            for(const f of list){{
                try {{
                    const content = await fetch(f + '?v=' + cacheBuster).then(r=>r.text());
                    pyodide.FS.writeFile("/"+f, content);
                    console.log(`✓ Loaded ${{f}}`);
                }} catch(e){{
                    console.warn(`✗ Failed to load ${{f}}:`, e);
                }}
            }}
        }}

        // Load all Python files
        await loadFiles(antiochFiles, 'antioch');
        await loadFiles(pythonFiles, 'scripts');
        await loadFiles(assetFiles, 'assets');

        // --- Setup Python path ---
        console.log('Setting up Python path...');
        let pythonPathSetup = `
import sys
# Add core directories to Python path
sys.path.insert(0, '/')
sys.path.insert(0, '/antioch')
sys.path.insert(0, '/antioch/macros')
sys.path.insert(0, '/antioch/macros/canvas_macros')
sys.path.insert(0, '/scripts')`;

        // Add additional directories to Python path
        for(const d of extraDirs){{
            pythonPathSetup += `\\nsys.path.insert(0, '${{d}}')`;
        }}
        
        pythonPathSetup += `\\nprint('Python path updated with:', sys.path[:8])`;
        await pyodide.runPython(pythonPathSetup);

        // --- Install local packages ---
        if(localPkgs.length > 0) {{
            console.log('Installing local packages:', localPkgs);
            for(const pkg of localPkgs){{
                try {{
                    await pyodide.runPythonAsync(`import micropip; await micropip.install("${{pkg}}")`); 
                    console.log(`✓ Installed local package: ${{pkg}}`);
                }} catch(e) {{
                    console.warn(`✗ Failed to install local package ${{pkg}}:`, e);
                }}
            }}
        }}

        // --- Install PyPI packages ---
        if(pypiPkgs.length > 0) {{
            console.log('Installing PyPI packages:', pypiPkgs);
            for(const pkg of pypiPkgs){{
                try {{
                    await pyodide.runPythonAsync(`import micropip; await micropip.install("${{pkg}}")`); 
                    console.log(`✓ Installed PyPI package: ${{pkg}}`);
                }} catch(e) {{
                    console.warn(`✗ Failed to install PyPI package ${{pkg}}:`, e);
                }}
            }}
        }}

        // --- Execute main.py if exists ---
        let mainScript = pythonFiles.includes('{scripts_folder}/main.py')
                        ? '{scripts_folder}/main.py'
                        : (pythonFiles.includes('main.py') ? 'main.py' : null);

        if(mainScript){{
            console.log(`Executing main script: ${{mainScript}}`);
            const code = await fetch(mainScript + '?v=' + cacheBuster).then(r=>r.text());
            await pyodide.runPythonAsync(code);
            console.log(`✓ Executed ${{mainScript}}`);
        }} else {{
            console.log('No main.py found, skipping execution');
        }}

        // Hide loading and show content (if elements still exist)
        const loadingEl = document.getElementById("loading");
        const contentEl = document.getElementById("content");
        
        if (loadingEl) {{
            loadingEl.style.display = "none";
        }}
        if (contentEl) {{
            contentEl.style.display = "block";
        }}
        console.log('🎉 Application loaded successfully!');

    }} catch(err) {{
        console.error('💥 Error loading application:', err);
        const loadingEl = document.getElementById("loading");
        if (loadingEl) {{
            loadingEl.innerHTML =
                `<div style="color:red; padding:20px;">
                    <h3>Error loading application</h3>
                    <p>${{err.message}}</p>
                    <details><summary>Stack trace</summary><pre>${{err.stack}}</pre></details>
                </div>`;
        }} else {{
            // If loading element doesn't exist, create error display in body
            const errorDiv = document.createElement('div');
            errorDiv.innerHTML = 
                `<div style="color:red; padding:20px;">
                    <h3>Error loading application</h3>
                    <p>${{err.message}}</p>
                    <details><summary>Stack trace</summary><pre>${{err.stack}}</pre></details>
                </div>`;
            document.body.appendChild(errorDiv);
        }}
    }}
}}

// Start loading when page is ready
window.addEventListener("DOMContentLoaded", initializeApp);
</script>
</body>
</html>'''
    else:
        # No custom splash - use default loading screen
        html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{page_title}</title>
{favicon_html}<script src="{pyodide_js_url}"></script>

<!-- JavaScript libraries are loaded dynamically when imported -->

<style>
body {{
    font-family: Arial, sans-serif;
    background: #f5f5f5;
    padding: 20px;
    margin: 0;
}}

#loading {{
    text-align: center;
    margin-top: 60px;
}}
#content {{
    display: none;
    max-width: 1200px;
    margin: 0 auto;
}}
.spinner {{
    width: 40px;
    height: 40px;
    border-radius: 50%;
    border: 4px solid #ccc;
    border-top-color: #037bfc;
    animation: spin 1.2s linear infinite;
    margin: auto;
}}
@keyframes spin {{
    0% {{ transform: rotate(0deg); }}
    100% {{ transform: rotate(360deg); }}
}}
</style>
</head>
<body>
<div id="loading">
    <div class="spinner"></div>
    <p>Loading Antioch Library...</p>
</div>
<div id="content"></div>

<script>
async function initializeApp() {{
    try {{
        // Cache-busting timestamp - prevents browser from serving stale files
        const cacheBuster = {cache_buster};

        // Initialize Pyodide
        const pyodide = await loadPyodide({{ indexURL: "{pyodide_index_url}" }});

        // Load Pyodide packages first
        const pyodidePackages = {pyodide_packages or ['micropip']};
        console.log('Loading Pyodide packages:', pyodidePackages);
        await pyodide.loadPackage(pyodidePackages);

        const pythonFiles = {python_files};
        const assetFiles = {asset_files};
        const antiochFiles = {antioch_files};
        const extraDirs = {additional_directories or []};
        const localPkgs = {local_packages or []};
        const pypiPkgs = {pypi_packages or []};

        // --- Create directories in Pyodide FS ---
        console.log('Creating directories in Pyodide filesystem...');

        // Helper function to create directories recursively
        function createDirectoryRecursive(path) {{
            const parts = path.split('/').filter(p => p);
            let currentPath = '';
            for (const part of parts) {{
                currentPath += '/' + part;
                try {{
                    pyodide.FS.mkdir(currentPath);
                    console.log(`Created directory: ${{currentPath}}`);
                }} catch (e) {{
                    // Directory already exists, ignore
                }}
            }}
        }}

        // Create base directories
        createDirectoryRecursive("/antioch");
        createDirectoryRecursive("/antioch/macros");
        createDirectoryRecursive("/scripts");
        createDirectoryRecursive("/assets");

        // Create all needed directories from Python files
        const allFiles = [...pythonFiles, ...antiochFiles, ...assetFiles];
        for (const file of allFiles) {{
            const dirPath = file.substring(0, file.lastIndexOf('/'));
            if (dirPath && !dirPath.includes('..')) {{
                createDirectoryRecursive('/' + dirPath);
            }}
        }}

        // Create additional directories
        for(const d of extraDirs){{
            try{{
                pyodide.FS.mkdir(d);
                console.log(`Created directory: ${{d}}`);
            }}catch(e){{
                console.warn(`Directory ${{d}} already exists or could not be created`);
            }}
        }}

        // --- Load files into FS ---
        async function loadFiles(list, label){{
            console.log(`Loading ${{label}} files:`, list);
            for(const f of list){{
                try {{
                    const content = await fetch(f + '?v=' + cacheBuster).then(r=>r.text());
                    pyodide.FS.writeFile("/"+f, content);
                    console.log(`✓ Loaded ${{f}}`);
                }} catch(e){{
                    console.warn(`✗ Failed to load ${{f}}:`, e);
                }}
            }}
        }}

        // Load all Python files
        await loadFiles(antiochFiles, 'antioch');
        await loadFiles(pythonFiles, 'scripts');
        await loadFiles(assetFiles, 'assets');

        // --- Setup Python path ---
        console.log('Setting up Python path...');
        let pythonPathSetup = `
import sys
# Add core directories to Python path
sys.path.insert(0, '/')
sys.path.insert(0, '/antioch')
sys.path.insert(0, '/antioch/macros')
sys.path.insert(0, '/antioch/macros/canvas_macros')
sys.path.insert(0, '/scripts')`;

        // Add additional directories to Python path
        for(const d of extraDirs){{
            pythonPathSetup += `\\nsys.path.insert(0, '${{d}}')`;
        }}

        pythonPathSetup += `\\nprint('Python path updated with:', sys.path[:8])`;
        await pyodide.runPython(pythonPathSetup);

        // --- Install local packages ---
        if(localPkgs.length > 0) {{
            console.log('Installing local packages:', localPkgs);
            for(const pkg of localPkgs){{
                try {{
                    await pyodide.runPythonAsync(`import micropip; await micropip.install("${{pkg}}")`);
                    console.log(`✓ Installed local package: ${{pkg}}`);
                }} catch(e) {{
                    console.warn(`✗ Failed to install local package ${{pkg}}:`, e);
                }}
            }}
        }}

        // --- Install PyPI packages ---
        if(pypiPkgs.length > 0) {{
            console.log('Installing PyPI packages:', pypiPkgs);
            for(const pkg of pypiPkgs){{
                try {{
                    await pyodide.runPythonAsync(`import micropip; await micropip.install("${{pkg}}")`);
                    console.log(`✓ Installed PyPI package: ${{pkg}}`);
                }} catch(e) {{
                    console.warn(`✗ Failed to install PyPI package ${{pkg}}:`, e);
                }}
            }}
        }}

        // --- Execute main.py if exists ---
        let mainScript = pythonFiles.includes('{scripts_folder}/main.py')
                        ? '{scripts_folder}/main.py'
                        : (pythonFiles.includes('main.py') ? 'main.py' : null);

        if(mainScript){{
            console.log(`Executing main script: ${{mainScript}}`);
            const code = await fetch(mainScript + '?v=' + cacheBuster).then(r=>r.text());
            await pyodide.runPythonAsync(code);
            console.log(`✓ Executed ${{mainScript}}`);
        }} else {{
            console.log('No main.py found, skipping execution');
        }}

        // Hide loading and show content (if elements still exist)
        const loadingEl = document.getElementById("loading");
        const contentEl = document.getElementById("content");

        if (loadingEl) {{
            loadingEl.style.display = "none";
        }}
        if (contentEl) {{
            contentEl.style.display = "block";
        }}
        console.log('🎉 Application loaded successfully!');

    }} catch(err) {{
        console.error('💥 Error loading application:', err);
        const loadingEl = document.getElementById("loading");
        if (loadingEl) {{
            loadingEl.innerHTML =
                `<div style="color:red; padding:20px;">
                    <h3>Error loading application</h3>
                    <p>${{err.message}}</p>
                    <details><summary>Stack trace</summary><pre>${{err.stack}}</pre></details>
                </div>`;
        }} else {{
            // If loading element doesn't exist, create error display in body
            const errorDiv = document.createElement('div');
            errorDiv.innerHTML =
                `<div style="color:red; padding:20px;">
                    <h3>Error loading application</h3>
                    <p>${{err.message}}</p>
                    <details><summary>Stack trace</summary><pre>${{err.stack}}</pre></details>
                </div>`;
            document.body.appendChild(errorDiv);
        }}
    }}
}}

// Start loading when page is ready
window.addEventListener("DOMContentLoaded", initializeApp);
</script>
</body>
</html>'''

    # Create output directory if needed
    output_path = Path(filename).parent
    if output_path != Path('.'):
        output_path.mkdir(parents=True, exist_ok=True)

    # Write the HTML file
    out = Path(filename)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html_content, encoding="utf-8")
    return f"✓ Generated: {filename}"



