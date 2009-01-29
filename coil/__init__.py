"""Coil: A Configuration Library.

Introduction
============

  Coil is a configuration file format that is parsed into a tree of dict
  like L{Struct} objects. The format supports inheritance, allowing
  complicated configurations to be as compact as possible.

Design Goals
============

  Below is a list of goals from GOALS.txt that needs to be updated....

    - Support non-Twisted reactor driven Python programs

    - Scalable to complex configurations

    - Scalable to many machines; for example, 50 machines that have almost
      same config with only minor changes to each should be easy to do.

    - Orthogonal to code; code should not be required to know about the
      config system used, it should be regular Python or Twisted code

    - Encourage design of code to be easily extendable and pluggable and
      not tightly coupled

    - Encourage creation of pre-made configuration libraries

    - Minimal boilerplate

    - Python object representation for automatic code generation as well
      as human editable text format which is not code (James pointed out
      how this is helpful, e.g. binding to pre-1024 ports, then changing
      uid, without actually importing any user code)

    - Maybe? Changeable at runtime; if not in first revision, should be
    kept in mind for further enhancement

Text Format
===========

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

    x: {a: 1}

    x: {
      a: 1
    }

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

  If the above example was a file called "foo.coil" and we did::

    sub: {
           @file: "foo.coil"
           x: {c : 2}
         }

  then sub.z  would be C{{c: 2 b: 4}}.

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
    sub: {@extends: ..base
          ~x  # sub now has no attribute "x"
         }

API Overview
============

  The core of the Coil API is the L{Struct} object. It is a dict-like
  mapping object that knows its place in a tree and can reference items
  anywhere in the tree.

  Assume we have a file at /tmp/example.coil with the following contents::

    x: { y: {a: 2}
         z: "hello"
         list: [1 2 3]}

    sub: {
         @extends: ..x
         y.b: 3
         ~z
    }

  We can then inspect the structure just like nested dict objects:

    >>> import coil
    >>> conf = coil.parse_file("/tmp/example.coil")
    >>> conf['x']['list']
    [1, 2, 3]
    >>> conf['x']['z']
    'hello'
    >>> conf.get('x').get('z')
    'hello'
    >>> conf.keys()
    ['x', 'sub']
    >>> 'z' in conf['sub'] # we deleted this with ~z
    False
    >>> conf['x']['y']
    Struct({'a': 2})
    >>> conf['sub']['y'] # inherited from x and added 'b'
    Struct({'a': 2, 'b': 3})

  Also, using L{get<struct.Struct.get>} and L{set<struct.Struct.set>}
  we can access and items based on absolute and relative paths as we
  can in the text format:

    >>> conf.get("x.z")
    'hello'
    >>> conf.get("@root.x.z")
    'hello'
    >>> x = conf['x']
    >>> x.get("..sub.y.b")
    3
    >>> conf.set("sub.y.c", 4)
    >>> conf['sub']['y']
    Struct({'a': 2, 'b': 3, 'c': 4})
"""

__version__ = "0.3.0"

from coil.parser import Parser

def parse_file(file_name):
    """Open and parse a coil file.

    Returns the root Struct.
    """
    coil = open(file_name)
    return Parser(coil, file_name).root()

def parse(string):
    """Parse a coil string.

    Returns the root Struct.
    """
    return Parser(string.splitlines()).root()

__all__ = ['parse_file', 'parse', 'struct', 'parser', 'tokenizer', 'errors']
