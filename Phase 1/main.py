from lexer import Lexer
from parser import Parser

file_name = "New test"
lexer = Lexer().build()
file = open('../Test/{file_name}.txt'.format(file_name=file_name), "r")
text_input = file.read()
file.close()
lexer.input(text_input)

# tokens = lexer.get_tokens()
# file = open('../Test/{file_name}_output.txt'.format(file_name=file_name), "w")

# for token in tokens:
#     file.write(token.__str__() + '\n')
#     print(token)
# file.close()

parser = Parser()
parser.build().parse(text_input, lexer, False)