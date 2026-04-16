#include <pybind11/pybind11.h>

void init_test_java(py::module);

void init_test_amulet_game(py::module m){
    init_test_java(m);
}
