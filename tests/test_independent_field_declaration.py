from pytest import raises
from typedpy import String, Number, Structure, ImmutableField, ImmutableStructure, Array, Map, Integer, Field
from typing import get_type_hints, Type


def test_field_declaration():
    def Names(): return Array(items=String(minLength=2))

    def TableName(): return String(minLength=3)

    class Foo(Structure):
        i = Integer
        foo_names = Names()
        table = TableName()

    class Bar(Structure):
        bar_names = Names()
        i = Integer
        table = TableName()
    foo = Foo(i=1, foo_names=["jack"], table="abc")
    bar = Bar(i=1, bar_names=["john", "amber"], table="def")
    assert foo.foo_names == ["jack"]
    assert bar.bar_names == ["john", "amber"]
    assert bar.table == "def"
    assert foo.table == "abc"


def test_field_declaration_compact_syntax():
    def Names(): return Array[String]

    def TableName(): return String

    class Foo(Structure):
        i = Integer
        foo_names = Names()
        table = TableName()

    class Bar(Structure):
        bar_names = Names()
        i = Integer
        table = TableName()
    foo = Foo(i=1, foo_names=["jack"], table="abc")
    bar = Bar(i=1, bar_names=["john", "amber"], table="def")
    assert foo.foo_names == ["jack"]
    assert bar.bar_names == ["john", "amber"]
    assert bar.table == "def"
    assert foo.table == "abc"


# noinspection DuplicatedCode
def test_field_declaration_bad_usage():
    Names = Array[String]

    class Foo(Structure):
        i = Integer
        foo_names = Names

    # since here Names points to a single instance of field, when Bar uses it, it "hijacks" it from Foo.
    class Bar(Structure):
        bar_names = Names
        i = Integer

    foo = Foo(i=1, foo_names=["jack"])
    with raises(AttributeError) as ex:
        foo.namesBar.bar_names
    assert "'Foo' object has no attribute 'names'" in str(ex.value)


def test_field_declaration_bad_usage():
    Name = String()

    class Foo(Structure):
        i = Integer
        first_name_foo = Name
        last_name_foo = Name
        _additionalProperties = False

    # Note that here Names points to a single instance of field,so when Bar uses it, it "hijacks" it from Foo.
    class Bar(Structure):
        first_name_bar = Name
        last_name_bar = Name
        i = Integer
        _additionalProperties = False

    with raises(KeyError) as ex:
        Foo.first_name_foo
    assert "last_name_bar" in str(ex.value)

    # this can cause a lot of weirdness....
    foo = Foo(i=1, first_name_foo="jack", last_name_foo="smith")
    assert foo.first_name_foo == foo.last_name_foo
    # and even:
    assert foo.last_name_bar == foo.first_name_foo
    # so watch out!


def test_field_declaration_simplified_syntax_v051():
    # we declare type hint of the return value:
    def Names() -> Type[Field]: return Array[String]
    def TableName()-> Type[Field]: return String

    class Foo(Structure):
        i = Integer
        foo_names = Names
        table = TableName

    class Bar(Structure):
        bar_names = Names
        i = Integer
        table = TableName

    foo = Foo(i=1, foo_names=["jack"], table="abc")
    bar = Bar(i=1, bar_names=["john", "amber"], table="def")
    assert foo.foo_names == ["jack"]
    assert bar.bar_names == ["john", "amber"]
    assert bar.table == "def"
    assert foo.table == "abc"


