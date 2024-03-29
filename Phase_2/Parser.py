from ply import yacc
from Phase_1.Lexer import Lexer


class Parser:
    reserved = Lexer().reserved
    tokens = Lexer().tokens

    precedence = (
        ('right', "PROCEDURE_KW", "FUNCTION_KW"),

        ('left', "SEMICOLON"),
        ('left', "IDENTIFIER"),

        ('left', "THEN_KW"),
        ('left', "IF_KW", "ELSE_KW"),

        ('right', "ASSIGN"),

        ('left', "REAL_KW"),
        ('left', "INTEGER_KW"),

        ('left', "OR_KW"),
        ('left', "AND_KW"),
        ('left', "NOT_KW"),

        ('left', "GT", "LT", "NE", "EQ", "LE", "GE"),

        ('left', "SUM", "SUB"),
        ('left', "MUL", "DIV", "DIV_KW", "MOD_KW"),

        ('left', "LRB", "RRB"),
    )

    @staticmethod
    def p_program(p):
        """program : PROGRAM_KW IDENTIFIER declarations procedure_list compound_statement DOT"""
        print("program : PROGRAM_KW IDENTIFIER declarations procedure_list compound_statement DOT")

    def p_declarations(self, p):
        """declarations : VAR_KW declaration_list SEMICOLON
                        | empty"""
        print("declarations : VAR_KW declaration_list SEMICOLON | empty")
        self.p = p
        print(p.stack)
        print(p.slice)
        text = ""
        for i in p.slice:
            text += str(i) + " "
        print(text)
        print()

    @staticmethod
    def p_declaration_list(p):
        """declaration_list : identifier_list COLON type
               | declaration_list SEMICOLON identifier_list COLON type"""

        print("declaration_list : identifier_list COLON type | declaration_list COLON identifier_list COLON type")
        print(p.stack)
        print(p.slice)
        text = ""
        for i in p.slice:
            text += str(i) + " "
        print(text)
        print()

    @staticmethod
    def p_identifier_list(p):
        """identifier_list : IDENTIFIER
                | identifier_list COMMA IDENTIFIER"""
        print("identifier_list : IDENTIFIER | identifier_list COMMA IDENTIFIER")
        print(p.stack)
        print(p.slice)
        text = ""
        for i in p.slice:
            text += str(i) + " "
        print(text)
        print()

    @staticmethod
    def p_type(p):
        """type : INTEGER_KW
                | REAL_KW"""
        print("type : INTEGER_KW | REAL_KW")
        print(p.stack)
        print(p.slice)
        text = ""
        for i in p.slice:
            text += str(i) + " "
        print(text)
        print()

    @staticmethod
    def p_procedure_list(p):
        """procedure_list : procedure_list procedure
                          | procedure_list function
                          | empty"""
        print("""procedure_list : procedure_list procedure
               | procedure_list function
               | empty""")
        print(p.stack)
        print(p.slice)
        text = ""
        for i in p.slice:
            text += str(i) + " "
        print(text)
        print()

    @staticmethod
    def p_procedure(p):
        """procedure : PROCEDURE_KW IDENTIFIER parameters SEMICOLON declarations compound_statement SEMICOLON"""
        print("procedure : PROCEDURE_KW IDENTIFIER parameters SEMICOLON declarations compound_statement")

    @staticmethod
    def p_function(p):
        """function : FUNCTION_KW IDENTIFIER parameters COLON type SEMICOLON declarations compound_statement SEMICOLON"""
        print("procedure : PROCEDURE_KW IDENTIFIER parameters COLON declarations compound_statement")

    @staticmethod
    def p_parameters(p):
        """parameters : LRB declaration_list RRB
                    | empty"""
        print("parameters : LRB declaration_list RRB | empty")
        print(p.stack)
        print(p.slice)
        text = ""
        for i in p.slice:
            text += str(i) + " "
        print(text)
        print()

    @staticmethod
    def p_compound_statement(p):
        """compound_statement : BEGIN_KW statement_list END_KW"""
        print("compound_statement : BEGIN_KW statement_list END_KW")
        print(p.stack)
        print(p.slice)
        text = ""
        for i in p.slice:
            text += str(i) + " "
        print(text)
        print()

    @staticmethod
    def p_statement_list(p):
        """statement_list : statement
                          | statement_list SEMICOLON statement"""
        print("statement_list : statement  | statement_list COLON statement")
        print(p.stack)
        print(p.slice)
        text = ""
        for i in p.slice:
            text += str(i) + " "
        print(text)
        print()

    # should check this !!!!!!!!!!!!!!!!
    @staticmethod
    def p_statement(p):
        """statement : IDENTIFIER ASSIGN expression
                     | IF_KW expression THEN_KW statement ELSE_KW statement
                     | IF_KW expression THEN_KW statement
                     | WHILE_KW expression DO_KW statement
                     | compound_statement
                     | IDENTIFIER arguments
                     | empty"""
        print("""statement :""")
        print(p.stack)
        print(p.slice)
        text = ""
        for i in p.slice:
            text += str(i) + " "
        print(text)
        print()


    @staticmethod
    def p_arguments(p):
        """arguments : LRB actual_parameter_list RRB"""
        print("arguments : LRB actual_parameter_list RRB")
        print(p.stack)
        print(p.slice)
        text = ""
        for i in p.slice:
            text += str(i) + " "
        print(text)
        print()

    @staticmethod
    def p_actual_parameter_list(p):
        """actual_parameter_list : actual_parameter_list COMMA actual_parameter
                                 | actual_parameter"""
        print("""actual_parameter_list : actual_parameter_list COMMA actual_parameter
                                 | actual_parameter""")
        print(p.stack)
        print(p.slice)
        text = ""
        for i in p.slice:
            text += str(i) + " "
        print(text)
        print()

    @staticmethod
    def p_actual_parameter(p):
        """actual_parameter : expression"""
        print("actual_parameter : expression")
        print(p.stack)
        print(p.slice)
        text = ""
        for i in p.slice:
            text += str(i) + " "
        print(text)
        print()

    @staticmethod
    def p_expression(p):
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
                      | LRB expression RRB
                      """
        print("""expression""")
        print(p.stack)
        print(p.slice)
        text = ""
        for i in p.slice:
            text += str(i) + " "
        print(text)
        print()

    @staticmethod
    def p_empty(p):
        """empty :"""
        print("empty")
        print(p.stack)
        print(p.slice)
        text = ""
        for i in p.slice:
            text += str(i) + " "
        print(text)
        print()
        pass

    def p_error(self, p):
        print("Error", p.type, p.lexpos)
        print(p)
        if self.p is not None:
            print(self.p.stack)
            print(self.p.slice)
            text = ""
            for i in self.p.slice:
                text += str(i) + " "
            print(text)
        print()

    def __init__(self):
        self.parser = None
        self.p = None

    def build(self, **kwargs):
        self.parser = yacc.yacc(module=self, **kwargs)
        return self.parser
