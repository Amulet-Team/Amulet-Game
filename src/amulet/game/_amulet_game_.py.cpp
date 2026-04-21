#include <pybind11/pybind11.h>

namespace py = pybind11;

void init_java(py::module);

void init_amulet_game(py::module m){
    init_java(m);
}
