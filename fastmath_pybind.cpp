#include <pybind11/pybind11.h>
#include <pybind11/stl.h>  // для автоматической конвертации std::vector
#include <vector>

double sum_of_squares(const std::vector<double>& numbers) {
    double total = 0.0;
    for (double n : numbers) {
        total += n * n;
    }
    return total;
}

namespace py = pybind11;

PYBIND11_MODULE(fastmath_pybind, m) {
    m.doc() = "Fast math module";
    m.def("sum_of_squares", &sum_of_squares, 
          "Compute sum of squares", 
          py::arg("numbers"));
}