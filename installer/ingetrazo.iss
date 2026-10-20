; Inno Setup script for TectSkill-3D — a Thai build of IngeTrazo.
;
; TectSkill-3D is based on IngeTrazo by Ing. Marco Sumari Tellez and the
; IngeTrazo contributors (https://github.com/ingelibre/ingetrazo), released
; under GPL-3.0-or-later. This derivative keeps that license and its credits.
;
; Builds a professional Windows installer: multilingual wizard, GPL license page,
; shortcuts, "Add or Remove Programs" entry and a clean uninstaller.
;
; Local build (needs Inno Setup 6+):
;     iscc /DMyAppVersion=0.2.0 installer\ingetrazo.iss
;
; CI build: see .github/workflows/build-windows.yml
;
; The AppId is a FIXED GUID — never change it between versions, or Windows
; treats every release as a different app and upgrades stop being clean.

#define MyAppName "TectSkill-3D"
#define MyAppPublisher "TectSkill"
#define MyAppURL "https://tectskill.com"
; The program inside the bundle keeps its build name (PyInstaller spec).
#define MyAppExeName "ingetrazo.exe"

; MyAppVersion is injected from the build command with /DMyAppVersion=X.Y.Z
#ifndef MyAppVersion
  #define MyAppVersion "0.0.0-dev"
#endif

[Setup]
; FIXED AppId GUID — generated once for TectSkill-3D (its own, so it installs
; side by side with the original IngeTrazo). Never change it between versions.
AppId={{3B09C71C-8F10-4787-8550-CD9813E130F2}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
AppComments=Based on IngeTrazo (GPL-3.0-or-later) by Marco Sumari Tellez and contributors
VersionInfoVersion={#MyAppVersion}
VersionInfoCompany={#MyAppPublisher}
VersionInfoDescription=TectSkill-3D - Thai 3D modeler based on IngeTrazo (GPL-3.0)
VersionInfoProductName={#MyAppName}

DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
PrivilegesRequired=admin
PrivilegesRequiredOverridesAllowed=dialog

; Free software: the "license" page shows the GPL-3.0 text.
LicenseFile=..\LICENSE

OutputDir=..\dist
OutputBaseFilename=TectSkill-3D-setup-v{#MyAppVersion}

WizardStyle=modern
; (Saved as UTF-8 WITH a BOM: that is how Inno Setup knows the texts
; below are UTF-8 — without it «Associações» would come out garbled.)
; The wizard speaks the language of Windows (English, Spanish, Brazilian
; Portuguese or Polish) and asks only when none of them matches (issue #135).
ShowLanguageDialog=auto
; Follow Windows on every install, upgrades included. Inno Setup reuses the
; language of the previous install by default, and every install up to
; 0.5.3 was Spanish-only: upgrading kept showing Spanish on an English
; Windows (issue #591).
UsePreviousLanguage=no
DisableProgramGroupPage=yes
; We register file-type icons/associations — tells Explorer to refresh them.
ChangesAssociations=yes
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
Compression=lzma2
SolidCompression=yes
UninstallDisplayIcon={app}\{#MyAppExeName}
SetupIconFile=..\resources\icons\ingetrazo.ico

[Languages]
; English first: it is the fallback when Windows speaks something else.
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"
Name: "polish"; MessagesFile: "compiler:Languages\Polish.isl"

[CustomMessages]
english.SkpDefault=Open .skp files with TectSkill-3D (double-click)
english.FileAssociations=File associations:
english.IgzDocument=TectSkill-3D document
english.DaeModel=COLLADA model (TectSkill-3D)
english.SkpModel=SKP model (TectSkill-3D)
spanish.SkpDefault=Abrir archivos .skp con TectSkill-3D (doble clic)
spanish.FileAssociations=Asociaciones de archivos:
spanish.IgzDocument=Documento de TectSkill-3D
spanish.DaeModel=Modelo COLLADA (TectSkill-3D)
spanish.SkpModel=Modelo SKP (TectSkill-3D)
brazilianportuguese.SkpDefault=Abrir arquivos .skp com o TectSkill-3D (clique duplo)
brazilianportuguese.FileAssociations=Associações de arquivos:
brazilianportuguese.IgzDocument=Documento do TectSkill-3D
brazilianportuguese.DaeModel=Modelo COLLADA (TectSkill-3D)
brazilianportuguese.SkpModel=Modelo SKP (TectSkill-3D)
polish.SkpDefault=Otwieraj pliki .skp w TectSkill-3D (dwukrotne kliknięcie)
polish.FileAssociations=Skojarzenia plików:
polish.IgzDocument=Dokument TectSkill-3D
polish.DaeModel=Model COLLADA (TectSkill-3D)
polish.SkpModel=Model SKP (TectSkill-3D)

[Tasks]
Name: "skpdefault"; Description: "{cm:SkpDefault}"; \
    GroupDescription: "{cm:FileAssociations}"
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; \
    GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; The whole PyInstaller one-dir bundle.
Source: "..\dist\ingetrazo\*"; DestDir: "{app}"; \
    Flags: ignoreversion recursesubdirs createallsubdirs
; Branded document icons, copied to the {app} root so [Registry] DefaultIcon
; entries can reference them with a stable path.
Source: "..\resources\icons\mimetypes\ingetrazo-igz.ico"; DestDir: "{app}"; \
    Flags: ignoreversion
Source: "..\resources\icons\mimetypes\ingetrazo-dae.ico"; DestDir: "{app}"; \
    Flags: ignoreversion
Source: "..\resources\icons\mimetypes\ingetrazo-skp.ico"; DestDir: "{app}"; \
    Flags: ignoreversion

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; \
    Tasks: desktopicon

[Registry]
; ── Hybrid laptops (Intel + NVIDIA/AMD): run on the discrete GPU ─────────────
; This is the value Settings ▸ System ▸ Display ▸ Graphics writes when the user
; picks "High performance" for a program; without it Windows starts IngeTrazo
; on the integrated chip and the viewport crawls. Only written when the user
; has not chosen anything yet (the app repeats the check at start-up).
Root: HKCU; Subkey: "Software\Microsoft\DirectX\UserGpuPreferences"; \
    ValueType: string; ValueName: "{app}\{#MyAppExeName}"; \
    ValueData: "GpuPreference=2;"; Flags: createvalueifdoesntexist uninsdeletevalue

; ── .igz — IngeTrazo's own format: full association + branded document icon ──
; Double-click opens the document in IngeTrazo and Explorer shows the .igz icon.
Root: HKA; Subkey: "Software\Classes\.igz"; ValueType: string; \
    ValueData: "TectSkill3D.Document"; Flags: uninsdeletevalue
Root: HKA; Subkey: "Software\Classes\TectSkill3D.Document"; ValueType: string; \
    ValueData: "{cm:IgzDocument}"; Flags: uninsdeletekey
Root: HKA; Subkey: "Software\Classes\TectSkill3D.Document\DefaultIcon"; \
    ValueType: string; ValueData: "{app}\ingetrazo-igz.ico,0"
Root: HKA; Subkey: "Software\Classes\TectSkill3D.Document\shell\open\command"; \
    ValueType: string; ValueData: """{app}\{#MyAppExeName}"" ""%1"""

; ── .dae / .skp — standard interchange formats: "Open with" only ────────────
; We DO NOT take over the default program or the file icon (Windows ties the
; shown icon to the default handler, and stealing .dae/.skp from the
; programs the user already has would surprise them). Instead we register a ProgId and add it to
; each extension's OpenWithProgids list, so IngeTrazo appears in the right-click
; "Open with" menu. The ProgId carries the branded icon, which only takes visual
; effect if the user later chooses IngeTrazo as the default for these files.
Root: HKA; Subkey: "Software\Classes\TectSkill3D.dae"; ValueType: string; \
    ValueData: "{cm:DaeModel}"; Flags: uninsdeletekey
Root: HKA; Subkey: "Software\Classes\TectSkill3D.dae\DefaultIcon"; \
    ValueType: string; ValueData: "{app}\ingetrazo-dae.ico,0"
Root: HKA; Subkey: "Software\Classes\TectSkill3D.dae\shell\open\command"; \
    ValueType: string; ValueData: """{app}\{#MyAppExeName}"" ""%1"""
Root: HKA; Subkey: "Software\Classes\.dae\OpenWithProgids"; \
    ValueType: string; ValueName: "TectSkill3D.dae"; ValueData: ""; \
    Flags: uninsdeletevalue

Root: HKA; Subkey: "Software\Classes\TectSkill3D.skp"; ValueType: string; \
    ValueData: "{cm:SkpModel}"; Flags: uninsdeletekey
Root: HKA; Subkey: "Software\Classes\TectSkill3D.skp\DefaultIcon"; \
    ValueType: string; ValueData: "{app}\ingetrazo-skp.ico,0"
Root: HKA; Subkey: "Software\Classes\TectSkill3D.skp\shell\open\command"; \
    ValueType: string; ValueData: """{app}\{#MyAppExeName}"" ""%1"""
Root: HKA; Subkey: "Software\Classes\.skp\OpenWithProgids"; \
    ValueType: string; ValueName: "TectSkill3D.skp"; ValueData: ""; \
    Flags: uninsdeletevalue
; Optional task: make IngeTrazo the DEFAULT opener for .skp (double-click).
; Checked by default — .skp now opens natively (openskp backend). Users who
; prefer another program for .skp can untick it; uninstall removes the value
; and Windows falls back to the previous handler.
Root: HKA; Subkey: "Software\Classes\.skp"; ValueType: string; \
    ValueData: "TectSkill3D.skp"; Tasks: skpdefault; Flags: uninsdeletevalue

[Run]
Filename: "{app}\{#MyAppExeName}"; \
    Description: "{cm:LaunchProgram,{#MyAppName}}"; \
    Flags: nowait postinstall skipifsilent
