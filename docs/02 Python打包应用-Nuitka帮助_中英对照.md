<!-- filepath: f:\Code\OCR\MyOCR\docs\OCRmyPDF手册\Nuitka帮助_中英对照.md -->
Usage: python.exe -m nuitka [--mode=compilation_mode] [--run] [options] main_module.py  
用法：python.exe -m nuitka [--mode=compilation_mode] [--run] [选项] main_module.py

    Note: For general plugin help (they often have their own
    command line options too), consider the output of
    '--help-plugins'.  
    注意：有关插件的通用帮助（它们通常也有自己的命令行选项），请参考 '--help-plugins' 的输出。

Options:  
选项：
  --help                show this help message and exit  
  --help                显示此帮助信息并退出
  --version             Show version information and important details for bug  
  --version             显示版本信息和用于错误报告的重要细节，然后退出。默认关闭。
                        reports, then exit. Defaults to off.
  --module              Create an importable binary extension module  
  --module              创建一个可导入的二进制扩展模块可执行文件，而不是程序。默认关闭。
                        executable instead of a program. Defaults to off.
  --mode=COMPILATION_MODE  
  --mode=COMPILATION_MODE  编译模式。Accelerated 在你的 Python 安装中运行并依赖于它。Standalone 创建一个包含可执行文件的文件夹以运行它。Onefile 创建一个用于部署的单一可执行文件。App 除 macOS 外等同于 onefile。Module 创建模块，package 包含所有子模块和子包。Dll 目前在开发中，尚未对用户开放。默认值为 'accelerated'。
                        Mode in which to compile. Accelerated runs in your
                        Python installation and depends on it. Standalone
                        creates a folder with an executable contained to run
                        it. Onefile creates a single executable to deploy. App
                        is onefile except on macOS where it's not to be used.
                        Module makes a module, and package includes also all
                        sub-modules and sub-packages. Dll is currently under
                        development and not for users yet. Default is
                        'accelerated'.
  --standalone          Enable standalone mode for output. This allows you to  
  --standalone          启用独立模式输出。这允许你将生成的二进制文件转移到其他机器，无需依赖现有 Python 安装。这也意味着文件会变大。它隐含这些选项："--follow-imports" 和 "--python-flag=no_site"。默认关闭。
                        transfer the created binary to other machines without
                        it using an existing Python installation. This also
                        means it will become big. It implies these options: "
                        --follow-imports" and "--python-flag=no_site".
                        Defaults to off.
  --onefile             On top of standalone mode, enable onefile mode. This  
  --onefile             在独立模式基础上，启用单文件模式。这意味着不是文件夹，而是创建并使用一个压缩的可执行文件。默认关闭。
                        means not a folder, but a compressed executable is
                        created and used. Defaults to off.
  --python-flag=FLAG    Python flags to use. Default is what you are using to  
  --python-flag=FLAG    要使用的 Python 标志。默认与你运行 Nuitka 时一致，这会强制特定模式。这些选项也存在于标准 Python 可执行文件中。目前支持："-S"（别名 "no_site"）、"static_hashes"（不使用哈希随机化）、"no_warnings"（不显示 Python 运行时警告）、"-O"（别名 "no_asserts"）、"no_docstrings"（不使用文档字符串）、"-u"（别名 "unbuffered"）、"isolated"（不加载外部代码）、"-P"（别名 "safe_path"，模块搜索时不使用当前目录）和 "-m"（包模式，编译为 "package.__main__"）。默认空。
                        run Nuitka, this enforces a specific mode. These are
                        options that also exist to standard Python executable.
                        Currently supported: "-S" (alias "no_site"),
                        "static_hashes" (do not use hash randomization),
                        "no_warnings" (do not give Python run time warnings),
                        "-O" (alias "no_asserts"), "no_docstrings" (do not use
                        doc strings), "-u" (alias "unbuffered"), "isolated"
                        (do not load outside code), "-P" (alias "safe_path",
                        do not used current directory in module search) and
                        "-m" (package mode, compile as "package.__main__").
                        Default empty.
  --python-debug        Use debug version or not. Default uses what you are  
  --python-debug        是否使用调试版本。默认与你运行 Nuitka 时一致，通常为非调试版本。仅用于调试和测试目的。
                        using to run Nuitka, most likely a non-debug version.
                        Only for debugging and testing purposes.
  --python-for-scons=PATH  
  --python-for-scons=PATH  使用 Python 3.4 编译时，提供用于 Scons 的 Python 二进制路径。否则 Nuitka 可使用你运行 Nuitka 的 Python，或从 Windows 注册表等找到 Python 安装。在 Windows 上需要 Python 3.5 或更高版本，非 Windows 上 2.6 或 2.7 也可。
                        When compiling with Python 3.4 provide the path of a
                        Python binary to use for Scons. Otherwise Nuitka can
                        use what you run Nuitka with, or find Python
                        installation, e.g. from Windows registry. On Windows,
                        a Python 3.5 or higher is needed. On non-Windows, a
                        Python 2.6 or 2.7 will do as well.
  --main=PATH           If specified once, this takes the place of the  
  --main=PATH           如果指定一次，则取代位置参数，即要编译的文件名。多次指定时，启用“multidist”（见用户手册），允许你根据文件名或调用名创建不同的二进制文件。
                        positional argument, i.e. the filename to compile.
                        When given multiple times, it enables "multidist" (see
                        User Manual) it allows you to create binaries that
                        depending on file name or invocation name.

  Control the inclusion of modules and packages in result  
  控制结果中模块和包的包含：
    --include-package=PACKAGE  
    --include-package=PACKAGE  包含整个包。以 Python 命名空间形式给出，例如 "some_package.sub_package"，Nuitka 会找到并包含该包及其下所有模块到生成的二进制或扩展模块中，并可供代码导入。为避免不需要的子包（如 tests），可用 "--nofollow-import-to=*.tests"。默认空。
                        Include a whole package. Give as a Python namespace,
                        e.g. "some_package.sub_package" and Nuitka will then
                        find it and include it and all the modules found below
                        that disk location in the binary or extension module
                        it creates, and make it available for import by the
                        code. To avoid unwanted sub packages, e.g. tests you
                        can e.g. do this "--nofollow-import-to=*.tests".
                        Default empty.
    --include-module=MODULE  
    --include-module=MODULE  包含单个模块。以 Python 命名空间形式给出，例如 "some_package.some_module"，Nuitka 会找到并包含该模块到生成的二进制或扩展模块中，并可供代码导入。默认空。
                        Include a single module. Give as a Python namespace,
                        e.g. "some_package.some_module" and Nuitka will then
                        find it and include it in the binary or extension
                        module it creates, and make it available for import by
                        the code. Default empty.
    --include-plugin-directory=MODULE/PACKAGE  
    --include-plugin-directory=MODULE/PACKAGE  还包含该目录下的代码，视为每个都作为主文件给出。覆盖所有其他包含选项。应优先使用按名称的其他包含选项，而不是文件名，这些通过 sys.path 查找。此选项仅用于特殊用途。可多次给出。默认空。
                        Include also the code found in that directory,
                        considering as if they are each given as a main file.
                        Overrides all other inclusion options. You ought to
                        prefer other inclusion options, that go by names,
                        rather than filenames, those find things through being
                        in "sys.path". This option is for very special use
                        cases only. Can be given multiple times. Default
                        empty.
    --include-plugin-files=PATTERN  
    --include-plugin-files=PATTERN  包含匹配 PATTERN 的文件。覆盖所有其他跟随选项。可多次给出。默认空。
                        Include into files matching the PATTERN. Overrides all
                        other follow options. Can be given multiple times.
                        Default empty.
    --prefer-source-code  
    --prefer-source-code  对于已编译的扩展模块，如果同时有源文件和扩展模块，通常使用扩展模块，但从可用源代码编译模块性能更佳。如不需要，可用 --no-prefer-source-code 禁用相关警告。默认关闭。
                        For already compiled extension modules, where there is
                        both a source file and an extension module, normally
                        the extension module is used, but it should be better
                        to compile the module from available source code for
                        best performance. If not desired, there is --no-
                        prefer-source-code to disable warnings about it.
                        Default off.

  Control the following into imported modules:  
  控制导入模块的以下行为：
    --follow-imports    Descend into all imported modules. Defaults to on in  
    --follow-imports    递归进入所有导入的模块。独立模式下默认开启，否则关闭。
                        standalone mode, otherwise off.