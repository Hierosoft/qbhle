import re

import numpy as np

from qbhle.qbfunction import QBFunction
from qbhle.qbsub import QBSub

class QBProcess:
    PY_TYPE_FOR_SUFFIXES = {
        '$': str,
        '%': np.int16,
        '&': np.int32,
        '!': np.float32,  # default
        '#': np.float64,
    }
    TYPE_TO_SUFFIX = {
        'STRING': r'$',  # String
        'SHORT': r'%',  # 2-byte short int (Integer)
        'LONG': r'&',  # 4-byte long int (Long integer)
        'SINGLE': r'!',  # 4-byte float (default) (Single precision)
        'DOUBLE': r'#',  # 8-byte float (Double precision)
    }
    STATEMENT_TO_SUFFIX = {
        'DEFSTR': r'$',
        'DEFINT': r'%',
        'DEFLNG': r'&',
        'DEFSNG': r'!',
        'DEFDBL': r'#',
    }
    def __init__(self):
        self._default_suffix = "!"
        self._default_suffix_of_regex = {}
        self.symbols = {}
        self.functions = {}
        self.subs = {}
        # TODO: bare DEF* statements set default_suffix
        self.line_index = -1
        self.lines = None

    def set_def_type(self, statement, *args):
        suffix = QBProcess.STATEMENT_TO_SUFFIX[statement]
        if len(args) < 1:
            self._default_suffix = suffix
            return
        for pattern in args:
            # if pattern.upper() != pattern:
            #     raise ValueError("Should be uppercase args: {}...{}"
            #                      .format(statement, pattern))
            reg = r'[' + pattern.upper() + pattern.lower() + r']'
            self._default_suffix_of_regex[reg] = suffix

    def default_suffix(self, name):
        for reg, suffix in self._default_suffix_of_regex.items():
            if re.match(reg, name[:1]):
                return suffix
        return self._default_suffix

    def type(self, name, is_decl=False):
        """Get the type of the symbol"""
        # TODO: Get from variables in scope (Exception if found but is_decl)
        _type = QBProcess.PY_TYPE_FOR_SUFFIXES.get(name[-1:])
        if not _type:
            _type = QBProcess.PY_TYPE_FOR_SUFFIXES[self.default_suffix(name)]
        return _type

    def add_function(self, name, arg_types, return_type, is_decl):
        qf = QBFunction(name, arg_types, return_type)
        if not is_decl:
            self.functions[name] = qf  # See also functions in Parser subclass
        self.symbols[name] = qf
        return qf

    def add_sub(self, name, arg_types, is_decl):
        qf = QBSub(name, arg_types)
        if not is_decl:
            self.subs[name] = qf  # See also functions in Parser subclass
        self.symbols[name] = qf
        return qf
