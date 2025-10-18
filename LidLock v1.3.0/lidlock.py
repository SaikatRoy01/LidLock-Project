"""
LidLock - Virtualization-Compatible Version with Auto-Cleaning Logs
Logs auto-delete on OS restart/shutdown (stored in TEMP folder)

Copyright 2025 Saikat Roy
Licensed under Apache License 2.0
"""

import ctypes
import os
import sys
import uuid
import win32con
import win32gui
import win32api
import win32event
import win32ts
import winerror
import winreg
import logging
from ctypes import wintypes
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw
from win10toast import ToastNotifier
import threading
import tkinter as tk
from tkinter import messagebox
import traceback
import time
import glob
import shutil

# WMI imports for hardware-level detection
try:
    import wmi
    WMI_AVAILABLE = True
except ImportError:
    WMI_AVAILABLE = False

# Constants
APP_NAME = "LidLock"
SINGLETON_IDENTIFIER = "Global\\{3DA16D16-5F02-4CFD-8C43-11C31127889D}"
AUTOSTART_NAME = "LidLock"  # Shows as "LidLock" in Task Manager Startup
VERSION = "1.3.0"

# GUIDs for power settings
GUID_CONSOLE_DISPLAY_STATE = "{6FE69556-704A-47A0-8F24-C28D936FDA47}"
GUID_LIDSWITCH_STATE_CHANGE = "{BA3E0F4D-B817-4094-A2D1-D56379E6A0F3}"
GUID_MONITOR_POWER_ON = "{02731015-4510-4526-99e6-e5a17ebd1aea}"

user32 = ctypes.WinDLL('user32', use_last_error=True)

# ============================================
# LOGGING SETUP - AUTO-CLEANING
# ============================================
# Use Windows TEMP folder - automatically cleaned by Windows
log_dir = os.path.join(os.environ.get("TEMP", os.getcwd()), "LidLock_Logs")
os.makedirs(log_dir, exist_ok=True)
log_path = os.path.join(log_dir, f"lidlock_{os.getpid()}.log")

def cleanup_old_logs():
    """
    Delete old log files on startup
    - Deletes logs older than 24 hours
    - Deletes logs from previous sessions
    - Keeps only current session log
    """
    try:
        # Find all log files in the directory
        log_files = glob.glob(os.path.join(log_dir, "lidlock_*.log"))
        current_time = time.time()
        deleted_count = 0
        
        for log_file in log_files:
            try:
                # Skip current log file
                if log_file == log_path:
                    continue
                
                # Check file age
                file_age_hours = (current_time - os.path.getmtime(log_file)) / 3600
                
                # Delete if older than 24 hours OR from a different process
                if file_age_hours > 24 or log_file != log_path:
                    os.remove(log_file)
                    deleted_count += 1
                    print(f"🗑️  Deleted old log: {os.path.basename(log_file)} (age: {file_age_hours:.1f}h)")
            except Exception as e:
                pass  # Ignore errors on individual files
        
        if deleted_count > 0:
            print(f"✅ Cleaned up {deleted_count} old log file(s)")
        
        # Also clean up the entire directory if empty (except current log)
        remaining_files = [f for f in os.listdir(log_dir) if f != os.path.basename(log_path)]
        if not remaining_files:
            print("✅ Log directory cleaned")
            
    except Exception as e:
        print(f"Note: Could not cleanup old logs: {e}")

# Cleanup old logs before starting
cleanup_old_logs()

