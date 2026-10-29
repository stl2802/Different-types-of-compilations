from setuptools import setup, Extension

# описываем наш модуль на языке С.
# Extension - это инструкция для сборщика. Какой файл скомпилировать и как назвать результат.
module = Extension(
    'fastmath',             # Имя модуля для импорта (import fastmath)
    sources=['fastmath.c']  # Путь к исходному коду на С
)

# Запускаем процесс сборки
setup(
    name='fastmath',        # Название пакета
    version='1.0',          # Версия
    ext_modules=[module]    # Передаем наше С-расширение в систему сборки
)