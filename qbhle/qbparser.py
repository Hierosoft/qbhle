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
    precedence = (  # noqa: F821
        ('nonassoc', LT, GT, EQ, NE, LE, GE),
        ('left', IF, ELSE, ELSEIF, END),
        # ('left', EQ, NE, LT, LE, GT, GE),
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
        self.core = QBProcess()
    """
    @_('functions function')  # noqa: F821 # type: ignore[reportUndefinedVariable]
    def functions(self, p):
        pass

    @_('function')  # noqa: F821 # type: ignore[reportUndefinedVariable]
    def functions(self, p):  # noqa: F811
        pass

    @_('function_decl SUB expr')  # noqa: F821 # type: ignore[reportUndefinedVariable]
    def function(self, p):
        self.function.block_end()
        self.function = None

    @_('function_decl SUB expr STATIC')  # noqa: F821 # type: ignore[reportUndefinedVariable]
    def function(self, p):  # noqa: F811
        self.function.block_end()
        self.function = None
    """

    def _types(self, p, set_locals):
        types = []
        for n, name in enumerate(p.parms):
            if set_locals:
                self.locals[name] = n  # same as commented dict comprehension
            types.append(self.core.type(name))
        return types

    # TODO: Forward declaration--which can be followed by any of:
    # - ()
    # - (argument(s))
    # - nothing
    @_('DECLARE SUB ID LPAREN RPAREN')  # noqa: F821 # type: ignore[reportUndefinedVariable]
    def sub_decl_no_parms(self, p):  # noqa: F811
        """Forward declaration with no arguments

        Example: DECLARE SUB LoadMaps ()
        """
        is_decl = True
        types = []
        self.function = self.core.add_sub(p.ID, types)
        self.function.block_end()
        self.function = None

    @_('DECLARE SUB ID LPAREN parms RPAREN')  # noqa: F821 # type: ignore[reportUndefinedVariable]
    def sub_decl(self, p):
        is_decl = True
        # self.locals = { name:n for n, name in enumerate(p.parms) }
        # TODO: Why make value a number (from expr.py)?
        types = self._types(p, not is_decl)
        self.function = self.core.add_sub(p.ID, types)
        self.functions[p.ID] = self.function

    @_('SUB ID LPAREN parms RPAREN')  # noqa: F821 # type: ignore[reportUndefinedVariable]
    def sub_def(self, p):
        is_decl = False
        self.locals = {}
        types = self._types(p, not is_decl)
        # self.function = self.core.add_function(p.ID, [np.float16]*len(p.parms), [np.float16])
        self.function = self.core.add_sub(p.ID, types)
        self.functions[p.ID] = self.function

    #   'SUB ID LPAREN RPAREN')  # TODO: add as 2nd regex if allowed in QB
    @_('SUB ID')  # noqa: F821 # type: ignore[reportUndefinedVariable]
    def sub_def_no_parms(self, p):
        is_decl = False
        types = []
        # self.function = self.core.add_function(p.ID, [np.float16]*len(p.parms), [np.float16])
        self.function = self.core.add_sub(p.ID, types)
        self.functions[p.ID] = self.function

    @_('DECLARE FUNCTION ID LPAREN RPAREN')  # noqa: F821 # type: ignore[reportUndefinedVariable]
    def function_decl_no_parms(self, p):  # noqa: F811
        is_decl = True
        types = []
        return_type = self.core.type(p.ID, is_decl=is_decl)
        self.function = self.core.add_function(p.ID, types, [return_type])
        self.functions[p.ID] = self.function

    @_('DECLARE FUNCTION ID LPAREN parms RPAREN')  # noqa: F821 # type: ignore[reportUndefinedVariable]
    def function_decl(self, p):  # noqa: F811
        is_decl = True
        types = self._types(p, not is_decl)
        return_type = self.core.type(p.ID, is_decl=is_decl)
        self.function = self.core.add_function(p.ID, types, [return_type])
        self.functions[p.ID] = self.function

    # 'FUNCTION ID LPAREN RPAREN')  # TODO: add as 2nd regex if allowed in qb
    @_('FUNCTION ID')  # noqa: F821 # type: ignore[reportUndefinedVariable]
    def function_def_no_parms(self, p):  # noqa: F811
        is_decl = False
        self.locals = {}
        types = []
        return_type = self.core.type(p.ID)
        self.function = self.core.add_function(p.ID, types, [return_type])
        self.functions[p.ID] = self.function

    @_('PRINT ID')
    def print(self, p):
        print("[PRINT ID] {}".format(p.ID))

    @_('PRINT LITERAL')
    def print(self, p):
        print("[PRINT LITERAL] {}".format(p.LITERAL))

    @_('PRINT parms')
    def print(self, p):
        for value in p.parms:
            print("[PRINT parms] {}".format(value))

    @_('FUNCTION ID LPAREN parms RPAREN')  # noqa: F821 # type: ignore[reportUndefinedVariable]
    def function_def(self, p):  # noqa: F811
        is_decl = False
        self.locals = {}
        types = self._types(p, not is_decl)
        return_type = self.core.type(p.ID)
        self.function = self.core.add_function(p.ID, types, [return_type])
        self.functions[p.ID] = self.function

    @_('parms COMMA parm')  # noqa: F821 # type: ignore[reportUndefinedVariable]
    def parms(self, p):
        return p.parms + [p.parm]

    @_('parm')  # noqa: F821 # type: ignore[reportUndefinedVariable]
    def parms(self, p):  # noqa: F811
        return [ p.parm ]

    @_('expr PLUS expr')  # noqa: F821 # type: ignore[reportUndefinedVariable]
    def expr(self, p):  # noqa: F811
        # self.function.i32.add()
        return p.expr0 + p.expr1

    @_('expr MINUS expr')  # noqa: F821 # type: ignore[reportUndefinedVariable]
    def expr(self, p):  # noqa: F811
        # self.function.i32.sub()
        return p.expr0 - p.expr1

    @_('expr TIMES expr')  # noqa: F821 # type: ignore[reportUndefinedVariable]
    def expr(self, p):  # noqa: F811
        # self.function.i32.mul()
        return p.expr0 * p.expr1

    @_('expr DIVIDE expr')  # noqa: F821 # type: ignore[reportUndefinedVariable]
    def expr(self, p):  # noqa: F811
        # self.function.i32.div_s()
        return p.expr0 / p.expr1

    @_('expr LT expr')  # noqa: F821 # type: ignore[reportUndefinedVariable]
    def expr(self, p):  # noqa: F811
        # self.function.i32.lt_s()
        return p.expr0 < p.expr1

    @_('expr LE expr')  # noqa: F821 # type: ignore[reportUndefinedVariable]
    def expr(self, p):  # noqa: F811
        # self.function.i32.le_s()
        return p.expr0 <= p.expr1

    @_('expr GT expr')  # noqa: F821 # type: ignore[reportUndefinedVariable]
    def expr(self, p):  # noqa: F811
        # self.function.i32.gt_s()
        return p.expr0 > p.expr1

    @_('expr GE expr')  # noqa: F821 # type: ignore[reportUndefinedVariable]
    def expr(self, p):  # noqa: F811
        # self.function.i32.ge_s()
        return p.expr0 >= p.expr1

    @_('expr EQ expr')  # noqa: F821 # type: ignore[reportUndefinedVariable]
    def expr(self, p):  # noqa: F811
        # self.function.i32.eq()
        return p.expr0 == p.expr1

    @_('ID EQ expr')  # noqa: F821 # type: ignore[reportUndefinedVariable]
    def expr(self, p):  # noqa: F811
        # self.function.i32.eq()
        # return p.expr0 = p.expr1
        # TODO: could be function return! Example: `SaveAs% = 1` inside SaveAs%
        print("[ID EQ expr] dir(p.expr0):{}".format(dir(p.expr0)))
        self.function.eq(p.ID, p.expr0.value)

    @_('expr NE expr')  # noqa: F821 # type: ignore[reportUndefinedVariable]
    def expr(self, p):  # noqa: F811
        # self.function.i32.ne()
        return p.expr0 != p.expr1

    @_('LPAREN expr RPAREN')  # noqa: F821 # type: ignore[reportUndefinedVariable]
    def expr(self, p):  # noqa: F811
        return p.expr

    @_('MINUS expr %prec UMINUS')  # noqa: F821 # type: ignore[reportUndefinedVariable]
    def expr(self, p):  # noqa: F811
        return -p.expr

    @_('LITERAL')
    def expr(self, p):
        if "." in p.LITERAL:
            # NOTE: QB floats are 32 and 64
            self.function.f64.const(np.float64(p.LITERAL))
        else:
            # NOTE: QB ints are 16 and 32
            self.function.i32.const(np.int32(p.LITERAL))

    @_('ID')  # noqa: F821 # type: ignore[reportUndefinedVariable]
    def parm(self, p):
        # TODO: could be a function call (but has to be RValue to be a call?)
        print("ID={}".format(p.ID))
        return p.ID

    @_('ID LPAREN exprlist RPAREN')
    def expr(self, p):
        self.function.call(self.functions[p.ID])

    @_('ID LPAREN RPAREN')
    def expr(self, p):
        self.function.call(self.functions[p.ID])

    # @_('IF expr thenexpr ELSE expr')
    # def expr(self, p):
    #     self.function.block_end()
    # TODO: ^ Is there a ternary operation of any sort in QBASIC?

    # TODO: IF condition THEN statements [ELSE statements]

    @_('exprlist COMMA expr')
    def exprlist(self, p):
        pass

    @_('expr')
    def exprlist(self, p):
        pass

    # @_('startthen expr')
    # def thenexpr(self, p):
    #     self.function.else_start()
    # ^ Symbol 'startthen' used, but not defined as a token or a rule

    # @_('THEN')
    # def startthen(self, p):
    #     self.function.if_start(wasm.i32)

def run_file(path):
    lexer = QBLexer()
    lexer.path = path
    # Only public method is "tokenize" which generates Token instances.
    with open(path, 'r', encoding='ascii') as file:
        lines = [line for line in file]
        # ^ Do *not* do `.rstrip()`, since \n is important in QB!
    parser = QBParser()
    parser.path = path
    parser.core.lines = lines
    # parser.core.line_index = 0
    # data = ""
    # while (parser.core.line_index + 1) < len(lines):
    #     data += lines[parser.core.line_index]
    #     parser.core.line_index += 1
    # parser.parse(lexer.tokenize(data))
    # return 0
    parser.core.line_index = 0
    print("len(lines)={}".format(len(lines)))
    while parser.core.line_index < len(lines):
        unmodified_index = parser.core.line_index
        data = lines[parser.core.line_index]
        if not data.strip():
            print('[run_file] line {} is blank'
                .format(parser.core.line_index+1))
            parser.core.line_index += 1
            continue
        if not data.endswith("\n"):
            # raise NotImplementedError("The lexer needs the newline.")
            data += "\n"
            logger.info("{}, line {}: No newline at end of file."
                        .format(path, parser.core.line_index+1))
        print('[run_file] line {} tokens:'
              .format(parser.core.line_index+1))
        # print("{}".format(dir(lexer))); break
        lexer.lineno = 0
        for tok in lexer.tokenize(data):  # for debug only
            print('  type=`{}`, value={}({})'
                  .format(tok.type, type(tok.value).__name__,
                          tok.value))
        # TODO: a number at the start of a line sets the numbering arbitrarily!
        # ^ line_index may not be lineno-1!

        parser.parse(lexer.tokenize(data))
        # ^ May override current line index using:
        # - GOSUB (as opposed to CALL)
        #   - or the SUB's RETURN having a number after it
        # - GOTO
        # Therefore only increment conditionally:
        if parser.core.line_index == unmodified_index:
            parser.core.line_index += 1
        # parser.restart()  # TODO: find out how to fix line after statement! Then indent into `if`
    print("Done (parser.core.line_index={})".format(parser.core.line_index))
    return 0


def main():
    import sys
    if len(sys.argv) != 2:
        raise SystemExit(f'Usage: {sys.argv[0]} <BAS file>')
    return run_file(sys.argv[1])


if __name__ == '__main__':
    sys.exit(main())