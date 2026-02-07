#!/usr/bin/env python3
"""
Download and setup Pyodide runtime for Antioch

This script downloads the Pyodide runtime (~420MB) required to run Antioch applications.
Run this once after cloning the repository.
"""

import os
import sys
import urllib.request
import tarfile
import shutil
from pathlib import Path


# Pyodide configuration
PYODIDE_VERSION = "0.24.1"
PYODIDE_URL = f"https://github.com/pyodide/pyodide/releases/download/{PYODIDE_VERSION}/pyodide-{PYODIDE_VERSION}.tar.bz2"
PYODIDE_FILENAME = f"pyodide-{PYODIDE_VERSION}.tar.bz2"
PYODIDE_DIR = "pyodide"


def download_file(url, filename):
    """Download file with progress bar."""
    print(f"Downloading {filename} from {url}")
    print("This is a large file (~420MB) and may take several minutes...")

    def progress_hook(block_num, block_size, total_size):
        """Show download progress."""
        downloaded = block_num * block_size
        if total_size > 0:
            percent = min(100, downloaded * 100 / total_size)
            bar_length = 40
            filled_length = int(bar_length * downloaded / total_size)
            bar = '=' * filled_length + '-' * (bar_length - filled_length)

            mb_downloaded = downloaded / (1024 * 1024)
            mb_total = total_size / (1024 * 1024)

            sys.stdout.write(f'\r[{bar}] {percent:.1f}% ({mb_downloaded:.1f}/{mb_total:.1f} MB)')
            sys.stdout.flush()

    try:
        urllib.request.urlretrieve(url, filename, progress_hook)
        print("\nDownload complete!")
        return True
    except Exception as e:
        print(f"\nError downloading file: {e}")
        return False


def extract_archive(filename, target_dir):
    """Extract tar.bz2 archive."""
    print(f"\nExtracting {filename}...")

    try:
        with tarfile.open(filename, 'r:bz2') as tar:
            # Extract to temporary directory first
            temp_dir = "pyodide_temp"
            tar.extractall(temp_dir)

            # Move extracted contents to target directory
            extracted_dir = os.path.join(temp_dir, "pyodide")
            if os.path.exists(extracted_dir):
                if os.path.exists(target_dir):
                    print(f"Removing existing {target_dir} directory...")
                    shutil.rmtree(target_dir)

                shutil.move(extracted_dir, target_dir)
                shutil.rmtree(temp_dir)
                print(f"Extracted to {target_dir}/")
                return True
            else:
                print(f"Error: Expected directory 'pyodide' not found in archive")
                return False

    except Exception as e:
        print(f"Error extracting archive: {e}")
        return False


def cleanup(filename):
    """Remove downloaded archive."""
    try:
        if os.path.exists(filename):
            os.remove(filename)
            print(f"Cleaned up {filename}")
    except Exception as e:
        print(f"Warning: Could not remove {filename}: {e}")


def verify_installation():
    """Verify Pyodide was installed correctly."""
    required_files = [
        "pyodide/pyodide.js",
        "pyodide/pyodide.asm.js",
        "pyodide/pyodide-lock.json",
    ]

    missing = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing.append(file_path)

    if missing:
        print("\nWarning: Installation may be incomplete. Missing files:")
        for file_path in missing:
            print(f"  - {file_path}")
        return False

    print("\n✅ Pyodide installation verified!")
    return True


def main():
    """Main download and setup process."""
    print("=" * 60)
    print("Antioch - Pyodide Runtime Setup")
    print("=" * 60)
    print()

    # Check if already installed
    if os.path.exists(PYODIDE_DIR) and os.path.exists(f"{PYODIDE_DIR}/pyodide.js"):
        response = input(f"Pyodide directory already exists. Re-download? (y/N): ")
        if response.lower() != 'y':
            print("Setup cancelled.")
            return 0

    # Download
    if not download_file(PYODIDE_URL, PYODIDE_FILENAME):
        print("\n❌ Download failed. Please check your internet connection and try again.")
        return 1

    # Extract
    if not extract_archive(PYODIDE_FILENAME, PYODIDE_DIR):
        print("\n❌ Extraction failed.")
        cleanup(PYODIDE_FILENAME)
        return 1

    # Cleanup
    cleanup(PYODIDE_FILENAME)

    # Verify
    if not verify_installation():
        print("\n⚠️  Installation completed but verification found issues.")
        print("You may need to re-run this script or manually download Pyodide.")
        return 1

    print()
    print("=" * 60)
    print("Setup complete! You can now build Antioch applications.")
    print()
    print("Next steps:")
    print("  1. Edit scripts/main.py to create your application")
    print("  2. Run: python3 -m build")
    print("  3. Serve: python3 -m http.server -d output 8000")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    sys.exit(main())