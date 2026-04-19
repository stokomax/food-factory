# food_factory - nanobind Sandbox & Tutorial Project

> The next step after completing the official nanobind tutorial. This is a complete, working sandbox for experimenting with modern Python/C++ extension development.

This project demonstrates real-world nanobind usage with industry standard tooling:
- ✅ **nanobind** - Modern C++ ↔ Python binding framework
- ✅ **uv** - Blazing fast Python package manager
- ✅ **scikit-build-core** - Next generation Python build backend
- ✅ **just** - Modern command runner (replaces make)

Built following patterns from:
- [nanobind official documentation](https://nanobind.readthedocs.io/)
- [Nanobind: The Bridge Between C++ and Python](https://dev.to/sommukhopadhyay/nanobind-the-bridge-between-c-and-python-fna)
- [nanobind_uv_template](https://github.com/XingxinHE/nanobind_uv_template)

Use this as a:
- 🧪 Sandbox for experimenting with nanobind features
- 📚 Reference for proper modern extension architecture
- 🚀 Template for your own C++ Python projects
- ✅ Working example of complete end-to-end setup

## Development Environment Setup

### Platform Support
- ✅ **Linux** (native)
- ✅ **WSL2** (Windows Subsystem for Linux)
- ❌ Native Windows is not supported

### Step 1: Install System Dependencies
```bash
# Ubuntu/Debian/WSL2
sudo apt update && sudo apt install -y \
    build-essential \
    cmake \
    curl
```

### Step 2: Install uv (Python package manager)
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Step 3: Install just (command runner)
```bash
curl --proto '=https' --tlsv1.2 -sSf https://just.systems/install.sh | bash -s -- --to ~/.local/bin
```

### Step 4: Setup Project
```bash
# Clone and enter project
git clone <repository-url>
cd food_factory

# Initialize environment and install dependencies
uv sync
```

### Toolchain used:
- **uv** - Modern Python package manager and virtual environment
- **scikit-build-core** - Next generation Python build backend (no setuptools)
- **nanobind** - C++ ↔ Python binding framework
- **just** - Command runner (replaces make)
- **CMake** - C++ build system

## Installation

### Standard Installation

```bash
just build
```

### Developer Installation
```bash
just dev
```

This will install the package in editable development mode with proper build isolation settings.


## Usage

```bash
uv run python
```

```python
import food_factory

factory = food_factory.Factory.getInstance()
biscuit = factory.makeFood("bi")
chocolate = factory.makeFood("ch")
```

## Starting your own nanobind project from scratch

To create a new nanobind project with this stack:

```bash
# Initialize library project with scikit-build-core backend
uv init --lib --build-backend=scikit myproject
cd myproject
```

Then edit `pyproject.toml`:
- Replace any pybind11 references with nanobind
- Add nanobind to build-system requires
- Configure scikit-build-core

Copy the justfile and CMakeLists.txt from this project to your project. Modify any hard references to "food_factory" to match your project layout and naming conventions. 

This project can be used as a working reference template for all configuration files.


## Development Commands

### Justfile
This project uses `just` as command runner. Available commands:

```bash
just                          # List all commands
just build                    # Build C++ extension
just build-no-factory         # Build without Factory pattern
just clean                    # Remove build artifacts
just wheel                    # Build distributable wheel
just test                     # Run all tests
just test-cpp                 # Run C++ tests only
just test-py                  # Run Python tests only
just dev                      # Install editable development mode
just stubs                    # Generate type stubs
just check-stubs              # Verify stubs with mypy
just lint                     # Run linter
just format                   # Format code
```

## Nanobind Type Stubs

Nanobind automatically generates complete type annotation files (`.pyi` stubs) that provide perfect IDE autocompletion and static type checking.

### How it works:
1. ✅ Stubs are automatically generated at build time
2. ✅ Generated directly from your C++ binding definitions
3. ✅ No manual stub maintenance required
4. ✅ Supports all nanobind features: inheritance, methods, properties, enums
5. ✅ `py.typed` marker file is automatically created

### Commands:
```bash
just stubs        # Generate stubs manually
just check-stubs  # Verify stubs with mypy type checking
```

Official documentation: [📖 Nanobind Stub Generation](https://nanobind.readthedocs.io/en/latest/stubgen.html)

## The `_core` Pattern

This project follows the standard nanobind / pybind11 convention of naming the native extension module `_core`.

### About this pattern:
- ✅ **History**: Originated in pybind11 projects and adopted as the universal standard for C++ extension modules.

### How it works:
1.  **Native code lives in `_core.*.so` - the actual compiled C++ extension
2.  **Pure Python wrapper** in `__init__.py` imports and re-exports symbols
3.  Clean separation between native bindings and pure Python code
4. Allows adding Python wrapper functions without modifying C++ bindings

### In this project:
- **CMake**: `nanobind_add_module(_core ...)` creates the native module
- **Python**: `src/food_factory/__init__.py` imports and re-exports all classes
- Users import `food_factory` (Python package) → imports `_core` (native implementation)

### Best practice: Always import from `food_factory`, never import directly from `food_factory._core`

This pattern lets you extend your module with pure Python code while keeping all native bindings isolated.

## CMake Build System

This project follows nanobind best practices for CMake configuration.

### Nanobind CMake Commands

| Command | Purpose | Official Documentation |
|---------|---------|------------------------|
| `nanobind_add_module()` | Creates Python extension module target. Handles all compiler flags, include paths, and linking configuration. | [📖 nanobind_add_module](https://nanobind.readthedocs.io/en/latest/building.html#nanobind-add-module) |
| `nanobind_add_stub()` | Automatic `.pyi` stub generation at build time. Generates complete type annotations for your extension. | [📖 nanobind_add_stub](https://nanobind.readthedocs.io/en/latest/stubgen.html#cmake-integration) |

### Nanobind Build Options

| Flag | Purpose |
|------|---------|
| `STABLE_ABI` | Uses Python 3.12+ Stable ABI. Builds one wheel that works across all future Python versions. |
| `NB_STATIC` | Statically links libnanobind into your extension. Creates a single self-contained `.so` file with zero external dependencies. Recommended for most projects. |
| `NB_SHARED` | Use shared nanobind library. Only needed when building multiple extension modules that will be loaded into the same process. |

### Defines & Environment Variables

| Variable | Description |
|----------|-------------|
| `FOOD_FACTORY_BUILD_FACTORY` | Compile time feature flag. Set this CMake option to conditionally include/exclude the Factory pattern implementation. This becomes `FOOD_FACTORY_HAS_FACTORY` C++ preprocessor define. |
| `SKBUILD` | Automatically set by scikit-build-core. Used to detect when CMake is running inside the Python build process vs standalone. |
| `SKBUILD_PROJECT_NAME` | Project name from `pyproject.toml`. Used everywhere to avoid hardcoding package name. |
| `Python_EXECUTABLE` | Path to the current virtual environment Python interpreter. Used to locate nanobind CMake configuration. |

### CMake Variables scikit-build-core Sets Automatically

| Option | Default | Description |
|--------|---------|-------------|
| `FOOD_FACTORY_BUILD_FACTORY` | `ON` | Build Factory pattern + Biscuit/Chocolate implementations |


### CMake Variables scikit-build-core Sets Automatically

| Variable                       | Value                                                 |
| ------------------------------ | ----------------------------------------------------- |
| `SKBUILD`                      | `"2"` (use to detect scikit-build-core in CMakeLists) |
| `SKBUILD_CORE_VERSION`         | Version of scikit-build-core                          |
| `SKBUILD_PROJECT_NAME`         | Package name from `pyproject.toml`                    |
| `SKBUILD_PROJECT_VERSION`      | CMake-compatible version string                       |
| `SKBUILD_PROJECT_VERSION_FULL` | Full version including dev/local suffix               |
| `SKBUILD_STATE`                | `sdist`, `wheel`, `editable`, etc.                    |
| `SKBUILD_PLATLIB_DIR`          | Install destination → `site-packages`                 |
| `SKBUILD_DATA_DIR`             | Install destination → env root                        |
| `SKBUILD_SCRIPTS_DIR`          | Install destination → env `bin/`                      |
| `CMAKE_BUILD_TYPE`             | Defaults to `Release`                                 |
| `CMAKE_INSTALL_PREFIX`         | Wheel staging area                                    |
| `Python_EXECUTABLE`            | Points to the venv Python                             |
