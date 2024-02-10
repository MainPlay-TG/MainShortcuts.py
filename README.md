# MainShortcuts
## Описание
Сокращение и упрощение встроенных операций Python
## Установка
Для установки через PIP используйте
```bash
pip install -U mainshortcuts
```
## Использование
Для импорта рекомендуется сокращённое название
```python
import MainShortcuts as ms
```
Встроенная информация о модуле
```python
ms.__version__ -> str # Версия модуля
ms.__functions__ -> list # Функции, которые существуют в модуле
ms.__variables__ -> list # Переменные, которые существуют в модуле
ms.__depends__ -> dict # Обязательные и необязательные зависимости
```
### Выход с кодом ошибки
Закрывает процесс программы с указанным кодом ошибки
```python
# Любой ненулевой код означает ошибку
ms.exit() # Выход с кодом 0 (нет ошибки)
ms.exit(1) # Выход с кодом 1
```
### Очистка терминала
Очищает окно терминала от всего текста
```python
ms.clear() # Очистить окно терминала
mc.cls() # То же самое, но с названием из Windows CMD
```
**Поддерживается только на Windows и Linux**
### Загрузка/сохранение данных
Для удобной загрузки или сохранения данных можно использовать класс `cfg`
```python
cfg=ms.cfg("config.json",json_args={"mode":"p"})
cfg.load() # Загрузить данные
print(cfg.data) # Вывести данные
cfg.data={"example":"Пример данных"} # Изменить данные
cfg.save() # Сохранить данные
```
Тип сохранения определяется по расширению, но можно это изменить
```python
cfg=ms.cfg("data",type="pickle") # Использовать Pickle для файла данных
# Предупреждение: использование Pickle может быть не безопасным!
```
Чтобы посмотреть поддерживаемые типы сохранения, импортируйте часть модуля
```python
from MainShortcuts.cfg import types
print(", ".join(types))
```
Также можно изменить расположение файла, тип и аргументы во время любой загрузки или сохранения, это не повлияет на обычные настройки
```python
cfg.load("data.toml",toml_args={"encoding":"utf-8"})
cfg.save("data.pkl")
```