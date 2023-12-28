import os as _o
def listdir(a):
  s=0
  f=[]
  d=[]
  for i in _o.listdir(a):
    i=_o.path.join(a,i)
    if _o.path.isfile(i):
      f.append(i)
      if not _o.path.islink(i):
        s+=_o.path.getsize(i)
    if _o.path.isdir(i):
      d.append(i)
      m=listdir(i)
      if not _o.path.islink(i):
        s+=m["s"]
      f=f+m["f"]
      d=d+m["d"]
  return {"s":s,"f":f,"d":d}
