# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('locales/', 'locales/'),
        ('src/', 'src/'),
        ('app_icon.ico', '.'),
        ('app_icon.png', '.'),
        ('database.py', '.'),
        ('login_dialog.py', '.'),
        ('main_window.py', '.'),
        ('consultation_dialog.py', '.'),
        ('person_dialog.py', '.'),
        ('assessment_dialog.py', '.'),
        ('change_password_dialog.py', '.'),
        ('medical_records_window.py', '.'),
        ('pdf_generator.py', '.'),
    ],
    hiddenimports=[
        'PyQt6.QtCore',
        'PyQt6.QtGui', 
        'PyQt6.QtWidgets',
        'PyQt6.QtPrintSupport',
        'cryptography',
        'cryptography.fernet',
        'bcrypt',
        'sqlite3',
        'json',
        'os',
        'sys',
        'hashlib',
        'src.utils.language_manager',
        'src.utils.app_translator',
        'src.utils.language_aware_mixin',
        'src.ui.styles',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'PIL',
        'email',
        'http',
        'urllib',
        'xml'
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='PsychologicalRecords',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='app_icon.ico',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='PsychologicalRecords',
)
