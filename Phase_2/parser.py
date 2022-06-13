from ply import yacc
from Phase_1.lexer import Lexer
from Phase_3 import *
from pydot import *


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

    def p_program(self, p):
        """program : PROGRAM_KW IDENTIFIER declarations procedure_list compound_statement DOT"""
        self.initialize_non_terminal(p, 'program')

    def p_declarations(self, p):
        """declarations : VAR_KW declaration_list SEMICOLON
                        | empty"""
        self.initialize_non_terminal(p, 'declarations')

    def p_declaration_list(self, p):
        """declaration_list : identifier_list COLON type
                            | declaration_list SEMICOLON identifier_list COLON type"""
        self.initialize_non_terminal(p, 'declaration_list')

    def p_identifier_list(self, p):
        """identifier_list : IDENTIFIER
                           | identifier_list COMMA IDENTIFIER"""
        self.initialize_non_terminal(p, 'identifier_list')

    def p_type(self, p):
        """type : INTEGER_KW
                | REAL_KW"""
        self.initialize_non_terminal(p, 'type')

    def p_procedure_list(self, p):
        """procedure_list : procedure_list procedure
                          | procedure_list function
                          | empty"""
        self.initialize_non_terminal(p, 'procedure_list')

    def p_procedure(self, p):
        """procedure : PROCEDURE_KW IDENTIFIER parameters SEMICOLON declarations compound_statement SEMICOLON"""
        self.initialize_non_terminal(p, 'procedure')

    def p_function(self, p):
        """function : FUNCTION_KW IDENTIFIER parameters COLON type SEMICOLON declarations compound_statement SEMICOLON"""
        self.initialize_non_terminal(p, 'function')

    def p_parameters(self, p):
        """parameters : LRB declaration_list RRB
                    | empty"""
        self.initialize_non_terminal(p, 'parameters')

    def p_compound_statement(self, p):
        """compound_statement : BEGIN_KW statement_list END_KW"""
        self.initialize_non_terminal(p, 'compound_statement')

        p[0].nextList = p[2].nextList

    def p_statement_list(self, p):
        """statement_list : statement
                          | statement_list SEMICOLON empty statement"""
        self.initialize_non_terminal(p, 'statement_list')

    def p_statement_assign(self, p):
        """statement : IDENTIFIER ASSIGN expression"""
        self.initialize_non_terminal(p, 'statement')

        S = p[0]
        E = p[3]

        assert isinstance(S, NonTerminal) and isinstance(E, NonTerminal)

        # S.nextList = None
        S.code = E.code + "{} = {}".format(p[1], E.get_value())
        self.code_output.append("{} = {}".format(p[1], E.get_value()))
        self.quadruples.append(Quadruple(p[1], E.get_value(), p[2]))

    def p_statement_if_else(self, p):
        """statement : IF_KW expression THEN_KW empty statement empty_N ELSE_KW empty statement"""
        self.initialize_non_terminal(p, 'statement')

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

        self.initialize_non_terminal(p, 'statement')

        S = p[0]
        B = p[2]
        M = p[4]
        S1 = p[5]

        assert isinstance(S, NonTerminal) and isinstance(B, NonTerminal)
        assert isinstance(S1, NonTerminal) and isinstance(M, NonTerminal)

        self.back_patch(B.trueList, M.instr)
        S.nextList = B.falseList + S1.nextList

    def p_statement_while(self, p):
        """statement : WHILE_KW empty expression DO_KW empty statement"""
        self.initialize_non_terminal(p, 'statement')

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

    def p_statement_compound(self, p):
        """statement : compound_statement"""
        self.initialize_non_terminal(p, 'statement')

        p[0].nextList = p[1].nextList

    def p_statement(self, p):
        """statement : IDENTIFIER arguments
                     | empty"""
        self.initialize_non_terminal(p, 'statement')

    def p_arguments(self, p):
        """arguments : LRB actual_parameter_list RRB"""
        self.initialize_non_terminal(p, 'arguments')

    def p_actual_parameter_list(self, p):
        """actual_parameter_list : actual_parameter_list COMMA actual_parameter
                                 | actual_parameter"""
        self.initialize_non_terminal(p, 'actual_parameter_list')

    def p_actual_parameter(self, p):
        """actual_parameter : expression"""
        self.initialize_non_terminal(p, 'actual_parameter')

    def p_expression_assign_constant(self, p):
        """expression : INTEGER_CONSTANT
                      | REAL_CONSTANT"""
        self.initialize_non_terminal(p, 'expression')

        p[0].value = p[1]

    def p_expression_assign_identifier(self, p):
        """expression : IDENTIFIER"""
        self.initialize_non_terminal(p, 'expression')

        p[0].place = p[1]

    def p_expression_uminus(self, p):
        """expression : SUB expression"""
        self.initialize_non_terminal(p, 'expression')

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
        self.initialize_non_terminal(p, 'expression')

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

    def p_expression_bool(self, p):
        """expression : expression AND_KW empty expression
                      | expression OR_KW empty expression
                      """
        self.initialize_non_terminal(p, 'expression')

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

    def p_expression_not(self, p):
        """expression : NOT_KW expression"""
        self.initialize_non_terminal(p, 'expression')

        B = p[0]
        B1 = p[2]

        assert isinstance(B, NonTerminal) and isinstance(B1, NonTerminal)

        B.trueList = B1.falseList
        B.falseList = B1.trueList

    def p_expression(self, p):
        """expression : LRB expression RRB"""
        self.initialize_non_terminal(p, 'expression')

        E = p[0]
        E1 = p[2]

        assert isinstance(E, NonTerminal) and isinstance(E1, NonTerminal)

        E.place = E1.place
        E.code = E1.code

        E.trueList = E1.trueList
        E.falseList = E1.falseList

    def p_empty(self, p):
        """empty :"""
        self.initialize_non_terminal(p, 'empty')

        p[0].instr = self.nextInstr

    def p_empty_N(self, p):
        """empty_N :"""
        self.initialize_non_terminal(p, 'empty_N')

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

    def initialize_non_terminal(self, p, label):
        p[0] = NonTerminal(self.nodeNum, label=label)
        self.nodeNum += 1

        self.node_list.append(p[0].node)

        for i in range(1, len(p)):
            item = p[i]
            if isinstance(item, NonTerminal):
                self.graph.add_edge(Edge(p[0].node, item.node))
            else:
                node = Node("N" + str(self.nodeNum), label='"{}"'.format(item))
                self.nodeNum += 1
                self.node_list.append(node)
                self.graph.add_edge(Edge(p[0].node, node))

    def __init__(self, path, file_name):
        self.parser = None
        self.p = None
        self.nodeNum = 0
        self.node_list = []
        self.graph = Dot(graph_type='graph', compound='true')
        self.code_output = []
        self.file = open('{path}\\Test\\{file_name}_code_output.txt'.format(path=path, file_name=file_name), "w")
        self.quadruples = []
        self.tempCount = -1
        self.labelCount = -1
        self.nextInstr = 1

    def build(self, **kwargs):
        self.parser = yacc.yacc(module=self, **kwargs)

    def parse(self, input=None, lexer=None, debug=False, tracking=False, tokenfunc=None):
        if self.parser:
            self.parser.parse(input, lexer, debug, tracking, tokenfunc)
            for node in self.node_list:
                self.graph.add_node(node)
        else:
            print("build first!")


