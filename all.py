#!/data/data/com.termux/files/usr/bin/python3
import os
import sys
import MainShortcuts as ms
from shutil import which
from time import sleep
from subprocess import Popen
package = "MainShortcuts"
md_lang={
  "added":"Добавлено:",
  "changed":"Изменено:",
  "fixed":"Исправлено:",
  "removed":"Удалено:",
}
os.chdir(os.path.dirname(__file__))
ms.dir.create("change_log")
for i in os.listdir("change_log"):
  file=f"change_log/{i}"
  if os.path.isfile(file):
    if file.lower().endswith(".json"):
      filename=i[:-5]
      if filename.lower()=="readme":
        continue
      json=ms.json.read(file)
      lines=[f"# {package}"]
      if "version" in json:
        lines.append("Версия {}".format(json["version"]))
      for k,v in md_lang.items():
        if k in json:
          lines.append("# "+v)
          for i in json[k]:
            lines.append("- "+i)
      ms.file.write(f"change_log/{filename}.md","\n".join(lines))
for i in os.listdir("src"):
  if os.path.isfile(f"src/{i}/__init__.py"):
    Popen(["nano", f"src/{i}/__init__.py"]).wait()
    if which("autopep8"):
      Popen(["autopep8", "-r", "--in-place", f"src/{i}"]).wait()
Popen(["nano", "pyproject.toml"]).wait()
Popen(["poetry", "publish", "--build"]).wait()
Popen([sys.executable, "-m", "pip", "install", "-U", package]).wait()
sleep(10)
Popen([sys.executable, "-m", "pip", "install", "-U", package]).wait()
