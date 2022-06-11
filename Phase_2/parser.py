from ply import yacc
from Phase_1.lexer import Lexer
from Phase_3 import *


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

    @staticmethod
    def p_declarations(p):
        """declarations : VAR_KW declaration_list SEMICOLON
                        | empty"""

    @staticmethod
    def p_declaration_list(p):
        """declaration_list : identifier_list COLON type
               | declaration_list SEMICOLON identifier_list COLON type"""

    @staticmethod
    def p_identifier_list(p):
        """identifier_list : IDENTIFIER
                | identifier_list COMMA IDENTIFIER"""

    @staticmethod
    def p_type(p):
        """type : INTEGER_KW
                | REAL_KW"""

    @staticmethod
    def p_procedure_list(p):
        """procedure_list : procedure_list procedure
                          | procedure_list function
                          | empty"""

    @staticmethod
    def p_procedure(p):
        """procedure : PROCEDURE_KW IDENTIFIER parameters SEMICOLON declarations compound_statement SEMICOLON"""

    @staticmethod
    def p_function(p):
        """function : FUNCTION_KW IDENTIFIER parameters COLON type SEMICOLON declarations compound_statement SEMICOLON"""

    @staticmethod
    def p_parameters(p):
        """parameters : LRB declaration_list RRB
                    | empty"""

    @staticmethod
    def p_compound_statement(p):
        """compound_statement : BEGIN_KW statement_list END_KW"""
        p[0] = NonTerminal()
        p[0].nextList = p[2].nextList

    @staticmethod
    def p_statement_list(p):
        """statement_list : statement
                          | statement_list SEMICOLON empty statement"""
        p[0] = NonTerminal()

    def p_statement_assign(self, p):
        """statement : IDENTIFIER ASSIGN expression"""
        p[0] = NonTerminal()
        S = p[0]
        E = p[3]

        assert isinstance(S, NonTerminal) and isinstance(E, NonTerminal)

        # S.nextList = None
        S.code = E.code + "{} = {}".format(p[1], E.get_value())
        self.code_output.append("{} = {}".format(p[1], E.get_value()))
        self.quadruples.append(Quadruple(p[1], E.get_value(), p[2]))

    def p_statement_if_else(self, p):
        """statement : IF_KW expression THEN_KW empty statement empty_N ELSE_KW empty statement"""
        p[0] = NonTerminal()

        S = p[0]
        B = p[2]
        M1 = p[4]
        S1 = p[5]
        N = p[6]
        M2 = p[8]
        S2 = p[9]

        assert isinstance(S, NonTerminal) and isinstance(B, NonTerminal)
        assert isinstance(S1, NonTerminal) and isinstance(S2, NonTerminal)
        assert isinstance(M1, NonTerminal) and isinstance(M2, NonTerminal)
        assert isinstance(N, NonTerminal)

        self.back_patch(B.trueList, M1.instr)
        self.back_patch(B.falseList, M2.instr)

        S.nextList = S1.nextList + N.nextList + S2.nextList

    def p_statement_if(self, p):
        """statement : IF_KW expression THEN_KW empty statement empty_N"""

        p[0] = NonTerminal()

        S = p[0]
        B = p[2]
        M = p[4]
        S1 = p[5]
        N = p[6]

        assert isinstance(S, NonTerminal) and isinstance(B, NonTerminal)
        assert isinstance(S1, NonTerminal) and isinstance(M, NonTerminal)

        self.back_patch(B.trueList, M.instr)
        S.nextList = B.falseList + S1.nextList

    def p_statement_while(self, p):
        """statement : WHILE_KW empty expression DO_KW empty statement"""
        p[0] = NonTerminal()

        S = p[0]
        M1 = p[2]
        B = p[3]
        M2 = p[5]
        S1 = p[6]

        assert isinstance(S, NonTerminal) and isinstance(B, NonTerminal)
        assert isinstance(S1, NonTerminal) and isinstance(M1, NonTerminal) and isinstance(M2, NonTerminal)

        self.back_patch(S1.nextList, M1.instr)
        self.back_patch(B.trueList, M2.instr)
        S.nextList = B.falseList
        self.code_output.append("goto {}".format(M1.instr))

    @staticmethod
    def p_statement_compound(p):
        """statement : compound_statement"""
        p[0] = NonTerminal()
        p[0].nextList = p[1].nextList

    @staticmethod
    def p_statement(p):
        """statement : IDENTIFIER arguments
                     | empty"""

    @staticmethod
    def p_arguments(p):
        """arguments : LRB actual_parameter_list RRB"""

    @staticmethod
    def p_actual_parameter_list(p):
        """actual_parameter_list : actual_parameter_list COMMA actual_parameter
                                 | actual_parameter"""

    @staticmethod
    def p_actual_parameter(p):
        """actual_parameter : expression"""

    @staticmethod
    def p_expression_assign_constant(p):
        """expression : INTEGER_CONSTANT
                      | REAL_CONSTANT"""
        # print(p[0], p[1])
        p[0] = NonTerminal()
        p[0].value = p[1]

    @staticmethod
    def p_expression_assign_identifier(p):
        """expression : IDENTIFIER"""
        # print(p[0], p[1])
        p[0] = NonTerminal()
        p[0].place = p[1]

    def p_expression_uminus(self, p):
        """expression : SUB expression"""
        # print(p[0], p[1], p[2])
        p[0] = NonTerminal()
        p[0].place = self.new_temp()
        p[0].code = p[2].code + "{} = -{}".format(p[0].place, p[2].get_value())

        self.quadruples.append(Quadruple(p[0].place, p[2].get_value(), "uminus"))

    def p_expression_op(self, p):
        """expression : expression SUM expression
                      | expression SUB expression
                      | expression MUL expression
                      | expression DIV expression
                      | expression DIV_KW expression
                      | expression MOD_KW expression
                      | expression LT expression
                      | expression LE expression
                      | expression EQ expression
                      | expression NE expression
                      | expression GT expression
                      | expression GE expression
                      """
        # print(p[0], p[1], p[2], p[3])
        p[0] = NonTerminal()

        E = p[0]
        E1 = p[1]
        op = p[2]
        E2 = p[3]

        assert isinstance(E, NonTerminal) and isinstance(E1, NonTerminal) and isinstance(E2, NonTerminal)

        E.place = self.new_temp()
        E.code = p[1].code + p[3].code + "\n"
        E.code += "{} = {} {} {}".format(E.place, E1.get_value(), op, E2.get_value())

        self.quadruples.append(Quadruple(E.place, E1.get_value(), op, E2.get_value()))

        if op in "<=,<>,>=":
            E.trueList = [self.nextInstr]
            self.nextInstr += 1
            E.falseList = [self.nextInstr]
            if op == "=":
                op += "="
            self.code_output.append("if {} {} {} goto ".format(E1.get_value(), op, E2.get_value()))
            self.code_output.append("goto ".format(E1.get_value(), op, E2.get_value()))

        print(E.code)

    def p_expression_bool(self, p):
        """expression : expression AND_KW empty expression
                      | expression OR_KW empty expression
                      """
        p[0] = NonTerminal()

        B = p[0]
        B1 = p[1]
        M = p[3]
        B2 = p[4]

        assert isinstance(B, NonTerminal) and isinstance(B1, NonTerminal)
        assert isinstance(M, NonTerminal) and isinstance(B2, NonTerminal)

        if p[2] == "and":
            self.back_patch(B1.trueList, M.instr)
            B.trueList = B2.trueList
            B.falseList = B1.falseList + B2.falseList
        else:
            self.back_patch(B1.falseList, M.instr)
            B.trueList = B1.trueList + B2.trueList
            B.falseList = B2.falseList

    @staticmethod
    def p_expression_not(p):
        """expression : NOT_KW expression"""
        p[0] = NonTerminal()

        B = p[0]
        B1 = p[2]

        assert isinstance(B, NonTerminal) and isinstance(B1, NonTerminal)

        B.trueList = B1.falseList
        B.falseList = B1.trueList

    @staticmethod
    def p_expression(p):
        """expression : LRB expression RRB"""
        # print(p[0], p[1], p[2].value)
        p[0] = NonTerminal()

        E = p[0]
        E1 = p[2]

        assert isinstance(E, NonTerminal) and isinstance(E1, NonTerminal)

        E.place = E1.place
        E.code = E1.code

        E.trueList = E1.trueList
        E.falseList = E1.falseList

    def p_empty(self, p):
        """empty :"""
        p[0] = NonTerminal()
        p[0].instr = self.nextInstr

    def p_empty_N(self, p):
        """empty_N :"""
        p[0] = NonTerminal()
        p[0].nextList.append(self.nextInstr)
        self.code_output.append("goto ")

    @staticmethod
    def p_error(p):
        print("Error", p.type, p.lexpos)
        print(p)

    def new_temp(self):
        self.tempCount += 1
        return "T" + str(self.tempCount)

    def new_label(self):
        self.labelCount += 1
        return "L" + str(self.labelCount)

    def back_patch(self, bool_list, instr):
        for i in bool_list:
            self.code_output[i - 1] += str(instr)

    def __init__(self, path, file_name):
        self.parser = None
        self.p = None
        self.code_output = []
        self.file = open('{path}\\Test\\{file_name}_code_output.txt'.format(path=path, file_name=file_name), "w")
        self.quadruples = []
        self.tempCount = -1
        self.labelCount = -1
        self.nextInstr = 1

    def build(self, **kwargs):
        self.parser = yacc.yacc(module=self, **kwargs)
        return self.parser
