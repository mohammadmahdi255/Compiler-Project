from ply.lex import lex


class Lexer:
    reserved = {
        r'program': 'PROGRAM_KW',

        r'if': 'IF_KW',
        r'then': 'THEN_KW',
        r'else': 'ELSE_KW',

        r'while': 'WHILE_KW',
        r'do': 'DO_KW',

        r'integer': 'INTEGER_KW',
        r'real': 'REAL_KW',

        r'mod': 'MOD_KW',
        r'procedure': 'PROCEDURE_KW',
        r'var': 'VAR_KW',
        r'div': 'DIV_KW',
        r'function': 'FUNCTION_KW',

        r'and': 'AND_KW',
        r'or': 'OR_KW',
        r'not': 'NOT_KW',
        r'begin': 'BEGIN_KW',
        r'end': 'END_KW'
    }

    tokens = [
                 "INTEGER_CONSTANT", "REAL_CONSTANT", "IDENTIFIER",
                 "SUM", "SUB", "MUL", "DIV", "POINT", "SIGN", "LT", "LE",
                 "EQ", "NE", "GT", "GE", "LRB", "RRB",
                 "ASSIGN", "SEMICOLON", "COLON", "COMMA", "DOT"
             ] + list(reserved.values())

    # COLONS
    t_SEMICOLON = r';'
    t_COLON = r':'
    t_COMMA = r','
    t_DOT = r'.'

    # OPERATORS
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

    # BRACKETS
    t_LRB = r'\('
    t_RRB = r'\)'

    # RESERVE KW
    t_IF_KW = r'if'
    t_THEN_KW = r'then'
    t_ELSE_KW = r'else'
    t_WHILE_KW = r'while'
    t_DO_KW = r'do'

    # A string containing ignored characters (spaces and tabs)
    t_ignore = '\n \t'

    @staticmethod
    def t_ERROR(t):
        r"""[0-9]+[a-z_A-Z][a-zA-Z_0-9]*"""
        return t

    @staticmethod
    def t_newline(t):
        r"""\n+"""
        t.lexer.lineno += len(t.value)

    @staticmethod
    def t_REAL_CONSTANT(t):
        r"""[0-9]*\.[0-9]+"""
        t.value = float(t.value)
        return t

    @staticmethod
    def t_INTEGER_CONSTANT(t):
        r"""(\d+)"""
        t.value = int(t.value)
        return t

    def t_IDENTIFIER(self, t):
        r"""[_a-zA-Z][_a-zA-Z0-9]*"""
        if t.value in self.reserved:
            t.type = self.reserved[t.value]
        return t

    # Error handling rule
    def t_error(self, t):
        raise Exception('Error at', t.value)

    def __init__(self, **kwargs):
        self.lexer = self.__build(**kwargs)
        self.token_list = []

    # Build the lexer
    def __build(self, **kwargs):
        return lex(module=self, **kwargs)

    def input(self, text):
        self.lexer.input(text)

    def get_tokens(self):
        token = ''
        while token is not None:
            token = self.lexer.token()
            self.token_list.append(token)
        return self.token_list[:-1]
