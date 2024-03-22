import pydoc

from propertycapsule import encapsulated_property


def help_output(value): return pydoc.render_doc(value)

def test_simple_case():
    class ReferenceClass:
        def __init__(self):
            self._data = None

        @property
        def data(self):
            """The `data` property."""
            return self._data

        @data.setter
        def data(self, val): self._data = val

        @data.deleter
        def data(self): del self._data

    ref = ReferenceClass()

    class ClassWithEncapsulatedPropertyFromClass:
        def __init__(self):
            self._data = None

        @encapsulated_property
        class data:
            """The `data` property."""
            def getter(self): return self._data
            def setter(self, val): self._data = val
            def deleter(self): del self._data

    encapsulated_from_class = ClassWithEncapsulatedPropertyFromClass()

    class ClassWithEncapsulatedPropertyFromFunction:
        def __init__(self):
            self._data = None

        @encapsulated_property
        def data():
            """The `data` property."""
            def getter(self): return self._data
            def setter(self, val): self._data = val
            def deleter(self): del self._data
            return getter, setter, deleter

    encapsulated_from_function = ClassWithEncapsulatedPropertyFromFunction()
    assert dir(ref) == dir(encapsulated_from_class)
    assert dir(ref.data.__doc__) == dir(encapsulated_from_class.data.__doc__)
    assert dir(ref) == dir(encapsulated_from_function)
    assert dir(ref.data.__doc__) == dir(encapsulated_from_function.data.__doc__)

    # Overwrite class names before comparison because these should be the only differences in the `help` output.
    ref.__class__.__name__ \
        = encapsulated_from_class.__class__.__name__ \
        = encapsulated_from_function.__class__.__name__ \
        = ""
    assert help_output(ref) == help_output(encapsulated_from_class)
    assert help_output(ref) == help_output(encapsulated_from_function)
