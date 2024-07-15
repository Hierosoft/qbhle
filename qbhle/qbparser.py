"""
QB Lexer and Parser implementation for SLY.
"""
from __future__ import division
# ^ QBASIC has both, and now Python does ;)
# based on example/expr.py in sly
# import sys
# sys.path.append('../..')
import os
import re
import sys

import numpy as np

from collections import OrderedDict
from logging import getLogger
from sly import Lexer, Parser

logger = getLogger(__name__)

MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
REPO_DIR = os.path.dirname(MODULE_DIR)

if __name__ == "__main__":
    sys.path.insert(0, REPO_DIR)

from qbhle.qbprocess import QBProcess
from qbhle.qblexer import QBLexer


class QBParser(Parser):
    tokens = QBLexer.tokens

    # TODO: Add COMMA to precedence?
    # 2-character ones *must* come 1st if 1st char has it's own meaning:
    precedence = (
        ('nonassoc', LT, GT),
        ('left', IF, ELSE, ELSEIF, END),
        ('left', EQ, NE, LT, LE, GT, GE),
        ('left', PLUS, MINUS),
        ('left', TIMES, DIVIDE, IDIVIDE, MOD),  # MODULUS),
        ('left', CARET),  # Exponent operator *differs* from EXP function
        ('left', LPAREN, RPAREN),
        # ('right', SUFFIX_TYPE_STRING, SUFFIX_TYPE_SHORT, SUFFIX_TYPE_LONG, SUFFIX_TYPE_SINGLE, SUFFIX_TYPE_DOUBLE),
        # ^ QB unary type specifiers
        ('right', UMINUS),  # '-' is used as negative sign not MINUS here
    )

    def __init__(self):
        self.functions = { }
        self.qb = QBProcess()

    @_('functions function')
    def functions(self, p):
        pass

    @_('function')
    def functions(self, p):
        pass

    @_('function_decl SUB expr')
    def function(self, p):
        self.function.block_end()
        self.function = None

    @_('function_decl SUB expr STATIC')
    def function(self, p):
        self.function.block_end()
        self.function = None

    # TODO: Forward declaration--which can be followed by any of:
    # - ()
    # - (argument(s))
    # - nothing
    @_('function_decl DECLARE SUB expr ()')
    def function(self, p):
        """Forward declaration with no arguments

        Example: DECLARE SUB LoadMaps ()
        """
        self.function.block_end()
        self.function = None

    @_('function_decl DECLARE SUB expr (expr)')
    def function(self, p):
        """Forward declaration with argument(s)

        Example: DECLARE SUB ShowLevel (Level%)
        """
        self.function.block_end()
        self.function = None

    @_('DECLARE FUNCTION NAME LPAREN parms RPAREN',
       'FUNCTION NAME LPAREN parms RPAREN')
    def function_decl(self, p):
        # self.locals = { name:n for n, name in enumerate(p.parms) }
        # TODO: Why map to number? (See expr.py)
        self.locals = {}
        types = []
        for n, name in enumerate(p.parms):
            self.locals[name] = n  # same as commented dict comprehension
            types.append(self.qb.type(name))
        # self.function = self.emu.add_function(p.NAME, [np.float16]*len(p.parms), [np.float16])
        return_type = self.qb.type(p.NAME, is_decl=True)
        self.function = self.qb.add_function(p.NAME, types, [return_type])
        self.functions[p.NAME] = self.function

    @_('DECLARE FUNCTION NAME LPAREN RPAREN',
       'FUNCTION NAME LPAREN RPAREN')
    def function_decl(self, p):
        self.locals = { }
        return_type = self.qb.type(p.NAME, is_decl=True)
        self.function = self.qb.add_function(p.NAME, [], [return_type])
        self.functions[p.NAME] = self.function

    @_('parms COMMA parm')
    def parms(self, p):
        return p.parms + [p.parm]

    @_('parm')
    def parms(self, p):
        return [ p.parm ]

    @_('NAME')
    def parm(self, p):
        print("NAME={}".format(p.NAME))
        return p.NAME

    @_('expr PLUS expr')
    def expr(self, p):
        # self.function.i32.add()
        return p.expr0 + p.expr1

    @_('expr MINUS expr')
    def expr(self, p):
        # self.function.i32.sub()
        return p.expr0 - p.expr1

    @_('expr TIMES expr')
    def expr(self, p):
        # self.function.i32.mul()
        return p.expr0 * p.expr1

    @_('expr DIVIDE expr')
    def expr(self, p):
        # self.function.i32.div_s()
        return p.expr0 / p.expr1

    @_('expr LT expr')
    def expr(self, p):
        # self.function.i32.lt_s()
        return p.expr0 < p.expr1

    @_('expr LE expr')
    def expr(self, p):
        # self.function.i32.le_s()
        return p.expr0 <= p.expr1

    @_('expr GT expr')
    def expr(self, p):
        # self.function.i32.gt_s()
        return p.expr0 > p.expr1

    @_('expr GE expr')
    def expr(self, p):
        # self.function.i32.ge_s()
        return p.expr0 >= p.expr1

    @_('expr EQ expr')
    def expr(self, p):
        # self.function.i32.eq()
        return p.expr0 == p.expr1

    @_('NAME EQ expr')
    def expr(self, p):
        # self.function.i32.eq()
        return p.expr0 = p.expr1

    @_('expr NE expr')
    def expr(self, p):
        # self.function.i32.ne()
        return p.expr0 != p.expr1

    @_('LPAREN expr RPAREN')
    def expr(self, p):
        return p.expr

    @_('MINUS expr %prec UMINUS')
    def expr(self, p):
        return -p.expr

    # TODO: Finish this (See example/expr.py in sly)


if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        raise SystemExit(f'Usage: {sys.argv[0]} <BAS file>')

    lexer = QBLexer()
    # Only public method is "tokenize" which generates Token instances.
    for tok in lexer.tokenize(data):
        print('type=%r, value=%r' % (tok.type, tok.value))
    raise NotImplementedError()
    parser = QBParser()
    parser.parse(lexer.tokenize(open(sys.argv[1]).read()))

    name = sys.argv[1].split('.')[0]
