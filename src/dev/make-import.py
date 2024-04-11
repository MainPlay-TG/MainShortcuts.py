import os
os.chdir(os.path.dirname(os.path.dirname(__file__))+"/MainShortcuts")
import_data={
  "import MainShortcuts.{name} as {name}":[
    "dict",
    "dir",
    "file",
    "json",
    "list",
    "os",
    "path",
    "proc",
    "str",
    ],
  "from MainShortcuts.{name} import {name}":[
    "cfg",
    "dictplus",
    "fileobj",
    ],
  "{name}=main.{name}":[
    "cd",
    "clear_ANSI",
    "cls_ANSI",
    "clear",
    "cls",
    "exit",
    "pwd",
    ]
  }
lines=[
  '"""Этот файл просто импортирует части модуля',
  'Он создаётся автоматически"""',
  "import MainShortcuts.main as main",
  "imports_all=[]",
  "imports_import_errors={}",
  ]
for code,names in import_data.items():
  for name in names:
    lines+=[
      "try:",
      "  "+code.format(name=name),
      "  imports_all.append('{name}')".format(name=name),
      "except Exception as e:",
      "  imports_import_errors['{name}']=e".format(name=name),
      ]
lines+=[
  "imports_all.sort()",
  ]
with open("imports.py","wb") as f:
  f.write("\n".join(lines).encode("utf-8"))
print("Импорт частей модуля собран")
