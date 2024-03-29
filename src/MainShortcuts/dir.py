import MainShortcuts.path as m_path
import os as _os
import shutil as _shutil
def create(path,force=False):
  """Создать папку
  Если путь существует, ничего не делает
  force - принудительно создать папку (удалит файл, который находится на её месте)"""
  if m_path.exists(path):
    type=m_path.info(path)["type"]
    if type=="dir":
      return True
    elif force:
      m_path.delete(path)
    else:
      raise Exception("The object exists and is not a folder")
  _os.makedirs(path)
  return True
mk=create
def delete(path):
  """Удалить папку с содержимым
  Если в назначении файл, выдаст ошибку"""
  type=m_path.info(path)["type"]
  if type=="dir":
    _shutil.rmtree(path)
  else:
    raise Exception("Unknown type: "+type)
rm=delete
def copy(fr,to,force=False):
  """Копировать папку с содержимым
  force - принудительно копировать"""
  type=m_path.info(fr)["dir"]
  if type=="dir":
    if m_path.info(to)["type"]!="dir" and force:
      try:
        m_path.delete(to)
      except:
        pass
    _shutil.copytree(fr,to)
  else:
    raise Exception("Unknown type: "+type)
cp=copy
def move(fr,to,force=False):
  """Переместить папку с содержимым
  force - принудительно переместить"""
  type=m_path.info(fr)["dir"]
  if type=="dir":
    if m_path.info(to)["type"]!="dir" and force:
      try:
        m_path.delete(to)
      except:
        pass
    _shutil.move(fr,to)
  else:
    raise Exception("Unknown type: "+type)
def rename(fr,to,force=False):
  """Переименовать папку
  force - принудительно переименовать"""
  t=m_path.info(fr)["dir"]
  if t=="dir":
    if m_path.info(to)["type"]!="dir" and force:
      try:
        m_path.delete(to)
      except:
        pass
    _os.rename(fr,to)
  else:
    raise Exception("Unknown type: "+t)
def list(path,files=True,dirs=True,links=None):
  """Получить список содержимого папки
  files - True: включать файлы в список
          False: не показывать файлы в списке
  dirs  - True: включать папки в список
          False: не показывать папки в списке
  links - None: показывать всё
          True: показывать только ссылки
          False: не показывать ссылки"""
  a=_os.listdir(path)
  b=[]
  for i in a:
    info=m_path.info(i)
    if links==None:
      c=True
    elif links==True:
      c=info["link"]
    elif links==False:
      c=not info["link"]
    else:
      raise Exception('"links" can only be True, False or None')
    if c:
      if files and info["type"]=="file":
        b.append(i)
      elif dirs and info["type"]=="dir":
        b.append(i)
  return b
