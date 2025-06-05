
# pyinstaller
uv add pyinstaller打包应用

## 安装pyinstaller
```bash

uv add pyinstaller

```
## 编制脚本
新建`build.spec`文件，代码如下：
```bash
# build.spec
block_cipher = None

a = Analysis(
    ['OCRmyPDF/main.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('.venv/Lib/site-packages/customtkinter', 'customtkinter'),
        ('.venv/Lib/site-packages/ocrmypdf/data', 'ocrmypdf/data')
    ],
    hiddenimports=[
        'pkg_resources.py2_warn',
        'pkg_resources.markers',
        'ocrmypdf._exec.ghostscript',
        'ocrmypdf._exec.tesseract',
        'ocrmypdf._exec.pngquant',
        'ocrmypdf._exec.unpaper',
        'ocrmypdf._exec.qpdf',
        'lxml.etree',
        'lxml._elementpath',
        'skimage.filters.rank.core_cy',
        'skimage.filters.rank.generic_cy',
        'skimage.filters.rank.core_cy_3d',
        'skimage.filters.rank.generic_cy_3d',
        'pikepdf._cpphelpers'
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='PDF_OCR_Tool',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,  # 启用strip，减小体积
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    icon='app_icon.ico',
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
```
执行下面脚本，开始打包应用。

```bash
pyinstaller build.spec #build.spec 脚本放在根目录，执行命令pyinstaller build.spec
```



3. UPX 进一步压缩
[下载UPX](https://github.com/upx/upx/releases)并添加到环境变量
上述nuitka中添加 --onefile-compression=upx，使用UPX压缩exe文件，体积小，但打包速度会慢一些。