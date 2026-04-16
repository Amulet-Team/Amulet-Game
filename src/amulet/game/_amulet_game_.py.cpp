#include <pybind11/pybind11.h>

void init_java(py::module);

void init_amulet_game(py::module m){
    init_java(m);
}
