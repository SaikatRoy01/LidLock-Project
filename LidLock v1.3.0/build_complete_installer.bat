@echo off
echo ============================================
echo    LidLock Complete Installer Builder
echo    Apache 2.0 License - 2025 Saikat Roy
echo ============================================
echo.

REM Check if Inno Setup is installed
set "INNO_PATH=C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
if not exist "%INNO_PATH%" (
    set "INNO_PATH=C:\Program Files\Inno Setup 6\ISCC.exe"
)

if not exist "%INNO_PATH%" (
    echo ERROR: Inno Setup not found!
    echo.
    echo Please install Inno Setup 6 from:
    echo https://jrsoftware.org/isdl.php
    echo.
    pause
    exit /b 1
)

echo [OK] Inno Setup found at: %INNO_PATH%
echo.

REM Check if dist\LidLock.exe exists
if not exist "dist\LidLock.exe" (
    echo ERROR: dist\LidLock.exe not found!
    echo.
    echo Please run PyInstaller first to create the executable:
    echo   pyinstaller --onefile --windowed --icon=lidlock.ico --name=LidLock lidlock.py
    echo.
    pause
    exit /b 1
)

echo [OK] LidLock.exe found
echo.

REM Check if LICENSE file exists
if not exist "LICENSE" (
    echo ERROR: LICENSE file not found!
    echo.
    echo The LICENSE file is REQUIRED for the installer.
    echo It contains the Apache 2.0 License that users must accept.
    echo.
    pause
    exit /b 1
)

echo [OK] LICENSE file found
echo.

REM Check if USER_GUIDE.md exists
if not exist "USER_GUIDE.md" (
    echo WARNING: USER_GUIDE.md not found!
    echo The installer expects this file for the "Open User Guide" option.
    echo.
    echo Creating a basic USER_GUIDE.md...
    (
        echo # LidLock User Guide
        echo.
        echo ## Welcome to LidLock!
        echo.
        echo LidLock automatically locks your Windows laptop when you close the lid.
        echo.
        echo ## Features:
        echo - Automatic lock when lid closes
        echo - System tray integration
        echo - Windows startup support
        echo - Virtualization compatible
        echo - Auto-cleaning logs
        echo.
        echo ## How to Use:
        echo 1. LidLock runs in the system tray ^(green lock icon^)
        echo 2. Right-click the tray icon for settings
        echo 3. Simply close your laptop lid - it will lock automatically!
        echo.
        echo ## Settings:
        echo - Enable/Disable autostart
        echo - Test lock functionality
        echo - View system information
        echo - Access logs
        echo.
        echo ## Support:
        echo For issues or questions, visit: https://github.com/SaikatRoy01/LidLock-Project
        echo.
        echo ## License:
        echo Apache License 2.0 - Copyright 2025 Saikat Roy
    ) > USER_GUIDE.md
    echo [OK] USER_GUIDE.md created
    echo.
)

echo [OK] USER_GUIDE.md found
echo.

REM Create output directory
if not exist "installer_output" mkdir installer_output

echo ============================================
echo Building installer...
echo ============================================
echo.

REM Compile the installer
"%INNO_PATH%" installer-complete.iss

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ============================================
    echo          BUILD SUCCESSFUL!
    echo ============================================
    echo.
    echo Installer created:
    echo   installer_output\LidLock-Setup-v1.3.0.exe
    echo.
    echo Features:
    echo   [✓] Apache 2.0 License acceptance required
    echo   [✓] Custom installation location ^(default: C:\Program Files\LidLock^)
    echo   [✓] Checkboxes for post-installation actions:
    echo       - Run with Windows Startup ^(CHECKED by default^)
    echo       - Start LidLock Process ^(CHECKED by default^)
    echo       - Open User Guide ^(CHECKED by default^)
    echo   [✓] Control Panel integration
    echo   [✓] Clean uninstall
    echo.
    echo Next steps:
    echo   1. Test the installer
    echo   2. Try unchecking the checkboxes during install
    echo   3. Verify license acceptance is required
    echo   4. Check custom install location works
    echo.
) else (
    echo.
    echo ============================================
    echo          BUILD FAILED!
    echo ============================================
    echo.
    echo Check the error messages above.
    echo.
)

echo ============================================
pause
