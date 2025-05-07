from lexer import lexer

data = 'SELECT name, age FROM users;'
lexer.input(data)

for tok in lexer:
    print(tok)
