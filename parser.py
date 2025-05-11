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
        '''program : statement_list'''
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
                    | create_table'''
        p[0] = p[1]

    def p_operator(self, p):
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

    # --------- Comandos - Tabela de dados ---------

    def p_import_table(self, p):
        '''import_table : IMPORT TABLE ID FROM STRING SEMICOLON'''
        p[0] = ('import', p[3], p[5])
    
    def p_export_table(self, p):
        '''export_table : EXPORT TABLE ID AS STRING SEMICOLON'''
        p[0] = ('export', p[3], p[5])

    def p_discard_table(self, p):
        '''discard_table : DISCARD TABLE ID SEMICOLON'''
        p[0] = ('discard', p[3])
    
    def p_rename_table(self, p):
        '''rename_table : RENAME TABLE ID ID SEMICOLON'''
        p[0] = ('rename', p[3], p[4])

    def p_print_table(self, p):
        '''print_table : PRINT TABLE ID SEMICOLON'''
        p[0] = ('print', p[3])
    
    # --------- Comandos - Queries ---------

    def p_select_table(self, p):
        '''select_table : SELECT STAR FROM ID SEMICOLON
                        | select_columns
                        | limit_select_table
                        | select_table_condition'''
        if len(p) == 6:  
            p[0] = ('select', p[4])
        else:
            p[0] = p[1]

    def p_select_columns(self, p):
        '''select_columns : SELECT comma_id FROM ID SEMICOLON'''
        p[0] = ('select_columns', p[2], p[4])

    def p_comma_id(self, p):
        '''comma_id : ID COMMA comma_id
                    | ID'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = [p[1]] + p[3]

    def p_limit_select_table(self, p):
        '''limit_select_table : SELECT STAR FROM ID LIMIT NUMBER SEMICOLON'''
        p[0] = ('select_all_limit', p[4], p[6])

    def p_select_table_condition(self, p):
        '''select_table_condition : SELECT STAR FROM ID WHERE ID operator ID SEMICOLON
                                | SELECT STAR FROM ID WHERE ID operator ID select_table_condition_and'''
        if len(p) == 10:  
            p[0] = ('select_where', p[4], (p[6], p[7], p[8]))
        else:  
            p[0] = ('select_where_and', p[4], (p[6], p[7], p[8]), p[9])

    def p_select_table_condition_and(self, p):
        '''select_table_condition_and : AND ID operator ID SEMICOLON
                                        | AND ID operator ID select_table_condition_and'''
        if p[5] == ';':
            p[0] = [('AND', p[2], p[3], p[4])]
        else:
            p[0] = [('AND', p[2], p[3], p[4])] + p[5]

    # --------- Comandos - Criação ---------

    def p_create_table(self, p):
        '''create_table : CREATE TABLE ID select_table
                        | CREATE TABLE ID FROM ID JOIN ID USING ID SEMICOLON
                        | CREATE TABLE ID SELECT comma_id FROM ID SEMICOLON'''
        if len(p) == 6 and p[2] == 'TABLE' and p[4] == 'SELECT':
            p[0] = ('create_select', p[3], p[5], p[7])  # ('create_select', new_table, columns, source_table)
        elif len(p) == 6:
            p[0] = ('create', p[3], p[4])
        else:
            p[0] = ('create', p[3], p[5], p[7], p[9])
    
    # --------- Comandos - Procedimentos ---------
    
    def p_procedure(self, p):
        '''procedure : PROCEDURE ID DO statement_list END SEMICOLON
                    | PROCEDURE ID DO statement_list END'''
        if len(p) == 7:
            p[0] = ('procedure', p[2], p[4])
        else:
            p[0] = ('procedure', p[2], p[4], None)
    
    def p_call_procedure(self, p):
        '''call_procedure : CALL ID SEMICOLON'''
        p[0] = ('call', p[2])


    # --------- Erros ---------

    def p_error(self, p):
        if p:
            print(f"Erro de sintaxe na linha: {p.lineno}, perto de '{p.value}'")
        else:
            print("Erro de sintaxe no fim do input")

    # ---------------------

    def parse_input(self, data):
        """
        Função para parsear a entrada e retornar a AST.
        """
        result = self.parser.parse(data, lexer=self.lexer.lexer)
        return result

