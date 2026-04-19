
# Read project name from pyproject.toml at load time
# Hyphens are normalised to underscores to match SKBUILD_PROJECT_NAME behaviour
package := `python -c "import tomllib; d=tomllib.load(open('pyproject.toml','rb')); print(d['project']['name'].replace('-','_'))"`

default:
    @just --list

# Run uv sync
sync:
    uv sync

dev:
    uv pip install -e . --no-build-isolation

install:
    uv pip install . --no-build-isolation

# Compile C++, create Python wheel and run nanobind stubgen
build:
    uv build --no-build-isolation

build-debug:
    uv pip install . --no-build-isolation \
        --config-settings "cmake.build-type=Debug"

build-verbose:
    uv pip install . --no-build-isolation -v \
        --config-settings "build.verbose=true" \
        --config-settings "logging.level=DEBUG"

build-define define:
    uv pip install . --no-build-isolation \
        --config-settings "cmake.define.{{define}}"

test: install
    uv run pytest

test-fast:
    uv run pytest

# Manually create stub files. 
stubs: install
    uv run python -m nanobind.stubgen \
        -m {{package}}._core \
        -M src/{{package}}/py.typed \
        -O src/{{package}}

# Verify stubs match the installed extension (type-check against them)
check-stubs: stubs
    uv run mypy src/{{package}} --ignore-missing-imports

clean:
    rm -rf dist/ build/ _skbuild/ *.egg-info
    find . -name "*.so" -delete
    find . -name "*.pyd" -delete

clean-all: clean
    rm -rf .venv

fmt:
    uv run ruff format .

lint:
    uv run ruff check .

typecheck:
    uv run mypy .

publish: wheel
    uv publish

wheel:
    uv build --wheel --no-build-isolation
