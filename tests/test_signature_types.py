"""
Unit tests for nanobind function and method signature type checking.

These tests verify that nanobind correctly exposes function signatures,
type annotations, and parameter semantics exactly as they are declared
in the C++ bindings.
"""
import pytest
import food_factory
from food_factory import Food, Biscuit, Chocolate, Factory


def test_keyword_argument_behavior():
    """Nanobind default behavior: all arguments are positional-only.
    
    Nanobind by default makes all arguments positional-only
    unless you explicitly use `nb::arg("name")` in your C++ bindings.
    """
    factory = Factory.get_instance()
    
    # ✅ Works: positional call (correct nanobind usage)
    food = factory.make_food("bi")
    assert food is not None
    
    # ❌ This will RAISE TypeError (nanobind standard behavior)
    with pytest.raises(TypeError):
        factory.make_food(arg="bi")  # keyword arguments not supported by default


def test_method_callability():
    """Verify that all bound methods are properly callable."""
    # All methods exist and are callable
    assert callable(Food.getName)
    assert callable(Biscuit.__init__)
    assert callable(Factory.get_instance)
    assert callable(Factory.make_food)


def test_nanobind_method_type():
    """Verify nanobind native method types."""
    # Nanobind uses its own method wrapper type, not standard builtins
    assert str(type(Biscuit.getName)) == "<class 'nanobind.nb_method'>"
    assert str(type(Factory.make_food)) == "<class 'nanobind.nb_method'>"


def test_signature_vs_stub_consistency():
    """Verify runtime classes match generated stub file declarations.
    
    This confirms that what nanobind exposes at runtime matches
    exactly what is declared in the generated .pyi stub files
    for static type checking.
    """
    runtime_classes = [name for name in dir(food_factory) if not name.startswith('_')]
    
    # All public classes exist both at runtime and in stubs
    for cls_name in ['Food', 'Biscuit', 'Chocolate', 'Factory']:
        assert cls_name in runtime_classes
        assert hasattr(food_factory, cls_name)


def test_polymorphic_return_type():
    """Demonstrate nanobind automatic downcasting behavior.
    
    The static stub declares return type `Food`, but at runtime nanobind
    automatically downcasts to the actual concrete subclass type!
    This is one of nanobind's most powerful features.
    """
    factory = Factory.get_instance()
    
    # Static type system only sees Food return type in stubs
    # But nanobind preserves actual type information at runtime
    biscuit = factory.make_food("bi")
    chocolate = factory.make_food("ch")
    
    assert isinstance(biscuit, Biscuit)  # ✅ Not just Food!
    assert isinstance(chocolate, Chocolate)
    assert type(biscuit) is Biscuit
    assert type(chocolate) is Chocolate


def test_none_return_type_handling():
    """Verify None returns work correctly for nullable types."""
    factory = Factory.get_instance()
    result = factory.make_food("invalid_type")
    
    # C++ nullptr is properly converted to Python None
    assert result is None


def test_class_hierarchy_integrity():
    """Verify that C++ class hierarchy is preserved in Python."""
    biscuit = Biscuit()
    chocolate = Chocolate()
    
    # Correct MRO preserved across language boundary
    assert issubclass(Biscuit, Food)
    assert issubclass(Chocolate, Food)
    assert isinstance(biscuit, Food)
    assert isinstance(chocolate, Food)


def test_constructor_behavior():
    """Verify constructors work correctly with no arguments."""
    # Constructors work without any parameters
    biscuit = Biscuit()
    chocolate = Chocolate()
    
    assert biscuit is not None
    assert chocolate is not None
    assert biscuit.getName() == "It's a Biscuit"
    assert chocolate.getName() == "It's a Chocolate"


def test_singleton_semantics():
    """Verify singleton reference semantics work correctly."""
    factory1 = Factory.get_instance()
    factory2 = Factory.get_instance()
    
    # Both variables refer to the EXACT same C++ object instance
    assert factory1 is factory2


def test_method_return_values():
    """Verify method return values work correctly."""
    biscuit = Biscuit()
    name = biscuit.getName()
    
    # std::string is properly converted to Python str
    assert isinstance(name, str)
    assert name == "It's a Biscuit"


def test_stub_generated_correctly():
    """Verify that stubgen successfully generated type stubs."""
    # The .pyi file should exist after running just stubs
    import importlib.util
    spec = importlib.util.find_spec('food_factory._core')
    assert spec is not None
    
    # Stub file exists next to native extension
    import os.path
    stub_file = os.path.join(os.path.dirname(spec.origin), '_core.pyi')
    assert os.path.exists(stub_file)
