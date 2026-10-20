#!/usr/bin/env bash
# Antioch installer
#
#   curl -sSL https://raw.githubusercontent.com/nielrya4/Antioch/master/install.sh | bash
#
# Installs the latest Antioch from GitHub: the framework (antioch/) and the
# files that sit beside it (cli.py, environment.py, vendor/), plus an `antioch` command.
# Running it again upgrades an existing installation.
#
# Options (when piping, pass them after `bash -s --`):
#   --system        Install to /opt/antioch with the command in /usr/local/bin (needs sudo)
#   --repo URL      Install from another repository
#   --branch NAME   Install from another branch (default: master)
#   --uninstall     Remove Antioch
#   --help, -h      Show this help

set -euo pipefail

INSTALL_DIR="${HOME}/.antioch"
BIN_DIR="${HOME}/.local/bin"
GITHUB_REPO="https://github.com/nielrya4/Antioch.git"
GITHUB_BRANCH="master"
UNINSTALL=false
SYSTEM_WIDE=false

# Everything outside antioch/ that the CLI needs, copied from the repository root.
# vendor/ holds tomli, which Pythons before 3.11 need to read antioch.toml.
BOOT_FILES=(cli.py environment.py)
BOOT_DIRS=(antioch vendor)

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

step()    { echo -e "${GREEN}▶${NC} $1"; }
success() { echo -e "${GREEN}✓${NC} $1"; }
warn()    { echo -e "${YELLOW}⚠${NC} $1"; }
fail()    { echo -e "${RED}✗${NC} $1" >&2; exit 1; }

usage() {
    cat << 'USAGE'
Antioch installer

Usage: install.sh [--system] [--repo URL] [--branch NAME] [--uninstall]

  --system        Install to /opt/antioch with the command in /usr/local/bin (needs root)
  --repo URL      Install from another repository
  --branch NAME   Install from another branch (default: master)
  --uninstall     Remove Antioch

When piping from curl, pass options after `bash -s --`.
USAGE
}

while [[ $# -gt 0 ]]; do
    case $1 in
        --uninstall) UNINSTALL=true; shift ;;
        --system)    SYSTEM_WIDE=true; INSTALL_DIR="/opt/antioch"; BIN_DIR="/usr/local/bin"; shift ;;
        --repo)      GITHUB_REPO="${2:?--repo needs a URL}"; shift 2 ;;
        --branch)    GITHUB_BRANCH="${2:?--branch needs a name}"; shift 2 ;;
        --help|-h)   usage; exit 0 ;;
        *)           fail "Unknown option: $1 (use --help)" ;;
    esac
done

if [ "$SYSTEM_WIDE" = true ] && [ "$EUID" -ne 0 ]; then
    fail "System-wide installation needs root: curl -sSL <url> | sudo bash -s -- --system"
fi

if [ "$UNINSTALL" = true ]; then
    step "Removing $INSTALL_DIR and $BIN_DIR/antioch"
    rm -rf "$INSTALL_DIR"
    rm -f "$BIN_DIR/antioch"
    success "Antioch has been uninstalled"
    exit 0
fi

step "Checking requirements..."
command -v python3 >/dev/null || fail "Python 3.9 or higher is required (python3 not found)"
python3 -c 'import sys; sys.exit(sys.version_info < (3, 9))' \
    || fail "Python 3.9 or higher is required (found $(python3 -c 'import platform; print(platform.python_version())'))"
command -v git >/dev/null || fail "git is required to download Antioch"

TEMP_CLONE=$(mktemp -d)
trap 'rm -rf "$TEMP_CLONE"' EXIT

step "Downloading $GITHUB_REPO (branch: $GITHUB_BRANCH)"
git clone --quiet --depth 1 --branch "$GITHUB_BRANCH" "$GITHUB_REPO" "$TEMP_CLONE/src" \
    || fail "Could not clone $GITHUB_REPO (branch $GITHUB_BRANCH)"

SRC="$TEMP_CLONE/src"
for dir in "${BOOT_DIRS[@]}"; do
    [ -d "$SRC/$dir" ] || fail "No $dir/ directory in the repository"
done
for file in "${BOOT_FILES[@]}"; do
    [ -f "$SRC/$file" ] || fail "No $file in the repository"
done

step "Installing to $INSTALL_DIR"
mkdir -p "$INSTALL_DIR" "$BIN_DIR"

# Replace the directories wholesale so files deleted upstream don't linger.
# Anything else in the install directory (e.g. certs/) is left alone.
for dir in "${BOOT_DIRS[@]}"; do
    rm -rf "$INSTALL_DIR/$dir"
    cp -R "$SRC/$dir" "$INSTALL_DIR/$dir"
done
for file in "${BOOT_FILES[@]}"; do
    cp "$SRC/$file" "$INSTALL_DIR/$file.new"
    mv -f "$INSTALL_DIR/$file.new" "$INSTALL_DIR/$file"
done
chmod +x "$INSTALL_DIR/cli.py"
find "$INSTALL_DIR/antioch" "$INSTALL_DIR/vendor" -name __pycache__ -type d -prune -exec rm -rf {} +

cat > "$BIN_DIR/antioch" << EOF
#!/usr/bin/env bash
# Antioch CLI - written by install.sh
exec python3 "$INSTALL_DIR/cli.py" "\$@"
EOF
chmod +x "$BIN_DIR/antioch"
success "Installed $BIN_DIR/antioch"

if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    echo
    warn "$BIN_DIR is not in your PATH. Add this to ~/.bashrc or ~/.zshrc:"
    echo
    echo "    export PATH=\"$BIN_DIR:\$PATH\""
fi

echo
success "Antioch is installed. Try:  antioch --help"
echo "  Upgrade later with:  antioch update"
