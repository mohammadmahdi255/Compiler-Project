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
                 "COLON", "COMMA", "DOT", "COMMENT", "ERROR"
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

    # RESERVE KW
    t_IF_KW = r'if'
    t_THEN_KW = r'then'
    t_ELSE_KW = r'else'

    t_WHILE_KW = r'while'
    t_DO_KW = r'do'

    t_INTEGER_KW = r'integer'
    t_REAL_KW = r'real'

    t_MOD_KW = r'mod'
    t_DIV_KW = r'div'
    t_VAR_KW = r'var'
    t_PROCEDURE_KW = r'procedure'
    t_FUNCTION_KW = r'function'

    t_AND_KW = r'and'
    t_OR_KW = r'or'
    t_NOT_KW = r'not'
    t_BEGIN_KW = r'begin'
    t_END_KW = r'end'

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

    # @staticmethod
    # def t_COMMENT_MULTI_LINE(t):
    #     r"""\/{2}.*"""
    #     pass

    @staticmethod
    def t_COMMENT(t):
        r"""\/{2}.*"""
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
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    def __init__(self, **kwargs):
        self.lexer = self.__build(**kwargs)
        self.token_list = []

    # Build the lexer
    def __build(self, **kwargs):
        return lex(module=self, **kwargs)

    # Input text for lexer
    def input(self, text):
        self.lexer.input(text)

    # Returns all tokens
    def get_tokens(self):
        token = ''
        while token is not None:
            token = self.lexer.token()
            self.token_list.append(token)
        return self.token_list[:-1]
