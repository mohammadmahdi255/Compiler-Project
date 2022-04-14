from Phase_2.Parser import *
import os

file_name = "Final test"
path = os.path.dirname(__file__)
lexer = Lexer().build()
file = open('{path}\\Test\\{file_name}.txt'.format(path=path, file_name=file_name), "r")
text_input = file.read()
file.close()
lexer.input(text_input)

token = ''
file = open('{path}\\Test\\{file_name}_output.txt'.format(path=path, file_name=file_name), "w")
while token is not None:
    token = lexer.token()
    file.write(token.__str__() + '\n')
file.close()

parser = Parser()
parser.build().parse(text_input, lexer, False)
