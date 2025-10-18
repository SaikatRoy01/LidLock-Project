# 🔒 LidLock - Automatic Laptop Lock

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Windows](https://img.shields.io/badge/Windows-10%20%7C%2011-0078D6?logo=windows)](https://www.microsoft.com/windows)
[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python)](https://www.python.org/)
[![Release](https://img.shields.io/badge/Version-1.3.0-green.svg)](https://github.com/SaikatRoy01/LidLock-Project/releases)

Automatically lock your Windows laptop when you close the lid. LidLock uses advanced polling-based detection that works reliably even on systems with virtualization enabled—where traditional Windows power management fails.

**Perfect for:** Gaming laptops, development machines, enterprise environments, and anyone who values security and reliability.

---

## 🎯 What is LidLock?

LidLock is a lightweight Windows application that automatically locks your laptop the moment you close the lid. Unlike built-in Windows power settings that rely on firmware events, LidLock actively monitors your hardware state every 2 seconds, ensuring consistent, reliable protection regardless of your system configuration.

### Why Choose LidLock?

- **Virtualization-Compatible** — Works seamlessly with Hyper-V, WSL2, VirtualBox, and VMware where other solutions fail
- **Smart Detection** — Won't lock if external displays are connected; respects your workflow
- **Lightweight** — Uses only ~35 MB RAM and 0.15% CPU; negligible battery impact
- **Zero Maintenance** — Runs silently in the background with automatic log cleanup
- **Open Source** — Transparent, auditable code; no telemetry or data collection

---

## ✨ Key Features

**Core Functionality**
- Automatic locking with 2–3 second response time
- Polling-based detection that bypasses virtualization layers
- External monitor awareness—won't lock when docked
- System tray integration for easy access and control

**User Experience**
- Optional Windows startup integration
- One-click desktop shortcut
- Intuitive settings panel for configuration
- Comprehensive user guide included

**Technical Excellence**
- Virtualization-agnostic architecture
- Minimal resource footprint
- Auto-cleaning logs (TEMP folder, 24-hour retention)
- Clean uninstall with zero residual files
- Professional Windows integration via Control Panel

---

## 🚀 Quick Start

### Installation

1. Download the latest installer from [Releases](https://github.com/SaikatRoy01/LidLock-Project/releases)
2. Run `LidLock-Setup-v1.3.0.exe` and follow the setup wizard
3. Accept the Apache 2.0 License
4. Choose your preferences (autostart, desktop shortcut)
5. Launch and enjoy automatic protection

**That's it!** Look for the green lock icon in your system tray.

### Usage

1. Close your laptop lid
2. Wait 2–3 seconds
3. Open the lid → You'll see the Windows lock screen ✓

Right-click the tray icon to access settings, test functionality, or view system information.

---

## 🔧 How It Works

LidLock uses **direct hardware polling** instead of relying on Windows Power Management APIs:

```
Every 2 seconds:
├─ Query active display count
├─ If displays: 1+ → 0 (lid closed detected)
└─ Trigger Windows lock (Win+L)
```

This approach:
- ✅ Works regardless of virtualization state
- ✅ Bypasses BIOS/firmware limitations
- ✅ More reliable than power event APIs
- ✅ Consistent behavior across all laptop brands

### Performance

| Metric | Value |
|--------|-------|
| CPU Usage | ~0.15% |
| Memory | ~35 MB |
| Battery Impact | <0.1% per hour |
| Detection Latency | 2–3 seconds |
| Disk Space | ~25 MB |

### Compatibility

**✅ Fully Compatible With:**
- Hyper-V, WSL2, VirtualBox, VMware
- Multiple displays and docking stations
- USB-C hubs, HDMI, DisplayPort
- All major laptop brands (Dell, HP, Lenovo, Alienware, Razer, MSI, ASUS ROG, etc.)

**⚠️ Design Limitations:**
- 2–3 second detection delay (intentional polling interval)
- Won't lock with external displays connected (by design)
- Windows x64 only

---

## 🔐 Privacy & Security

**Your privacy is paramount:**
- Runs entirely locally on your computer
- Zero data collection or transmission
- No internet connection required
- No telemetry, no tracking, no analytics
- Open source—audit the code yourself

---

## 📥 Installation Options

### Option 1: Installer (Recommended)

Download and run the installer from [Releases](https://github.com/SaikatRoy01/LidLock-Project/releases). The setup wizard handles everything.

### Option 2: Build from Source

```bash
# Clone the repository
git clone https://github.com/SaikatRoy01/LidLock-Project.git
cd LidLock-Project

# Install dependencies
pip install -r requirements.txt

# Run directly
python lidlock.py

# Build executable
pyinstaller --onefile --windowed --icon=lidlock.ico --name=LidLock lidlock.py

# Build installer (requires Inno Setup 6)
build_complete_installer.bat
```

---

## 🛠️ Build Instructions

### Prerequisites
- Python 3.9+
- Windows 10/11
- Inno Setup 6 (for building installer)

### Build Steps

**1. Create Executable**
```bash
pip install -r requirements.txt
pyinstaller --onefile --windowed --icon=lidlock.ico --name=LidLock lidlock.py
```
Output: `dist/LidLock.exe`

**2. Build Installer**
```bash
# Ensure Inno Setup 6 is installed
build_complete_installer.bat
```
Output: `installer_output/LidLock-Setup-v1.3.0.exe`

---

## 📋 System Requirements

- **OS:** Windows 10 or Windows 11
- **RAM:** ~35 MB
- **Disk Space:** ~25 MB
- **CPU:** ~0.15%
- **Privileges:** User level (administrator access not required)

---

## 🗑️ Uninstallation

**Via Control Panel:**
1. Settings → Apps → LidLock → Uninstall

**Completely removed:**
- All program files
- Registry entries
- Start menu shortcuts
- Desktop shortcut (if created)
- Log files and autostart entry

Result: Zero residual files.

---

## 🐛 Troubleshooting

**LidLock isn't locking?**
- Verify the app is running (check system tray for green icon)
- Right-click tray icon → Settings → Test Lock
- Review Settings → System Info and logs

**Locking too slowly?**
- This is normal. Polling every 2 seconds means 2–3 second expected delay.

**Not working with external monitor?**
- Expected behavior. LidLock won't lock when docked with external displays.

**Still need help?**
See the [User Guide](USER_GUIDE.md) for comprehensive troubleshooting.

---

## 📖 Documentation

- **[User Guide](USER_GUIDE.md)** — Complete usage and configuration documentation
- **[License](LICENSE)** — Apache 2.0 License

---

## 📜 License

Copyright © 2025 Saikat Roy

Licensed under the Apache License, Version 2.0. See [LICENSE](LICENSE) for details.

```
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
```

---

## 🤝 Contributing

Contributions welcome! Feel free to:
- Report bugs via [GitHub Issues](https://github.com/SaikatRoy01/LidLock-Project/issues)
- Suggest features
- Submit pull requests

---

**Made with ❤️ for secure laptops everywhere** 🔒

*LidLock v1.3.0 — Virtualization-Compatible Automatic Laptop Lock*
