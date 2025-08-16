;--------------------------------
; Psychological Records Management System v1.0.0 Installer
; Created: August 13, 2025
; NSIS Script for Windows Installation
;--------------------------------

;--------------------------------
; Includes
!include "MUI2.nsh"
!include "FileFunc.nsh"
!include "LogicLib.nsh"
!include "WinVer.nsh"

;--------------------------------
; General Configuration
!define PRODUCT_NAME "Psychological Records Management System"
!define PRODUCT_VERSION "1.0.0"
!define PRODUCT_PUBLISHER "Medical Software Solutions"
!define PRODUCT_WEB_SITE "https://github.com/medical-software/psychological-records"
!define PRODUCT_DIR_REGKEY "Software\Microsoft\Windows\CurrentVersion\App Paths\PsychologicalRecords.exe"
!define PRODUCT_UNINST_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}"
!define PRODUCT_UNINST_ROOT_KEY "HKLM"
!define PRODUCT_STARTMENU_REGVAL "NSIS:StartMenuDir"

; Output file
OutFile "PsychologicalRecords-v1.0.0-Setup.exe"

; Installation directory
InstallDir "$PROGRAMFILES64\Psychological Records"

; Get installation folder from registry if available
InstallDirRegKey HKCU "Software\Psychological Records" ""

; Request application privileges
RequestExecutionLevel admin

; Compression
SetCompressor /SOLID lzma
SetCompressorDictSize 32

; Version Information
VIProductVersion "1.0.0.0"
VIAddVersionKey "ProductName" "${PRODUCT_NAME}"
VIAddVersionKey "Comments" "Professional medical records management software"
VIAddVersionKey "CompanyName" "${PRODUCT_PUBLISHER}"
VIAddVersionKey "LegalTrademarks" "Medical Software Solutions"
VIAddVersionKey "LegalCopyright" "© 2025 Medical Software Solutions"
VIAddVersionKey "FileDescription" "${PRODUCT_NAME} Setup"
VIAddVersionKey "FileVersion" "${PRODUCT_VERSION}"
VIAddVersionKey "ProductVersion" "${PRODUCT_VERSION}"

;--------------------------------
; Interface Settings
!define MUI_ABORTWARNING
!define MUI_ICON "assets\app_icon.ico"
!define MUI_UNICON "assets\app_icon.ico"

; Header Image
!define MUI_HEADERIMAGE
!define MUI_HEADERIMAGE_BITMAP "assets\app_icon.ico"
!define MUI_HEADERIMAGE_RIGHT

; Welcome Page
!define MUI_WELCOMEPAGE_TITLE "Welcome to ${PRODUCT_NAME} Setup"
!define MUI_WELCOMEPAGE_TEXT "This wizard will guide you through the installation of ${PRODUCT_NAME}.$\r$\n$\r$\nThis software provides secure management of psychological and medical records with enterprise-grade encryption.$\r$\n$\r$\nClick Next to continue."

; License Page
!define MUI_LICENSEPAGE_TEXT_TOP "Please review the license terms before installing ${PRODUCT_NAME}."
!define MUI_LICENSEPAGE_TEXT_BOTTOM "If you accept the terms of the agreement, click I Agree to continue. You must accept the agreement to install ${PRODUCT_NAME}."

; Components Page
!define MUI_COMPONENTSPAGE_SMALLDESC

; Directory Page
!define MUI_DIRECTORYPAGE_TEXT_TOP "Setup will install ${PRODUCT_NAME} in the following folder.$\r$\n$\r$\nTo install in a different folder, click Browse and select another folder."

; Finish Page
!define MUI_FINISHPAGE_RUN "$INSTDIR\PsychologicalRecords.exe"
!define MUI_FINISHPAGE_RUN_TEXT "Launch ${PRODUCT_NAME}"
!define MUI_FINISHPAGE_SHOWREADME_TEXT "Show README"
!define MUI_FINISHPAGE_LINK "Visit our website for support and updates"
!define MUI_FINISHPAGE_LINK_LOCATION "${PRODUCT_WEB_SITE}"

;--------------------------------
; Pages
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "LICENSE.txt"
!insertmacro MUI_PAGE_COMPONENTS
!insertmacro MUI_PAGE_DIRECTORY
; Start menu page temporarily disabled due to macro conflicts
; !insertmacro MUI_PAGE_STARTMENU Application $StartMenuFolder
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

;--------------------------------
; Languages
!insertmacro MUI_LANGUAGE "English"

;--------------------------------
; Variables
; Var StartMenuFolder  ; Disabled for now due to macro conflicts

;--------------------------------
; Functions

