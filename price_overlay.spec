# -*- mode: python ; coding: utf-8 -*-
added_files = [

("actions.png", "."),
("gif.dll", "tesseract"),
("jpeg62.dll", "tesseract"),
("leptonica-1.81.1.dll", "tesseract"),
("liblzma.dll", "tesseract"),
("libpng16.dll", "tesseract"),
("libwebpmux.dll", "tesseract"),
("tiff.dll", "tesseract"),
("webp.dll", "tesseract"),
("zlib1.dll", "tesseract"),
("tesseract/tessdata", "tesseract/tessdata"),

]
added_binaries = [
('tesseract.exe', 'tesseract')
]

block_cipher = None


a = Analysis(['price_overlay.py'],
             pathex=[],
             binaries=added_binaries,
             datas=added_files,
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,  
          [],
          name='price_overlay',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
