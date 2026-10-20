#!/usr/bin/env python3
"""
Antioch CLI - Command-line interface for Antioch projects

Commands:
  antioch env       Initialize/setup the project environment
  antioch build     Build the project to output directory
  antioch run       Start development server
  antioch install   Install a package dependency
  antioch update    Update Antioch framework to latest from GitHub
"""

import argparse
import sys
import os
import shutil
import http.server
import socketserver
import ssl
import subprocess
import webbrowser
from pathlib import Path
from typing import Any, Dict, Optional

# environment.py is installed beside the CLI (~/.antioch/ or the repository root)
INSTALL_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(INSTALL_DIR))
# bundled tomli, for Pythons older than 3.11 (no tomllib)
sys.path.append(str(INSTALL_DIR / "vendor"))

try:
    import tomllib  # Python 3.11+
except ImportError:
    try:
        import tomli as tomllib  # Fallback for older Python
    except ImportError:
        # If neither available, we'll work with default config only
        tomllib = None

from environment import build_page, init_environment


class AntiochCLI:
    """Main CLI class for Antioch project management."""

    def __init__(self, config_path: str = "antioch.toml"):
        """Initialize CLI with configuration."""
        self.config_path = Path(config_path)
        self.config = self._load_config()

    @staticmethod
    def _find_framework() -> Optional[Path]:
        """Locate the antioch library: the installed copy beside the CLI, else an importable one."""
        installed = INSTALL_DIR / "antioch"
        if installed.exists():
            return installed
        try:
            import antioch
            return Path(antioch.__file__).parent
        except ImportError:
            return None

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from TOML file."""
        if not self.config_path.exists():
            print(f"📝 No {self.config_path} found. Creating default configuration...")
            config = self._default_config()
            self._create_default_toml()
            print(f"✅ Created {self.config_path}")
            print(f"   You can customize it for your project.\n")
            return config

        if tomllib is None:
            print("Warning: TOML parser not available (Python < 3.11 and tomli not installed)")
            print(f"Using default configuration, so {self.config_path} is ignored.")
            print("Fix: re-run the Antioch installer, or run: pip install tomli")
            return self._default_config()

        try:
            with open(self.config_path, 'rb') as f:
                return tomllib.load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
            print("Using default configuration.")
            return self._default_config()

    def _default_config(self) -> Dict[str, Any]:
        """Return default configuration."""
        return {
            'project': {
                'name': 'antioch-project',
                'version': '0.1.0',
                'entry_point': 'scripts/main.py'
            },
            'build': {
                'output_dir': 'output',
                'scripts_dir': 'scripts',
                'pyodide_source': 'cdn',
                'pyodide_version': '0.29.3'
            },
            'dependencies': {
                'pyodide_packages': ['micropip'],
                'pypi_packages': [],
                'local_packages': []
            },
            'server': {
                'host': 'localhost',
                'port': 8000,
                'auto_open': True
            }
        }

    def _create_default_toml(self):
        """Create a default antioch.toml file."""
        default_toml = """[project]
name = "antioch-project"
version = "0.1.0"
entry_point = "scripts/main.py"

[build]
output_dir = "output"
scripts_dir = "scripts"
pyodide_source = "cdn"  # Options: "local" or "cdn" (cdn recommended - smaller, auto-updates)
pyodide_version = "0.29.3"  # Used when pyodide_source = "cdn"
splash_file = ""  # Optional: .html or .py file rendered as a static splash screen while Pyodide loads
title = ""  # Optional: browser tab title. Falls back to the splash screen's <title>, then project.name
favicon = ""  # Optional: emoji (e.g. "🏛️"), path (e.g. "assets/favicon.png"), or URL
snapshot = true  # Keep an interpreter snapshot in the browser so repeat visits start faster

[dependencies]
# Pyodide built-in packages to load
pyodide_packages = [
    "micropip",
]

# PyPI packages to install via micropip
pypi_packages = [
    # Add packages like: "numpy", "pandas", etc.
]

