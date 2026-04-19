cmake_minimum_required(VERSION 3.15...3.26)
project(${SKBUILD_PROJECT_NAME} LANGUAGES CXX)

# Optional compilation options
option(FOOD_FACTORY_BUILD_FACTORY "Build Factory pattern implementation" ON)
option(BUILD_CPP_TESTS "Build C++ unit tests" OFF)

if (NOT SKBUILD)
  message(WARNING "\
  This CMake file is meant to be executed using 'scikit-build'. Running
  it directly will almost certainly not produce the desired result. If
  you are a user trying to install this package, please use the command
  below, which will install all necessary build dependencies, compile
  the package in an isolated environment, and then install it.
  =====================================================================
   $ pip install .
  =====================================================================
  If you are a software developer, and this is your own package, then
  it is usually much more efficient to install the build dependencies
  in your environment once and use the following command that avoids
  a costly creation of a new virtual environment at every compilation:
  =====================================================================
   $ pip install nanobind scikit-build-core[pyproject]
   $ pip install --no-build-isolation -ve .
  =====================================================================
  You may optionally add -Ceditable.rebuild=true to auto-rebuild when
  the package is imported. Otherwise, you need to re-run the above
  after editing C++ files.")
endif()

# Per nanobind docs.
if (CMAKE_VERSION VERSION_LESS 3.18)
  set(DEV_MODULE Development)
else()
  set(DEV_MODULE Development.Module)
endif()

# Try to import all Python components potentially needed by nanobind
find_package(Python 3.12 COMPONENTS Interpreter ${DEV_MODULE} REQUIRED)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Per nanobind docs.
if (NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
  set(CMAKE_BUILD_TYPE Release CACHE STRING "Choose the type of build." FORCE)
  set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS "Debug" "Release" "MinSizeRel" "RelWithDebInfo")
endif()

# Detect the installed nanobind package and import it into 
execute_process(
  COMMAND "${Python_EXECUTABLE}" -m nanobind --cmake_dir
  OUTPUT_STRIP_TRAILING_WHITESPACE OUTPUT_VARIABLE nanobind_ROOT)
find_package(nanobind CONFIG REQUIRED)

# Source file lists (conditionally populated)
set(FOOD_FACTORY_SOURCES
    src/food_factory/cpp/food_factory_ext.cpp
)

if(FOOD_FACTORY_BUILD_FACTORY)
    list(APPEND FOOD_FACTORY_SOURCES
        src/food_factory/cpp/Factory.cpp
        src/food_factory/cpp/Biscuit.cpp
        src/food_factory/cpp/Chocolate.cpp
    )
endif()

# We are now ready to compile the actual extension module
nanobind_add_module(
  # Name of the extension
  _core

  # Target the stable ABI for Python 3.12+, which reduces
  # the number of binary wheels that must be built. This
  # does nothing on older Python versions
  STABLE_ABI

  # Build libnanobind statically and merge it into the
  # extension (which itself remains a shared library)
  #
  # If your project builds multiple extensions, you can
  # replace this flag by NB_SHARED to conserve space by
  # reusing a shared libnanobind across libraries
  NB_STATIC

  # Source code goes here
  ${FOOD_FACTORY_SOURCES}
)

# Pass compilation flag to code
if(FOOD_FACTORY_BUILD_FACTORY)
    target_compile_definitions(_core PRIVATE FOOD_FACTORY_HAS_FACTORY=1)
endif()

# py.typed stub marker target
nanobind_add_stub(
    ${SKBUILD_PROJECT_NAME}_core_stub
    MODULE      _core
    OUTPUT      _core.pyi
    MARKER_FILE py.typed
    PYTHON_PATH $<TARGET_FILE_DIR:_core>
    DEPENDS     _core
)

# Install directive for scikit-build-core
install(TARGETS _core LIBRARY DESTINATION ${SKBUILD_PROJECT_NAME})
install(FILES ${CMAKE_CURRENT_BINARY_DIR}/_core.pyi DESTINATION ${SKBUILD_PROJECT_NAME})
install(FILES ${CMAKE_CURRENT_BINARY_DIR}/py.typed DESTINATION ${SKBUILD_PROJECT_NAME})

# C++ Tests configuration
if(BUILD_CPP_TESTS)
    enable_testing()
    # Test target placeholder - will be implemented when tests are added
    add_custom_target(${SKBUILD_PROJECT_NAME}_tests
        COMMENT "C++ test target placeholder"
    )
endif()
