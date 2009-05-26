**********
User Guide
**********

Whee

Text Format
===========

Data Types
----------

Coil provides the concept of a struct - an ordered list of key/value
pairs. Basic types are True, False, None, integers, floats, unicode
strings and lists of basic types. Here we define a single struct::

    x: {
        anInt: 1
        aFloat: 2.4
        aString: "hello"
        andAList: [1 2 "hello" 4 None]
    }

Whitespace doesn't matter, so these two are identical::

    fx: {a: 1}

    x: {
        a: 1
    }

Inheritance
-----------

Structs can extends other structs: this means they inherit all
attributes from that struct. Extending is done with a special
attribute, @extends, with a value that is a path to another struct.
Paths can be relative, with a prefix of ".." meaning go up one level,
"..." go up two levels, etc., or absolute, starting from the special
location @root.  In this example, y and z inherit from x and override
some of its attributes::

    x: {a: 1  b: 2}
    y: {
        @extends: ..x # relative path
        b: 3
    }
    z: {
        @extends: @root.x # absolute path
        b: 4
    }

In this example y is the same as::

    y: {a: 1 b: 3}

For extending substructs there is a shorthand syntax. In this example
y and z both extend x, and have identical contents::

    x: { a: {b: 1} }
    y: {
        @extends: ..x
        a.b: 3
    }
    z: {
        @extends: ..x
        a: {
            @extends: ..x.a
            b: 3
        }
    }

Importing Files
---------------

Structs can also be used to import files, either given a path on the
filesystem, which can be absolute or relative to the current coil
file::

    example: {@file: "/home/joe/test/example.coil"}

or give a path which is relative to the path of Python package which
is present in sys.path, for example the file "example.coil" which is
present in the coil.test package::

    example: {@package: "ops.avs:./example.coil"}

Links can be used to have attributes whose value is determined based
on their context, i.e. at lookup time rather then at parse time. Their
syntax is like the paths used for @extends, except that they have a
"=" prefixed. For example, server1.myaddress.host will be the same as
server1.host in this example::

    address: {host: =..host  port: 1234}
    server1: {
        myaddress: {@extends: @root.address}
        host: "www.example.com"
    }

Finally, sub-structs can delete attributes provided by structs they
extend::

    base: {x: 1  y: 2}
    sub: {
        @extends: ..base
        ~x  # sub now has no attribute "x"
    }

References are also allowed within strings by using ${name}. For example::

    foo: "zomg"
    bar: "${foo}bbq"
    sub: {
        x: "foo is ${..foo}"
        y: "foo is ${@root.foo}"
    }

expands out to be::

    foo: "zomg"
    bar: "zomgbbq"
    sub: {
        x: "foo is zomg"
        y: "foo is zomg"
    }

Emacs users may be interested in the coil mode provided by
misc/coil.el in the coil distribution tarball.
