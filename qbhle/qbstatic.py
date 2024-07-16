import copy
from logging import getLogger
import os
import sys

from collections import OrderedDict

logger = getLogger(__name__)

MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
REPO_DIR = os.path.dirname(MODULE_DIR)

if __name__ == "__main__":
    sys.path.insert(0, REPO_DIR)

from qb_1_1 import HELP_INDEX_QB_1_1

# TODO: Boolean Operators: https://www.qbasic.net/en/reference/qb11/Operators/Boolean.htm
# TODO: Declaring User Defined Keys: https://www.qbasic.net/en/reference/qb11/User-Defined-Keys/Declaring.htm
# TODO: Data Type Keyword
# TODO: DEFtype Statements
# TODO: OPEN Statement File Modes: https://www.qbasic.net/en/reference/qb11/File-Modes/OPEN-Statement.htm

# ERDEV:
# https://www.qbasic.net/en/reference/qb11/Function/ERDEV.htm
# The low byte of the value returned by ERDEV contains the DOS error code. The high byte contains device-attribute information.


def to_ci_regex(s):
    result = ""
    for c in s:
        if c == "#":
            result += r'\#'  # escaped as per SLY documentation.
        elif not c.isalpha():
            result += c
            continue
        result += "[{}{}]".format(c.lower(), c.upper())
    return result


class QBStatic:
    BUILTIN_SYMBOL_TYPES = ["Function", "Keyword", "Operator", "Statement"]
    BUILTIN_TOKEN_ROLES = ["NAME", "KEYWORD", "BOOLEAN_OPERATOR", "ARITHMETIC_OPERATOR", "STATEMENT"]
    BUILTIN_ARITHMETIC_OPS = ("MOD",)  # The rest are binary!
    # {'<>', '>=', '<=', '<', '>', '=', '(', ')', '^'}
    # '$', '%', '&', '!', '#'}  # type decorator suffixes (See TYPE_SUFFIX_*)
    TYPE_SUFFIXES = {
        '$': "STRING",
        '%': "SHORT",
        '&': "LONG",
        '!': "SINGLE",
        '#': "DOUBLE",
    }

    def get_line_meta(self, line):
        d_open_start = line.find("(")
        meta = {}
        old_line = line
        if d_open_start >= 0:
            d_open_end = line.find(")", d_open_start)
            if d_open_end < 0:
                raise ValueError("No ending ')' in {}".format(line))
            meta['note'] = line[d_open_start+1:d_open_end]
            line = (line[:d_open_start].strip() + " "
                    + line[d_open_end+1:].strip())
        last_space_i = line.rfind(" ")
        if last_space_i < 0:
            raise ValueError(
                "Missing space and role."
                " Expected space then any of: {} after: `{}` in `{}`"
                .format(QBStatic.BUILTIN_SYMBOL_TYPES, line, old_line))
        meta['role'] = line[last_space_i+1:].strip()  # such as "Function"
        _statement = line[:last_space_i].strip()
        del last_space_i
        meta['phrases'] = _statement.split("...")
        meta['symbols'] = []
        for phrase in meta['phrases']:
            meta['symbols'] += phrase.split()  # += since RValue is a list

        return meta

    def __init__(self):
        # self.symbol_indices = {}
        self.symbol_metas = OrderedDict()
        self.arithmetic_ops = OrderedDict()
        self.boolean_ops = OrderedDict()

        token_metas = []
        _lines = HELP_INDEX_QB_1_1.split("\n")
        known_roles = {}
        for rawl in _lines:
            line = rawl.strip()
            if not line:
                continue
            meta = self.get_line_meta(line)
            if len(meta['symbols']) == 1:
                if meta['symbols'][0] not in known_roles:
                    known_roles[meta['symbols'][0]] = meta['role']
            # else multi-symbol statements could have
            #   keywords etc that are defined elsewhere
            #   (earlier or later in the list).

        suffixes = ""
        for suffix in QBStatic.TYPE_SUFFIXES.keys():
            suffixes += suffix
        # suffixes_re = r'['+suffixes']'
        line_n = 0
        for rawl in _lines:
            line_n += 1  # Counting numbers start at 1.
            line = rawl.strip()
            if not line:
                continue
            meta = self.get_line_meta(line)
            token_metas.append(meta)
            # NOTE: Avoid 'token' since there is context-based
            #   behavior for most of these, & adding a handler
            #   for each will be faster anyway.
            if meta['role'] == "Function":
                # meta['token'] = "NAME"
                pass
            elif meta['role'] == "Operator":
                if meta['role'] in QBStatic.BUILTIN_ARITHMETIC_OPS:
                    meta['role'] = "ARITHMETIC_OPERATOR"
                else:
                    meta['role'] = "BOOLEAN_OPERATOR"
                    # 'token' is the python constant
                    # 'symbol' is the actual word
            elif meta['role'] == "Statement":
                # meta['token'] = "NAME"
                pass
            elif meta['role'] == "Keyword":
                # meta['token'] = "NAME"
                pass
            else:
                # if token['token'] not in QBStatic.BUILTIN_SYMBOL_TYPES:
                raise ValueError(
                    "Not in BUILTIN_SYMBOL_TYPES: {}".format(meta['roles']))

            for raw_symbol in meta['symbols']:
                # token = symbol.replace("$", "_")
                # symbol = raw_symbol.rstrip(suffixes)
                symbol = raw_symbol  # allow suffix as part of token

                # if symbol in SYMBOLS:
                #     continue
                # SYMBOLS.append(symbol)
                # SYMBOL_INDICES[symbol] = index
                # .replace(" ", "_")
                if symbol in self.symbol_metas:
                    # Must have already gotten one without suffixes
                    logger.warning("Skipping redundant {}".format(line))
                    continue
                # self.symbol_indices[symbol] = index

                # 'symbol' is the actual word--
                # 'token' is the Python constant:
                token = symbol.rstrip(suffixes)
                if token != symbol:
                    token += "_" * (len(symbol) - len(token))
                self.symbol_metas[symbol] = copy.deepcopy(meta)
                self.symbol_metas[symbol]['token'] = token
                if meta['role'] == "ARITHMETIC_OPERATOR":
                    if len(meta['symbols']) > 1:
                        raise NotImplementedError(
                            "Got more than one symbol for operator: {}"
                            .format(line))
                    self.arithmetic_ops[symbol] = self.symbol_metas[symbol]
                elif meta['role'] == "BOOLEAN_OPERATOR":
                    if len(meta['symbols']) > 1:
                        raise NotImplementedError(
                            "Got more than one symbol for operator: {}"
                            .format(line))
                    self.boolean_ops[symbol] = self.symbol_metas[symbol]


