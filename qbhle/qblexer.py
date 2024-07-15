# type: ignore[reportUndefinedVariable]
"""
QB Lexer implementation for SLY.
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
# _name = r'[a-zA-Z_][a-zA-Z0-9_]*(\$|\%|\&|\!|\#)*'
# ^ NOTE: Parts without () are not captured by Python if there is any group!
#   Therefore:
_ID = r'[a-zA-Z_][a-zA-Z0-9_]*[$%&!\#]*'
# NOTE: # *requires* square brackets due to re.VERBOSE mode
#   as per SLY documentation (It says use `[#]` or `\#`
#   so I've added `\` explicitly just to be sure).
_pat = re.compile(_ID)
# NOTE: search(s) only gets one match.
assert(_pat.findall("A type is not defined.")[4] == "defined")
assert(_pat.findall("A variable$ is here.")[1] == "variable$")
assert(_pat.findall("A variable% is here.")[1] == "variable%")
assert(_pat.findall("A variable& is here.")[1] == "variable&")
assert(_pat.findall("A variable! is here.")[1] == "variable!")
assert(_pat.findall("A variable# is here.")[1] == "variable#")
assert(_pat.findall("% is not a variable.")[0] == "is")
assert(_pat.findall("Separate # is not a variable.")[1] == "is")


class QBLexer(Lexer):
    # TODO: A forward declaration can be a suffix alone to specify type:
    #   DECLARE SUB cube(!)
    #   (for single precision)
    # region generated by qbstatic
    tokens = {
        ID,  # Use ID for symbol since NAME itself is a statement!
        NUMBER,
        PLUS,
        MINUS,
        TIMES,
        DIVIDE,
        IDIVIDE,
        # MODULUS,
        CARET,
        LPAREN,
        RPAREN,
        COMMA,
        NE,
        LE,
        LT,
        GE,
        GT,
        EQ,
        SEMI,
        ABS, ABSOLUTE, ACCESS,
        AND,  # BOOLEAN_OPERATOR
        ANY, APPEND, AS, ASC, ATN,
        BASE, BEEP, BINARY, BLOAD, BSAVE,
        CALL, CASE, CDBL, CHAIN, CHDIR, CHR_, CINT, CIRCLE, CLEAR, CLNG, CLOSE, CLS, COLOR, COM, COMMON, CONST, COS, CSNG, CSRLIN, CVD, CVDMBF, CVI, CVL, CVS, CVSMBF,
        DATA, DATE_, DECLARE, DEF,
        FN,
        SEG,
        DEFDBL, DEFINT, DEFLNG, DEFSNG, DEFSTR, DIM, DO,
        LOOP,
        DOUBLE, DRAW,
        ELSE, ELSEIF, END, ENDIF, ENVIRON, ENVIRON_, EOF,
        EQV,  # BOOLEAN_OPERATOR
        ERASE, ERDEV, ERDEV_, ERL, ERR, ERROR, EXIT, EXP,
        FIELD, FILEATTR, FILES, FIX, FOR,
        NEXT,
        FRE, FREEFILE, FUNCTION,
        GET, GOSUB,
        RETURN,
        GOTO,
        HEX_,
        IF,
        THEN,
        IMP,  # BOOLEAN_OPERATOR
        INKEY_, INP, INPUT, INPUT_, INSTR, INT, INTEGER, IOCTL, IOCTL_, IS,
        KEY, KILL,
        LBOUND, LCASE_, LEFT_, LEN, LET, LINE, LIST, LOC, LOCATE, LOCK, LOF, LOG, LONG, LPOS, LPRINT,
        USING,
        LSET, LTRIM_,
        MID_, MKD_, MKDIR, MKDMBF_, MKI_, MKL_, MKS_, MKSMBF_,
        MOD,  # BOOLEAN_OPERATOR
        NAME,
        NOT,  # BOOLEAN_OPERATOR
        OCT_, OFF, ON,
        PEN, PLAY,
        STRIG,
        TIMER,
        OPEN, OPTION,
        OR,  # BOOLEAN_OPERATOR
        OUT, OUTPUT,
        PAINT, PALETTE, PCOPY, PEEK, PMAP, POINT, POKE, POS, PRESET, PRINT, PSET, PUT,
        RANDOM, RANDOMIZE, READ, REDIM, REM, RESET, RESTORE, RESUME, RIGHT_, RMDIR, RND, RSET, RTRIM_, RUN,
        SCREEN, SEEK, SELECT, SGN, SHARED, SHELL, SIN, SINGLE, SLEEP, SOUND, SPACE_, SPC, SQR, STATIC, STEP, STICK, STOP, STR_, STRING, STRING_, SUB, SWAP, SYSTEM,
        TAB, TAN, TIME_, TO, TROFF, TRON, TYPE,
        UBOUND, UCASE_, UNLOCK, UNTIL,
        VAL, VARPTR, VARPTR_, VARSEG, VIEW,
        WAIT, WEND, WHILE, WIDTH, WINDOW, WRITE,
        XOR,  # BOOLEAN_OPERATOR
    }
    # endregion generated by qbstatic
    ignore = ' \t'
    literals = {'(', ')', ":"}

    # Tokens
    # TODO: use SUFFIX_TYPE_* values as part of name:

    # ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    ID = _ID

    # Special cases (override pattern matching & change to non-ID token):
    # ID['']

    # ID['IF'] = IF
    # ID['THEN'] = THEN
    # TODO: Make sure elseif is implemented actually
    # ID['ELSEIF'] = ELSEIF
    # ID['ELSE'] = ELSE
    # TODO:? ID['INKEY$'] = INKEY_
    # ID['ABS'] = ABS

    # NOTE: Some have suffixes:
    #  - Always require suffix for:
    #    CHR$, DATE$, ENVIRON$, HEX$, INKEY$, LCASE$, LEFT$, LTRIM$, MID$, MKD$, MKDMBF$, MKI$, MKL$, MKS$, MKSMBF$, OCT$, RIGHT$, RTRIM$, SPACE$, STR$, STRING$, TIME$, UCASE$, VARPTR$
    #  - "$" at end *optionally*:
    #    ERRDEV$
    #    INPUT$
    #    IOCTL$
    #  - the following has two words for a different meaning:
    #    VIEW PRINT*
    #    CALL ABSOLUTE
    #    DEF FN
    #    DEF SEG
    #    LINE INPUT*
    #    LPRINT USING*
    #    ON COM*
    #    ON ERROR*
    #    ON KEY*
    #    ON PEN*
    #    ON PLAY*
    #    ON STRIG*
    #    ON TIMER*
    #    OPEN COM*
    #    PALETTE USING*
    #    PRINT USING*
    #  - the following require second word:
    #    OPTION BASE*
    #    SELECT CASE*
    #
    #    *: second word is also a keyword if used alone
    # TODO: How is two's compliment ("NOT" in QB) handled?
    # "NOT X = -(X + 1); the two’s complement of any integer is the bit
    # complement plus one."
    # -<https://qbasic.com/documentation/>

    # NUMBER = r'\d+'  # See regex in @_ decorator for NUMBER instead.

    # Special symbols
    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    DIVIDE = r'/'
    # TODO: INTEGER DIVISION:
    IDIVIDE = r'\\'
    # MODULUS = r'[Mm][Oo][Dd]'  # 10 MOD 3 is 1
    CARET = r'^'
    LPAREN = r'\('
    RPAREN = r'\)'
    COMMA = r','
    # 2-character ones *must* come 1st if 1st char has it's own meaning:
    NE = r'<>'
    LE = r'<='
    LT = r'<'
    GE = r'>='
    GT = r'>'
    EQ = r'='  # Same as ASSIGN in QB (depends on context)
    # Example: LET A$ = "File" : LET B$ = "name"
    # ASSIGN = r'='
    SEMI = r';'  # TODO: flush character for PRINT, or adds "?" for INPUT
    # COLON = ':'  # ':' starts a new statement on same line
    # TODO: UNARY TYPE DECORATORS
    #   (Symbol right of variable makes it statically typed):
    # SUFFIX_TYPE_STRING = r'$'
    # SUFFIX_TYPE_SHORT = r'%'  # 2-byte short int
    # SUFFIX_TYPE_LONG = r'&'  # 4-byte long int
    # SUFFIX_TYPE_SINGLE = r'!'  # 4-byte float (default)
    # SUFFIX_TYPE_DOUBLE = r'#'  # 8-byte float
    # ^ See also QBProcess.PY_TYPE_FOR_SUFFIXES
    # TODO: STRING * n%	A fixed-length string variable n% bytes long.
    UMINUS = r'-'  # negative sign before a number

    # Ignored pattern
    ignore_newline = r'[\n:]+'  # treat ':' as newline too
    ignore_comment = r"'.*\n|^\s*REM .*\n"  # ' or startswith REM

    def __init__(self):
        self.scope_depth = 0  # vertical nesting level
        self.expression_depth = 0  # horizontal nesting level

    def on_newline(self):
        if self.expression_depth > 0:
            raise SyntaxError("Line {} ended before ')'"
                              .format(self.lineno))
        elif self.expression_depth < 0:
            raise SyntaxError("Line {} had extra ')'"
                              .format(self.lineno))
        # self.expression_depth = 0

    # Extra action for newlines
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')
        self.on_newline()

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1  # Skip ahead to try to find a landmark.

    @_(r'\(')
    def lparen(self, t):
        t.type = "("
        self.expression_depth += 1
        return t

    @_(r'\)')
    def rparen(self, t):
        t.type = ")"
        self.expression_depth -= 1
        return t

    @_(r':')
    def colon(self, t):
        t.type = ":"
        self.on_newline()
        return t

    @_(r'&H[0-9a-fA-F]+',
       r'&O[0-7]+',
       r'&B[0-1]+',
       r'\d+')
    def NUMBER(self, t):
        if t.value.startswith('&H'):
            t.value = int(t.value[2:], 16)
        elif t.value.startswith('&O'):
            t.value = int(t.value[2:], 8)
        elif t.value.startswith('&B'):
            t.value = int(t.value[2:], 2)
        return t
    # region generated by qbstatic

    # def ID(self, t):
    #     return t

    @_(r'[aA][bB][sS]')
    def ABS(self, t):
        return t

    @_(r'[aA][bB][sS][oO][lL][uU][tT][eE]')
    def ABSOLUTE(self, t):
        return t

    @_(r'[aA][cC][cC][eE][sS][sS]')
    def ACCESS(self, t):
        return t

    @_(r'[aA][nN][dD]')
    def AND(self, t):
        return t

    @_(r'[aA][nN][yY]')
    def ANY(self, t):
        return t

    @_(r'[aA][pP][pP][eE][nN][dD]')
    def APPEND(self, t):
        return t

    @_(r'[aA][sS]')
    def AS(self, t):
        return t

    @_(r'[aA][sS][cC]')
    def ASC(self, t):
        return t

    @_(r'[aA][tT][nN]')
    def ATN(self, t):
        return t

    @_(r'[bB][aA][sS][eE]')
    def BASE(self, t):
        return t

    @_(r'[bB][eE][eE][pP]')
    def BEEP(self, t):
        return t

    @_(r'[bB][iI][nN][aA][rR][yY]')
    def BINARY(self, t):
        return t

    @_(r'[bB][lL][oO][aA][dD]')
    def BLOAD(self, t):
        return t

    @_(r'[bB][sS][aA][vV][eE]')
    def BSAVE(self, t):
        return t

    @_(r'[cC][aA][lL][lL]')
    def CALL(self, t):
        return t

    @_(r'[cC][aA][sS][eE]')
    def CASE(self, t):
        return t

    @_(r'[cC][dD][bB][lL]')
    def CDBL(self, t):
        return t

    @_(r'[cC][hH][aA][iI][nN]')
    def CHAIN(self, t):
        return t

    @_(r'[cC][hH][dD][iI][rR]')
    def CHDIR(self, t):
        return t

    @_(r'[cC][hH][rR]$')
    def CHR_(self, t):
        return t

    @_(r'[cC][iI][nN][tT]')
    def CINT(self, t):
        return t

    @_(r'[cC][iI][rR][cC][lL][eE]')
    def CIRCLE(self, t):
        return t

    @_(r'[cC][lL][eE][aA][rR]')
    def CLEAR(self, t):
        return t

    @_(r'[cC][lL][nN][gG]')
    def CLNG(self, t):
        return t

    @_(r'[cC][lL][oO][sS][eE]')
    def CLOSE(self, t):
        return t

    @_(r'[cC][lL][sS]')
    def CLS(self, t):
        return t

    @_(r'[cC][oO][lL][oO][rR]')
    def COLOR(self, t):
        return t

    @_(r'[cC][oO][mM]')
    def COM(self, t):
        return t

    @_(r'[cC][oO][mM][mM][oO][nN]')
    def COMMON(self, t):
        return t

    @_(r'[cC][oO][nN][sS][tT]')
    def CONST(self, t):
        return t

    @_(r'[cC][oO][sS]')
    def COS(self, t):
        return t

    @_(r'[cC][sS][nN][gG]')
    def CSNG(self, t):
        return t

    @_(r'[cC][sS][rR][lL][iI][nN]')
    def CSRLIN(self, t):
        return t

    @_(r'[cC][vV][dD]')
    def CVD(self, t):
        return t

    @_(r'[cC][vV][dD][mM][bB][fF]')
    def CVDMBF(self, t):
        return t

    @_(r'[cC][vV][iI]')
    def CVI(self, t):
        return t

    @_(r'[cC][vV][lL]')
    def CVL(self, t):
        return t

    @_(r'[cC][vV][sS]')
    def CVS(self, t):
        return t

    @_(r'[cC][vV][sS][mM][bB][fF]')
    def CVSMBF(self, t):
        return t

    @_(r'[dD][aA][tT][aA]')
    def DATA(self, t):
        return t

    @_(r'[dD][aA][tT][eE]$')
    def DATE_(self, t):
        return t

    @_(r'[dD][eE][cC][lL][aA][rR][eE]')
    def DECLARE(self, t):
        return t

    @_(r'[dD][eE][fF]')
    def DEF(self, t):
        return t

    @_(r'[fF][nN]')
    def FN(self, t):
        return t

    @_(r'[sS][eE][gG]')
    def SEG(self, t):
        return t

    @_(r'[dD][eE][fF][dD][bB][lL]')
    def DEFDBL(self, t):
        return t

    @_(r'[dD][eE][fF][iI][nN][tT]')
    def DEFINT(self, t):
        return t

    @_(r'[dD][eE][fF][lL][nN][gG]')
    def DEFLNG(self, t):
        return t

    @_(r'[dD][eE][fF][sS][nN][gG]')
    def DEFSNG(self, t):
        return t

    @_(r'[dD][eE][fF][sS][tT][rR]')
    def DEFSTR(self, t):
        return t

    @_(r'[dD][iI][mM]')
    def DIM(self, t):
        return t

    @_(r'[dD][oO]')
    def DO(self, t):
        return t

    @_(r'[lL][oO][oO][pP]')
    def LOOP(self, t):
        return t

    @_(r'[dD][oO][uU][bB][lL][eE]')
    def DOUBLE(self, t):
        return t

    @_(r'[dD][rR][aA][wW]')
    def DRAW(self, t):
        return t

    @_(r'[eE][lL][sS][eE]')
    def ELSE(self, t):
        return t

    @_(r'[eE][lL][sS][eE][iI][fF]')
    def ELSEIF(self, t):
        return t

    @_(r'[eE][nN][dD]')
    def END(self, t):
        return t

    @_(r'[eE][nN][dD][iI][fF]')
    def ENDIF(self, t):
        return t

    @_(r'[eE][nN][vV][iI][rR][oO][nN]')
    def ENVIRON(self, t):
        return t

    @_(r'[eE][nN][vV][iI][rR][oO][nN]$')
    def ENVIRON_(self, t):
        return t

    @_(r'[eE][oO][fF]')
    def EOF(self, t):
        return t

    @_(r'[eE][qQ][vV]')
    def EQV(self, t):
        return t

    @_(r'[eE][rR][aA][sS][eE]')
    def ERASE(self, t):
        return t

    @_(r'[eE][rR][dD][eE][vV]')
    def ERDEV(self, t):
        return t

    @_(r'[eE][rR][dD][eE][vV]$')
    def ERDEV_(self, t):
        return t

    @_(r'[eE][rR][lL]')
    def ERL(self, t):
        return t

    @_(r'[eE][rR][rR]')
    def ERR(self, t):
        return t

    @_(r'[eE][rR][rR][oO][rR]')
    def ERROR(self, t):
        return t

    @_(r'[eE][xX][iI][tT]')
    def EXIT(self, t):
        return t

    @_(r'[eE][xX][pP]')
    def EXP(self, t):
        return t

    @_(r'[fF][iI][eE][lL][dD]')
    def FIELD(self, t):
        return t

    @_(r'[fF][iI][lL][eE][aA][tT][tT][rR]')
    def FILEATTR(self, t):
        return t

    @_(r'[fF][iI][lL][eE][sS]')
    def FILES(self, t):
        return t

    @_(r'[fF][iI][xX]')
    def FIX(self, t):
        return t

    @_(r'[fF][oO][rR]')
    def FOR(self, t):
        return t

    @_(r'[nN][eE][xX][tT]')
    def NEXT(self, t):
        return t

    @_(r'[fF][rR][eE]')
    def FRE(self, t):
        return t

    @_(r'[fF][rR][eE][eE][fF][iI][lL][eE]')
    def FREEFILE(self, t):
        return t

    @_(r'[fF][uU][nN][cC][tT][iI][oO][nN]')
    def FUNCTION(self, t):
        return t

    @_(r'[gG][eE][tT]')
    def GET(self, t):
        return t

    @_(r'[gG][oO][sS][uU][bB]')
    def GOSUB(self, t):
        return t

    @_(r'[rR][eE][tT][uU][rR][nN]')
    def RETURN(self, t):
        return t

    @_(r'[gG][oO][tT][oO]')
    def GOTO(self, t):
        return t

    @_(r'[hH][eE][xX]$')
    def HEX_(self, t):
        return t

    @_(r'[iI][fF]')
    def IF(self, t):
        return t

    @_(r'[tT][hH][eE][nN]')
    def THEN(self, t):
        return t

    @_(r'[iI][mM][pP]')
    def IMP(self, t):
        return t

    @_(r'[iI][nN][kK][eE][yY]$')
    def INKEY_(self, t):
        return t

    @_(r'[iI][nN][pP]')
    def INP(self, t):
        return t

    @_(r'[iI][nN][pP][uU][tT]')
    def INPUT(self, t):
        return t

    @_(r'[iI][nN][pP][uU][tT]$')
    def INPUT_(self, t):
        return t

    @_(r'[iI][nN][sS][tT][rR]')
    def INSTR(self, t):
        return t

    @_(r'[iI][nN][tT]')
    def INT(self, t):
        return t

    @_(r'[iI][nN][tT][eE][gG][eE][rR]')
    def INTEGER(self, t):
        return t

    @_(r'[iI][oO][cC][tT][lL]')
    def IOCTL(self, t):
        return t

    @_(r'[iI][oO][cC][tT][lL]$')
    def IOCTL_(self, t):
        return t

    @_(r'[iI][sS]')
    def IS(self, t):
        return t

    @_(r'[kK][eE][yY]')
    def KEY(self, t):
        return t

    @_(r'[kK][iI][lL][lL]')
    def KILL(self, t):
        return t

    @_(r'[lL][bB][oO][uU][nN][dD]')
    def LBOUND(self, t):
        return t

    @_(r'[lL][cC][aA][sS][eE]$')
    def LCASE_(self, t):
        return t

    @_(r'[lL][eE][fF][tT]$')
    def LEFT_(self, t):
        return t

    @_(r'[lL][eE][nN]')
    def LEN(self, t):
        return t

    @_(r'[lL][eE][tT]')
    def LET(self, t):
        return t

    @_(r'[lL][iI][nN][eE]')
    def LINE(self, t):
        return t

    @_(r'[lL][iI][sS][tT]')
    def LIST(self, t):
        return t

    @_(r'[lL][oO][cC]')
    def LOC(self, t):
        return t

    @_(r'[lL][oO][cC][aA][tT][eE]')
    def LOCATE(self, t):
        return t

    @_(r'[lL][oO][cC][kK]')
    def LOCK(self, t):
        return t

    @_(r'[lL][oO][fF]')
    def LOF(self, t):
        return t

    @_(r'[lL][oO][gG]')
    def LOG(self, t):
        return t

    @_(r'[lL][oO][nN][gG]')
    def LONG(self, t):
        return t

    @_(r'[lL][pP][oO][sS]')
    def LPOS(self, t):
        return t

    @_(r'[lL][pP][rR][iI][nN][tT]')
    def LPRINT(self, t):
        return t

    @_(r'[uU][sS][iI][nN][gG]')
    def USING(self, t):
        return t

    @_(r'[lL][sS][eE][tT]')
    def LSET(self, t):
        return t

    @_(r'[lL][tT][rR][iI][mM]$')
    def LTRIM_(self, t):
        return t

    @_(r'[mM][iI][dD]$')
    def MID_(self, t):
        return t

    @_(r'[mM][kK][dD]$')
    def MKD_(self, t):
        return t

    @_(r'[mM][kK][dD][iI][rR]')
    def MKDIR(self, t):
        return t

    @_(r'[mM][kK][dD][mM][bB][fF]$')
    def MKDMBF_(self, t):
        return t

    @_(r'[mM][kK][iI]$')
    def MKI_(self, t):
        return t

    @_(r'[mM][kK][lL]$')
    def MKL_(self, t):
        return t

    @_(r'[mM][kK][sS]$')
    def MKS_(self, t):
        return t

    @_(r'[mM][kK][sS][mM][bB][fF]$')
    def MKSMBF_(self, t):
        return t

    @_(r'[mM][oO][dD]')
    def MOD(self, t):
        return t

    @_(r'[nN][aA][mM][eE]')
    def NAME(self, t):
        return t

    @_(r'[nN][oO][tT]')
    def NOT(self, t):
        return t

    @_(r'[oO][cC][tT]$')
    def OCT_(self, t):
        return t

    @_(r'[oO][fF][fF]')
    def OFF(self, t):
        return t

    @_(r'[oO][nN]')
    def ON(self, t):
        return t

    @_(r'[pP][eE][nN]')
    def PEN(self, t):
        return t

    @_(r'[pP][lL][aA][yY]')
    def PLAY(self, t):
        return t

    @_(r'[sS][tT][rR][iI][gG]')
    def STRIG(self, t):
        return t

    @_(r'[tT][iI][mM][eE][rR]')
    def TIMER(self, t):
        return t

    @_(r'[oO][pP][eE][nN]')
    def OPEN(self, t):
        return t

    @_(r'[oO][pP][tT][iI][oO][nN]')
    def OPTION(self, t):
        return t

    @_(r'[oO][rR]')
    def OR(self, t):
        return t

    @_(r'[oO][uU][tT]')
    def OUT(self, t):
        return t

    @_(r'[oO][uU][tT][pP][uU][tT]')
    def OUTPUT(self, t):
        return t

    @_(r'[pP][aA][iI][nN][tT]')
    def PAINT(self, t):
        return t

    @_(r'[pP][aA][lL][eE][tT][tT][eE]')
    def PALETTE(self, t):
        return t

    @_(r'[pP][cC][oO][pP][yY]')
    def PCOPY(self, t):
        return t

    @_(r'[pP][eE][eE][kK]')
    def PEEK(self, t):
        return t

    @_(r'[pP][mM][aA][pP]')
    def PMAP(self, t):
        return t

    @_(r'[pP][oO][iI][nN][tT]')
    def POINT(self, t):
        return t

    @_(r'[pP][oO][kK][eE]')
    def POKE(self, t):
        return t

    @_(r'[pP][oO][sS]')
    def POS(self, t):
        return t

    @_(r'[pP][rR][eE][sS][eE][tT]')
    def PRESET(self, t):
        return t

    @_(r'[pP][rR][iI][nN][tT]')
    def PRINT(self, t):
        return t

    @_(r'[pP][sS][eE][tT]')
    def PSET(self, t):
        return t

    @_(r'[pP][uU][tT]')
    def PUT(self, t):
        return t

    @_(r'[rR][aA][nN][dD][oO][mM]')
    def RANDOM(self, t):
        return t

    @_(r'[rR][aA][nN][dD][oO][mM][iI][zZ][eE]')
    def RANDOMIZE(self, t):
        return t

    @_(r'[rR][eE][aA][dD]')
    def READ(self, t):
        return t

    @_(r'[rR][eE][dD][iI][mM]')
    def REDIM(self, t):
        return t

    @_(r'[rR][eE][mM]')
    def REM(self, t):
        return t

    @_(r'[rR][eE][sS][eE][tT]')
    def RESET(self, t):
        return t

    @_(r'[rR][eE][sS][tT][oO][rR][eE]')
    def RESTORE(self, t):
        return t

    @_(r'[rR][eE][sS][uU][mM][eE]')
    def RESUME(self, t):
        return t

    @_(r'[rR][iI][gG][hH][tT]$')
    def RIGHT_(self, t):
        return t

    @_(r'[rR][mM][dD][iI][rR]')
    def RMDIR(self, t):
        return t

    @_(r'[rR][nN][dD]')
    def RND(self, t):
        return t

    @_(r'[rR][sS][eE][tT]')
    def RSET(self, t):
        return t

    @_(r'[rR][tT][rR][iI][mM]$')
    def RTRIM_(self, t):
        return t

    @_(r'[rR][uU][nN]')
    def RUN(self, t):
        return t

    @_(r'[sS][cC][rR][eE][eE][nN]')
    def SCREEN(self, t):
        return t

    @_(r'[sS][eE][eE][kK]')
    def SEEK(self, t):
        return t

    @_(r'[sS][eE][lL][eE][cC][tT]')
    def SELECT(self, t):
        return t

    @_(r'[sS][gG][nN]')
    def SGN(self, t):
        return t

    @_(r'[sS][hH][aA][rR][eE][dD]')
    def SHARED(self, t):
        return t

    @_(r'[sS][hH][eE][lL][lL]')
    def SHELL(self, t):
        return t

    @_(r'[sS][iI][nN]')
    def SIN(self, t):
        return t

    @_(r'[sS][iI][nN][gG][lL][eE]')
    def SINGLE(self, t):
        return t

    @_(r'[sS][lL][eE][eE][pP]')
    def SLEEP(self, t):
        return t

    @_(r'[sS][oO][uU][nN][dD]')
    def SOUND(self, t):
        return t

    @_(r'[sS][pP][aA][cC][eE]$')
    def SPACE_(self, t):
        return t

    @_(r'[sS][pP][cC]')
    def SPC(self, t):
        return t

    @_(r'[sS][qQ][rR]')
    def SQR(self, t):
        return t

    @_(r'[sS][tT][aA][tT][iI][cC]')
    def STATIC(self, t):
        return t

    @_(r'[sS][tT][eE][pP]')
    def STEP(self, t):
        return t

    @_(r'[sS][tT][iI][cC][kK]')
    def STICK(self, t):
        return t

    @_(r'[sS][tT][oO][pP]')
    def STOP(self, t):
        return t

    @_(r'[sS][tT][rR]$')
    def STR_(self, t):
        return t

    @_(r'[sS][tT][rR][iI][nN][gG]')
    def STRING(self, t):
        return t

    @_(r'[sS][tT][rR][iI][nN][gG]$')
    def STRING_(self, t):
        return t

    @_(r'[sS][uU][bB]')
    def SUB(self, t):
        return t

    @_(r'[sS][wW][aA][pP]')
    def SWAP(self, t):
        return t

    @_(r'[sS][yY][sS][tT][eE][mM]')
    def SYSTEM(self, t):
        return t

    @_(r'[tT][aA][bB]')
    def TAB(self, t):
        return t

    @_(r'[tT][aA][nN]')
    def TAN(self, t):
        return t

    @_(r'[tT][iI][mM][eE]$')
    def TIME_(self, t):
        return t

    @_(r'[tT][oO]')
    def TO(self, t):
        return t

    @_(r'[tT][rR][oO][fF][fF]')
    def TROFF(self, t):
        return t

    @_(r'[tT][rR][oO][nN]')
    def TRON(self, t):
        return t

    @_(r'[tT][yY][pP][eE]')
    def TYPE(self, t):
        return t

    @_(r'[uU][bB][oO][uU][nN][dD]')
    def UBOUND(self, t):
        return t

    @_(r'[uU][cC][aA][sS][eE]$')
    def UCASE_(self, t):
        return t

    @_(r'[uU][nN][lL][oO][cC][kK]')
    def UNLOCK(self, t):
        return t

    @_(r'[uU][nN][tT][iI][lL]')
    def UNTIL(self, t):
        return t

    @_(r'[vV][aA][lL]')
    def VAL(self, t):
        return t

    @_(r'[vV][aA][rR][pP][tT][rR]')
    def VARPTR(self, t):
        return t

    @_(r'[vV][aA][rR][pP][tT][rR]$')
    def VARPTR_(self, t):
        return t

    @_(r'[vV][aA][rR][sS][eE][gG]')
    def VARSEG(self, t):
        return t

    @_(r'[vV][iI][eE][wW]')
    def VIEW(self, t):
        return t

    @_(r'[wW][aA][iI][tT]')
    def WAIT(self, t):
        return t

    @_(r'[wW][eE][nN][dD]')
    def WEND(self, t):
        return t

    @_(r'[wW][hH][iI][lL][eE]')
    def WHILE(self, t):
        return t

    @_(r'[wW][iI][dD][tT][hH]')
    def WIDTH(self, t):
        return t

    @_(r'[wW][iI][nN][dD][oO][wW]')
    def WINDOW(self, t):
        return t

    @_(r'[wW][rR][iI][tT][eE]')
    def WRITE(self, t):
        return t

    @_(r'[xX][oO][rR]')
    def XOR(self, t):
        return t

    # endregion generated by qbstatic