from parser import *

file_name = "Full test"
lexer = Lexer().build()
file = open('../Test/{file_name}.txt'.format(file_name=file_name), "r")
text_input = file.read()
file.close()
lexer.input(text_input)

parser = Parser()
parser.build().parse(text_input, lexer, False)


