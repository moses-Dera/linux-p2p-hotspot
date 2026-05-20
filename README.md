# Linux P2P Hotspot Manager

A lightweight, robust graphical desktop application for Ubuntu/Linux that creates a Wi-Fi Hotspot by forcing your hardware into a Wi-Fi Direct (P2P Group Owner) mode. 

## The Problem

Have you ever tried to turn on the default Ubuntu Wi-Fi Hotspot while connected to a 5 GHz Wi-Fi network, only for it to instantly crash or silently fail? 

This happens because of two strict limitations in the Linux networking stack:
1. **The `NO-IR` Regulatory Flag:** Many 5 GHz frequencies are legally marked as "No Initiate Radiation", meaning the Linux kernel physically forbids your Wi-Fi card from broadcasting a standard router signal on that frequency.
2. **The `#channels <= 1` Hardware Limit:** Most laptop Wi-Fi cards only have one antenna. They cannot connect to a 5 GHz router and broadcast a 2.4 GHz hotspot simultaneously without time-slicing.

Standard hotspot tools (like `linux-wifi-hotspot` or GNOME's built-in hotspot) try to start a Standard AP (`mode 2`), which gets instantly blocked by these rules.

## The Solution (The Loophole)

This application bypasses these restrictions by utilizing the **Wi-Fi Direct (P2P GO)** loophole. It tricks `wpa_supplicant` into treating the hotspot as a peer-to-peer connection, which is often the *only* mode the Linux kernel allows under these strict conditions.

It packages all the complex underlying routing, DHCP, and firewall rules into a simple, single-click GUI.

### Features
- 🚀 **Bypass 5GHz Hardware Locks:** Share your internet even when the default GNOME hotspot refuses to start.
- 📱 **Instant QR Code:** Automatically generates a scannable QR code so iPhones and Androids can connect instantly without typing passwords.
- 🛡️ **Built-in Firewall Management:** Automatically punches temporary holes in `ufw` to allow DHCP (`dnsmasq`) traffic to flow securely.
- 🚫 **One-Click User Blocking:** Instantly cut off a connected device's internet access using direct `iptables` MAC dropping.
- 📸 **Howdy (Face ID) Compatible:** Bundles all root commands into a single execution to prevent your camera from scanning your face 15 times.

## Installation

```bash
git clone https://github.com/moses-Dera/linux-p2p-hotspot.git
cd linux-p2p-hotspot
chmod +x install.sh
./install.sh
```

## Uninstallation

To completely remove the application and its desktop shortcut:
```bash
cd linux-p2p-hotspot
chmod +x uninstall.sh
./uninstall.sh
```

## Usage

1. Open your applications menu and search for **P2P Hotspot Manager**.
2. Enter your desired Network Name and Password.
3. Click **Start Hotspot**.
4. Scan the **QR Code** with your phone's camera to connect.
5. Click **Refresh Devices** to see who is connected, and use the **Block** button if necessary.

## Requirements
- Ubuntu/Debian based Linux
- `python3-tk`, `dnsmasq`, `iptables`, `qrencode` (All automatically installed via `install.sh`)

## License
MIT License
