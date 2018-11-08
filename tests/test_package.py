import inspect

import pytest
from dependencies import Injector, Package
from helpers import CodeCollector


package_definitions = CodeCollector()


@package_definitions.parametrize
def test_provide_module(code):
    """Package instance itself should refer to the module."""

    Container = code()

    assert inspect.ismodule(Container.itself)
    assert inspect.ismodule(Container.submodule)


@package_definitions.parametrize
def test_provide_an_instance(code):
    """
    Package instance attribute access should provide injectable spec
    when refer to a class.
    """

    Container = code()

    from pkg.submodule import Foo, Bar

    assert isinstance(Container.instance, Foo) or isinstance(Container.instance, Bar)
    assert hasattr(Container.instance, "do")


@package_definitions.parametrize
def test_provide_instance_method(code):
    """
    Package instance attribute access should provide instance method.
    """

    Container = code()

    assert inspect.ismethod(Container.instance_method)
    assert Container.instance_method() == 1


@package_definitions.parametrize
def test_provide_a_function(code):
    """
    Package instance attribute access should provide regular function.
    """

    Container = code()

    assert inspect.isfunction(Container.function)
    assert Container.function() == 1


@package_definitions.parametrize
def test_provide_a_variable(code):
    """
    Package instance attribute access should provide regular variable.
    """

    Container = code()

    assert Container.variable == 1


# FIXME: Protect `Package` and `this` from `_class` named attributes.
@pytest.mark.xfail
@package_definitions.parametrize
def test_provide_a_class(code):
    """
    Package instance attribute should provide a class when it stored
    in the attribute with `_class` in its name.
    """

    Container = code()

    from pkg.submodule import Foo

    assert inspect.isclass(Container.keep_class)
    assert Container.keep_class is Foo


@package_definitions
def rQlPiacYOKsN():
    """Attribute access submodule."""

    pkg = Package("pkg")

    class Container(Injector):
        itself = pkg
        submodule = pkg.submodule
        instance = pkg.submodule.Foo
        instance_method = pkg.submodule.Foo.do
        function = pkg.submodule.function
        variable = pkg.submodule.variable
        keep_class = pkg.submodule.Foo

    return Container


@package_definitions
def uHSfYcZjGSJQ():
    """Constructor argument submodule."""

    pkg = Package("pkg")
    sub = Package("pkg.submodule")

    class Container(Injector):
        itself = pkg
        submodule = sub
        instance = sub.Bar
        instance_method = sub.Bar.do
        function = sub.function
        variable = sub.variable
        keep_class = sub.Bar

        a = -1
        b = 2

    return Container


injector_pointer = CodeCollector()


@pytest.mark.xfail
@injector_pointer.parametrize
def test_point_to_injector(code):
    """
    Package pointer should be able to point to `Injector` subclass
    attribute defined in another module.
    """

    Container = code()

    assert Container.foo == 1
    assert Container.bar == 2


@injector_pointer
def zprTYSyMkLEC():
    """Attribute access submodule."""

    pkg = Package("pkg")

    class Container(Injector):

        foo = pkg.injected.Container.foo
        bar = pkg.injected.Container.bar
        baz = 2

    return Container


@injector_pointer
def dqXJgFoftQja():
    """Constructor argument submodule."""

    injected = Package("pkg.injected")

    class Container(Injector):

        foo = injected.Container.foo
        bar = injected.Container.bar
        baz = 2

    return Container
