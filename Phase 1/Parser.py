from ply import yacc
from Lexer import Lexer


class Parser:
    tokens = Lexer().tokens

    precedence = (
        ('left', "LRB", "RRB"),

        ('left', "ELSE"),
        ('left', "IF"),

        ('left', "OR"),
        ('left', "AND"),
        ('left', "NOT"),

        ('left', "GT", "LT", "NE", "EQ", "LE", "GE"),

        ('left', "MOD"),
        ('left', "SUM", "SUB"),
        ('left', "MUL", "DIV"),

        ('left', "INTEGER_KW"),
        ('left', "REAL_KW"),

        ('left', "ID"),
        ('right', "ASSIGN"),

        ("left", "ERROR")
    )

    def __init__(self):
        self.parser = None

    @staticmethod
    def p_program(self, p):
        """program : PROGRAM_KW IDENTIFIER declarations procedure_list compound_statement DOT"""
        print("program : PROGRAM_KW IDENTIFIER declarations procedure_list compound_statement DOT")

    @staticmethod
    def p_declarations(self, p):
        """declarations : VAR_KW declaration_list SEMICOLON
                        | empty"""
        print("declarations : VAR_KW declaration_list SEMICOLON | empty")

    @staticmethod
    def p_declaration_list(self, p):
        """declaration_list : identifier_list  COLON type
               | declaration_list COLON identifier_list  COLON type"""

        print("declaration_list : identifier_list  COLON type|declaration_list COLON identifier_list  COLON type")

    @staticmethod
    def p_identifier_list(self, p):
        """identifier_list : IDENTIFIER
                | identifier_list COMMA IDENTIFIER"""

        print("identifier_list : IDENTIFIER | identifier_list COMMA IDENTIFIER")

    @staticmethod
    def p_type(self, p):
        """type : INTEGER_KW
                | REAL_KW"""
        print("type : INTEGER_KW | REAL_KW")

    @staticmethod
    def p_procedure_list(self, p):
        """procedure_list : procedure_list procedure"""
        print("procedure_list : procedure_list procedure")

    @staticmethod
    def p_procedure(self, p):
        """procedure : PROCEDURE_KW IDENTIFIER parameters COLON declarations compound_statement"""
        print("procedure : PROCEDURE_KW IDENTIFIER parameters COLON declarations compound_statement")

    @staticmethod
    def p_parameters(self, p):
        """paramdec : LRB declaration_list RRB
                    | empty"""
        print("paramdec : LRB declaration_list RRB | empty")

    @staticmethod
    def p_compound_statement(self, p):
        """compound_statement : BEGIN_KW statement_list END_KW"""
        print("compound_statement : BEGIN_KW statement_list END_KW")

    @staticmethod
    def p_statement_list(self, p):
        """statement_list : statement
                          | statement_list COLON statement"""
        print("statement_list : statement  | statement_list COLON statement")

    @staticmethod
    def p_statement(self, p):
        """statement : IDENTIFIER ASSIGN expression
                     | IF_KW expression THEN_KW statement ELSE_KW statement
                     | IF_KW expression THEN_KW statement
                     | WHILE_KW expression DO_KW statement
                     | compound_statement
                     | IDENTIFIER arguments
                     | empty"""
        print("""statement : IDENTIFIER ASSIGN expression
                     | IF_KW expression THEN_KW statement ELSE_KW statement
                     | IF_KW expression THEN_KW statement
                     | WHILE_KW expression DO_KW statement
                     | compound_statement
                     | IDENTIFIER arguments
                     | empty""")

    @staticmethod
    def p_arguments(self, p):
        """arguments : LRB actual_parameter_list RRB"""
        print("arguments : LRB actual_parameter_list RRB")

    @staticmethod
    def p_actual_parameter_list(self, p):
        """actual_parameter_list : actual_parameter_list COMMA actual_parameter
                                 | actual_parameter"""
        print("""actual_parameter_list : actual_parameter_list COMMA actual_parameter
                                 | actual_parameter""")

    @staticmethod
    def p_actual_parameter(self, p):
        """actual_parameter : expression | IDENTIFIER"""
        print("actual_parameter : expression | IDENTIFIER")

    @staticmethod
    def p_empty(self, p):
        """empty :"""
        print("empty")
        pass

    @staticmethod
    def p_error(self, p):
        print("Error", p.type, p.lexpos)

    def build(self, **kwargs):
        self.parser = yacc.yacc(module=self, **kwargs)
        return self.parser
