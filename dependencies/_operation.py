import inspect

from .exceptions import DependencyError


def operation(function):
    """FIXME: Write a docstring."""

    if inspect.isclass(function):
        raise DependencyError("'operation' decorator can not be used on classes")
    __init__ = make_init(function)
    return type("Operation", (object,), {"__init__": __init__, "__call__": __call__})


def make_init(function):

    names = get_arguments(function)
    arguments = ", ".join(names)
    def_expr = "def __init__(self, {arguments}):"
    func_expr = "    self.__function__ = function"
    args_expr = "    self.__arguments__ = [{arguments}]"
    template = "\n".join([def_expr, func_expr, args_expr])
    code = template.format(arguments=arguments)
    scope = {"function": function}
    exec(code, scope)
    __init__ = scope["__init__"]
    return __init__


def __call__(self):

    return self.__function__(*self.__arguments__)


def get_arguments(function):

    names = get_argument_names(function)
    if "self" in names:
        raise DependencyError("'operation' decorator can not be used on methods")
    return names


try:
    inspect.signature
except AttributeError:

    def get_argument_names(function):

        argspec = inspect.getargspec(function)
        args, varargs, kwargs, defaults = argspec
        return args


else:

    def get_argument_names(function):

        signature = inspect.signature(function)
        parameters = iter(signature.parameters.items())
        return [name for name, param in parameters]