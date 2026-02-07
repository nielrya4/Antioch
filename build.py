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

def main():
    print("🚀 Building Antioch Demo...")
    
    # Setup the complete environment in output folder (copies all files)
    print("Setting up environment...")
    env_result = init_environment("output", "scripts")
    print(env_result)
    
    # Build the HTML page in output folder
    print("Generating demo page...")
    print(f"Including Pyodide packages: {PYODIDE_PACKAGES}")
    print(f"Including PyPI packages: {PYPI_PACKAGES}")
    
    page_result = build_page(
        filename="output/index.html",
        scripts_folder="scripts",
        pyodide_packages=PYODIDE_PACKAGES,
        pypi_packages=PYPI_PACKAGES
    )
    
    print(page_result)
    print("\n✅ Build complete!")

if __name__ == "__main__":
    main()