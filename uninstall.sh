#!/usr/bin/env bash
set -e

echo "Uninstalling Linux P2P Hotspot Manager..."

sudo rm -f /usr/local/bin/p2p-hotspot-manager
rm -f "$HOME/.local/share/applications/p2p-hotspot-manager.desktop"
update-desktop-database ~/.local/share/applications/

echo "Uninstalled successfully."
