from ply import lex


class Lexer:

    tokens = [
        "PROGRAM_KW", "VAR_KW", "INTEGER_KW",
        "REAL_KW", "PROCEDURE_KW", "BEGIN_KW", "END_KW",
        "IF_KW", "THEN_KW", "ELSE_KW", "WHILE_KW",
        "DO_KW", "IDENTIFIER", "INTEGER_CONSTANT",
        "REAL_CONSTANT", "SUM", "SUB", "MUL", "DIV",
        "DIV_KW", "MOD_KW", "LT", "LE",
        "EQ", "NE", "GT", "GE", "AND_KW",
        "OR_KW", "NOT_KW", "LRB", "RRB",
        "ASSIGN", "FUNCTION_KW", "SEMICOLON", "COLON", "COMMA", "DOT","ERROR",
    ]
    reserved = {
        'program': 'PROGRAM_KW',

        'if': 'IF_KW',
        'then': 'THEN_KW',
        'else': 'ELSE_KW',

        'while': 'WHILE_KW',
        'do': 'DO_KW',

        'integer': 'INTEGER_KW',
        'real': 'REAL_KW',

        'mod': 'MOD_KW',
        'procedure': 'PROCEDURE_KW',
        'var': 'VAR_KW',
        'div': 'DIV_KW',
        'function': 'FUNCTION_KW',

        'and': 'AND_KW',
        'or': 'OR_KW',
        'not': 'NOT_KW',
        'begin': 'BEGIN_KW',
        'end': 'END_KW'
    }
    t_SEMICOLON = r';'
    t_COLON = r':'
    t_COMMA = r','
    t_DOT = r'.'

    t_MUL = r'\*'
    t_DIV = r'/'
    t_SUM = r'\+'
    t_SUB = r'\-'
    t_ASSIGN = r':='
    t_EQ = r'='
    t_GT = r'>'
    t_GE = r'>='
    t_LT = r'<'
    t_LE = r'<='
    t_NE = r'<>'

    t_LRB = r'\('
    t_RRB = r'\)'
    def t_ERROR(self, t):
        r'[0-9]+[a-z_A-Z][a-zA-Z_0-9]*'
        return t
    
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    t_ignore = '\n \t'

    def t_REAL_CONSTANT(self, t):
        r'[0-9]*\.[0-9]+'
        t.value = float(t.value)
        return t

    def t_INTEGER_CONSTANT(self, t):
        r'(\d+)'
        t.value = int(t.value)
        return t

    def t_IDENTIFIER(self, t):
        r'[_a-zA-Z][_a-zA-Z0-9]*'
        if t.value in self.reserved:
            t.type = self.reserved[t.value]
        return t

    # Error handling rule
    def t_error(self, t):
        raise Exception('Error at', t.value)

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)
        return self.lexer

