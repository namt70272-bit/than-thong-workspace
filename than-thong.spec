# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_submodules

hiddenimports = ['pystray', 'PIL', 'plyer', 'winshell', 'win32com']
hiddenimports += collect_submodules('than_thong')


a = Analysis(
    ['E:\\KY-DATA\\OpenClaw\\runtime-mirror\\.openclaw\\workspace\\packaging\\than-thong\\__main__.py'],
    pathex=[],
    binaries=[],
    datas=[('E:\\KY-DATA\\OpenClaw\\runtime-mirror\\.openclaw\\workspace\\tools-internal\\scripts', 'scripts'), ('E:\\KY-DATA\\OpenClaw\\runtime-mirror\\.openclaw\\workspace\\packaging\\than-thong\\resources\\icon.png', 'resources'), ('E:\\KY-DATA\\OpenClaw\\runtime-mirror\\.openclaw\\workspace\\packaging\\than-thong\\resources\\icon.ico', 'resources')],
    hiddenimports=hiddenimports,
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
    name='than-thong',
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
    icon=['E:\\KY-DATA\\OpenClaw\\runtime-mirror\\.openclaw\\workspace\\packaging\\than-thong\\resources\\icon.ico'],
)
