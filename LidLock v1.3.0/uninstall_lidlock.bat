@echo off
REM ============================================================
REM LidLock Complete Uninstaller - Version 1.0
REM ============================================================

echo.
echo ============================================================
echo            LidLock Complete Uninstaller
echo ============================================================
echo.
echo This will completely remove LidLock from your system.
echo.
pause

net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: Administrator privileges required!
    pause
    exit /b 1
)

echo.
echo Starting uninstallation...
echo.

echo [1/8] Stopping LidLock process...
taskkill /F /IM LidLock.exe >nul 2>&1
timeout /t 2 /nobreak >nul

echo [2/8] Removing startup entries...
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "LidLock" /f >nul 2>&1
reg delete "HKLM\Software\Microsoft\Windows\CurrentVersion\Run" /v "LidLock" /f >nul 2>&1

echo [3/8] Removing startup shortcuts...
del "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\LidLock.lnk" >nul 2>&1
del "%ProgramData%\Microsoft\Windows\Start Menu\Programs\Startup\LidLock.lnk" >nul 2>&1

echo [4/8] Removing desktop shortcuts...
del "%USERPROFILE%\Desktop\LidLock.lnk" >nul 2>&1
del "%PUBLIC%\Desktop\LidLock.lnk" >nul 2>&1

echo [5/8] Removing Start Menu entries...
rmdir /S /Q "%APPDATA%\Microsoft\Windows\Start Menu\Programs\LidLock" >nul 2>&1
rmdir /S /Q "%ProgramData%\Microsoft\Windows\Start Menu\Programs\LidLock" >nul 2>&1

echo [6/8] Removing registry entries...
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall\LidLock" /f >nul 2>&1
reg delete "HKLM\Software\Microsoft\Windows\CurrentVersion\Uninstall\LidLock" /f >nul 2>&1
reg delete "HKLM\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\LidLock" /f >nul 2>&1

echo [7/8] Removing program files...
rmdir /S /Q "%ProgramFiles%\LidLock" >nul 2>&1
rmdir /S /Q "%ProgramFiles(x86)%\LidLock" >nul 2>&1
rmdir /S /Q "%LOCALAPPDATA%\Programs\LidLock" >nul 2>&1
rmdir /S /Q "%APPDATA%\LidLock" >nul 2>&1
rmdir /S /Q "%USERPROFILE%\LidLock" >nul 2>&1

echo [8/8] Removing configuration files...
del "%LOCALAPPDATA%\LidLock\*.log" >nul 2>&1
del "%TEMP%\lidlock_*.log" >nul 2>&1
rmdir /S /Q "%LOCALAPPDATA%\LidLock" >nul 2>&1

echo.
echo ============================================================
echo Uninstallation Complete!
echo ============================================================
echo.
pause