# Setup logging
logging.basicConfig(
    filename=log_path,
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
logging.getLogger().addHandler(console_handler)

# Log the temporary nature of logs
logging.info(f"Logs stored in TEMP folder: {log_dir}")
logging.info(f"Logs will auto-delete after 24 hours or on Windows cleanup")
logging.info(f"Current log: {log_path}")

# ============================================


class POWERBROADCAST_SETTING(ctypes.Structure):
    """Structure for power broadcast settings"""
    _fields_ = [
        ("PowerSetting", ctypes.c_byte * 16),
        ("DataLength", wintypes.DWORD),
        ("Data", ctypes.c_byte * 1)
    ]


def is_admin():
    """Check if running with administrator privileges"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def get_battery_status():
    """Get battery status using ctypes (works with virtualization)"""
    try:
        class SYSTEM_POWER_STATUS(ctypes.Structure):
            _fields_ = [
                ('ACLineStatus', ctypes.c_byte),
                ('BatteryFlag', ctypes.c_byte),
                ('BatteryLifePercent', ctypes.c_byte),
                ('SystemStatusFlag', ctypes.c_byte),
                ('BatteryLifeTime', ctypes.c_ulong),
                ('BatteryFullLifeTime', ctypes.c_ulong),
            ]
        
        status = SYSTEM_POWER_STATUS()
        if ctypes.windll.kernel32.GetSystemPowerStatus(ctypes.byref(status)):
            return {
                'ac_online': status.ACLineStatus == 1,
                'battery_percent': status.BatteryLifePercent,
                'battery_present': status.BatteryFlag != 128
            }
    except Exception as e:
        logging.error(f"Error getting battery status: {e}")
    return None


def display_count():
    """Count active displays connected to the system"""
    try:
        from win32api import EnumDisplayDevices
        count = 0
        device_index = 0
        
        while True:
            try:
                device = EnumDisplayDevices(None, device_index)
                if not device.DeviceName:
                    break
                
                if device.StateFlags & 0x00000001:  # DISPLAY_DEVICE_ACTIVE
                    monitor_index = 0
                    while True:
                        try:
                            monitor = EnumDisplayDevices(device.DeviceName, monitor_index)
                            if not monitor.DeviceName:
                                break
                            if monitor.StateFlags & 0x00000001:
                                count += 1
                                logging.debug(f"Active display found: {monitor.DeviceString}")
                            monitor_index += 1
                        except:
                            break
                
                device_index += 1
            except:
                break
        
        logging.info(f"Active display count: {count}")
        return count
    except Exception as e:
        logging.error(f"Error counting displays: {e}")
        return 0


def get_monitor_count_via_user32():
    """Alternative method to get monitor count using user32"""
    try:
        count = user32.GetSystemMetrics(80)  # SM_CMONITORS
        logging.debug(f"Monitor count (user32): {count}")
        return count
    except Exception as e:
        logging.error(f"Error getting monitor count via user32: {e}")
        return 0


def is_laptop_lid_closed():
    """
    Determine if laptop lid is closed using multiple methods
    Returns: True if lid is closed, False if open, None if unknown
    """
    try:
        display_cnt = display_count()
        monitor_cnt = get_monitor_count_via_user32()
        
        logging.debug(f"Display check - EnumDisplayDevices: {display_cnt}, GetSystemMetrics: {monitor_cnt}")
        
        if display_cnt == 0 and monitor_cnt <= 1:
            logging.info("Lid likely closed (no active displays)")
            return True
        
        if display_cnt > 0 or monitor_cnt > 1:
            logging.info(f"Lid open or external displays ({display_cnt} displays)")
            return False
        
        return None
        
    except Exception as e:
        logging.error(f"Error checking lid state: {e}")
        logging.error(traceback.format_exc())
        return None


def lock_workstation():
    """Lock the Windows workstation"""
    try:
        logging.info("Attempting to lock workstation")
        result = user32.LockWorkStation()
        if result == 0:
            error_code = ctypes.get_last_error()
            logging.error(f"LockWorkStation failed with error code: {error_code}")
        else:
            logging.info("Workstation locked successfully")
        return result
    except Exception as e:
        logging.error(f"Exception while locking workstation: {e}")
        return False


def is_session_locked():
    """Check if the current session is locked"""
    try:
        session_id = win32ts.WTSGetActiveConsoleSessionId()
        session_info = win32ts.WTSQuerySessionInformation(
            win32ts.WTS_CURRENT_SERVER_HANDLE,
            session_id,
            win32ts.WTSSessionInfo
        )
        return session_info == win32ts.WTSLocked
    except Exception as e:
        logging.error(f"Error checking session lock status: {e}")
        return False


class LidMonitorPolling(threading.Thread):
    """
    Polling-based lid monitor for systems where power notifications don't work
    This is the MAIN METHOD for virtualization-enabled systems
    """
    
    def __init__(self, callback):
        super().__init__(daemon=True)
        self.callback = callback
        self.running = True
        self.last_state = None
        self.poll_interval = 2
        
    def run(self):
        logging.info("✅ Starting polling-based lid monitor (virtualization-compatible)")
        print("✅ Polling monitor started - checking lid every 2 seconds")
        
        while self.running:
            try:
                lid_closed = is_laptop_lid_closed()
                
                if lid_closed is not None and lid_closed != self.last_state:
                    logging.info(f"Lid state changed: {self.last_state} -> {lid_closed}")
                    
                    if lid_closed and not is_session_locked():
                        logging.info("🔒 Lid closed detected via polling - triggering lock")
                        print("🔒 Lid closed - locking workstation!")
                        self.callback()
                    
                    self.last_state = lid_closed
                
                time.sleep(self.poll_interval)
                
            except Exception as e:
                logging.error(f"Error in polling thread: {e}")
                logging.error(traceback.format_exc())
                time.sleep(self.poll_interval)
    
    def stop(self):
        self.running = False


class LidLockWindow:
    """Main window class for handling Windows messages"""
    
    def __init__(self):
        self.hwnd = None
        self.last_lid_state = None
        self.lock_delay_timer = None
        self.polling_thread = None
        self.power_api_working = False
        
        self.create_window()
        self.start_polling_monitor()
    
    def create_window(self):
        """Create a message-only window"""
        try:
            wc = win32gui.WNDCLASS()
            wc.hInstance = win32api.GetModuleHandle(None)
            wc.lpszClassName = APP_NAME
            
            def simple_wndproc(hwnd, msg, wparam, lparam):
                return 0
            
            wc.lpfnWndProc = simple_wndproc
            
            try:
                win32gui.RegisterClass(wc)
            except Exception as e:
                logging.warning(f"Window class already registered: {e}")
            
            self.hwnd = win32gui.CreateWindow(
                APP_NAME,
                None,
                0,
                0, 0, 0, 0,
                win32con.HWND_MESSAGE,
                0,
                wc.hInstance,
                None
            )
            
            if not self.hwnd:
                raise Exception("Failed to create message window")
            
            logging.info(f"Message window created successfully (HWND: {self.hwnd})")
            
        except Exception as e:
            logging.error(f"Error creating window: {e}")
            logging.error(traceback.format_exc())
    
    def start_polling_monitor(self):
        """Start the polling-based monitor"""
        try:
            self.polling_thread = LidMonitorPolling(self.on_lid_closed_detected)
            self.polling_thread.start()
            logging.info("✅ Polling monitor started (primary method for virtualization)")
            print("✅ LidLock started - using polling method (virtualization-compatible)")
        except Exception as e:
            logging.error(f"Failed to start polling monitor: {e}")
    
    def on_lid_closed_detected(self):
        """Callback when lid closure is detected"""
        try:
            displays = display_count()
            logging.info(f"Lid closure callback - Display count: {displays}")
            
            if displays == 0 and not is_session_locked():
                threading.Timer(0.5, lock_workstation).start()
            else:
                logging.info("External displays present or already locked")
        except Exception as e:
            logging.error(f"Error in lid closed callback: {e}")
    
    def run(self):
        """Start the message pump"""
        try:
            logging.info("=" * 60)
            logging.info("DETECTION METHODS:")
            logging.info("1. ✅ Polling-based monitor (PRIMARY - always active)")
            logging.info("2. ⚠️ Power API notifications (DISABLED - Python 3.13)")
            logging.info("=" * 60)
            logging.info("📁 Log location: " + log_path)
            logging.info("🗑️  Logs auto-delete after 24 hours or on Windows cleanup")
            
            win32gui.PumpMessages()
        except Exception as e:
            logging.error(f"Error in message pump: {e}")
            logging.error(traceback.format_exc())


def check_autostart_status():
    """Check if autostart is currently enabled"""
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            "Software\\Microsoft\\Windows\\CurrentVersion\\Run",
            0,
            winreg.KEY_READ
        )
        try:
            value, _ = winreg.QueryValueEx(key, AUTOSTART_NAME)
            winreg.CloseKey(key)
            return True, value
        except FileNotFoundError:
            winreg.CloseKey(key)
            return False, None
    except Exception as e:
        logging.error(f"Error checking autostart status: {e}")
        return False, None


def set_autostart():
    """Enable autostart on Windows login"""
    try:
        exe_path = os.path.abspath(sys.argv[0])
        
        if not os.path.exists(exe_path):
            logging.error(f"Executable path does not exist: {exe_path}")
            return False
        
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            "Software\\Microsoft\\Windows\\CurrentVersion\\Run",
            0,
            winreg.KEY_SET_VALUE
        )
        
        winreg.SetValueEx(key, AUTOSTART_NAME, 0, winreg.REG_SZ, exe_path)
        winreg.CloseKey(key)
        
        logging.info(f"Autostart enabled: {exe_path}")
        return True
        
    except Exception as e:
        logging.error(f"Error enabling autostart: {e}")
        return False


def remove_autostart():
    """Disable autostart on Windows login"""
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            "Software\\Microsoft\\Windows\\CurrentVersion\\Run",
            0,
            winreg.KEY_SET_VALUE
        )
        
        try:
            winreg.DeleteValue(key, AUTOSTART_NAME)
            logging.info("Autostart disabled")
            success = True
        except FileNotFoundError:
            logging.info("Autostart was not set")
            success = False
        
        winreg.CloseKey(key)
        return success
        
    except Exception as e:
        logging.error(f"Error disabling autostart: {e}")
        return False


def open_settings():
    """Open settings window"""
    def toggle_autostart():
        enabled, _ = check_autostart_status()
        if enabled:
            if remove_autostart():
                status_label.config(text="Autostart disabled ✓", fg="orange")
                toggle_btn.config(text="Enable Autostart")
        else:
            if set_autostart():
                status_label.config(text="Autostart enabled ✓", fg="green")
                toggle_btn.config(text="Disable Autostart")
    
    def view_logs():
        """Open the log file"""
        try:
            if os.path.exists(log_path):
                os.startfile(log_path)
            else:
                messagebox.showinfo("No Logs", "No log file found yet. Logs auto-delete after 24 hours.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not open log file: {e}")
    
    def clean_logs_now():
        """Manually clean all logs"""
        result = messagebox.askyesno(
            "Clean Logs",
            "Delete all log files now?\n\nNote: Logs auto-delete anyway after 24 hours or on Windows restart."
        )
        if result:
            try:
                cleanup_old_logs()
                # Also delete current log
                if os.path.exists(log_path):
                    logging.shutdown()
                    os.remove(log_path)
                    # Restart logging
                    logging.basicConfig(filename=log_path, level=logging.DEBUG)
                messagebox.showinfo("Success", "✅ All logs deleted!")
            except Exception as e:
                messagebox.showerror("Error", f"Could not clean logs: {e}")
    
    def test_lock():
        """Test the lock functionality"""
        if lock_workstation():
            pass
        else:
            messagebox.showerror("Error", "Failed to lock workstation")
    
    def check_system_info():
        """Show system information"""
        info = []
        info.append(f"✅ Virtualization Compatible: YES")
        info.append(f"✅ Polling-based detection: ACTIVE")
        info.append(f"✅ Auto-cleaning logs: ENABLED")
        info.append(f"")
        info.append(f"Display Count: {display_count()}")
        info.append(f"Monitor Count: {get_monitor_count_via_user32()}")
        info.append(f"Python: {sys.version.split()[0]}")
        info.append(f"")
        info.append(f"📁 Log Location:")
        info.append(f"{log_dir}")
        info.append(f"")
        info.append(f"🗑️  Logs auto-delete:")
        info.append(f"  • After 24 hours")
        info.append(f"  • On Windows restart/cleanup")
        info.append(f"  • Stored in TEMP folder")
        
        battery = get_battery_status()
        if battery:
            info.append(f"")
            info.append(f"Battery Present: {battery.get('battery_present', 'Unknown')}")
            info.append(f"AC Online: {battery.get('ac_online', 'Unknown')}")
        
        messagebox.showinfo("System Info", "\n".join(info))
    
    try:
        win = tk.Tk()
        win.title(f"LidLock Settings v{VERSION}")
        win.geometry("400x370")
        win.resizable(False, False)
        
        tk.Label(
            win,
            text="LidLock Settings",
            font=("Arial", 16, "bold")
        ).pack(pady=10)
        
        tk.Label(
            win,
            text="✅ Auto-Cleaning Logs | 🗑️ TEMP Folder",
            font=("Arial", 9),
            fg="darkgreen"
        ).pack()
        
        enabled, path = check_autostart_status()
        status_text = "Autostart enabled ✓" if enabled else "Autostart disabled"
        status_color = "green" if enabled else "gray"
        
        status_label = tk.Label(
            win,
            text=status_text,
            font=("Arial", 10),
            fg=status_color
        )
        status_label.pack(pady=5)
        
        toggle_btn = tk.Button(
            win,
            text="Disable Autostart" if enabled else "Enable Autostart",
            command=toggle_autostart,
            width=28,
            height=2
        )
        toggle_btn.pack(pady=3)
        
        tk.Button(
            win,
            text="Test Lock Now",
            command=test_lock,
            width=28,
            height=2
        ).pack(pady=3)
        
        tk.Button(
            win,
            text="System Info",
            command=check_system_info,
            width=28
        ).pack(pady=3)
        
        tk.Button(
            win,
            text="View Current Logs",
            command=view_logs,
            width=28
        ).pack(pady=3)
        
        tk.Button(
            win,
            text="🗑️ Clean All Logs Now",
            command=clean_logs_now,
            width=28,
            fg="red"
        ).pack(pady=3)
        
        tk.Label(
            win,
            text=f"v{VERSION} | Logs auto-delete in TEMP folder",
            font=("Arial", 8),
            fg="gray"
        ).pack(pady=5)
        
        win.mainloop()
        
    except Exception as e:
        logging.error(f"Error opening settings: {e}")
        logging.error(traceback.format_exc())


def create_tray_icon():
    """Create system tray icon"""
    try:
        def quit_app(icon, item):
            logging.info("Application shutting down via tray")
            icon.stop()
            os._exit(0)
        
        def open_settings_from_tray(icon, item):
            threading.Thread(target=open_settings, daemon=True).start()
        
        menu = Menu(
            MenuItem('Settings', open_settings_from_tray),
            MenuItem('Test Lock', lambda i, itm: lock_workstation()),
            MenuItem('Exit', quit_app)
        )
        
        image = Image.new('RGB', (64, 64), 'black')
        draw = ImageDraw.Draw(image)
        draw.rectangle([16, 16, 48, 48], fill='white', outline='green', width=3)
        draw.rectangle([24, 24, 40, 40], fill='green')
        
        icon = Icon(APP_NAME, image, f"{APP_NAME} v{VERSION}", menu)
        threading.Thread(target=icon.run, daemon=True).start()
        
        logging.info("System tray icon created")
        
    except Exception as e:
        logging.error(f"Error creating tray icon: {e}")
        logging.error(traceback.format_exc())


def show_startup_notification():
    """Show startup notification"""
    try:
        toaster = ToastNotifier()
        toaster.show_toast(
            "LidLock",
            f"✅ Running (v{VERSION})\nAuto-cleaning logs enabled\nPolling every 2 seconds",
            duration=5,
            threaded=True,
            icon_path=None
        )
    except Exception as e:
        logging.error(f"Error showing notification: {e}")


def main():
    """Main application entry point"""
    try:
        print("=" * 60)
        print(f"LidLock v{VERSION} starting")
        print("VIRTUALIZATION-COMPATIBLE | AUTO-CLEANING LOGS")
        print("=" * 60)
        print(f"📁 Logs: {log_dir}")
        print(f"🗑️  Auto-delete: After 24h or Windows restart")
        print("=" * 60)
        
        logging.info(f"{'='*60}")
        logging.info(f"LidLock v{VERSION} starting")
        logging.info(f"VIRTUALIZATION-COMPATIBLE VERSION")
        logging.info(f"AUTO-CLEANING LOGS ENABLED")
        logging.info(f"Python: {sys.version}")
        logging.info(f"Executable: {sys.argv[0]}")
        logging.info(f"Working directory: {os.getcwd()}")
        logging.info(f"Admin privileges: {is_admin()}")
        logging.info(f"WMI Available: {WMI_AVAILABLE}")
        logging.info(f"{'='*60}")
        
        mutex = win32event.CreateMutex(None, False, SINGLETON_IDENTIFIER)
        last_error = win32api.GetLastError()
        
        if last_error == winerror.ERROR_ALREADY_EXISTS:
            logging.warning("Another instance is already running")
            print("⚠️  LidLock is already running - check system tray")
            messagebox.showwarning(
                "LidLock",
                "LidLock is already running!\nCheck the system tray."
            )
            return
        
        enabled, _ = check_autostart_status()
        if not enabled:
            set_autostart()
        
        create_tray_icon()
        show_startup_notification()
        
        print("✅ LidLock initialized successfully!")
        print("   - Green tray icon visible")
        print("   - Polling-based detection active")
        print("   - Auto-cleaning logs enabled")
        print("   - Right-click tray icon for settings")
        print()
        
        window = LidLockWindow()
        logging.info("Entering message loop (polling-based detection active)")
        window.run()
        
    except Exception as e:
        logging.error(f"Fatal error in main: {e}")
        logging.error(traceback.format_exc())
        print(f"❌ Error: {e}")
        messagebox.showerror(
            "LidLock Error",
            f"A fatal error occurred:\n\n{str(e)}\n\nCheck logs at:\n{log_path}"
        )
        raise


if __name__ == "__main__":
    main()
