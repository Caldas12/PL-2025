import ply.lex as lex # type: ignore



# List of token names.
tokens = (
    'SELECT', 'FROM', 'IDENTIFIER',
    'COMMA', 'SEMICOLON',
)

# Regular expressions for simple tokens
t_SELECT = r'SELECT'
t_FROM = r'FROM'
t_COMMA = r','
t_SEMICOLON = r';'

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

# Ignore spaces and tabs
t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()
