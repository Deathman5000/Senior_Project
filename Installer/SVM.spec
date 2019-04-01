# -*- mode: python -*-

block_cipher = None


a = Analysis(['SVM.py'],
             pathex=['C:\\Users\\James\\Documents\\CS4391\\Senior_Project\\Installer'],
             binaries=[],
             datas=[],
             hiddenimports=['sklearn.neighbors.typedefs'],
             hookspath=[],
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
          name='SVM',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
