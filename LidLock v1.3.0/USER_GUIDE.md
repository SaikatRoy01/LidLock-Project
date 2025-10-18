# 🔒 LidLock User Guide v1.3.0

## Welcome to LidLock!

LidLock automatically locks your Windows laptop when you close the lid. This guide will help you get started and troubleshoot any issues.

---

## 📖 Table of Contents

1. [What is LidLock?](#what-is-lidlock)
2. [How to Use](#how-to-use)
3. [Features](#features)
4. [Settings](#settings)
5. [Troubleshooting](#troubleshooting)
6. [Technical Details](#technical-details)
7. [Uninstall](#uninstall)
8. [Support](#support)

---

## 🎯 What is LidLock?

LidLock is a lightweight Windows application that automatically locks your laptop when you close the lid. It's designed to work reliably even on systems with virtualization enabled (like Alienware M16 R2, gaming laptops, and development machines running Hyper-V or WSL2).

### Key Benefits
- ✅ **Automatic security** - Never forget to lock your laptop
- ✅ **Virtualization-compatible** - Works where other solutions fail
- ✅ **Lightweight** - Uses only 0.15% CPU
- ✅ **Smart detection** - Won't lock if external displays are connected
- ✅ **Zero maintenance** - Logs auto-delete, no clutter

---

## 🚀 How to Use

### Step 1: Installation
You've already installed LidLock! If you checked the "Start with Windows" option during installation, LidLock will automatically start every time you log in to Windows.

### Step 2: Look for the Tray Icon
Look at the bottom-right corner of your screen (system tray). You should see a **green lock icon**. This means LidLock is running and protecting your laptop.

```
System Tray → 🔒 (Green lock icon)
```

### Step 3: Test It!
1. Save your work
2. Close your laptop lid
3. Wait 2-3 seconds
4. Open your laptop lid
5. You should see the Windows lock screen ✓

**That's it!** LidLock is now protecting your laptop automatically.

---

## ✨ Features

### Automatic Locking
- Locks within 2-3 seconds of closing the lid
- Uses polling-based detection (checks every 2 seconds)
- Works with virtualization enabled

### Smart Detection
- **Won't lock** if external monitors are connected
- Detects multiple display configurations
- Handles docking stations correctly

### System Tray Integration
- Green lock icon for easy visibility
- Right-click for quick access to:
  - Settings
  - Test Lock function
  - Exit option

### Auto-Cleaning Logs
- Logs stored in Windows TEMP folder
- Automatically deleted after 24 hours
- Cleaned on Windows restart
- No manual maintenance needed

### Windows Integration
- Appears in Control Panel
- Professional uninstaller
- Start with Windows option
- Desktop shortcut (optional)

---

## ⚙️ Settings

### Opening Settings
Right-click the **green lock icon** in your system tray and select **"Settings"**.

### Settings Options

#### 1. Autostart Toggle
```
[Enable Autostart] / [Disable Autostart]
```
- **Enable**: LidLock starts automatically when Windows starts
- **Disable**: You'll need to manually start LidLock after login
- **Recommendation**: Keep enabled for automatic protection

#### 2. Test Lock Now
```
[Test Lock Now]
```
- Immediately locks your computer
- Use this to verify LidLock is working
- Same as pressing Win+L

#### 3. System Info
```
[System Info]
```
Shows:
- Virtualization compatibility status
- Current display count
- Monitor count
- Python version
- Log location
- Battery status
- Detection method status

Example output:
```
✅ Virtualization Compatible: YES
✅ Polling-based detection: ACTIVE
✅ Auto-cleaning logs: ENABLED

Display Count: 1
Monitor Count: 1
Python: 3.13.0

📁 Log Location:
C:\Users\[YourName]\AppData\Local\Temp\LidLock_Logs

🗑️  Logs auto-delete:
  • After 24 hours
  • On Windows restart/cleanup
  • Stored in TEMP folder

Battery Present: True
AC Online: True
```

#### 4. View Current Logs
```
[View Current Logs]
```
- Opens the current session's log file
- Useful for troubleshooting
- Shows all detection events
- Located in TEMP folder (auto-deleted)

#### 5. Clean All Logs Now
```
🗑️ [Clean All Logs Now]
```
- Manually delete all log files
- Not usually necessary (auto-cleaned anyway)
- Use if you want immediate cleanup

---

## 🔍 Troubleshooting

### Problem: LidLock Not Locking When I Close the Lid

**Solution 1: Verify LidLock is Running**
```
1. Look for green lock icon in system tray
2. If not visible, open Start Menu
3. Search for "LidLock"
4. Click to launch
```

**Solution 2: Check System Info**
```
1. Right-click tray icon → Settings
2. Click "System Info"
3. Verify:
   - "Virtualization Compatible: YES"
   - "Polling-based detection: ACTIVE"
   - "Display Count" shows correct number
```

**Solution 3: Test Lock Function**
```
1. Right-click tray icon → Settings
2. Click "Test Lock Now"
3. If this locks your PC, LidLock is working
4. If not, see "Advanced Troubleshooting" below
```

### Problem: Locking Too Slowly (More Than 5 Seconds)

**This is usually normal!** LidLock uses polling-based detection which checks every 2 seconds. Expected lock time: 2-3 seconds.

If it's taking longer:
```
1. Check System Info
2. Look at "Display Count" value
3. Close lid and check logs (Settings → View Logs)
4. Look for: "Lid state changed: False -> True"
```

### Problem: Not Locking When External Monitor Connected

**This is expected behavior!** LidLock won't lock if external displays are active. This allows you to:
- Use laptop in clamshell mode
- Work with external monitors
- Avoid accidental locks when docked

To verify:
```
1. Disconnect external monitor
2. Close laptop lid
3. Should lock within 2-3 seconds ✓
```

### Problem: Green Tray Icon Not Visible

**Solution:**
```
1. Press Ctrl+Shift+Esc (Task Manager)
2. Look for "LidLock.exe" in Processes
3. If running but icon hidden:
   - Click "Show hidden icons" (^ arrow in system tray)
   - Look for green lock icon
4. If not running:
   - Open Start Menu
   - Search "LidLock"
   - Launch it
```

### Problem: Not Starting with Windows

**Solution:**
```
1. Right-click tray icon → Settings
2. Check autostart status
3. If disabled, click "Enable Autostart"
4. Verify in Task Manager:
   - Ctrl+Shift+Esc
   - Click "Startup" tab
   - Look for "LidLock" - should be "Enabled"
```

### Advanced Troubleshooting

**Check Logs:**
```
1. Right-click tray icon → Settings
2. Click "View Current Logs"
3. Look for error messages
4. Search for: "ERROR" or "FAILED"
```

**Common Log Messages:**

✅ **Good Messages:**
```
[INFO] Polling-based lid monitor (virtualization-compatible)
[INFO] Polling monitor started
[INFO] Lid state changed: False -> True
[INFO] Lid closed detected via polling - triggering lock
[INFO] Workstation locked successfully
```

❌ **Problem Messages:**
```
[ERROR] LockWorkStation failed with error code: [number]
→ Solution: Restart LidLock as administrator

[ERROR] Error checking lid state
→ Solution: Check System Info for display detection

[WARNING] Another instance is already running
→ Solution: Close duplicate instance
```

---

## 🔬 Technical Details

### Detection Method
LidLock uses **polling-based detection** instead of Windows Power Management APIs. Here's why:

**Traditional Method (doesn't work with virtualization):**
- Relies on Windows Power Management events
- Breaks when virtualization is enabled
- Used by most lid detection apps

**LidLock Method (works everywhere):**
- Checks display state every 2 seconds
- Direct hardware queries
- Bypasses virtualization layer
- More reliable on modern laptops

### How It Works
```
Every 2 seconds:
1. Check: How many displays are active?
2. Previous state: 1+ displays → Current state: 0 displays
3. Conclusion: Lid was closed!
4. Action: Lock the laptop (Win+L)
```

### System Requirements
- **OS**: Windows 10 or Windows 11
- **Memory**: ~35 MB
- **CPU**: ~0.15% (negligible)
- **Disk Space**: ~25 MB
- **Privileges**: User level (admin not required)

### Compatibility
✅ **Works With:**
- Virtualization enabled (Hyper-V, WSL2, VirtualBox)
- Gaming laptops (Alienware, Razer, MSI, ASUS ROG)
- Development machines
- Multiple displays
- Docking stations
- USB-C hubs
- HDMI/DisplayPort monitors

❌ **Known Limitations:**
- Checks every 2 seconds (small delay)
- Won't lock if external displays active (by design)

### Log Management
- **Location**: `%TEMP%\LidLock_Logs\`
- **Auto-delete**: After 24 hours
- **Also deleted**: On Windows restart/shutdown
- **Manual cleanup**: Available in Settings
- **No privacy concerns**: Only system information logged

### Performance Impact
```
CPU Usage:     0.15% (0.0015 of 1 core)
Memory:        35 MB
Battery:       <0.1% per hour
Network:       None (100% offline)
Disk I/O:      Minimal (log writes only)
```

**Translation for Gamers**: You won't notice any performance impact while gaming! 🎮

---

## 🗑️ Uninstall

### Method 1: Control Panel (Recommended)
```
1. Open Control Panel
2. Click "Programs and Features"
3. Find "LidLock v1.3.0"
4. Click "Uninstall"
5. Follow prompts
6. All files will be removed ✓
```

### Method 2: Windows Settings
```
1. Open Settings (Win+I)
2. Go to "Apps"
3. Search for "LidLock"
4. Click → Uninstall
5. Confirm removal
```

### What Gets Removed
- ✅ LidLock.exe
- ✅ All program files
- ✅ Start menu shortcuts
- ✅ Desktop shortcut (if created)
- ✅ Autostart registry entry
- ✅ Control Panel registration
- ✅ All log files
- ✅ System tray icon

**Result**: Zero files left behind! Clean uninstall.

---

## 💬 Support

### Getting Help

**Step 1: Check This Guide**
Most questions are answered in the [Troubleshooting](#troubleshooting) section above.

**Step 2: Check System Info**
```
Right-click tray icon → Settings → System Info
```
This shows your system configuration and detection status.

**Step 3: Check Logs**
```
Right-click tray icon → Settings → View Current Logs
```
Look for error messages or unexpected behavior.

**Step 4: Test Functionality**
```
Right-click tray icon → Settings → Test Lock Now
```
This verifies if the lock mechanism works.

### Common Questions

**Q: Is LidLock safe?**  
A: Yes! It's open source (Apache 2.0), uses only standard Windows APIs, and runs entirely offline. No data is collected or transmitted.

**Q: Do I need to keep it running?**  
A: Yes, LidLock must be running to protect your laptop. Enable "Start with Windows" for automatic protection.

**Q: Will it drain my battery?**  
A: No, the impact is negligible (<0.1% per hour). The polling check uses minimal resources.

**Q: Can I use it on multiple laptops?**  
A: Yes! Install on as many devices as you want. Licensed under Apache 2.0.

**Q: Does it work with BitLocker?**  
A: Yes, LidLock triggers the Windows lock screen, which works normally with BitLocker and other encryption.

**Q: Can I modify the source code?**  
A: Yes! Apache 2.0 license allows modification. The source code is available on GitHub.

**Q: Why 2-3 seconds instead of instant?**  
A: Polling-based detection checks every 2 seconds for reliability with virtualization. The small delay ensures compatibility with all systems.

**Q: Will it work with my docking station?**  
A: Yes! LidLock correctly detects external displays. It won't lock if monitors are connected to your docking station.

---

## 📜 License

LidLock is licensed under **Apache License 2.0**

```
Copyright 2025 Saikat Roy

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

This means:
- ✅ Free to use
- ✅ Free to modify
- ✅ Free to distribute
- ✅ Can use commercially
- ✅ Must include license notice

---

## 🎉 Thank You!

Thank you for using LidLock! This application was specifically designed to work on systems with virtualization enabled, ensuring your laptop is always protected when you close the lid.

**Enjoy automatic laptop security!** 🔒

---

*LidLock v1.3.0 - Made with ❤️ for all laptops with virtualization enabled*

*Questions or issues? Check the GitHub repository or open an issue!*
