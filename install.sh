#!/usr/bin/env bash
set -e

echo "Installing Linux P2P Hotspot Manager..."

# 1. Install dependencies
echo "Installing system dependencies (tkinter, dnsmasq, iptables, qrencode)..."
sudo apt update
sudo apt install -y python3-tk dnsmasq iptables qrencode

# 2. Copy the main script
echo "Installing p2p-hotspot-manager to /usr/local/bin..."
sudo cp src/p2p-hotspot-manager.py /usr/local/bin/p2p-hotspot-manager
sudo chmod +x /usr/local/bin/p2p-hotspot-manager

# 3. Setup Desktop Entry
echo "Setting up desktop launcher..."
DESKTOP_FILE="$HOME/.local/share/applications/p2p-hotspot-manager.desktop"
cat > "$DESKTOP_FILE" << EOL
[Desktop Entry]
Name=P2P Hotspot Manager
Comment=Manage Wi-Fi Direct Hotspot
Exec=/usr/local/bin/p2p-hotspot-manager
Icon=network-wireless
Terminal=false
Type=Application
Categories=Settings;Network;
EOL

update-desktop-database ~/.local/share/applications/

echo "Installation complete! You can now launch 'P2P Hotspot Manager' from your application menu."
