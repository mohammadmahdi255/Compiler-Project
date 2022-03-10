from ply import lex


class Lexer:
    reserved = {
        'IF_KW': r'if',
        'THEN_KW': r'then',
        'ELSE_KW': r'else',
        'WHILE_KW': r'while',
        'DO_KW': r'do',
    }

    tokens = [
        "PROGRAM_KW", "VAR_KW", "EMPTY", "INTEGER_KW",
        "REAL_KW", "PROCEDURE_KW", "BEGIN_KW", "END_KW",
        "IDENTIFIER", "INTEGER_CONSTANT","REAL_CONSTANT",
        "SUM_KW", "SUB_KW", "MUL_KW","DIV_KW", "MOD_KW",
        "LT_KW", "LE_KW", "EQ_KW", "NE_KW", "GT_KW", "GE_KW",
        "AND_KW", "OR_KW", "NOT_KW", "LRB_KW", "RRB_KW", "SEMICOLON",
    ] + list(reserved.keys())

    # COLONS
    t_SEMICOLON = r'\;'

    # BRACKETS
    t_LRB_KW = r'\('
    t_RRB_KW = r'\)'

    # OPERATORS
    t_SUM_KW = r'\+'
    t_SUB_KW = r'\-'
    t_MUL_KW = r'\*'
    t_DIV_KW = r'\/'
    t_MOD_KW = r'\%'
    t_LT_KW = r'\<'
    t_LE_KW = r'\<='
    t_EQ_KW = r'\='
    t_NE_KW = r'\<>'
    t_GT_KW = r'\>'
    t_GE_KW = r'\>='

    # RESERVE KW

    t_IF_KW = r'\if'
    t_THEN_KW = r'\then'
    t_ELSE_KW = r'\else'
    t_WHILE_KW = r'\while'
    t_DO_KW = r'\do'

    def t_INTEGER_CONSTANT(self):
        r'[-|+]?(\d+)'
        return self

    # Error handling rule
    def t_error(self):
        print("Illegal character '%s'" % self)
        self.lexer.skip(1)

    # Build the lexer
    lexer = lex.lex()
