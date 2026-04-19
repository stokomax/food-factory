"""
Test suite demonstrating nanobind features and usage patterns.

These tests verify the nanobind binding implementation and show
how C++ objects behave when accessed from Python.
"""
import pytest
import food_factory
from food_factory import Food, Biscuit, Chocolate, Factory


def test_nanobind_module_import():
    """Verify that the native extension module loads correctly."""
    # Importing the module means nanobind successfully initialized
    # all class bindings and registered them with Python interpreter
    assert food_factory is not None
    assert hasattr(food_factory, 'Factory')
    assert hasattr(food_factory, 'Food')
    assert hasattr(food_factory, 'Biscuit')
    assert hasattr(food_factory, 'Chocolate')


def test_class_hierarchy_preserved():
    """Nanobind preserves C++ inheritance relationships in Python."""
    biscuit = Biscuit()
    chocolate = Chocolate()
    
    # Verify isinstance works across the inheritance chain
    assert isinstance(biscuit, Biscuit)
    assert isinstance(biscuit, Food)
    assert isinstance(chocolate, Chocolate)
    assert isinstance(chocolate, Food)
    
    # Verify type identification works correctly
    assert type(biscuit) is Biscuit
    assert type(chocolate) is Chocolate


def test_cpp_method_calls():
    """Demonstrate calling native C++ methods from Python."""
    biscuit = Biscuit()
    chocolate = Chocolate()
    
    # These method calls go through nanobind into C++
    # std::string is automatically converted to Python str
    assert biscuit.getName() == "It's a Biscuit"
    assert chocolate.getName() == "It's a Chocolate"


def test_singleton_reference_policy():
    """Demonstrate nanobind reference return policy.
    
    The Factory::getInstance() method is bound with nb::rv_policy::reference
    which means nanobind returns a reference to the existing singleton
    instance instead of creating a copy.
    """
    factory1 = Factory.get_instance()
    factory2 = Factory.get_instance()
    
    # Both instances point to THE SAME C++ object
    # This verifies that reference policy works correctly
    assert factory1 is factory2
    
    # Identity check passes because nanobind caches instances
    assert id(factory1) == id(factory2)


def test_factory_ownership_transfer():
    """Demonstrate nanobind take_ownership policy.
    
    Factory::makeFood() is bound with nb::rv_policy::take_ownership
    which means nanobind takes ownership of the C++ object and will
    automatically delete it when the Python object is garbage collected.
    """
    factory = Factory.get_instance()
    
    # Factory creates object in C++, transfers full ownership to Python
    food1 = factory.make_food("bi")
    food2 = factory.make_food("ch")
    
    assert isinstance(food1, Food)
    assert isinstance(food2, Food)
    
    # Each call returns a new unique instance
    assert food1 is not food2


def test_polymorphic_behavior():
    """Demonstrate that nanobind preserves polymorphic behavior."""
    factory = Factory.get_instance()
    
    # Factory returns base Food pointer, but nanobind correctly
    # resolves to the actual subclass type in Python
    biscuit = factory.make_food("bi")
    chocolate = factory.make_food("ch")
    
    assert type(biscuit) is Biscuit
    assert type(chocolate) is Chocolate
    
    # Polymorphic method calls work exactly as in C++
    assert biscuit.getName() == "It's a Biscuit"
    assert chocolate.getName() == "It's a Chocolate"


def test_snake_case_conversion():
    """Demonstrate nanobind automatic snake_case method naming.
    
    In C++ we have:
      - Factory::getInstance()
      - Factory::makeFood()
    
    Nanobind automatically converts these to Pythonic:
      - Factory.get_instance()
      - Factory.make_food()
    """
    factory = Factory.get_instance()
    
    # Verify Python conventions were applied during binding
    assert hasattr(factory, 'make_food')
    assert not hasattr(factory, 'makeFood')
    assert hasattr(Factory, 'get_instance')
    assert not hasattr(Factory, 'getInstance')


def test_string_marshalling():
    """Demonstrate nanobind std::string ↔ Python str conversion."""
    biscuit = Biscuit()
    name = biscuit.getName()
    
    # Verify we get a proper Python string, not some wrapped type
    assert isinstance(name, str)
    assert name == "It's a Biscuit"
    assert len(name) == 14
    assert name.upper() == "IT'S A BISCUIT"


def test_invalid_factory_type():
    """Test error handling for unknown food types."""
    factory = Factory.get_instance()
    
    # C++ nullptr return will be converted to Python None
    result = factory.make_food("invalid_type")
    assert result is None
