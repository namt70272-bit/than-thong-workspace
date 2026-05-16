# -*- mode: python ; coding: utf-8 -*-
a = Analysis(
    ['E:\\KY-DATA\\OpenClaw\\runtime-mirror\\.openclaw\\workspace\\packaging\\than_thong\\__main__.py'],
    pathex=['E:\\KY-DATA\\OpenClaw\\runtime-mirror\\.openclaw\\workspace\\packaging'],
    binaries=[],
    datas=[
        ('E:\\KY-DATA\\OpenClaw\\runtime-mirror\\.openclaw\\workspace\\tools-internal\\scripts', 'scripts'),
        ('E:\\KY-DATA\\OpenClaw\\runtime-mirror\\.openclaw\\workspace\\packaging\\than_thong\\resources\\icon.png', 'resources'),
        ('E:\\KY-DATA\\OpenClaw\\runtime-mirror\\.openclaw\\workspace\\packaging\\than_thong\\resources\\icon.ico', 'resources'),
    ],
    hiddenimports=['pystray', 'PIL', 'plyer', 'plyer.platforms.win', 'plyer.platforms.win.notification', 'plyer.facades.notification', 'winshell', 'win32com', 'win32com.client', 'psutil'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
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
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    icon='E:\\KY-DATA\\OpenClaw\\runtime-mirror\\.openclaw\\workspace\\packaging\\than_thong\\resources\\icon.ico',
)
