from time import time as bencmark_time
from numba import njit
import NumPy as np

data = np.random.rand(10_000_000)

def sum_of_squares_py(numbers):
    total = 0.0
    for n in numbers:
        total += n * n
    return total

result_times = {'python':sum_of_squares_py,'c-api':None,'Pybind11':None,'NumPy':None,'Numba':None}


if __name__ == '__main__':
    for name,func in enumerate(result_times):
        start = bencmark_time()
        func(data)
        end = bencmark_time()
        print(str(name) + ':' + str(end - start))