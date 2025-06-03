#include <pybind11/pybind11.h>

#include <amulet/pybind11_extensions/py_module.hpp>

namespace pyext = Amulet::pybind11_extensions;

namespace py = pybind11;

void init_java_block(py::module);

void init_java(py::module m_parent)
{
    auto m = pyext::def_subpackage(m_parent, "java");
    init_java_block(m);
}
