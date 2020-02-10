
# ------ IMPORTS ----------#
import cx_Freeze

# -------------------------#


base = "Win32GUI"
#if sys.platform == 'win32':
#    base = "Win32GUI"

shortcut_table = [
    ("DesktopShortcut",            # Shortcut
     "DesktopFolder",              # Directory_
     "Lucro da Acao",              # Name
     "TARGETDIR",                  # Component_
     "[TARGETDIR]stock_eval.exe",  # Target
     None,                         # Arguments
     None,                         # Description
     None,                         # Hotkey
     None,                         # Icon
     None,                         # IconIndex
     None,                         # ShowCmd
     'TARGETDIR'                   # WkDir
     )
    ]


executables = [cx_Freeze.Executable("stock_eval.py", base=base, icon="images/atados.ico",)]
additional_mods = ['numpy.core._methods', 'numpy.lib.format']
cx_Freeze.setup(
    name="Lucro da Acao",
    options={"build_exe": {"packages": ["tkinter", "matplotlib", "numpy"],
                           "include_files": ["images/atados.ico",
                                             "images/atados-small.PNG",
                                             "images/start.png",
                                             "images",
                                             "tcl86t.dll",
                                             "tk86t.dll"],
                           'includes': additional_mods,
                           'include_msvcr': True,
                           },
             "bdist_msi": {"data": {"Shortcut": shortcut_table}}},
    version="1.0",
    description="Atados: O Lucro da Acao por Jose Salgueiro",
    executables=executables
    )

