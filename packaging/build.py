"""
Than-thong App — PyInstaller build script.

Usage:
    python build.py              # Build single-file exe
    python build.py --onedir     # Build directory mode
"""
import os, sys, shutil, subprocess, argparse
from pathlib import Path

HERE = Path(__file__).resolve().parent
APP_DIR = HERE / "than_thong"
SCRIPTS_DIR = HERE.parent / "tools-internal" / "scripts"
DIST_DIR = HERE / "dist"
BUILD_DIR = HERE / "build"
RES_DIR = APP_DIR / "resources"


def clean():
    for d in [DIST_DIR, BUILD_DIR]:
        if d.exists():
            shutil.rmtree(d)


def _safe(s):
    """Escape path for .spec file (double backslashes)."""
    return str(s).replace("\\", "\\\\")


def _write_spec():
    """Generate .spec file with proper escaping."""
    spec_path = HERE / "than-thong.spec"

    entry = _safe(APP_DIR / "__main__.py")
    pkgdir = _safe(APP_DIR.parent)  # parent of than-thong/
    sdir = _safe(SCRIPTS_DIR)
    ipng = _safe(RES_DIR / "icon.png")
    iico = _safe(RES_DIR / "icon.ico")

    spec_content = """# -*- mode: python ; coding: utf-8 -*-
a = Analysis(
    ['""" + entry + """'],
    pathex=['""" + pkgdir + """'],
    binaries=[],
    datas=[
        ('""" + sdir + """', 'scripts'),
        ('""" + ipng + """', 'resources'),
        ('""" + iico + """', 'resources'),
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
    icon='""" + iico + """',
)
"""
    spec_path.write_text(spec_content, encoding="utf-8")
    return spec_path


def build():
    spec_path = _write_spec()
    cmd = [
        sys.executable, "-m", "PyInstaller",
        str(spec_path),
        "--noconfirm",
        "--clean",
        "--distpath=" + str(DIST_DIR),
        "--workpath=" + str(BUILD_DIR),
    ]
    print("[TT] Building...")
    subprocess.run(cmd, check=True)


def main():
    parser = argparse.ArgumentParser(description="Build than-thong app")
    parser.add_argument("--onedir", action="store_true")
    parser.add_argument("--no-clean", action="store_true")
    args = parser.parse_args()

    if not args.no_clean:
        clean()

    build()

    exe = DIST_DIR / "than-thong.exe"
    if exe.exists():
        mb = exe.stat().st_size / (1024 * 1024)
        print("[TT] Build success: %s (%.1f MB)" % (exe, mb))
    else:
        print("[TT] Build done. Check: " + str(DIST_DIR))


if __name__ == "__main__":
    main()
