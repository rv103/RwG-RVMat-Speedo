# -*- mode: python ; coding: utf-8 -*-
import os
import tkinterdnd2

# Bundle the tkinterdnd2 package data (the tkdnd binaries) portably, wherever
# it is installed in the building environment.
tkdnd_dir = os.path.dirname(tkinterdnd2.__file__)

a = Analysis(
    ['RwG_RVMat_Speedo.py'],
    pathex=[],
    binaries=[],
    datas=[
        (tkdnd_dir, 'tkinterdnd2/'),
        ('RwG_Logo_Modelling.ico', '.'),
    ],
    hiddenimports=['tkinterdnd2'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='RwG_RVMat_Speedo',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='RwG_Logo_Modelling.ico',
)
