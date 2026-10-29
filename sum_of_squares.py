from time import time as benchmark_time
from typing import Callable
from numba import njit
import numpy as np
import numpy.typing as npt

try:
    import fastmath
    HAS_FASTMATH: bool = True
except ImportError:
    HAS_FASTMATH = False
    print("Warning: fastmath not built. Run: python setup_c.py build_ext --inplace")

try:
    import fastmath_pybind
    HAS_PYBIND: bool = True
except ImportError:
    HAS_PYBIND = False
    print("Warning: fastmath_pybind not built. Run: python setup_pybind.py build_ext --inplace")

N: int = 10_000_000
NUM_ITERATIONS: int = 3
numbers_array: npt.NDArray[np.float64] = np.random.rand(N)
numbers_list: list[float] = numbers_array.tolist()

BenchmarkFunc = Callable[[npt.NDArray[np.float64] | list[float]], float]

def sum_of_squares_py(numbers: list[float]) -> float:
    """Чистый Python: сумма квадратов элементов списка."""
    total: float = 0.0
    for n in numbers:
        total += n * n
    return total


def sum_of_squares_numpy(numbers: npt.NDArray[np.float64]) -> float:
    """NumPy: сумма квадратов через dot product."""
    return float(np.dot(numbers, numbers))


@njit
def sum_of_squares_numba(numbers: npt.NDArray[np.float64]) -> float:
    """Numba JIT: сумма квадратов элементов массива."""
    total: float = 0.0
    for n in numbers:
        total += n * n
    return total


def run_benchmark(name: str, func: BenchmarkFunc, data: list[float] | npt.NDArray[np.float64]) -> float:
    """Запускает функцию несколько раз и возвращает среднее время."""
    times: list[float] = []
    for _ in range(NUM_ITERATIONS):
        start: float = benchmark_time()
        func(data)
        end: float = benchmark_time()
        times.append(end - start)
    return sum(times) / len(times)


# Прогрев JIT (чтобы не мерить время компиляции)
_: float = sum_of_squares_numba(numbers_array[:100])

if __name__ == '__main__':
    print(f"Testing with {N:,} numbers\n")
    print("-" * 60)
    
    benchmarks: dict[str, tuple[BenchmarkFunc, list[float] | npt.NDArray[np.float64]]] = {
        'Python': (sum_of_squares_py, numbers_list),
        'NumPy': (sum_of_squares_numpy, numbers_array),
        'Numba': (sum_of_squares_numba, numbers_array),
    }
    
    if HAS_FASTMATH:
        benchmarks['C-API'] = (fastmath.sum_of_squares, numbers_list)
        
    if HAS_PYBIND:
        benchmarks['Pybind11'] = (fastmath_pybind.sum_of_squares, numbers_list)
        
    results: dict[str, float] = {}
    for name, (func, data) in benchmarks.items():
        avg_time: float = run_benchmark(name, func, data)
        results[name] = avg_time
        print(f"{name:15s}: {avg_time:.4f} sec")
    
    print("-" * 60)

    python_time: float = results['Python']
    print("\nУскорение относительно чистого Python:")
    print("-" * 60)
    for name, time in results.items():
        if name != 'Python':
            speedup: float = python_time / time
            print(f"{name:15s}: {speedup:.1f}x")