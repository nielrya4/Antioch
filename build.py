#!/usr/bin/env python3
"""
Build script for Antioch library demo - creates self-contained static website
"""

from environment import build_page, init_environment

# Package Configuration
PYODIDE_PACKAGES = [
    'micropip',
    # Add other pyodide packages as needed
]

# PyPI packages to install via micropip
PYPI_PACKAGES = [
    # Add PyPI packages here if needed
]

# Pyodide Configuration
# Set to "local" to use local pyodide folder (requires download_pyodide.py)
# Set to "cdn" to load from CDN (smaller deployment, requires internet)
PYODIDE_SOURCE = "local"  # Options: "local" or "cdn"
PYODIDE_VERSION = "0.29.3"  # Used when PYODIDE_SOURCE = "cdn"

def main():
    print("🚀 Building Antioch Demo...")

    use_cdn = PYODIDE_SOURCE == "cdn"

    # Setup the complete environment in output folder (copies all files)
    print("Setting up environment...")
    env_result = init_environment("output", "scripts", use_cdn_pyodide=use_cdn)
    print(env_result)

    # Build the HTML page in output folder
    print("Generating demo page...")
    print(f"Pyodide source: {PYODIDE_SOURCE}" + (f" (v{PYODIDE_VERSION})" if use_cdn else ""))
    print(f"Including Pyodide packages: {PYODIDE_PACKAGES}")
    print(f"Including PyPI packages: {PYPI_PACKAGES}")

    page_result = build_page(
        filename="output/index.html",
        scripts_folder="scripts",
        pyodide_packages=PYODIDE_PACKAGES,
        pypi_packages=PYPI_PACKAGES,
        use_cdn_pyodide=use_cdn,
        pyodide_version=PYODIDE_VERSION
    )

    print(page_result)
    print("\n✅ Build complete!")

if __name__ == "__main__":
    main()