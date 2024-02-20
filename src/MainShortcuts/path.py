import MainShortcuts.addon as _a
import os as _os
import shutil as _shutil
sep=_os.sep # Разделитель в пути файла
extsep=_os.extsep # Разделитель в расширении файла
pathsep=sep
separator=sep
pwd=_os.getcwd
cd=_os.chdir
def exists(path): # Объект существует?
  return _os.path.exists(path)
def merge(array,sep=pathsep): # Собрать путь к объекту из массива
  return sep.join(array)
def split(path,sep=pathsep): # Разложить путь к объекту на массив
  return path.split(sep)
def info(path=_os.getcwd(),listdir=False,listlinks=False): # Информация о пути
  path=path.replace("\\","/")
  i={
    "dir":None, # Папка, в которой находится объект
    "dirs":None, # Рекурсивный список папок (если аргумент listdir=True)
    "exists":None, # Существует ли объект? | True/False
    "ext":None, # Расширение файла, даже если это папка
    "files":None, # Рекурсивный список файлов (если аргумент listdir=True)
    "fullname":None, # Полное название объекта (включая расширение)
    "fullpath":None, # Полный путь к объекту
    "link":None, # Это ссылка или оригинал? | True/False
    "name":None, # Название файла без расширения, даже если это папка
    "path":None, # Полученный путь к объекту
    "realpath":None, # Путь к оригиналу, если указана ссылка
    "relpath":None, # Относительный путь
    "size":None, # Размер. Для получения размера папки укажите аргумент listdir=True
    "split":[], # Путь, разделённый на массив
    "type":None, # Тип объекта | "file"/"dir"
    "errors":{}, # Параметры, при получении которых возникла ошибка
    }
  errors={}
  i["path"]=path
  i["split"]=path.split("/")
  i["dir"],i["fullname"]=_os.path.split(path)
  try:
    i["fullpath"]=_os.path.abspath(path)
  except Exception as e:
    errors["fullpath"]=e
  try:
    i["relpath"]=_os.path.relpath(path)
  except Exception as e:
    errors["relpath"]=e
  if "." in i["fullname"]:
    i["ext"]=i["fullname"].split(".")[-1]
    i["name"]=".".join(i["fullname"].split(".")[:-1])
  else:
    i["ext"]=None
    i["name"]=i["fullname"]
  try:
    i["exists"]=exists(path)
  except Exception as e:
    errors["exists"]=e
  if i["exists"]:
    i["link"]=_os.path.islink(path)
    if i["link"]:
      try:
        i["realpath"]=_os.path.realpath(path)
      except Exception as e:
        errors["realpath"]=e
    if _os.path.isfile(path):
      i["size"]=_os.path.getsize(path)
      i["type"]="file"
    elif _os.path.isdir(path):
      i["type"]="dir"
      if listdir:
        tmp=_a.listdir(path,listlinks)
        i["dirs"]=tmp["d"]
        i["files"]=tmp["f"]
        i["size"]=tmp["s"]
    else:
      i["type"]="unknown"
  i["errors"]=errors
  return i
class recurse_info:
  def __init__(self,p=_os.getcwd(),links=False):
    self.path=p
    for k,v in info(p,listdir=True,listlinks=links).items():
      self[k]=v
    if self.type=="dir":
      f={}
      d={}
      for i in self.files:
        f[i]=info(i)
      for i in self.dirs:
        d[i]=info(i)
      self.files=f
      self.dirs=d
  def __repr__(self):
    return f"ms.recurse_info('{self.path}')"
  def __bool__(self):
    return self.exists
  def __getitem__(self,k):
    return getattr(self,k)
  def __setitem__(self,k,v):
    setattr(self,k,v)
  def __delitem__(self,k):
    delattr(self,k)
  def __eq__(self,other):
    try:
      myD={}
      otD={}
      for k in dir(self):
        if not k.startswith("_"):
          myD[k]=self[k]
      for k in dir(other):
        if not k.startswith("_"):
          otD[k]=other[k]
      return myD==otD
    except:
      return False
def delete(path): # Удалить
  inf=info(path)
  if inf["exists"]:
    if _os.path.islink(path):
      _os.unlink(path)
    if inf["type"]=="file":
      _os.remove(path)
    elif inf["type"]=="dir":
      _shutil.rmtree(path)
    else:
      raise Exception("Unknown type: "+inf["type"])
rm=delete
# del=delete
def copy(fr,to): # Копировать
  type=info(fr)["type"]
  if type=="file":
    _shutil.copy(fr,to)
  elif type=="dir":
    _shutil.copytree(fr,to)
  else:
    raise Exception("Unknown type: "+type)
cp=copy
def move(fr,to): # Переместить
  _shutil.move(fr,to)
mv=move
def rename(fr,to): # Переименовать
  _os.rename(fr,to)
rn=rename
def link(fr,to,force=False): # Сделать символическую ссылку
  if exists(to) and force:
    delete(to)
  _os.symlink(fr,to)
ln=link
def format(path,replace_to="_",replace_errors=True,sep=pathsep): # Форматировать путь к файлу (изменить разделитель, удалить недопустимые символы)
  for i in ["/","\\"]:
    path=path.replace(i,sep)
  if replace_errors:
    for i in ["\n",":","*","?","\"","<",">","|","+","%","!","@"]:
      path=path.replace(i,replace_to)
  return path