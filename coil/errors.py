# Copyright (c) 2008-2009 ITA Software, Inc.
# See LICENSE.txt for details.

class CoilError(Exception):
    """Generic error for Coil"""

    def __init__(self, reason, location=None):
        if location:
            self.filePath = location.filePath
            self.line = location.line
            self.column = location.column
        else:
            self.filePath = None
            self.line = None
            self.column = None

        self.reason = reason
        Exception.__init__(self, reason)

    def __str__(self):
        if self.filePath or self.line:
            return "<%s:%s> %s" % (self.filePath, self.line, self.reason)
        else:
            return self.reason

class CoilStructError(CoilError):
    """Generic error for Coil Struct objects, used by various Key errors"""

    def __init__(self, struct, reason):
        self.structPath = struct.path()
        CoilError.__init__(self, reason, struct)

    def __str__(self):
        if self.filePath or self.line:
            return "<%s %s:%s> %s" % (self.structPath,
                    self.filePath, self.line, self.reason)
        else:
            return "<%s> %s" % (self.structPath, self.reason)

class KeyMissingError(CoilStructError, KeyError):
    """The given key was not found"""

    def __init__(self, struct, key, path=None):
        if path:
            msg = "The key %s (in %s) was not found" % (repr(key), repr(path))
        else:
            msg = "The key %s was not found" % repr(key)

        CoilStructError.__init__(self, struct, msg)

class KeyTypeError(CoilStructError, TypeError):
    """The given key was not a string"""

    def __init__(self, struct, key):
        msg = "Keys must be strings, got %s" % type(key)
        CoilStructError.__init__(self, struct, msg)

class KeyValueError(CoilStructError, ValueError):
    """The given key contained invalid characters"""

    def __init__(self, struct, key):
        msg = "The key %s contains invalid characters" % repr(key)
        CoilStructError.__init__(self, struct, msg)

class CoilSyntaxError(CoilError):
    """General error during parsing"""
    pass

class CoilUnicodeError(CoilSyntaxError):
    """Invalid unicode string"""
    pass
