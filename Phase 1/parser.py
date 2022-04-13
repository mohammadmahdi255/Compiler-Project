from ply import yacc
from lexer import Lexer


class Parser:
    tokens = Lexer().tokens

    precedence = (
        ('left', "LRB", "RRB"),

        ('left', "THEN_KW", "ELSE_KW"),
        ('left', "IF_KW"),

        ('left', "OR_KW"),
        ('left', "AND_KW"),
        ('left', "NOT_KW"),

        ('left', "GT", "LT", "NE", "EQ", "LE", "GE"),

        ('left', "MOD_KW"),
        ('left', "SUM", "SUB"),
        ('left', "MUL", "DIV", 'DIV_KW'),

        ('left', "INTEGER_KW"),
        ('left', "REAL_KW"),


        ('left', "IDENTIFIER"),
        ('right', "ASSIGN"),

        ("left", "ERROR")
    )

    def __init__(self):
        # self.parser = None
        pass

    def p_program(self, p):
        """program : PROGRAM_KW IDENTIFIER declarations procedure_list compound_statement DOT"""
        print("program : PROGRAM_KW IDENTIFIER declarations procedure_list compound_statement DOT")

    def p_declarations(self, p):
        """declarations : VAR_KW declaration_list SEMICOLON
                        | empty"""
        print("declarations : VAR_KW declaration_list SEMICOLON | empty")

    def p_declaration_list(self, p):
        """declaration_list : identifier_list  COLON type
               | declaration_list SEMICOLON identifier_list  COLON type"""

        print("declaration_list : identifier_list  COLON type|declaration_list COLON identifier_list  COLON type")

    def p_identifier_list(self, p):
        """identifier_list : IDENTIFIER
                | identifier_list COMMA IDENTIFIER"""

        print("identifier_list : IDENTIFIER | identifier_list COMMA IDENTIFIER")

    def p_type(self, p):
        """type : INTEGER_KW
                | REAL_KW"""
        print("type : INTEGER_KW | REAL_KW")

    def p_procedure_list(self, p):
        """procedure_list : procedure_list procedure
                          | empty"""
        print("procedure_list : procedure_list procedure | empty")

    def p_procedure(self, p):
        """procedure : PROCEDURE_KW IDENTIFIER parameters COLON declarations compound_statement"""
        print("procedure : PROCEDURE_KW IDENTIFIER parameters COLON declarations compound_statement")

    def p_parameters(self, p):
        """parameters : LRB declaration_list RRB"""
        print("parameters : LRB declaration_list RRB")

    def p_compound_statement(self, p):
        """compound_statement : BEGIN_KW statement_list END_KW"""
        print("compound_statement : BEGIN_KW statement_list END_KW")

    def p_statement_list(self, p):
        """statement_list : statement
                     | statement_list COLON statement"""
        print("statement_list : statement  | statement_list COLON statement")

    def p_statement(self, p):
        """statement : IDENTIFIER ASSIGN expression
                     | IF_KW expression THEN_KW statement ELSE_KW
                     | IF_KW expression THEN_KW
                     | WHILE_KW expression DO_KW statement
                     | compound_statement
                     | IDENTIFIER arguments
                     | empty"""
        print("statement : IDENTIFIER ASSIGN expression | IF_KW expression THEN_KW statement ELSE_KW | IF_KW expression THEN_KW | WHILE_KW expression DO_KW statement | compound_statement | IDENTIFIER arguments |empty")

    def p_arguments(self, p):
        """arguments : LRB actual_parameter_list RRB
                     | empty"""
        print("arguments : LRB actual_parameter_list RRB | empty")

    def p_actual_parameter_list(self, p):
        """actual_parameter_list : actual_parameter_list COMMA actual_parameter
                     | actual_parameter"""
        print("actual_parameter_list : actual_parameter_list COMMA actual_parameter | actual_parameter")

    def p_actual_parameter(self, p):
        """actual_parameter : expression
                     | IDENTIFIER"""
        print("actual_parameter : expression | IDENTIFIER")

    def p_expression(self, p):
        """expression : INTEGER_CONSTANT
               | REAL_CONSTANT
               | IDENTIFIER
               | expression SUM expression
               | expression SUB expression
               | expression MUL expression
               | expression DIV expression
               | SUB expression
               | expression DIV_KW expression
               | expression MOD_KW expression
               | expression LT expression
               | expression LE expression
               | expression EQ expression
               | expression NE expression
               | expression GT expression
               | expression GE expression
               | expression AND_KW expression
               | expression OR_KW expression
               | NOT_KW expression
               | LRB expression RRB"""
        print("expression : INTEGER_CONSTANT | REAL_CONSTANT | IDENTIFIER | expression SUM expression | expression SUB expression | expression MUL expression | expression DIV expression | SUB expression | expression DIV_KW expression | expression MOD_KW expression | expression LT expression | expression LE expression | expression EQ expression | expression NE expression | expression GT expression | expression GE expression | expression AND_KW expression | expression OR_KW expression | NOT_KW expression | LRB expression RRB")

    def p_empty(self, p):
        """empty :"""
        print("empty")
        pass

    def p_error(self, p):
        print("Error", p.type, p.lexpos)

    def build(self, **kwargs):
        self.parser = yacc.yacc(module=self, **kwargs)
        return self.parser