qbstatic = QBStatic()

if __name__ == "__main__":
    indent = "    "
    indent2 = indent + "    "
    print(indent+"# region generated by qbstatic")
    print(indent+"tokens = {")
    print(indent2+"ID,")  # Use ID for symbol as NAME itself is a statement!
    print(indent2+"LITERAL,")
    print(indent2+"NUMBER,")
    print(indent2+"STRING_LITERAL,")
    print(indent2+"PLUS,")
    print(indent2+"MINUS,")
    print(indent2+"TIMES,")
    print(indent2+"DIVIDE,")
    # TODO: INTEGER DIVISION:
    print(indent2+"IDIVIDE,")
    print(indent2+"MODULUS,")  # 10 MOD 3 is 1
    print(indent2+"CARET,")
    print(indent2+"LPAREN,")
    print(indent2+"RPAREN,")
    print(indent2+"COMMA,")
    # 2-character ones *must* come 1st if 1st char has it's own meaning:
    print(indent2+"NE,")
    print(indent2+"LE,")
    print(indent2+"LT,")
    print(indent2+"GE,")
    print(indent2+"GT,")
    print(indent2+"EQ,")  # Same as ASSIGN in QB (depends on context)
    print(indent2+"SEMI,")  # The flush character (also adds "?" to INPUT)

    done_tokens = set()
    prev_letter = None
    comment = ""
    for symbol, meta in (qbstatic.symbol_metas.items()):
        if symbol in done_tokens:
            continue
        done_tokens.add(symbol)
        token = meta.get('token')
        if not token:
            raise ValueError(
                "Token (Python constant) was not calculated.")
        if " " in symbol:
            raise ValueError(
                "Command with space was not split into tokens: \"{}\""
                .format(symbol))
        if "$" in token:
            raise ValueError(
                "A token was not made into a Python constant: \"{}\""
                .format(token))
        is_on_new_line = False
        newline = ""
        if (token[0] != prev_letter) or comment:
            if prev_letter:
                newline = "\n"
            # Also newline after comment so code won't be commented!
            sys.stdout.write(newline + indent + "   ")  # 7 since space is added below
            sys.stdout.flush()
            comment = ""
        if "OPERATOR" in meta['role'].upper():
            if not newline:
                sys.stdout.write("\n" + indent + "   ")  # 7 since space is added below
                sys.stdout.flush()
            comment = "  # " + meta['role']
        # else:
        #     comment = ""
        prev_letter = token[0]
        sys.stdout.write(" " + token + "," + comment)
    print("\n" + indent + "}")
    # NAME[] notation is *only* necessary when regex for NAME should
    #   *not* be NAME.
    #   - In other cases, the regex passed to the underscore decorator
    #     matches the handler to the symbol:
    print(indent+"# endregion generated by qbstatic")
    print(indent+"# region generated by qbstatic")
    print()
    for symbol, meta in qbstatic.symbol_metas.items():
        token = meta['token']
        # if token != symbol:
        #     print(indent+"{}['{}'] = {}".format(token, symbol, token))
        print(indent+"@_(r'{}')".format(to_ci_regex(symbol)))
        print(indent+"def {}(self, t):".format(token))
        # print(indent2+"print('{} is not implemented.', file=sys.stderr)"
        #       .format(symbol))
        if token.upper() == "REM":
            print(indent2+"# no return (ignore the comment)")
            print(indent2+"pass")
        else:
            print(indent2+"return t")
        print()

    # print(indent+"ignore = ' \t'")

    print(indent+"# endregion generated by qbstatic")
