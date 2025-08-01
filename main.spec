# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('audio', 'audio'), ('game_classes', 'game_classes'), ('all_liquid_animations.png', '.'), ('bg_liquids.png', '.'), ('bgtiles.png', '.'), ('blank.png', '.'), ('deeper_bgs.png', '.'), ('entities_level1.png', '.'), ('entities_level2.png', '.'), ('entities_level3.png', '.'), ('entities_level4.png', '.'), ('font.png', '.'), ('hot_bar_selector.png', '.'), ('hotbar.png', '.'), ('inventory.png', '.'), ('items_and_fx.png', '.'), ('liqsall.png', '.'), ('liquids.png', '.'), ('newliqdsall.png', '.'), ('tile_liquid_animations.png', '.'), ('tinyfont.png', '.'), ('title.png', '.')],
    hiddenimports=[],
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
    [],
    exclude_binaries=True,
    name='main',
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
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)
