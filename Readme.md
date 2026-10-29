# Fast Python Extensions: C-API vs pybind11 vs Numba

Исходный код к статье **«Когда Python медленный: пишем C-расширение с нуля и сравниваем с pybind11»**.

В проекте реализована одна и та же задача — сумма квадратов элементов массива — пятью способами:
на чистом Python, через Python C-API, через pybind11, через NumPy и через Numba (JIT).
Цель — на минимальном, воспроизводимом примере показать, откуда берётся ускорение в 30–60 раз
и когда вообще стоит лезть в компилируемый код.

[Ссылка на статью на Хабре](ССЫЛКА_НА_СТАТЬЮ будет как ее одобрят наврное, если мне не станет всеравно)

---


## Требования

- **Python 3.10+** (в коде используются `X | Y` в аннотациях)
- **Компилятор C/C++**:
  - **Windows:** [Visual Studio Build Tools](https://visualstudio.microsoft.com/ru/downloads/) с workload *«Разработка классических приложений на C++»* (MSVC).
  - **Linux:** `sudo apt install build-essential python3-dev`
  - **macOS:** `xcode-select --install`
- **pip** и актуальный `setuptools`

Проверка компилятора (Windows, запускать из **Developer Command Prompt for VS**):

```bat
cl
```

Если команда не найдена — расширением заниматься пока рано, сначала поставь Build Tools.

---

## Установка

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate

python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

---

## Сборка расширений

Без этого шага `import fastmath` и `import fastmath_pybind` не сработают —
бенчмарк корректно это обработает и просто пропустит соответствующие строки.

### Чистый C-API

```bash
python setup.py build_ext --inplace
```

### pybind11

```bash
python setup_py.py build_ext --inplace
```

> **Важно:** `.pyd` / `.so` привязаны к конкретной версии Python и архитектуре.
> Собранный под 3.11 модуль не заработает под 3.12 — пересобери.

---

## Запуск бенчмарка аля (к сожалению эта по русски не общается а вот артемида общается вдумайтесь) главного файла

```bash
python sum_of_squares.py
```


## Важные нюансы измерения

1. **Типы данных разные — и это намеренно.**
   C-API-версия делает `PyList_Check()` и принимает **только Python-список**.
   Поэтому для `Python` и `C-API` используется `numbers_list`,
   а для `NumPy` / `Numba` — `numbers_array`.
   Передача `np.ndarray` в C-API-функцию приведёт к
   `TypeError: Expected a list`.

2. **Конвертация вынесена за пределы замера.**
   `numbers_array.tolist()` выполняется один раз при старте скрипта
   и в среднее время выполнения не входит.

3. **JIT прогревается.**
   До замеров вызывается `sum_of_squares_numba(numbers_array[:100])`,
   иначе в результат попадёт время компиляции LLVM (секунды).

4. **Берётся среднее из 3 прогонов.**
   Один замер слишком зависит от шума системы. Для более серьёзных замеров
   используй `timeit` или `perf_counter` + 10–20 повторов.

5. **NumPy считает через `np.dot`.**
   Это BLAS-операция с SIMD-векторизацией, а не аналог Python-цикла.
   Она показывает потолок для этой задачи, но не является «прямой» заменой
   произвольного циклического алгоритма.

6. **pybind11 не медленнее C-API.**
   Разница в пределах шума: под капотом генерируется примерно тот же код,
   просто рутину по `refcount` и конвертации типов пишет за тебя библиотека.

---

## Типизация C-расширения

Скомпилированный модуль не несёт Python-аннотаций. Чтобы IDE и mypy понимали сигнатуру,
рядом лежит `fastmath.pyi`:

```python
def sum_of_squares(numbers: list[float]) -> float: ...
```

---

## Типичные проблемы

| Симптом | Причина / решение |
|---|---|
| `ModuleNotFoundError: fastmath` | Расширение не собрано. Выполни `python setup_c.py build_ext --inplace`. |
| `TypeError: Expected a list` | В C-API-функцию передали `np.ndarray`. Нужен `list`. |
| `error: Microsoft Visual C++ 14.0 or greater is required` | Не установлен MSVC Build Tools. См. раздел «Требования». |
| `cl.exe` not found | Скрипт запущен не из Developer Command Prompt for VS. |
| `undefined symbol: PyInit_...` | Имя модуля в `PYBIND11_MODULE` / `PyModuleDef` не совпадает с именем в `setup.py`. |
| Numba первый вызов занимает секунды | Это JIT-компиляция. Прогрей функцию или используй `@njit(cache=True)`. |
| `ImportError: numpy.core.multiarray failed to import` | Версии numpy и numba несовместимы. Обнови оба: `pip install -U numpy numba`. |

---

## Вывод

- Сначала **алгоритм**, потом **NumPy**, потом **Numba**, и только потом **C/C++**.
- `@njit` — две строчки кода и часто 30–50x ускорения.
- `pybind11` — выбор, когда уже есть C++-библиотека или сложная структура данных.
- Чистый `C-API` — инструмент для понимания устройства CPython, а не для ежедневной разработки.

---

## Ссылки

- [Python C-API](https://docs.python.org/3/c-api/)
- [Extending and Embedding the Python Interpreter](https://docs.python.org/3/extending/)
- [pybind11 documentation](https://pybind11.readthedocs.io/)
- [Numba documentation](https://numba.readthedocs.io/)
- [Numba Performance Tips](https://numba.readthedocs.io/en/stable/user/performance-tips.html)

---

## Автор

[Stl2802]

Если нашёл баг или хочешь предложить более честный бенчмарк - открывай issue или PR.
А если статья была полезной, обсудим в комментариях на Хабре.