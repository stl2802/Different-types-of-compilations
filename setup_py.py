from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension

ext_modules = [
    Pybind11Extension(
        "fastmath_pybind",
        ["fastmath_pybind.cpp"],
        cxx_std=11,
    ),
]

setup(
    name="fastmath_pybind",
    version="1.0",
    ext_modules=ext_modules,
)