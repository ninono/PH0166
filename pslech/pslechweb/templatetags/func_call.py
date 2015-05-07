# -*- coding: utf-8 -*-
from django.template import Library
from functools import partial

register = Library()

@register.filter
def method(value, arg):
    """
    Prepare the specified object for invoking a method.

    This is used in conjunction with the "with" and "call" tags.  For
    example, with

      class Foo:
        def bar(self, a, b, c):
          return "a is %s, b is %b, c is %c" % (a, b, c)

        def bop(self, a):
          return "a is %s" % a

    and { "foo": Foo() } passed to the template, then:

      foo|method:"bar"|with:"one"|with:"two"|with:"three"|call

    will invoke foo("one", "two", "three"), and emit:

      a is one, b is two, c is three.

    Alternatively,

      foo|method:"bop"|call_with:"baz"

    is a bit of a short cut.
    """
    if hasattr(value, str(arg)):
        return getattr(value, str(arg))

    return "[%s has no method %s]" % (value, arg)

@register.filter
def call_with(value, arg):
    """
    Call a function with the specified argument.

    Meant to be used with the "method" tag.
    """
    if not callable(value):
        return "[%s is not callable]" % value

    return value(arg)

@register.filter
def call(value):
    """
    Call a function with no arguments.

    Meant to be used with the "method" tag.
    """
    if not callable(value):
        return "[%s is not callable]" % value

    return value()

@register.filter(name="with")
def with_(value, arg):
    """
    Accumulate the specified positional argument.

    Meant to be used with the "method" tag.
    """
    if callable(value):
        return partial(value, arg)

    return "[%s is not callable]" % value
