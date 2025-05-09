import ply.lex as lex # type: ignore

# Lista de tokens
tokens = [
    'ID', 
    'STRING', 
    'NUMBER',
    'EQUALS', 
    'STAR',
    'NOT_EQUAL', 
    'LESS_THAN', 
    'GREATER_THAN', 
    'LESS_EQUAL', 
    'GREATER_EQUAL',
    'COMMA', 
    'SEMICOLON'
]

# Palavras-chave
reserved = {
    'import': 'IMPORT',
    'table': 'TABLE',
    'from': 'FROM',
    'select': 'SELECT',
    'where': 'WHERE',
    'and': 'AND',
    'create': 'CREATE',
    'join': 'JOIN',
    'using': 'USING',
    'procedure': 'PROCEDURE',
    'do': 'DO',
    'end': 'END',
    'call': 'CALL',
    'export': 'EXPORT',
    'as': 'AS',
    'discard': 'DISCARD',
    'rename': 'RENAME',
    'print': 'PRINT',
    'limit': 'LIMIT'
}

tokens += list(reserved.values())

# Regras de expressão regular
t_EQUALS = r'='
t_NOT_EQUAL = r'<>'
t_LESS_THAN = r'<'
t_GREATER_THAN = r'>'
t_LESS_EQUAL = r'<='
t_GREATER_EQUAL = r'>='
t_COMMA = r','
t_SEMICOLON = r';'
t_STAR = r'\*'

def t_STRING(t):
    r'\"[^"\n]*\"'
    t.value = t.value.strip('"')
    return t

def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value.lower(), 'ID')
    return t

def t_comment_line(t):
    r'\-\-.*'
    pass  # ignora

def t_comment_block(t):
    r'\{\-.*?\-\}'
    pass

t_ignore = ' \t\r\n'

def t_error(t):
    print(f"Token not recognized: {t.value[:10]}")
    exit(1)

lexer = lex.lex()