; Check if application is running
Function .onInit
  ; Check Windows version
  ${IfNot} ${AtLeastWin10}
    MessageBox MB_OK|MB_ICONSTOP "This application requires Windows 10 or later.$\r$\n$\r$\nInstallation will be aborted."
    Abort
  ${EndIf}
  
  ; Check if running as administrator
  UserInfo::GetAccountType
  Pop $0
  ${If} $0 != "admin"
    MessageBox MB_OK|MB_ICONEXCLAMATION "Administrator privileges required.$\r$\n$\r$\nPlease run this installer as Administrator."
    SetErrorLevel 740 ; ERROR_ELEVATION_REQUIRED
    Abort
  ${EndIf}
  
  ; Check if application is already running
  System::Call 'kernel32::CreateMutex(i 0, i 0, t "PsychologicalRecordsMutex") i .r1 ?e'
  Pop $R0
  StrCmp $R0 0 +3
    MessageBox MB_OK|MB_ICONEXCLAMATION "Psychological Records is currently running. Please close it and try again."
    Abort
FunctionEnd

; Uninstaller initialization
Function un.onInit
  ; Check if application is running
  System::Call 'kernel32::CreateMutex(i 0, i 0, t "PsychologicalRecordsMutex") i .r1 ?e'
  Pop $R0
  StrCmp $R0 0 +3
    MessageBox MB_OK|MB_ICONEXCLAMATION "Psychological Records is currently running. Please close it and try again."
    Abort
FunctionEnd

;--------------------------------
; Installer Sections

Section "Core Application" SecCore
  SectionIn RO ; Read-only (always installed)
  
  SetDetailsPrint textonly
  DetailPrint "Installing core application files..."
  SetDetailsPrint listonly
  
  ; Set output path to the installation directory
  SetOutPath "$INSTDIR"
  
  ; Install main application files
  File "dist\PsychologicalRecords\PsychologicalRecords.exe"
  
  ; Install the _internal directory and all subdirectories
  SetOutPath "$INSTDIR\_internal"
  File /r "dist\PsychologicalRecords\_internal\*"
  
  ; Create application data directory
  CreateDirectory "$APPDATA\Psychological Records"
  
  ; Set permissions for application data directory (AccessControl plugin required)
  ; AccessControl::GrantOnFile "$APPDATA\Psychological Records" "(S-1-5-32-545)" "FullAccess"
  
  ; Store installation folder
  WriteRegStr HKCU "Software\Psychological Records" "" $INSTDIR
  
  ; Create uninstaller
  SetDetailsPrint textonly
  DetailPrint "Creating uninstaller..."
  SetDetailsPrint listonly
  WriteUninstaller "$INSTDIR\Uninstall.exe"
  
  ; Register application
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayName" "$(^Name)"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "UninstallString" "$INSTDIR\Uninstall.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayIcon" "$INSTDIR\PsychologicalRecords.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayVersion" "${PRODUCT_VERSION}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "URLInfoAbout" "${PRODUCT_WEB_SITE}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "Publisher" "${PRODUCT_PUBLISHER}"
  WriteRegDWORD ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "NoModify" 1
  WriteRegDWORD ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "NoRepair" 1
  
  ; Calculate and store installation size
  ${GetSize} "$INSTDIR" "/S=0K" $0 $1 $2
  IntFmt $0 "0x%08X" $0
  WriteRegDWORD ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "EstimatedSize" "$0"
  
  ; Register application path
  WriteRegStr HKLM "${PRODUCT_DIR_REGKEY}" "" "$INSTDIR\PsychologicalRecords.exe"
  WriteRegStr HKLM "${PRODUCT_DIR_REGKEY}" "Path" "$INSTDIR"
SectionEnd

Section "Documentation" SecDocs
  SetDetailsPrint textonly
  DetailPrint "Installing documentation..."
  SetDetailsPrint listonly
  
  SetOutPath "$INSTDIR"
  
  ; Install documentation files
  File /oname=README.txt "README.md"
  File /oname=RELEASE_NOTES.txt "RELEASE_NOTES.md"
  File "SHA256SUMS.txt"
SectionEnd

Section "Desktop Shortcut" SecDesktop
  SetDetailsPrint textonly
  DetailPrint "Creating desktop shortcut..."
  SetDetailsPrint listonly
  
  CreateShortcut "$DESKTOP\Psychological Records.lnk" "$INSTDIR\PsychologicalRecords.exe" "" "$INSTDIR\PsychologicalRecords.exe" 0 SW_SHOWNORMAL ALT|CONTROL|SHIFT|F5 "Professional Medical Records Management"
SectionEnd

