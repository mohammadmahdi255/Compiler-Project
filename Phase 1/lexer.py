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
                 "ASSIGN", "SEMICOLON", "COLON", "COMMA",
             ] + list(reserved.values())

    # COLONS
    t_SEMICOLON = r'\;'

    # BRACKETS
    t_LRB = r'\('
    t_RRB = r'\)'

    # OPERATORS
    t_MUL = r'\*'
    t_DIV = r'\/'
    t_LT = r'\<'
    t_LE = r'\<='
    t_EQ = r'\='
    t_NE = r'\<>'
    t_GT = r'\>'
    t_GE = r'\>='

    # RESERVE KW
    t_IF_KW = r'if'
    t_THEN_KW = r'then'
    t_ELSE_KW = r'else'
    t_WHILE_KW = r'while'
    t_DO_KW = r'do'

    # A string containing ignored characters (spaces and tabs)
    t_ignore = '\n \t'

    @staticmethod
    def t_SIGN(t):
        r"""[-|+][-|+|\s]*"""
        if str(t.value).count('-') % 2 == 0:
            t.type = 'SUM'
            t.value = '+'
        else:
            t.type = 'SUB'
            t.value = '-'
        return t

    def t_REAL_CONSTANT(self, t):
        r"""[\d]+\.[\d]*"""
        t.value = str(t.value).strip('0')
        if t.value[-1] == '.':
            t.value += '0'
        if t.value[0] == '.':
            t.value = '0' + t.value
        return self.__update_token(t)

    # INTEGER REGULAR EXPRESSION
    def t_INTEGER_CONSTANT(self, t):
        r"""[\d]+"""
        t.value = str(t.value).lstrip('0')
        if t.value == '':
            t.value = '0'
        return self.__update_token(t)

    # Define a rule so we can track line numbers
    @staticmethod
    def t_newline(t):
        r"""\n+"""
        t.lexer.lineno += len(t.value)

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

    def input(self, text):
        self.lexer.input(text)

    def get_tokens(self):
        token = ''
        while token is not None:
            valid, token = self.__token()
            if valid:
                self.token_list.append(token)
        return self.token_list[:-1]

    def __token(self):
        token = self.lexer.token()

        if token is None:
            return True, token

        return True, token

    def __update_token(self, t):
        try:
            token = self.token_list.pop()
            if token in ['SUM', 'SUB'] and (
                    len(self.token_list) == 0 or self.token_list[-1].type != 'INTEGER_CONSTANT'):
                if self.token_list[-1].type == 'SUB':
                    t.value = "-" + t.value
            else:
                self.token_list.append(token)
        except IndexError:
            pass
        finally:
            return t
