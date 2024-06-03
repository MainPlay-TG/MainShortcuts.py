import os
os.chdir(os.path.dirname(os.path.dirname(__file__)) + "/MainShortcuts")
import_data = {
    "{name}=main.{name}": [
        "cd",
        "clear_ANSI",
        "clear",
        "cls_ANSI",
        "cls",
        "exit",
        "pwd",
        "timedelta",
    ],
    "from MainShortcuts.{name} import {name}": [
        "cfg",
        "dictplus",
        "fileobj"
    ],
    "import MainShortcuts.{name} as {name}": [
        "dict",
        "dir",
        "file",
        "json",
        "list",
        "os",
        "path",
        "proc",
        "str",
        "win"
    ]
}
lines = [
    '"""Этот файл просто импортирует части модуля',
    'Он создаётся автоматически"""',
    "import os",
    "import MainShortcuts.main as main",
    "imports_all=[]",
    "imports_import_errors={}",
    "noimport=[]",
    'if "MS_NOIMPORT" in os.environ:',
    '  for i in os.environ["MS_NOIMPORT"].split(","):',
    "    if i.strip():",
    "      noimport.append(i.strip().lower())",
    "noimport.sort()",
]
for code, names in import_data.items():
  for name in names:
    lines += [
        f"if not '{name}' in noimport:",
        "  try:",
        "    " + code.format(name=name),
        "    imports_all.append('{name}')".format(name=name),
        "  except Exception as e:",
        "    imports_import_errors['{name}']=e".format(name=name),
    ]
lines += [
    "imports_all.sort()",
]
with open("imports.py", "wb") as f:
  f.write("\n".join(lines).encode("utf-8"))
print("Импорт частей модуля собран в файл " + os.path.abspath("imports.py"))