Section "Quick Launch Shortcut" SecQuickLaunch
  SetDetailsPrint textonly
  DetailPrint "Creating quick launch shortcut..."
  SetDetailsPrint listonly
  
  CreateShortcut "$QUICKLAUNCH\Psychological Records.lnk" "$INSTDIR\PsychologicalRecords.exe" "" "$INSTDIR\PsychologicalRecords.exe" 0
SectionEnd

Section -AdditionalIcons
  SetDetailsPrint textonly
  DetailPrint "Creating start menu shortcuts..."
  SetDetailsPrint listonly
  
  ; Create Start Menu shortcuts
  CreateDirectory "$SMPROGRAMS\${PRODUCT_NAME}"
  CreateShortcut "$SMPROGRAMS\${PRODUCT_NAME}\Psychological Records.lnk" "$INSTDIR\PsychologicalRecords.exe" "" "$INSTDIR\PsychologicalRecords.exe" 0
  CreateShortcut "$SMPROGRAMS\${PRODUCT_NAME}\Uninstall.lnk" "$INSTDIR\Uninstall.exe"
SectionEnd

Section -Post
  ; Register file associations (optional)
  WriteRegStr HKCR ".prms" "" "PsychologicalRecords.Document"
  WriteRegStr HKCR "PsychologicalRecords.Document" "" "Psychological Records Document"
  WriteRegStr HKCR "PsychologicalRecords.Document\DefaultIcon" "" "$INSTDIR\PsychologicalRecords.exe,0"
  WriteRegStr HKCR "PsychologicalRecords.Document\shell\open\command" "" '"$INSTDIR\PsychologicalRecords.exe" "%1"'
SectionEnd

;--------------------------------
; Section Descriptions
!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
  !insertmacro MUI_DESCRIPTION_TEXT ${SecCore} "Core application files (required)"
  !insertmacro MUI_DESCRIPTION_TEXT ${SecDocs} "Documentation and user guide"
  !insertmacro MUI_DESCRIPTION_TEXT ${SecDesktop} "Create a desktop shortcut"
  !insertmacro MUI_DESCRIPTION_TEXT ${SecQuickLaunch} "Create a quick launch shortcut"
!insertmacro MUI_FUNCTION_DESCRIPTION_END

;--------------------------------
; Uninstaller Section
Section Uninstall
  ; Check if application is running
  System::Call 'kernel32::CreateMutex(i 0, i 0, t "PsychologicalRecordsMutex") i .r1 ?e'
  Pop $R0
  StrCmp $R0 0 +3
    MessageBox MB_OK|MB_ICONEXCLAMATION "Psychological Records is currently running. Please close it and try again."
    Abort
  
  ; Confirm uninstall with user data warning
  MessageBox MB_YESNO|MB_ICONQUESTION "This will remove Psychological Records from your computer.$\r$\n$\r$\nNote: Your patient data and settings will be preserved in your user profile.$\r$\n$\r$\nDo you want to continue?" IDYES +2
  Abort
  
  SetDetailsPrint textonly
  DetailPrint "Removing application files..."
  SetDetailsPrint listonly
  
  ; Remove registry keys
  DeleteRegKey ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}"
  DeleteRegKey HKLM "${PRODUCT_DIR_REGKEY}"
  DeleteRegKey HKCU "Software\Psychological Records"
  
  ; Remove file associations
  DeleteRegKey HKCR ".prms"
  DeleteRegKey HKCR "PsychologicalRecords.Document"
  
  ; Remove shortcuts
  Delete "$SMPROGRAMS\${PRODUCT_NAME}\Psychological Records.lnk"
  Delete "$SMPROGRAMS\${PRODUCT_NAME}\Uninstall.lnk"
  RMDir "$SMPROGRAMS\${PRODUCT_NAME}"
  
  Delete "$DESKTOP\Psychological Records.lnk"
  Delete "$QUICKLAUNCH\Psychological Records.lnk"
  
  ; Remove application files
  Delete "$INSTDIR\PsychologicalRecords.exe"
  Delete "$INSTDIR\README.txt"
  Delete "$INSTDIR\RELEASE_NOTES.txt"
  Delete "$INSTDIR\SHA256SUMS.txt"
  Delete "$INSTDIR\Uninstall.exe"
  
  ; Remove _internal directory
  RMDir /r "$INSTDIR\_internal"
  
  ; Remove installation directory if empty
  RMDir "$INSTDIR"
  
  SetDetailsPrint textonly
  DetailPrint "Uninstallation completed successfully."
  SetDetailsPrint listonly
  
  ; Inform user about preserved data
  MessageBox MB_OK|MB_ICONINFORMATION "Psychological Records has been successfully removed.$\r$\n$\r$\nYour patient data and settings have been preserved in:$\r$\n$APPDATA\Psychological Records"
SectionEnd
