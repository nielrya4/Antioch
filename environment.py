def init_environment(output_folder: str, scripts_folder: str = "scripts") -> str:
    """Setup antioch environment by copying necessary files to output folder."""
    import os
    import shutil
    from pathlib import Path

    output_path = Path(output_folder)

    # Create output directory
    output_path.mkdir(parents=True, exist_ok=True)
    print(f"Created output directory: {output_path}")

    # Copy pyodide folder if it exists
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
        print("Warning: pyodide folder not found")

    # Copy antioch library
    if os.path.exists("antioch"):
        antioch_dest = output_path / "antioch"
        if antioch_dest.exists():
            shutil.rmtree(antioch_dest)
        shutil.copytree("antioch", antioch_dest)
        print(f"Copied antioch library to {antioch_dest}")

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
        print(f"Copied {scripts_folder} folder to {assets_dest}")

    return f"Environment setup complete in {output_path}"

def build_page(
        filename: str,
        scripts_folder: str = "scripts",
        additional_directories: list = None,
        pyodide_packages: list = None,
        local_packages: list = None,
        pypi_packages: list = None
) -> str:
    """
    Generate Pyodide-powered HTML app for antioch library.

    - pyodide_packages: list of packages to load from Pyodide (numpy, matplotlib, etc.)
    - local_packages: list of local packages/directories to include as modules
    - pypi_packages: list of packages to install from PyPI via micropip
    """
    import os
    import glob
    from pathlib import Path

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

    # Generate the HTML template
    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Antioch - Python DOM Library</title>
<script src="pyodide/pyodide.js"></script>

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
        // Initialize Pyodide with local installation
        const pyodide = await loadPyodide({{ indexURL: "./pyodide/" }});
        
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
                    const content = await fetch(f).then(r=>r.text());
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
            const code = await fetch(mainScript).then(r=>r.text());
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



