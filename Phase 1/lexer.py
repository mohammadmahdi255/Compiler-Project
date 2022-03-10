from ply import lex


class Lexer:

    tokens = [
        "PROGRAM_KW", "VAR_KW", "EMPTY", "INTEGER_KW",
        "REAL_KW", "PROCEDURE_KW", "BEGIN_KW", "END_KW"
        "IF_KW", "THEN_KW", "ELSE_KW", "WHILE_KW",
        "DO_KW", "IDENTIFIER", "INTEGER_CONSTANT",
        "REAL_CONSTANT", "SUM_KW", "SUB_KW", "MUL_KW",
        "DIV_KW", "NEG", "MOD_KW", "LT_KW", "LE_KW",
        "EQ_KW", "NE_KW", "GT_KW", "GE_KW", "AND_KW",
        "OR_KW", "NOT_KW", "LRB_KW", "RRB_KW",
    ]
