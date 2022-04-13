from ply import lex

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

        r'div': 'DIV_KW',
        r'mod': 'MOD_KW',
        r'var': 'VAR_KW',
        r'procedure': 'PROCEDURE_KW',
        r'function': 'FUNCTION_KW',

        r'and': 'AND_KW',
        r'or': 'OR_KW',
        r'not': 'NOT_KW',
        r'begin': 'BEGIN_KW',
        r'end': 'END_KW'
    }

    tokens = [
                 "INTEGER_CONSTANT", "REAL_CONSTANT", "IDENTIFIER",
                 "SUM", "SUB", "MUL", "DIV", "ASSIGN", "LT", "LE",
                 "EQ", "NE", "GT", "GE", "LRB", "RRB", "SEMICOLON",
                 "COLON", "COMMA", "DOT", "ERROR"
             ] + list(reserved.values())

    # OPERATORS
    t_SUM = r'\+'
    t_SUB = r'\-'
    t_MUL = r'\*'
    t_DIV = r'/'
    t_ASSIGN = r':='
    t_LT = r'<'
    t_LE = r'<='
    t_EQ = r'='
    t_NE = r'<>'
    t_GT = r'>'
    t_GE = r'>='

    # BRACKETS
    t_LRB = r'\('
    t_RRB = r'\)'

    # COLONS
    t_SEMICOLON = r';'
    t_COLON = r':'
    t_COMMA = r','
    t_DOT = r'\.'


    # A string containing ignored characters (spaces and tabs)
    t_ignore = ' \t'

    @staticmethod
    def t_ERROR(t):
        r"""\d+[_|a-z|A-Z]\w*"""
        return t

    @staticmethod
    def t_newline(t):
        r"""\n+"""
        t.lexer.lineno += len(t.value)
        pass


    @staticmethod
    def t_REAL_CONSTANT(t):
        r"""\d+\.\d*"""
        t.value = float(t.value)
        return t

    @staticmethod
    def t_INTEGER_CONSTANT(t):
        r"""\d+"""
        t.value = int(t.value)
        return t

    def t_IDENTIFIER(self, t):
        r"""[_|a-z|A-Z]\w*"""
        t.type = self.reserved.get(t.value, 'IDENTIFIER')
        return t

    # Error handling rule
    @staticmethod
    def t_error(t):
        raise Exception("Illegal character '%s'" % t.value[0])

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)
        return self.lexer
