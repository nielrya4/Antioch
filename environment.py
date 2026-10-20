import os


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


def _posix(path: str) -> str:
    """A path with forward slashes, as the virtual filesystem and URLs use."""
    return path.replace(os.sep, "/")


def _digest(data) -> str:
    """A short content hash, used to version URLs."""
    import hashlib
    if isinstance(data, str):
        data = data.encode("utf-8")
    return hashlib.sha1(data).hexdigest()[:10]


def _read_source(sources: dict, key: str, path: str) -> None:
    try:
        with open(path, "r", encoding="utf-8") as handle:
            sources[key] = handle.read()
    except Exception as e:
        print(f"Warning: could not bundle {path}: {e}")


def _write_bundle(output_dir: str, name: str, sources: dict) -> str:
    """Write a source bundle and return its content-versioned URL."""
    import json
    text = json.dumps(sources, separators=(",", ":"))
    with open(os.path.join(output_dir, name), "w", encoding="utf-8") as handle:
        handle.write(text)
    print(f"Bundled {len(sources)} Python files into {name}")
    return f"{name}?v={_digest(text)}"


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
        favicon: str = None,
        snapshot: bool = True
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

    The Python sources, assets and boot loader (antioch/boot.js) are versioned
    by content hash. `snapshot` lets the page keep a memory snapshot of the
    interpreter in IndexedDB and restore it on later visits instead of booting
    from scratch; it falls back to a normal boot if that is not possible.

    The page title is taken from the first of: `title`, the splash screen's
    <title>, `default_title`.
    """
    import os
    import glob
    import json
    from pathlib import Path

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

    # The framework is served from the output folder, so that copy is the one
    # to bundle and to take boot.js from; fall back to a local checkout if the
    # environment has not been initialised.
    framework_dir = next((d for d in (os.path.join(output_dir, "antioch"), "antioch")
                          if os.path.isdir(d)), None)
    if framework_dir is None:
        raise FileNotFoundError(
            "antioch library not found. Run init_environment() (or 'antioch env') first")
    boot_js = os.path.join(framework_dir, "boot.js")
    if not os.path.exists(boot_js):
        raise FileNotFoundError(
            f"{boot_js} not found: this project's antioch/ folder predates the boot loader. "
            "Delete the antioch/ folder and run 'antioch env' to copy in the current framework")

    # Application sources: the scripts folder, or loose .py files beside the build.
    app_sources = {}
    if os.path.exists(scripts_folder):
        app_files = [os.path.join(root, f)
                     for root, _dirs, files in os.walk(scripts_folder)
                     for f in files if f.endswith(".py")]
    else:
        app_files = glob.glob("*.py")
    for path in sorted(app_files):
        _read_source(app_sources, _posix(os.path.relpath(path, ".")), path)

    # Framework sources, keyed as they appear in the virtual filesystem.
    framework_sources = {}
    for root, _dirs, files in os.walk(framework_dir):
        for f in sorted(files):
            if f.endswith(".py"):
                path = os.path.join(root, f)
                key = "antioch/" + _posix(os.path.relpath(path, framework_dir))
                _read_source(framework_sources, key, path)

    # Assets are versioned by content, so an unchanged file stays cached
    # across deploys.
    asset_versions = {}
    if os.path.exists("assets"):
        for root, _dirs, files in os.walk("assets"):
            for f in files:
                path = os.path.join(root, f)
                with open(path, "rb") as handle:
                    asset_versions[_posix(os.path.relpath(path, "."))] = _digest(handle.read())

    # Every Python source travels in two bundles, not one request per file: a
    # hundred files would spend a hundred round trips before a line of Python
    # runs, invisible on localhost and ruinous over a real network. The
    # framework and the app are separate so that a deploy of the app alone
    # leaves the (much larger, rarely changing) framework bundle cached.
    # Each URL carries a hash of its content, so a changed bundle gets a new
    # URL and an unchanged one never has to be fetched again.
    bundles = [
        _write_bundle(output_dir, "antioch_sources.json", framework_sources),
        _write_bundle(output_dir, "python_sources.json", app_sources),
    ]

    main_script = next((c for c in (f"{_posix(os.path.normpath(scripts_folder))}/main.py", "main.py")
                        if c in app_sources), None)

    # Determine Pyodide source URLs
    if use_cdn_pyodide:
        pyodide_js_url = f"https://cdn.jsdelivr.net/pyodide/v{pyodide_version}/full/pyodide.js"
        pyodide_index_url = f"https://cdn.jsdelivr.net/pyodide/v{pyodide_version}/full/"
        pyodide_id = pyodide_version
    else:
        pyodide_js_url = "pyodide/pyodide.js"
        pyodide_index_url = "./pyodide/"
        # A snapshot only restores into the exact build that made it, and a
        # local runtime can be swapped without the config changing.
        lock = os.path.join(output_dir, "pyodide", "pyodide-lock.json")
        pyodide_id = "local"
        if os.path.exists(lock):
            with open(lock, "rb") as handle:
                pyodide_id = "local-" + _digest(handle.read())

    with open(boot_js, "rb") as handle:
        boot_js_url = f"antioch/boot.js?v={_digest(handle.read())}"

    boot_config = {
        "pyodide": {
            "id": pyodide_id,
            "jsURL": pyodide_js_url,
            "indexURL": pyodide_index_url,
            "packages": list(pyodide_packages or ["micropip"]),
        },
        "snapshot": bool(snapshot),
        "bundles": [{"url": url} for url in bundles],
        "assets": asset_versions,
        "mainScript": main_script,
        "extraDirs": list(additional_directories or []),
        "localPackages": list(local_packages or []),
        "pypiPackages": list(pypi_packages or []),
    }
    # "<" is escaped so no value can close the script element early.
    boot_config_json = json.dumps(boot_config, separators=(",", ":")).replace("<", "\\u003c")
    boot_head = (
        f'<script src="{pyodide_js_url}"></script>\n'
        f'<script type="application/json" id="antioch-boot">{boot_config_json}</script>\n'
        f'<script src="{boot_js_url}"></script>'
    )

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
{favicon_html}{boot_head}
{head_extras}
</head>
{body_tag}
{custom_body_content}
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
{favicon_html}{boot_head}
</head>
<body>
{body_content}
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
{favicon_html}{boot_head}

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



