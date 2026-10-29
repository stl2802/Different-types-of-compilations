#define PY_SSIZE_T_CLEAN
#include <Python.h>

// быстрая функция
static PyObject* sum_of_squares_c(PyObject* self, PyObject* args) {
    PyObject* numbers_list;
    
    // 1. парсим аргументы: ожидаем один список
    if (!PyArg_ParseTuple(args, "O", &numbers_list)) {
        return NULL;  // NULL = исключение в Python
    }
    
    // 2. проверяем, что это действительно список
    if (!PyList_Check(numbers_list)) {
        PyErr_SetString(PyExc_TypeError, "Expected a list");
        return NULL;
    }
    
    // 3. проходим по списку и считаем
    Py_ssize_t n = PyList_Size(numbers_list);
    double total = 0.0;
    
    for (Py_ssize_t i = 0; i < n; i++) {
        PyObject* item = PyList_GetItem(numbers_list, i);  // borrowed ref
        double value = PyFloat_AsDouble(item);
        
        if (PyErr_Occurred()) {
            return NULL;  // если элемент не float
        }
        
        total += value * value;
    }
    
    // 4. создаём Python-float для результата
    return PyFloat_FromDouble(total);
}

// описание методов модуля
static PyMethodDef FastMathMethods[] = {
    {"sum_of_squares", sum_of_squares_c, METH_VARARGS, 
     "Compute sum of squares of a list of floats"},
    {NULL, NULL, 0, NULL}  // sentinel
};

// описание самого модуля
static struct PyModuleDef fastmathmodule = {
    PyModuleDef_HEAD_INIT,
    "fastmath",        // имя модуля
    NULL,              // docstring
    -1,
    FastMathMethods
};

// точка входа - функция инициализации модуля
PyMODINIT_FUNC PyInit_fastmath(void) {
    return PyModule_Create(&fastmathmodule);
}