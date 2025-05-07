import ply.yacc as yacc
from lexer import tokens

def p_statement_select(p):
    'statement : SELECT column_list FROM IDENTIFIER SEMICOLON'
    p[0] = ('select', p[2], p[4])

def p_column_list_multiple(p):
    'column_list : column_list COMMA IDENTIFIER'
    p[0] = p[1] + [p[3]]

def p_column_list_single(p):
    'column_list : IDENTIFIER'
    p[0] = [p[1]]

def p_error(p):
    print("Syntax error at", p.value if p else "EOF")

parser = yacc.yacc()