# Local packages (paths relative to project root)
local_packages = []

[server]
host = "localhost"
port = 8000
auto_open = true  # Automatically open browser
"""
        with open(self.config_path, 'w') as f:
            f.write(default_toml)

    def cmd_env(self):
        """Initialize a new Antioch project with example files."""
        print("🔧 Setting up new Antioch project...")

        # Create config if it doesn't exist
        if not self.config_path.exists():
            self._create_default_toml()
            print(f"✅ Created {self.config_path}")

        # Create scripts directory with example
        scripts_dir = Path("scripts")
        if not scripts_dir.exists():
            print(f"📁 Creating {scripts_dir}/")
            scripts_dir.mkdir()

            # Create example main.py
            main_py = scripts_dir / "main.py"
            example_code = '''"""
Example Antioch Application

This is a starter template. Modify it to build your app!
"""
from antioch import *

def main():
    # Add page title
    DOM.add(
        H1("Welcome to Antioch!"),
        P("Edit scripts/main.py to start building your app.")
    )

    # Add a simple counter example
    count = 0

    counter_display = H2(f"Count: {count}")
    DOM.add(counter_display)

    increment_btn = Button("Increment", style={
        "padding": "10px 20px",
        "margin": "5px",
        "font-size": "16px",
        "cursor": "pointer"
    })

    decrement_btn = Button("Decrement", style={
        "padding": "10px 20px",
        "margin": "5px",
        "font-size": "16px",
        "cursor": "pointer"
    })
    
    DOM.add(
        Div(increment_btn, decrement_btn, style={"margin-top": "20px"})
    )
    
    @when(increment_btn.events.click)
    def increment(sender, *args):
        nonlocal count
        count += 1
        counter_display.set_text(f"Count: {count}")
        
    @when(decrement_btn.events.click)
    def decrement(sender, *args):
        nonlocal count
        count -= 1
        counter_display.set_text(f"Count: {count}")


if __name__ == "__main__":
    main()
'''
            with open(main_py, 'w') as f:
                f.write(example_code)
            print(f"✅ Created {main_py}")
        else:
            print(f"📁 {scripts_dir}/ already exists")

        # Create assets directory
        assets_dir = Path("assets")
        if not assets_dir.exists():
            print(f"📁 Creating {assets_dir}/")
            assets_dir.mkdir()

            # Create example CSS
            css_file = assets_dir / "styles.css"
            example_css = '''/* Custom styles for your Antioch app */

body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    background-color: #f5f5f5;
}

h1 {
    color: #333;
    border-bottom: 2px solid #007bff;
    padding-bottom: 10px;
}

button {
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    transition: background-color 0.2s;
}

button:hover {
    background-color: #0056b3;
}
'''
            with open(css_file, 'w') as f:
                f.write(example_css)
            print(f"✅ Created {css_file}")
        else:
            print(f"📁 {assets_dir}/ already exists")

        # Copy antioch library to project directory
        antioch_dest = Path("antioch")
        if not antioch_dest.exists():
            print(f"📁 Copying antioch library...")

            antioch_lib_path = self._find_framework()
            if antioch_lib_path is None:
                print("⚠️  Warning: Could not find antioch library!")

            if antioch_lib_path and antioch_lib_path.exists():
                shutil.copytree(antioch_lib_path, antioch_dest)
                print(f"✅ Copied antioch library to {antioch_dest}/")
            else:
                print("⚠️  Warning: Could not copy antioch library!")
        else:
            print(f"📁 {antioch_dest}/ already exists")

        print("\n✅ Project initialized!")
        print("\nNext steps:")
        print("  1. Edit scripts/main.py to build your app")
        print("  2. Run: antioch build")
        print("  3. Run: antioch run")
        print("\nHappy coding! 🚀")

    def cmd_build(self):
        """Build the project."""
        print("🚀 Building Antioch project...")

        build_config = self.config.get('build', {})
        output_dir = build_config.get('output_dir', 'output')
        scripts_dir = build_config.get('scripts_dir', 'scripts')
        use_cdn = build_config.get('pyodide_source', 'cdn') == 'cdn'

        # Check if scripts directory exists
        if not Path(scripts_dir).exists():
            print(f"\n⚠️  Warning: {scripts_dir}/ directory not found!")
            print(f"   Run 'antioch env' first to create a new project.\n")

        # A project's own antioch/ wins (for developing antioch itself)
        if Path("antioch").exists():
            antioch_lib_path = Path("antioch").resolve()
        else:
            antioch_lib_path = self._find_framework()
            if antioch_lib_path is None:
                print("⚠️  Warning: Could not find antioch library!")

        # Initialize build environment with antioch library path
        print(f"📦 Preparing build environment...")
        print(f"   Output: {output_dir}/")
        print(f"   Scripts: {scripts_dir}/")
        print(f"   Pyodide: {'CDN' if use_cdn else 'Local'}")

        result = init_environment(
            output_dir,
            scripts_dir,
            use_cdn_pyodide=use_cdn,
            antioch_source=str(antioch_lib_path)
        )
        if "Warning" not in result:
            print(f"✅ Environment ready")

        # Then build the page
        build_config = self.config.get('build', {})
        deps_config = self.config.get('dependencies', {})

        output_dir = build_config.get('output_dir', 'output')
        scripts_dir = build_config.get('scripts_dir', 'scripts')
        use_cdn = build_config.get('pyodide_source', 'local') == 'cdn'
        pyodide_version = build_config.get('pyodide_version', '0.29.3')

        pyodide_packages = deps_config.get('pyodide_packages', ['micropip'])
        pypi_packages = deps_config.get('pypi_packages', [])
        local_packages = deps_config.get('local_packages', [])

        print(f"\nGenerating HTML page...")
        print(f"Pyodide packages: {pyodide_packages}")
        print(f"PyPI packages: {pypi_packages}")
        print(f"Local packages: {local_packages}")

        try:
            result = build_page(
                filename=f"{output_dir}/index.html",
                scripts_folder=scripts_dir,
                pyodide_packages=pyodide_packages,
                local_packages=local_packages,
                pypi_packages=pypi_packages,
                use_cdn_pyodide=use_cdn,
                pyodide_version=pyodide_version,
                splash_file=build_config.get('splash_file') or None,
                title=build_config.get('title') or None,
                default_title=self.config.get('project', {}).get('name') or 'Antioch App',
                favicon=build_config.get('favicon') or None,
                snapshot=bool(build_config.get('snapshot', True))
            )
        except FileNotFoundError as e:
            print(f"\n❌ {e}")
            sys.exit(1)

        print(result)
        print("\n✅ Build complete!")
        print(f"\nTo view: antioch run")

    def _local_certificate(self):
        """
        A self-signed certificate for localhost, created on first use.

        Kept beside the CLI rather than in a project, so every project shares
        it and none commits a private key. Browsers show a warning for it
        until it is accepted once; Google sign-in accepts https://localhost as
        an origin regardless.
        """
        shared = INSTALL_DIR / "certs"
        cert_dir = shared if os.access(INSTALL_DIR, os.W_OK) else Path.home() / ".antioch" / "certs"
        for candidate in (shared, cert_dir):
            cert, key = candidate / "localhost.crt", candidate / "localhost.key"
            if cert.exists() and key.exists():
                return cert, key
        cert, key = cert_dir / "localhost.crt", cert_dir / "localhost.key"

        cert_dir.mkdir(parents=True, exist_ok=True)
        try:
            subprocess.run(
                ["openssl", "req", "-x509", "-newkey", "rsa:2048", "-nodes",
                 "-days", "825", "-subj", "/CN=localhost",
                 "-addext", "subjectAltName=DNS:localhost,IP:127.0.0.1",
                 "-keyout", str(key), "-out", str(cert)],
                check=True, capture_output=True, text=True)
        except (OSError, subprocess.CalledProcessError) as error:
            detail = getattr(error, "stderr", "") or error
            raise RuntimeError(
                f"Could not create a certificate with openssl: {detail}")
        key.chmod(0o600)
        return cert, key

    def cmd_run(self, port: int = None, https: bool = None):
        """Start development server."""
        server_config = self.config.get('server', {})
        if https is None:
            https = bool(server_config.get('https', False))
        build_config = self.config.get('build', {})

        host = server_config.get('host', 'localhost')
        port = port or server_config.get('port', 8000)
        auto_open = server_config.get('auto_open', True)
        output_dir = build_config.get('output_dir', 'output')

        # Check if output directory exists
        output_path = Path(output_dir)
        if not output_path.exists():
            print(f"Error: Output directory '{output_dir}' not found.")
            print("Run 'antioch build' first to build the project.")
            return

        # Check if index.html exists
        index_path = output_path / "index.html"
        if not index_path.exists():
            print(f"Error: index.html not found in '{output_dir}'.")
            print("Run 'antioch build' first to build the project.")
            return

        # Change to output directory
        os.chdir(output_dir)

        # Create server
        class Handler(http.server.SimpleHTTPRequestHandler):
            # Revalidate on every request so a rebuild shows up on reload;
            # without this the browser may keep serving the previous index.html.
            def end_headers(self):
                self.send_header("Cache-Control", "no-cache")
                super().end_headers()

        try:
            with socketserver.TCPServer((host, port), Handler) as httpd:
                if https:
                    cert, key = self._local_certificate()
                    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
                    context.load_cert_chain(str(cert), str(key))
                    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
                url = f"{'https' if https else 'http'}://{host}:{port}"
                print(f"🌐 Development server running at {url}")
                print(f"📁 Serving files from: {output_path.absolute()}")
                if https:
                    print("🔒 Self-signed certificate: accept the browser warning once. "
                          f"Register {url} under Authorized JavaScript origins "
                          "for Google sign-in.")
                print(f"\nPress Ctrl+C to stop the server")

                # Open browser
                if auto_open:
                    print(f"Opening browser...")
                    webbrowser.open(url)

                httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n👋 Server stopped")
        except RuntimeError as e:
            print(f"Error: {e}")
        except OSError as e:
            if "Address already in use" in str(e):
                print(f"Error: Port {port} is already in use.")
                print(f"Try a different port: antioch run --port <PORT>")
            else:
                print(f"Error starting server: {e}")

    def cmd_update(self, repo: str = None, branch: str = None, use_ssh: bool = False):
        """Update the installed Antioch framework to the latest version from GitHub."""
        import subprocess
        import tempfile

        # Default GitHub repository
        if not repo:
            if use_ssh:
                repo = "git@github.com:nielrya4/antioch.git"
            else:
                repo = "https://github.com/nielrya4/antioch.git"
        if not branch:
            branch = "master"

        print("🔄 Updating Antioch framework from GitHub...")
        print(f"   Repository: {repo}")
        print(f"   Branch: {branch}")
        print()

        # Check for git
        try:
            subprocess.run(['git', '--version'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ Error: git is not installed")
            print("Please install git to use 'antioch update'")
            return

        # Find the installed antioch location
        # Priority: same directory as CLI (installed version)
        cli_parent = INSTALL_DIR
        antioch_install_path = cli_parent / "antioch"

        if not antioch_install_path.exists():
            print(f"❌ Error: Could not find antioch installation at {antioch_install_path}")
            print("The antioch framework should be installed alongside the CLI")
            return

        print(f"📍 Found antioch at: {antioch_install_path}")

        if not os.access(cli_parent, os.W_OK):
            print(f"❌ Error: {cli_parent} is not writable by you")
            print("For a system-wide install, run the update with sudo (e.g. sudo antioch update)")
            return

        # Create temporary directory for clone
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_clone = Path(temp_dir) / "antioch-temp"

            print(f"⬇️  Cloning from GitHub...")
            try:
                subprocess.run(
                    ['git', 'clone', '--depth', '1', '--branch', branch, repo, str(temp_clone)],
                    capture_output=True,
                    check=True,
                    text=True
                )
            except subprocess.CalledProcessError as e:
                print(f"❌ Error cloning repository:")
                print(e.stderr)
                return

            # Check if antioch folder exists in clone
            new_antioch = temp_clone / "antioch"
            if not new_antioch.exists():
                print(f"❌ Error: No 'antioch' folder found in repository")
                return

            # Backup current antioch (just in case)
            backup_path = antioch_install_path.parent / "antioch.backup"
            if backup_path.exists():
                shutil.rmtree(backup_path)

            print(f"💾 Creating backup at: {backup_path}")
            shutil.copytree(antioch_install_path, backup_path)

            try:
                # Remove old antioch
                print(f"🗑️  Removing old version...")
                shutil.rmtree(antioch_install_path)

                # Copy new antioch
                print(f"📦 Installing new version...")
                shutil.copytree(new_antioch, antioch_install_path)

                    # vendor/ (tomli) is optional for older repositories; replace it if present
                new_vendor = temp_clone / "vendor"
                if new_vendor.exists():
                    shutil.rmtree(cli_parent / "vendor", ignore_errors=True)
                    shutil.copytree(new_vendor, cli_parent / "vendor")

                # Update the files that sit beside the framework: environment.py
                # builds pages and cli.py drives it, so they must move together.
                for name in ("environment.py", "cli.py"):
                    new_file = temp_clone / name
                    if new_file.exists():
                        print(f"📦 Updating {name}...")
                        # Replace atomically; cli.py is the file currently running
                        staged = cli_parent / f"{name}.new"
                        shutil.copy2(new_file, staged)
                        os.replace(staged, cli_parent / name)
                    else:
                        print(f"⚠️  No {name} found in repository, leaving existing one unchanged")
            except Exception as e:
                print(f"❌ Update failed: {e}")
                print("Restoring the previous version...")
                shutil.rmtree(antioch_install_path, ignore_errors=True)
                shutil.copytree(backup_path, antioch_install_path)
                return

            # Remove backup if successful
            shutil.rmtree(backup_path)

            print()
            print("✅ Antioch framework updated successfully!")
            print()
            print("The update includes:")
            print("  • Latest antioch framework library")
            print("  • Updated environment.py and cli.py")
            print("  • All themes and macros")
            print("  • Core functionality improvements")
            print()
            print("Your projects remain unchanged.")
            print()
            print("Run 'antioch build' to rebuild your project with the updated framework.")

    def cmd_install(self, package: str = None, dev: bool = False):
        """Install a package dependency."""
        if not package:
            print("Error: Please specify a package to install")
            print("Usage: antioch install <package>")
            return

        print(f"📦 Adding {package} to dependencies...")

        # Add to config in memory
        deps_config = self.config.setdefault('dependencies', {})
        pypi_packages = deps_config.setdefault('pypi_packages', [])

        if package in pypi_packages:
            print(f"'{package}' is already in dependencies")
            return

        pypi_packages.append(package)

        # Update TOML file (simple text manipulation)
        self._add_package_to_toml(package)
        print(f"✅ Added '{package}' to {self.config_path}")
        print(f"\nRun 'antioch build' to rebuild with new dependency")

    def _add_package_to_toml(self, package: str):
        """Add a package to the pypi_packages list in the TOML file."""
        if not self.config_path.exists():
            self._create_default_toml()

        with open(self.config_path, 'r') as f:
            lines = f.readlines()

        # Find the pypi_packages section and add the package
        in_pypi_section = False
        insert_index = None

        for i, line in enumerate(lines):
            if 'pypi_packages' in line and '=' in line:
                in_pypi_section = True
                # Check if it's an inline empty list
                if '[]' in line:
                    # Replace with multi-line format
                    lines[i] = 'pypi_packages = [\n'
                    lines.insert(i + 1, f'    "{package}",\n')
                    lines.insert(i + 2, ']\n')
                    break
            elif in_pypi_section:
                # Look for the closing bracket
                if ']' in line:
                    insert_index = i
                    # Insert before the closing bracket
                    indent = '    '
                    lines.insert(i, f'{indent}"{package}",\n')
                    break

        with open(self.config_path, 'w') as f:
            f.writelines(lines)


def main():
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        prog='antioch',
        description='Antioch - Python web framework CLI\n\nBuild Python web applications that run entirely in the browser using Pyodide.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Commands:
  env         Initialize new project (creates scripts/, assets/, antioch.toml, and antioch/)
  build       Build project to output/ directory (ready to serve)
  run         Start local development server from output/
  install     Add Python package to project dependencies
  update      Update Antioch framework to latest from GitHub

Examples:
  # Create a new project
  antioch env

  # Build the project
  antioch build

  # Start development server
  antioch run
  antioch run --port 3000
  antioch run --no-open

  # Add dependencies
  antioch install numpy
  antioch install pandas matplotlib

  # Update framework to latest version
  antioch update
  antioch update --branch dev
  antioch update --ssh  # Use SSH for private repos

Configuration:
  Edit antioch.toml to customize build settings, dependencies, and server options.

For more information, visit: https://github.com/nielrya4/antioch
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # env command
    subparsers.add_parser('env',
        help='Initialize new project with example files',
        description='Create a new Antioch project with starter files (scripts/main.py, assets/styles.css, antioch.toml, antioch/)')

    # build command
    subparsers.add_parser('build',
        help='Build the project to output directory',
        description='Build your Antioch project, creating output/index.html and copying all necessary files')

    # run command
    run_parser = subparsers.add_parser('run',
        help='Start development server',
        description='Start a local HTTP(S) server to view your built Antioch application')
    run_parser.add_argument('--port', type=int, help='Server port (default: 8000)')
    run_parser.add_argument('--no-open', action='store_true', help='Do not auto-open browser')
    run_parser.add_argument('--https', action='store_true', default=None,
                            help='Serve over HTTPS with a self-signed localhost certificate '
                                 '(also set by https = true under [server])')

    # install command
    install_parser = subparsers.add_parser('install',
        help='Add a Python package to dependencies',
        description='Add a package to antioch.toml dependencies (installed via micropip when app runs)')
    install_parser.add_argument('package', nargs='?', help='Package name from PyPI')
    install_parser.add_argument('--dev', action='store_true', help='Install as dev dependency (not implemented yet)')

    # update command
    update_parser = subparsers.add_parser('update',
        help='Update Antioch framework to latest from GitHub',
        description='Update the installed antioch framework library to the latest version from GitHub')
    update_parser.add_argument('--repo', type=str, help='GitHub repository URL (default: https://github.com/nielrya4/antioch.git)')
    update_parser.add_argument('--branch', type=str, help='Branch to install (default: master)')
    update_parser.add_argument('--ssh', action='store_true', help='Use SSH instead of HTTPS (requires SSH key setup)')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # Initialize CLI
    cli = AntiochCLI()

    # Override auto_open if --no-open is specified
    if args.command == 'run' and args.no_open:
        cli.config['server']['auto_open'] = False

    # Execute command
    if args.command == 'env':
        cli.cmd_env()
    elif args.command == 'build':
        cli.cmd_build()
    elif args.command == 'run':
        cli.cmd_run(port=args.port, https=args.https)
    elif args.command == 'install':
        cli.cmd_install(package=args.package, dev=args.dev)
    elif args.command == 'update':
        cli.cmd_update(repo=args.repo, branch=args.branch, use_ssh=args.ssh)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
