import MainShortcuts.addon as _a
import os
import shutil
sep = os.sep  # Разделитель в пути файла
extsep = os.extsep  # Разделитель в расширении файла
pathsep = sep
separator = sep
pwd = os.getcwd
cd = os.chdir
exists = os.path.exists


def merge(array: list, sep: str = pathsep):
  """Собрать путь к объекту из массива"""
  return sep.join(array)


def split(path: str):
  """Разложить путь к объекту на массив"""
  return path.replace("\\", "/").split("/")


def info(path: str = ".", listdir: bool = False, listlinks: bool = False) -> dict:
  """Информация о файле/папке
  path - путь к объекту
  listdir - если папка, то рекурсивно создать список содержимого и суммарный размер
  listlinks - проверять ссылки при рекурсии?"""
  path = path.replace("\\", "/")
  i = {
      "dir": None,  # Папка, в которой находится объект
      "dirs": None,  # Рекурсивный список папок (если аргумент listdir=True)
      "exists": None,  # Существует ли объект? | True/False
      "ext": None,  # Расширение файла, даже если это папка
      "files": None,  # Рекурсивный список файлов (если аргумент listdir=True)
      "fullname": None,  # Полное название объекта (включая расширение)
      "fullpath": None,  # Полный путь к объекту
      "link": None,  # Это ссылка или оригинал? | True/False
      "name": None,  # Название файла без расширения, даже если это папка
      "path": None,  # Полученный путь к объекту
      "realpath": None,  # Путь к оригиналу, если указана ссылка
      "relpath": None,  # Относительный путь
      "size": None,  # Размер. Для получения размера папки укажите аргумент listdir=True
      "split": [],  # Путь, разделённый на массив
      "type": None,  # Тип объекта | "file"/"dir"
      "errors": {},  # Параметры, при получении которых возникла ошибка
      "created": None,  # Timestamp создания файла
      "modified": None,  # Timestamp последнего изменения файла
      "used": None,  # Timestamp последнего использования файла
  }
  errors = {}
  i["path"] = path
  i["split"] = path.split("/")
  i["dir"], i["fullname"] = os.path.split(path)
  try:
    i["fullpath"] = os.path.abspath(path)
  except Exception as e:
    errors["fullpath"] = e
  try:
    i["relpath"] = os.path.relpath(path)
  except Exception as e:
    errors["relpath"] = e
  if "." in i["fullname"]:
    i["ext"] = i["fullname"].split(".")[-1]
    i["name"] = ".".join(i["fullname"].split(".")[:-1])
  else:
    i["ext"] = None
    i["name"] = i["fullname"]
  try:
    i["exists"] = exists(path)
  except Exception as e:
    errors["exists"] = e
  if i["exists"]:
    i["created"] = os.path.getctime(path)
    i["modified"] = os.path.getmtime(path)
    i["used"] = os.path.getatime(path)
    i["link"] = os.path.islink(path)
    if i["link"]:
      try:
        i["realpath"] = os.path.realpath(path)
      except Exception as e:
        errors["realpath"] = e
    if os.path.isfile(path):
      i["size"] = os.path.getsize(path)
      i["type"] = "file"
    elif os.path.isdir(path):
      i["type"] = "dir"
      if listdir:
        tmp = _a.listdir(path, listlinks)
        i["dirs"] = tmp["d"]
        i["files"] = tmp["f"]
        i["size"] = tmp["s"]
    else:
      i["type"] = "unknown"
  i["errors"] = errors
  return i


class recurse_info:
  """Рекурсивная информация о папке
  В разработке"""

  def __init__(self, p: str = os.getcwd(), links: bool = False):
    self.path = p
    for k, v in info(p, listdir=True, listlinks=links).items():
      self[k] = v
    if self.type == "dir":
      f = {}
      d = {}
      for i in self.files:
        f[i] = info(i)
      for i in self.dirs:
        d[i] = info(i)
      self.files = f
      self.dirs = d

  def __repr__(self):
    return f"ms.recurse_info('{self.path}')"

  def __bool__(self):
    return self.exists

  def __getitem__(self, k):
    return getattr(self, k)

  def __setitem__(self, k, v):
    setattr(self, k, v)

  def __delitem__(self, k):
    delattr(self, k)

  def __eq__(self, other):
    try:
      myD = {}
      otD = {}
      for k in dir(self):
        if not k.startswith("_"):
          myD[k] = self[k]
      for k in dir(other):
        if not k.startswith("_"):
          otD[k] = other[k]
      return myD == otD
    except:
      return False


def delete(path: str):
  """Удалить папку или файл, если существует"""
  if os.path.exists(path):
    if os.path.islink(path):
      os.unlink(path)
    elif os.path.isfile(path):
      os.remove(path)
    elif os.path.isdir(path):
      shutil.rmtree(path)
    else:
      raise Exception("Unknown type")


rm = delete
# del=delete


def copy(fr: str, to: str):
  """Копировать"""
  if os.path.isfile(fr):
    shutil.copy(fr, to)
  elif os.path.isdir(fr):
    shutil.copytree(fr, to)
  else:
    raise Exception("Unknown type")


cp = copy


def move(fr: str, to: str):
  """Переместить"""
  shutil.move(fr, to)


mv = move


def rename(fr: str, to: str):
  """Переименовать"""
  os.rename(fr, to)


rn = rename


def link(fr: str, to: str, force: bool = False):
  """Сделать символическую ссылку"""
  if exists(to) and force:
    delete(to)
  os.symlink(fr, to)


ln = link


def format(path: str, replace_to: str = None, sep=pathsep) -> str:
  """Форматировать путь к файлу (изменить разделитель, удалить недопустимые символы)
  replace_to - заменить недопустимые символы на указанный"""
  for i in ["/", "\\"]:
    path = path.replace(i, sep)
  if replace_to != None:
    for i in ["\n", ":", "*", "?", "\"", "<", ">", "|", "+", "%", "!", "@"]:
      path = path.replace(i, replace_to)
  return path
# 1.7.4


def in_dir(path: str, dir: str, recursion_limit: int = 1000) -> bool:
  dir = os.path.abspath(dir).replace("\\", "/")
  path = os.path.abspath(path).replace("\\", "/")
  while True:
    pdir = os.path.dirname(path)
    if path == pdir:
      return False
    if dir == pdir:
      return True
    path = pdir
    recursion_limit -= 1
    if recursion_limit < 0:
      raise RecursionError()
