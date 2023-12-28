# MainShortcuts by MainPlay YT
# https://t.me/MainPlay_YT
import MainShortcuts.addon as _a
import json as _j
import os as _o
import platform as _p
import sys as _s
from glob import glob as _g
# Универсальные команды
class mproc:
  args=_s.argv # Аргументы запуска программы
class mpath: # Операции с путями к файлам/папкам
  sep=_o.sep # Разделитель в пути файла
  def exists(a): # Объект существует?
    return _o.path.exists(a)
  def merge(a): # Собрать путь к объекту из массива
    return mpath.sep.join(a)
  def split(a): # Разложить путь к объекту на массив
    return a.split(mpath.sep)
  def info(a,listdir=False):
    info={"dir":None,"size":None,"exists":None,"ext":None,"fullname":None,"fullpath":None,"link":None,"name":None,"path":None,"realpath":None,"split":[],"type":None,}
    info["path"]=a
    info["split"]=mpath.split(a)
    info["dir"]=mpath.merge(info["split"][:-1])
    info["fullname"]=info["split"][-1]
    if "." in info["fullname"]:
      info["ext"]=info["fullname"].split(".")[-1]
      info["name"]=".".join(info["fullname"].split(".")[:-1])
    else:
      info["ext"]=None
      info["name"]=info["fullname"]
    info["exists"]=mpath.exists(a)
    if info["exists"]:
      info["fullpath"]=_o.path.abspath(a)
      info["link"]=_o.path.islink(a)
      if info["link"]:
        info["realpath"]=_o.path.realpath(a)
      if _o.path.isfile(a):
        info["size"]=_o.path.getsize(a)
        info["type"]="file"
      elif _o.path.isdir(a):
        info["type"]="dir"
        if listdir:
          tmp=_a.listdir(a)
          info["dirs"]=tmp["d"]
          info["files"]=tmp["f"]
          info["size"]=tmp["s"]
      else:
        info["type"]="unknown"
    return info
class mos: # Операции с системой
  platform=_p.system() # Тип ОС
def exit(code=0): # Закрытие программы с кодом
  _s.exit(code)
class mvar: # Операции с переменныии
  def procSet(name="MainShortcutsTMP",value=None):
    _o.environ[name]=value
    return True
  def procGet(name="MainShortcutsTMP"):
    return _o.environ[name]
  proc=_o.environ
class mfile: # Операции с файлами
  def read(p,encoding="utf-8"): # Прочитать текстовый файл
    if mpath.info(p)["type"]=="file":
      with open(p,"r",encoding=encoding) as f:
        t=f.read()
    else:
      t=""
    return t
  def write(p,text="",encoding="utf-8",force=False): # Записать текстовый файл
    if mpath.info(p)["type"]=="dir" and force:
      _o.remove(p)
    with open(p,"w",encoding=encoding) as f:
      f.write(f"{text}")
    return True
  def open(p): # Открыть содержимое файла
    if _o.path.exists(p):
      with open(p,"rb") as f:
        b=f.read()
    else:
      b=None
    return b
  def save(p,bin=None,force=False): # Сохранить содержимое файла
    if mpath.info(p)["type"]=="dir" and force:
      _o.remove(p)
    with open(p,"wb") as f:
      f.write(bin)
    return True
class mdir: # Операции с папками
  def create(p): # Создать папку
    if not mpath.exists(p):
      _o.makedirs(p)
    return True
class mstr: # Операции с текстом
  def array2str(a):
    r=[]
    for i in a:
      r.append(str(i))
    return r
  def dict2str(d):
    r={}
    for i in d:
      r[i]=str(d[i])
    return r
  class replace:
    def multi(text=None,dict=None): # Мульти-замена {"что заменить":"чем заменить"}
      t=str(text)
      for i in dict:
        t=t.replace(i,str(dict[i]))
      return t
    def all(text=None,fr=None,to=None): # Замена пока заменяемый текст не исчезнет. МОЖЕТ ВЫЗВАТЬ ВЕЧНЫЙ ЦИКЛ
      t=str(text)
      a=str(fr)
      b=str(to)
      if a in b:
        raise endlessCycle("\""+a+"\" is contained in \""+b+"\", this causes an infinite loop")
      while a in t:
        t=t.replace(a,b)
      return t
class mjson: # Операции с JSON
  def encode(data=None,mode="c",indent=2,sort=True): # Данные в текст
    if mode in ["c","compress","min","zip"]: # Сжатый
      t=_j.dumps(data,separators=[",",":"],sort_keys=sort)
    elif mode in ["pretty","p","print","max"]: # Развёрнутый
      t=_j.dumps(data,indent=int(indent),sort_keys=sort)
    else: # Без параметров
      t=_j.dumps(data,sort_keys=sort)
    return t
  def decode(text): # Текст в данные
    return _j.loads(str(text))
  def write(p=None,data=None,encoding="utf-8",mode="c",indent=2,sort=True,force=False): # Данные в файл
    if mpath.info(p)["type"]=="dir" and force:
      _o.remove(p)
    with open(p,"w",encoding=encoding) as f:
      f.write(mjson.encode(data,mode=mode,indent=indent,sort=sort))
    return True
  def read(p,encoding="utf-8"): # Данные из файла
    with open(p,"r",encoding=encoding) as f:
      return _j.load(f)
# Команды для разных ОС
if mos.platform=="Windows": # Windows
  def clear():
    _o.system("cls")
elif mos.platform=="Linux": # Linux
  def clear():
    _o.system("clear")
elif mos.platform=="Darwin": # MacOS
  pass
else: # Неизвестный тип
  print("MainShortcuts WARN: Unknown OS \""+mos.platform+"\"")
