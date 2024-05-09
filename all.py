import os
from time import sleep
from subprocess import Popen
package = "MainShortcuts"
for i in os.listdir("src"):
  if os.path.exists(f"src/{i}/__init__.py"):
    Popen(["nano", f"src/{i}/__init__.py"]).wait()
Popen(["nano", "pyproject.toml"]).wait()
Popen(["py", "src/dev/make-import.py"]).wait()
Popen(["autopep8","-r","src"]).wait()
Popen(["poetry", "publish", "--build"]).wait()
Popen(["pip", "install", "-U", package]).wait()
sleep(10)
Popen(["pip", "install", "-U", package]).wait()
