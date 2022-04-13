from Parser import *

file_name = "Final test"
lexer = Lexer().build()
file = open('../Test/{file_name}.txt'.format(file_name=file_name), "r")
text_input = file.read()
file.close()
lexer.input(text_input)

parser = Parser()
parser.build().parse(text_input, lexer, False)

# tokens = lexer.get_tokens()
# file = open('../Test/{file_name}_output.txt'.format(file_name=file_name), "w")
#
# for token in tokens:
#     file.write(token.__str__() + '\n')
#     print(token)
# file.close()
