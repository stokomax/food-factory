#include <nanobind/nanobind.h>
#include <nanobind/stl/string.h> // Required for std::string support
#include "Factory.h"

namespace nb = nanobind;

// Use NB_MODULE to define the extension
NB_MODULE(_core, m) {
    // 1. Wrap the Base Class
    // We use nb::class_<T> and provide the name it will have in Python
    nb::class_<Food>(m, "Food")
        .def("getName", &Food::getName);

    // 2. Wrap the Subclasses
    // Note: We specify the base class <Biscuit, Food> so Python knows the relationship
    nb::class_<Biscuit, Food>(m, "Biscuit")
        .def(nb::init<>());

    nb::class_<Chocolate, Food>(m, "Chocolate")
        .def(nb::init<>());

    // 3. Wrap the Singleton Factory
    nb::class_<Factory>(m, "Factory")
        .def_static("get_instance", &Factory::getInstance, // Renamed to snake_case for Python idiomatic style
                        nb::rv_policy::reference)

        .def("make_food", &Factory::makeFood, // Match your Python script's call
                 nb::rv_policy::take_ownership);
}
