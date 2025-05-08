import ply.yacc as yacc
from lexer import tokens  # Usa os tokens definidos no lexer.py

# ---------------------
# Árvore de Sintaxe Abstrata (exemplo básico)
# ---------------------

class ImportTable:
    def __init__(self, table_name, file_name):
        self.table_name = table_name
        self.file_name = file_name

    def __repr__(self):
        return f"ImportTable({self.table_name}, '{self.file_name}')"

# ---------------------
# Regras de Produção
# ---------------------

def p_program(p):
    '''program : statement_list'''
    p[0] = p[1]

def p_statement_list(p):
    '''statement_list : statement_list statement
                      | statement'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_statement(p):
    '''statement : import_table SEMICOLON
                 | export_table SEMICOLON
                 | select_statement SEMICOLON'''
    p[0] = p[1]

def p_operator(p):
    '''operator : EQUALS
                | NOT_EQUAL
                | LESS_THAN
                | GREATER_THAN
                | LESS_EQUAL
                | GREATER_EQUAL
                | COMMA
                | SEMICOLON
                | STAR'''
    p[0] = p[1]

# --------- Comandos ---------

def p_import_table(p):
    '''import_table : IMPORT TABLE ID FROM STRING'''
    p[0] = ImportTable(p[3], p[5])

def p_export_table(p):
    '''export_table : EXPORT TABLE ID AS STRING'''
    p[0] = ('export', p[3], p[5])  # Podes usar uma classe depois, como fizemos com ImportTable

def p_select_statement(p):
    '''select_statement : SELECT STAR FROM ID opt_where_clause
                        | SELECT column_list FROM ID opt_where_clause'''
    if p[2] == '*':
        p[0] = ('select_all', p[4], p[5])
    else:
        p[0] = ('select_columns', p[2], p[4], p[5])

def p_column_list(p):
    '''column_list : column_list COMMA ID
                   | ID'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

def p_opt_where_clause(p):
    '''opt_where_clause : WHERE condition
                        | empty'''
    if len(p) == 3:
        p[0] = p[2]
    else:
        p[0] = None

def p_condition(p):
    '''condition : condition AND condition
                 | ID operator value'''
    if len(p) == 4 and p[2] == 'AND':
        p[0] = ('and', p[1], p[3])
    else:
        p[0] = ('cond', p[1], p[2], p[3])

def p_value(p):
    '''value : NUMBER
             | STRING'''
    p[0] = p[1]

def p_empty(p):
    'empty :'
    pass # Produz um valor nulo para o caso de não haver nada



# --------- Erros ---------

def p_error(p):
    if p:
        print(f"Erro de sintaxe na linha: {p.lineno}, perto de '{p.value}'")
    else:
        print("Erro de sintaxe no fim do input")

# ---------------------
# Construção do parser
# ---------------------

parser = yacc.yacc(debug=True)