# Contributing to Linux P2P Hotspot Manager

First off, thank you for considering contributing to this project! It's people like you that make open-source software such a great community.

This tool was born out of the frustration of dealing with strict Wi-Fi hardware limitations in Linux, and any help in making it more robust or adding new features is highly appreciated.

## How Can I Contribute?

### Reporting Bugs
If you find a bug, please create an Issue on GitHub. Include as much detail as possible:
* Your Linux distribution and version (e.g., Ubuntu 24.04).
* The specific Wi-Fi hardware you are using (`lspci | grep Network` or `lsusb`).
* The exact error message or behavior you are experiencing.

### Suggesting Enhancements
Have an idea for a new feature or a way to improve the UI? 
* Open an Issue and tag it as an "enhancement".
* Explain the feature, why it would be useful, and how it should work.

### Pull Requests
If you want to contribute code, whether it's a bug fix or a new feature:

1. **Fork the repository** to your own GitHub account.
2. **Create a new branch** for your feature or bugfix (`git checkout -b feature/my-awesome-feature`).
3. **Make your changes** to the Python script or setup files.
4. **Test your changes** locally to ensure they don't break existing functionality.
5. **Commit your changes** with clear, descriptive commit messages.
6. **Push the branch** to your fork (`git push origin feature/my-awesome-feature`).
7. **Open a Pull Request** against the `main` branch of this repository.

## Development Setup
If you are modifying the Python GUI:
1. You can run the script directly from the source folder without installing it globally:
   ```bash
   python3 src/p2p-hotspot-manager.py
   ```
2. Make sure you have the dependencies installed locally (`python3-tk`, `dnsmasq`, `iptables`, `qrencode`).

We welcome contributions of all sizes!
