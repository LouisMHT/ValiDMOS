# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['your_script.py'],
    pathex=['.'],
    binaries=[],
    datas=[('logo3.png', '.'), ('logo.png', '.')],  # Ajoutez vos fichiers ici
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='GRDF_DMOSControl',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    icon='logo3.png',  # Optionnel, pour ajouter une icône
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='GRDF_DMOSControl',
)
