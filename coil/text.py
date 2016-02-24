# Copyright (c) 2005-2006 Itamar Shtull-Trauring.
# Copyright (c) 2008-2009 ITA Software, Inc.
# See LICENSE.txt for details.

"""Compatibility with <= 0.2.2, do not use in new code!"""

from coil import parser, parse_file, errors

ParseError = errors.CoilError


def from_sequence(iter_of_strings, file_path=None):
    """Load a Struct from a sequence of strings.

    @param file_path: path the strings were loaded from. Required for
    relative @file arguments to work.
    """
    # The strings in 0.2.2 were allowed to contain newlines. We now
    # expect the iter to be of lines, not arbitrary strings.
    lines = []
    for line in iter_of_strings:
        lines += line.splitlines()
    return parser.Parser(lines, file_path, 'utf-8').root()


def from_string(st, file_path=None):
    """Load a Struct from a string.

    @param file_path: path the string was loaded from. Required for
    relative @file arguments to work.
    """
    return parser.Parser(st.splitlines(), file_path, 'utf-8').root()


def from_file(path):
    """Load a struct from a file, given a path on the filesystem."""
    return parse_file(path)
