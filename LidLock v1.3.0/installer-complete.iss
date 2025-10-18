; ================================================================
; LidLock Installer Script - CORRECTED VERSION
; Apache License 2.0 - Copyright 2025 Saikat Roy
; ================================================================
; 
; FEATURES:
; ✓ Apache 2.0 License acceptance REQUIRED
; ✓ Custom installation location (default: C:\Program Files\LidLock)
; ✓ Checkboxes for post-installation (CHECKED by default):
;   - Run with Windows Startup
;   - Start LidLock Process
;   - Open User Guide
;
; ================================================================

#define MyAppName "LidLock"
#define MyAppVersion "1.3.0"
#define MyAppPublisher "Saikat Roy"
#define MyAppURL "https://github.com/SaikatRoy01/LidLock-Project"
#define MyAppExeName "LidLock.exe"
#define MyAppId "{{3DA16D16-5F02-4CFD-8C43-11C31127889D}"

[Setup]
; ============================================================
; App Identity
; ============================================================
AppId={#MyAppId}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppCopyright=Copyright © 2025 {#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}/issues
AppUpdatesURL={#MyAppURL}/releases

; ============================================================
; Installation Location
; User can choose (default: C:\Program Files\LidLock)
; ============================================================
DefaultDirName={autopf}\{#MyAppName}
DisableDirPage=no
AllowNoIcons=yes
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes

; ============================================================
; Output Configuration
; ============================================================
OutputDir=installer_output
OutputBaseFilename=LidLock-Setup-v{#MyAppVersion}

; ============================================================
; Compression Settings
; ============================================================
Compression=lzma2/ultra64
SolidCompression=yes

; ============================================================
; Visual Settings
; ============================================================
SetupIconFile=lidlock.ico
UninstallDisplayIcon={app}\{#MyAppExeName}
WizardStyle=modern

; ============================================================
; License Page - Apache 2.0
; User MUST accept to continue
; ============================================================
LicenseFile=LICENSE

; ============================================================
; Control Panel Registration
; ============================================================
UninstallDisplayName={#MyAppName} - Automatic Laptop Lock

; ============================================================
; Privileges
; ============================================================
PrivilegesRequired=admin
PrivilegesRequiredOverridesAllowed=dialog

; ============================================================
; Version Information
; ============================================================
VersionInfoVersion={#MyAppVersion}
VersionInfoCompany={#MyAppPublisher}
VersionInfoDescription=Automatic laptop lock when lid closes
VersionInfoProductName={#MyAppName}
VersionInfoProductVersion={#MyAppVersion}
VersionInfoCopyright=Copyright © 2025 {#MyAppPublisher}

; ============================================================
; Architecture
; ============================================================
ArchitecturesInstallIn64BitMode=x64compatible

; ============================================================
; Minimum Windows Version
; ============================================================
MinVersion=10.0

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
; ============================================================
; CHECKBOXES BEHAVIOR:
; - No Flags = CHECKED by default
; - Flags: unchecked = UNCHECKED by default
; - Flags: checkedonce = CHECKED on first install only
; ============================================================

; Additional Icons (UNCHECKED by default)
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional icons:"; Flags: unchecked

; System Integration (CHECKED by default)
Name: "startup"; Description: "Run with Windows Startup"; GroupDescription: "System Integration:"; Flags: checkedonce

; Post-Installation Actions (CHECKED by default)
; Note: No Flags parameter means CHECKED by default
Name: "startnow"; Description: "Start LidLock Process (system tray notification)"; GroupDescription: "After Installation:"
Name: "viewguide"; Description: "Open User Guide (README file)"; GroupDescription: "After Installation:"

[Files]
; ============================================================
; Files to Install
; ============================================================

; Main Application
Source: "dist\LidLock.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "lidlock.ico"; DestDir: "{app}"; Flags: ignoreversion

; Documentation
Source: "LICENSE"; DestDir: "{app}"; Flags: ignoreversion
Source: "USER_GUIDE.md"; DestDir: "{app}"; DestName: "UserGuide.txt"; Flags: ignoreversion

[Icons]
; ============================================================
; Shortcuts
; ============================================================

; Start Menu Icons
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\lidlock.ico"
Name: "{group}\User Guide"; Filename: "{app}\UserGuide.txt"
Name: "{group}\Uninstall {#MyAppName}"; Filename: "{uninstallexe}"

; Desktop Icon (optional - based on task selection)
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\lidlock.ico"; Tasks: desktopicon

; Quick Launch Icon (optional - based on task selection)

[Registry]
; ============================================================
; Registry Entries
; ============================================================

; Autostart Registry Entry (if "Run with Windows Startup" is checked)
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; ValueType: string; ValueName: "{#MyAppName}"; ValueData: """{app}\{#MyAppExeName}"""; Flags: uninsdeletevalue; Tasks: startup

; Application Settings (HKCU)
Root: HKCU; Subkey: "Software\{#MyAppPublisher}\{#MyAppName}"; ValueType: string; ValueName: "InstallPath"; ValueData: "{app}"; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\{#MyAppPublisher}\{#MyAppName}"; ValueType: string; ValueName: "Version"; ValueData: "{#MyAppVersion}"; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\{#MyAppPublisher}\{#MyAppName}"; ValueType: string; ValueName: "InstallDate"; ValueData: "{code:GetInstallDate}"; Flags: uninsdeletekey

; Control Panel Uninstall Registry (HKLM - visible to all users)
Root: HKLM; Subkey: "Software\Microsoft\Windows\CurrentVersion\Uninstall\{#MyAppId}_is1"; ValueType: string; ValueName: "DisplayName"; ValueData: "{#MyAppName}"; Flags: uninsdeletekey
Root: HKLM; Subkey: "Software\Microsoft\Windows\CurrentVersion\Uninstall\{#MyAppId}_is1"; ValueType: string; ValueName: "DisplayVersion"; ValueData: "{#MyAppVersion}"; Flags: uninsdeletekey
Root: HKLM; Subkey: "Software\Microsoft\Windows\CurrentVersion\Uninstall\{#MyAppId}_is1"; ValueType: string; ValueName: "Publisher"; ValueData: "{#MyAppPublisher}"; Flags: uninsdeletekey
Root: HKLM; Subkey: "Software\Microsoft\Windows\CurrentVersion\Uninstall\{#MyAppId}_is1"; ValueType: string; ValueName: "DisplayIcon"; ValueData: "{app}\{#MyAppExeName},0"; Flags: uninsdeletekey
Root: HKLM; Subkey: "Software\Microsoft\Windows\CurrentVersion\Uninstall\{#MyAppId}_is1"; ValueType: string; ValueName: "UninstallString"; ValueData: """{uninstallexe}"""; Flags: uninsdeletekey
Root: HKLM; Subkey: "Software\Microsoft\Windows\CurrentVersion\Uninstall\{#MyAppId}_is1"; ValueType: string; ValueName: "InstallLocation"; ValueData: "{app}"; Flags: uninsdeletekey

[Run]
; ============================================================
; Post-Installation Actions
; ============================================================

; Start LidLock after installation (if checkbox is CHECKED)
Filename: "{app}\{#MyAppExeName}"; Description: "Launch {#MyAppName}"; Flags: nowait postinstall skipifsilent; Tasks: startnow

; Open User Guide (if checkbox is CHECKED)
Filename: "notepad.exe"; Parameters: """{app}\UserGuide.txt"""; Description: "View User Guide"; Flags: postinstall skipifsilent shellexec; Tasks: viewguide

[UninstallRun]
; ============================================================
; Actions Before Uninstall
; ============================================================

; Stop LidLock before uninstall
Filename: "taskkill"; Parameters: "/F /IM {#MyAppExeName}"; Flags: runhidden

[UninstallDelete]
; ============================================================
; Clean Up Files During Uninstall
; ============================================================

; Clean up log files from TEMP folder
Type: files; Name: "{%TEMP}\LidLock_Logs\*.log"
Type: dirifempty; Name: "{%TEMP}\LidLock_Logs"

; Clean up any leftover files in installation directory
Type: filesandordirs; Name: "{app}\*"

[Messages]
; ============================================================
; Custom Messages
; ============================================================
BeveledLabel={#MyAppName} v{#MyAppVersion} - © 2025 {#MyAppPublisher}
SetupWindowTitle=Setup - {#MyAppName} v{#MyAppVersion}
WelcomeLabel1=Welcome to the {#MyAppName} Setup Wizard
WelcomeLabel2=This will install {#MyAppName} v{#MyAppVersion} on your computer.%n%n{#MyAppName} automatically locks your Windows laptop when the lid is closed, providing enhanced security for your device.%n%nIt is recommended that you close all other applications before continuing.
LicenseLabel=Please read the Apache License 2.0 agreement below.
LicenseLabel3=Please read the following License Agreement. You must accept the terms of this agreement before continuing with the installation.
LicenseAccepted=I &accept the agreement
LicenseNotAccepted=I &do not accept the agreement

[Code]
// Get current date for install date (YYYYMMDD format)
function GetInstallDate(Param: String): String;
begin
  Result := GetDateTimeString('yyyymmdd', #0, #0);
end;

// Stop running app before uninstall
function InitializeUninstall(): Boolean;
var
  ResultCode: Integer;
begin
  Result := True;
  Exec('taskkill', '/F /IM LidLock.exe', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
  Sleep(500);
  RegDeleteValue(HKEY_CURRENT_USER, 'Software\Microsoft\Windows\CurrentVersion\Run', 'LidLock');
end;

// Check if app is already installed and handle upgrade
function InitializeSetup(): Boolean;
var
  OldVersion: String;
  UninstallString: String;
  ResultCode: Integer;
begin
  Result := True;
  
  if RegQueryStringValue(HKEY_CURRENT_USER, 'Software\Saikat Roy\LidLock', 'Version', OldVersion) then
  begin
    if MsgBox('LidLock ' + OldVersion + ' is already installed.' + #13#10 + #13#10 +
              'Do you want to uninstall the previous version first?', 
              mbConfirmation, MB_YESNO) = IDYES then
    begin
      Exec('taskkill', '/F /IM LidLock.exe', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
      Sleep(500);
      
      if RegQueryStringValue(HKEY_LOCAL_MACHINE, 'Software\Microsoft\Windows\CurrentVersion\Uninstall\{{3DA16D16-5F02-4CFD-8C43-11C31127889D}}_is1', 'UninstallString', UninstallString) then
      begin
        Exec(RemoveQuotes(UninstallString), '/SILENT', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
        Sleep(1000);
      end;
    end
    else
      Result := False;
  end;
end;
