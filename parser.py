import ply.yacc as yacc
from lexer import Lexer

class Parser:
    def __init__(self):
        self.lexer = Lexer()
        self.tokens = self.lexer.tokens
        self.lexer.build()
        self.parser = yacc.yacc(module=self)

    # ---------------------
    # Regras de Produção
    # ---------------------

    def p_program(self, p):
        'program : statement_list'
        p[0] = p[1]

    def p_statement_list(self, p):
        '''statement_list : statement_list statement
                          | statement'''
        if len(p) == 3:
            p[0] = p[1] + [p[2]]
        else:
            p[0] = [p[1]]

    def p_statement(self, p):
        '''statement : import_table
                     | export_table
                     | discard_table
                     | rename_table
                     | print_table
                     | select_table
                     | create_table_select
                     | create_table_join
                     | create_table_from_select_columns
                     | procedure
                     | call_procedure'''
        p[0] = p[1]

    # --------- Operators ---------

    def p_operator(self, p):
        '''operator : EQUALS
                    | NOT_EQUAL
                    | LESS_THAN
                    | GREATER_THAN
                    | LESS_EQUAL
                    | GREATER_EQUAL'''
        p[0] = p[1]

    # --------- Comandos - Tabela de dados ---------

    def p_import_table(self, p):
        'import_table : IMPORT TABLE ID FROM STRING SEMICOLON'
        p[0] = ('import', p[3], p[5])

    def p_export_table(self, p):
        'export_table : EXPORT TABLE ID AS STRING SEMICOLON'
        p[0] = ('export', p[3], p[5])

    def p_discard_table(self, p):
        'discard_table : DISCARD TABLE ID SEMICOLON'
        p[0] = ('discard', p[3])

    def p_rename_table(self, p):
        'rename_table : RENAME TABLE ID ID SEMICOLON'
        p[0] = ('rename', p[3], p[4])

    def p_print_table(self, p):
        'print_table : PRINT TABLE ID SEMICOLON'
        p[0] = ('print', p[3])

    # --------- Comandos - Queries --------- 

    def p_select_table(self, p):
        '''select_table : SELECT STAR FROM ID SEMICOLON
                        | select_columns
                        | select_where
                        | select_where_and
                        | select_limit'''
        p[0] = p[1] if isinstance(p[1], tuple) else ('select', p[4])

    def p_select_columns(self, p):
        'select_columns : SELECT comma_id FROM ID SEMICOLON'
        p[0] = ('select_columns', p[2], p[4])

    def p_select_where(self, p):
        'select_where : SELECT STAR FROM ID WHERE ID operator ID SEMICOLON'
        p[0] = ('select_where', p[4], (p[6], p[7], p[8]))

    def p_select_where_and(self, p):
        'select_where_and : SELECT STAR FROM ID WHERE ID operator ID select_and'
        p[0] = ('select_where_and', p[4], (p[6], p[7], p[8]), p[9])

    def p_select_and(self, p):
        '''select_and : AND ID operator ID SEMICOLON
                                | AND ID operator ID select_and'''
        if p[5] == ';':
            p[0] = [('AND', p[2], p[3], p[4])]
        else:
            p[0] = [('AND', p[2], p[3], p[4])] + p[5]

    def p_select_limit(self, p):
        'select_limit : SELECT STAR FROM ID LIMIT NUMBER SEMICOLON'
        p[0] = ('select_limit', p[4], p[6])

    def p_comma_id(self, p):
        '''comma_id : ID COMMA comma_id
                    | ID'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = [p[1]] + p[3]

    # --------- Comandos - Criação ---------

    def p_create_table_select(self, p):
        'create_table_select : CREATE TABLE ID select_table'
        p[0] = ('create_from_query', p[3], p[4])

    def p_create_table_join(self, p):
        'create_table_join : CREATE TABLE ID FROM ID JOIN ID USING ID SEMICOLON'
        p[0] = ('create_join', p[3], p[5], p[7], p[9])

    def p_create_table_from_select_columns(self, p):
        'create_table_from_select_columns : CREATE TABLE ID SELECT comma_id FROM ID SEMICOLON'
        p[0] = ('create_select_columns', p[3], p[5], p[7])

    # --------- Comandos - Procedimentos ---------

    def p_procedure(self, p):
        'procedure : PROCEDURE ID DO statement_list END SEMICOLON'
        p[0] = ('procedure', p[2], p[4])

    def p_call_procedure(self, p):
        'call_procedure : CALL ID SEMICOLON'
        p[0] = ('call', p[2])

    # --------- Erros ---------

    def p_error(self, p):
        if p:
            print(f"Erro de sintaxe na linha {p.lineno}, perto de '{p.value}'")
        else:
            print("Erro de sintaxe no fim do input")

    # --------- AST ---------
    
    def parse_input(self, data):
        """
        Função para parsear a entrada e retornar a AST.
        """
        result = self.parser.parse(data, lexer=self.lexer.lexer)
        return result
