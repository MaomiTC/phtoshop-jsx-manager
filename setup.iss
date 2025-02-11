#define MyAppName "PS JSX Manager"
#define MyAppVersion "1.0"
#define MyAppPublisher "猫咪老师Reimagined"
#define MyAppURL "https://www.xiaohongshu.com/user/profile/59f1fcc411be101aba7f048f"
#define MyAppExeName "PS-JSX-Manager.exe"

[Setup]
; 基本信息
AppId={{A8C89E2F-6973-45B2-B0D4-E9738E9AE55C}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}

; 安装目录设置
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
OutputDir=installer
OutputBaseFilename=PS-JSX-Manager-Setup
SetupIconFile=ps-jsx.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern

; 权限设置
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
; 如果安装了中文语言包，可以取消下面这行的注释
; Name: "chinesesimplified"; MessagesFile: "compiler:Languages\ChineseSimplified.isl"

[Messages]
; 自定义中文消息
english.BeveledLabel=PS JSX Manager
english.ButtonNext=下一步(&N) >
english.ButtonBack=< 上一步(&B)
english.ButtonCancel=取消(&C)
english.ButtonInstall=安装(&I)
english.ButtonFinish=完成(&F)
english.SelectDirLabel3=安装程序将安装 [name] 到下列文件夹。
english.SelectDirBrowseLabel=点击"下一步"继续。如果要选择其他文件夹，请点击"浏览"。

[Tasks]
Name: "desktopicon"; Description: "创建桌面快捷方式"; GroupDescription: "附加任务:"; Flags: unchecked
Name: "quicklaunchicon"; Description: "创建快速启动栏图标"; GroupDescription: "附加任务:"; Flags: unchecked

[Files]
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "mao.png"; DestDir: "{app}"; Flags: ignoreversion
Source: "ps-jsx.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\ps-jsx.ico"
Name: "{group}\卸载 {#MyAppName}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\ps-jsx.ico"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\ps-jsx.ico"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "运行 {#MyAppName}"; Flags: nowait postinstall skipifsilent

[CustomMessages]
english.LaunchProgram=运行 %1 