# -*- mode: python ; coding: utf-8 -*-
import os

block_cipher = None

# Entry script at project root (spec is in config/)
spec_dir = os.path.dirname(os.path.abspath(SPEC))
project_root = os.path.dirname(spec_dir)
main_script = os.path.join(project_root, 'main.py')

a = Analysis(
    [main_script],
    pathex=[project_root],
    binaries=[],
    datas=[
        (os.path.join(project_root, 'locales'), 'locales'),
        (os.path.join(project_root, 'src'), 'src'),
        (os.path.join(project_root, 'assets', 'app_icon.ico'), '.'),
        (os.path.join(project_root, 'assets', 'app_icon.png'), '.'),
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
        # Explicitly include Pillow and urllib so reportlab.pdf can use them
        'PIL',
        'PIL.Image',
        'urllib',
        'urllib.request',
        'urllib.parse',
        'urllib.error',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Keep heavy/unused libs out to reduce size
        'tkinter',
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
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
    icon=os.path.join(project_root, 'assets', 'app_icon.ico'),
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
