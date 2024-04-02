# Short Overview
In order to write Python 3 properties while better adhering to the idea of ["Don't repeat yourself" (DRY)](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself), with this package,
```python
class SomeClass:
    def __init__(self): self._data = "Some data"

    @property
    def data(self):
        """Docstring for the `data` property."""
        return self._data

    @data.setter
    def data(self, val): self._data = val

    @data.deleter
    def data(self): del self._data
```
can be replaced by
```python
from propertycapsule import encapsulated_property

class SomeClass:
    def __init__(self): self._data = "Some data"

    @encapsulated_property
    class data:
        """Docstring for the `data` property."""
        def getter(self): return self._data
        def setter(self, val): self._data = val
        def deleter(self): del self._data
```
or by
```python
from propertycapsule import encapsulated_property

class SomeClass:
    def __init__(self): self._data = "Some data"

    @encapsulated_property
    def data():
        """Docstring for the `data` property."""
        def getter(self): return self._data
        def setter(self, val): self._data = val
        def deleter(self): del self._data
        return getter, setter, deleter
```

# Introduction
To specify a class property in Python 3, one of the following [two methods](https://docs.python.org/3/library/functions.html#property) is often used:
1. applying the `@property` decorator, or
2. calling the built-in `property` class directly.

The first method is probably the most popular one; however, I find that it goes against the principle of ["Don't repeat yourself" (DRY)](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself). In the simple example below,
```python
class ClassA:
    def __init__(self): self._data = "Some data"

    @property
    def data(self):
        """Docstring for the `data` property."""
        return self._data

    @data.setter
    def data(self, val): self._data = val

    @data.deleter
    def data(self): del self._data
```
the name of the `data` property appears at least *five* times that are critical to obtaining the behaviour that would typically be expected (unless you have a fairly good understanding of this property-creation mechanism above; see the discussion in the Additional Comments section further down).

This repetition is indeed in accordance with the Python 3 documentation itself ([version 3.12.2](https://docs.python.org/3/library/functions.html#property)) for the built-in `property` class:
> Be sure to give the additional functions the same name as the original property (x in this case.)

I find that this is an example of code that should be more DRY. The alternative of calling `property` directly is perhaps DRY-er:
```python
class ClassB:
    def __init__(self): self._data = "Some data"

    def data_getter(self): return self._data

    def data_setter(self, val): self._data = val

    def data_deleter(self): del self._data

    data = property(data_getter,
                    data_setter,
                    data_deleter,
                    "Docstring for the `data` property.")
```
However, a consequence of this method is that `data_getter`, `data_setter`, and `data_deleter` would remain methods of `ClassB`. If this is undesirable (and I expect that it would typically be since such getter, setter, and deleter methods would not be directly accessible when using the `@property` decorator to create a property), then the following line could be appended inside the class definition:
```python
    del data_getter, data_setter, data_deleter
```
However, this makes the resulting definition for `ClassB` less DRY because `data_getter`, `data_setter`, and `data_deleter` each appear twice.

# The Value of This Package
In order to allow for DRY-er property specifications, the `encapsulated_property` function, intended to be used as a decorator, is included in this package. The `@encapsulated_property` decorator can be applied to either
1. a nested class to be converted into a property of the outer class, or
2. a class method.

Here is a simple example using a *nested class*:
```python
from propertycapsule import encapsulated_property

class ClassC:
    def __init__(self): self._data = "Some data"

    @encapsulated_property
    class data:
        """Docstring for the `data` property."""
        def getter(self): return self._data
        def setter(self, val): self._data = val
        def deleter(self): del self._data
```
Note that the `data` in `class data` is the name that will be used for the property that will be created; therefore, the nested class name does not follow the [CapWords convention](https://peps.python.org/pep-0008/#class-names), which is typically used for classes in Python. However, since this class would be converted to a property, I presume that it would be a reasonable exception when adhering to this convention. Nonetheless, if this is something that you really want to avoid, or if you would like to avoid converting a class to a property, you can also use `@encapsulated_property` on a function definition. Here is an example:
```python
from propertycapsule import encapsulated_property

class ClassD:
    def __init__(self): self._data = "Some data"

    @encapsulated_property
    def data():
        """Docstring for the `data` property."""
        def getter(self): return self._data
        def setter(self, val): self._data = val
        def deleter(self): del self._data
        return getter, setter, deleter
```

These approaches of using `@encapsulated_property` have an advantage in addition to being DRY-er: these formats for specifying properties have inherent structure, and it is thus more readily clear that the `getter`, `setter`, and `deleter` methods are grouped together and are methods of the `data` property.

# Additional Comments
When method 1. to create a property (i.e., using the `@property` decorator) is used and `setter` and `deleter` methods are specified, what happens if you *do not* use the property name in all five of those locations? You are indeed not *required* to use the function name `data` in all five locations, but not doing so might not result in behaviour that you want, save for perhaps some unusual scenarios. For example, let's assume that you want to create a `data` property with custom `setter` and `deleter` methods but that you do not want `def data` to appear two additional times (after its first appearance under `@property`):
```python
class ClassE:
    def __init__(self): self._data = "Some data"

    @property
    def data(self):
        """Docstring for the `data` property."""
        return self._data

    @data.setter
    def data_setter(self, val): self._data = val

    @data.deleter
    def data_deleter(self): del self._data
```
Then, when you run
```
>>> e = ClassE()
>>> print(e.data)
'Some data'
```
the behaviour seems to be as expected. However, if you try to (implicitly) use the `setter` method using assignment with the `=` symbol, an error is raised:
```
>>> e.data = "New data"
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: can't set attribute
```
This may not be what you would have originally hoped for. The `setter` method does exist and is accessible, but it is implicitly accessible through `e.data_setter`, not `e.data`:
```
>>> e.data_setter = "New data, second try"
>>> e.data
'New data, second try'
```
Similarly, the `deleter` method is used when calling `del e.data_deleter`, *not* `del e.data` (which would raise an `AttributeError` error).
