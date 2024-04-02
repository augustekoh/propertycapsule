import inspect


GETTER_NAME = "getter"
SETTER_NAME = "setter"
DELETER_NAME = "deleter"
DOC_NAME = "__doc__"

def _format_docstring_with_constant_names(func):
    func.__doc__ = func.__doc__.format(getter_name=GETTER_NAME, setter_name=SETTER_NAME, deleter_name=DELETER_NAME)
    return func

@_format_docstring_with_constant_names
def encapsulated_property(class_or_function):
    """
    A function intended to be used as a decorator on a class or a function
    to convert it into a property.

    Args:
        class_or_function (collections.abc.Callable): A class or a function
            to which the decorator is applied.

    Returns:
        A property.

    If `class_or_function` is a class, then the only user-defined attributes
    should be zero, one, two, or three methods, each named
    - "{getter_name}",
    - "{setter_name}", or
    - "{deleter_name}".
    Any docstring of this class will be used as the docstring of the
    property to be created.

    If `class_or_function` is a function, then it should return an iterable
    of three values: a getter, a setter, and a deleter (in that order). Any
    of these three values may be `None`. Any docstring of this function will
    be used as the docstring of the property to be created.
    """
    if inspect.isclass(class_or_function):
        return _encapsulated_property_from_class(class_or_function)
    elif inspect.isfunction(class_or_function):
        return _encapsulated_property_from_function(class_or_function)
    else:
        raise ValueError("The given function argument is neither a class nor a function.")

@_format_docstring_with_constant_names
def _encapsulated_property_from_class(cls):
    """
    A function intended to be used as a decorator on a class to convert it
    into a property.

    Args:
        cls (collections.abc.Callable): A class to which the decorator is
            applied.

    Returns:
        A property.

    The only user-defined attributes should be zero, one, two, or three
    methods, each named
    - "{getter_name}",
    - "{setter_name}", or
    - "{deleter_name}".
    Any docstring of this class will be used as the docstring of the
    property to be created.
    """
    expected_attrs = (GETTER_NAME, SETTER_NAME, DELETER_NAME, DOC_NAME)
    default_attrs = dir(type("", (), {}))
    unexpected_attrs = set(dir(cls)) - set(default_attrs) - set(expected_attrs)
    if len(unexpected_attrs) > 0:
        raise ValueError(f"One or more unexpected class attributes are defined: {', '.join(unexpected_attrs)}")
    return property(*(getattr(cls, attr) if hasattr(cls, attr) else None for attr in expected_attrs))

def _encapsulated_property_from_function(function):
    """
    A function intended to be used as a decorator on a function to convert
    it into a property.

    Args:
        function (collections.abc.Callable): A class to which the decorator
            is applied.

    Returns:
        A property.

    `function` should return an iterable of three values: a getter, a
    setter, and a deleter (in this order). Any of these three values may be
    `None`. Any docstring of this function will be used as the docstring of
    the property to be created.
    """
    function_output = function()
    try:
        getter, setter, deleter = function_output
    except ValueError:
        raise ValueError("The given function should output a value that can be unpacked into three elements. These "
                         "should correspond to the getter, setter, and deleter (in that order).")
    return property(getter, setter, deleter, function.__doc__)
