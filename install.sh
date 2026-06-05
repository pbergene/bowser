#!/usr/bin/env bash
# install.sh — Install Bowser and register it as the default browser on Fedora.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

LIB_DIR="${HOME}/.local/lib/bowser"
BIN_DIR="${HOME}/.local/bin"
APPLICATIONS_DIR="${HOME}/.local/share/applications"
BOWSER_CONFIG_DIR="${HOME}/.config/bowser"

echo "==> Installing Bowser from ${SCRIPT_DIR}"

# ── 1. Copy library files ──────────────────────────────────────────────────────
echo "--> Copying files to ${LIB_DIR}"
mkdir -p "${LIB_DIR}"
cp "${SCRIPT_DIR}/bowser.py" "${LIB_DIR}/bowser.py"
cp -r "${SCRIPT_DIR}/browsers" "${LIB_DIR}/browsers"
cp -r "${SCRIPT_DIR}/config" "${LIB_DIR}/config"

# ── 2. Create wrapper in PATH ──────────────────────────────────────────────────
echo "--> Creating wrapper at ${BIN_DIR}/bowser"
mkdir -p "${BIN_DIR}"
cat > "${BIN_DIR}/bowser" <<EOF
#!/usr/bin/env bash
exec python3 "${LIB_DIR}/bowser.py" "\$@"
EOF
chmod +x "${BIN_DIR}/bowser"

# ── 3. Ensure ~/.local/bin is on PATH ─────────────────────────────────────────
if [[ ":${PATH}:" != *":${BIN_DIR}:"* ]]; then
    echo "WARNING: ${BIN_DIR} is not in your PATH."
    echo "         Add the following to your shell profile:"
    echo "           export PATH=\"${BIN_DIR}:\${PATH}\""
fi

# ── 4. Install desktop entry ───────────────────────────────────────────────────
echo "--> Installing desktop entry to ${APPLICATIONS_DIR}"
mkdir -p "${APPLICATIONS_DIR}"
# Rewrite Exec path to use the installed wrapper.
sed "s|Exec=.*|Exec=${BIN_DIR}/bowser %u|" \
    "${SCRIPT_DIR}/bowser.desktop" \
    > "${APPLICATIONS_DIR}/bowser.desktop"
update-desktop-database "${APPLICATIONS_DIR}" 2>/dev/null || true

# ── 5. Register as default browser ────────────────────────────────────────────
echo "--> Registering Bowser as the default web browser"
xdg-mime default bowser.desktop x-scheme-handler/http
xdg-mime default bowser.desktop x-scheme-handler/https

# ── 6. Seed user config if absent ─────────────────────────────────────────────
if [[ ! -f "${BOWSER_CONFIG_DIR}/config.toml" ]]; then
    echo "--> Creating default config at ${BOWSER_CONFIG_DIR}/config.toml"
    mkdir -p "${BOWSER_CONFIG_DIR}"
    cp "${SCRIPT_DIR}/config/config.toml" "${BOWSER_CONFIG_DIR}/config.toml"
else
    echo "--> Config already exists at ${BOWSER_CONFIG_DIR}/config.toml (not overwritten)"
fi

echo ""
echo "==> Bowser installed successfully!"
echo "    Edit ${BOWSER_CONFIG_DIR}/config.toml to configure URL routing rules."
echo "    Run 'xdg-settings get default-web-browser' to verify registration."
