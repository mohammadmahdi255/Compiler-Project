from lexer import Lexer

lexer = Lexer()
file = open('../Test/Full test.txt')
text_input = file.read()
file.close()
lexer.input(text_input)

tokens = lexer.get_tokens()

for token in tokens:
    print(token)

