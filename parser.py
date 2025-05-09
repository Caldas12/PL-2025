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
                    | export_table'''
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
        p[0] = ('rename', p[3], p[5])

    def p_print_table(self, p):
        '''print_table : PRINT TABLE ID SEMICOLON'''
        p[0] = ('print', p[3])
    
    # --------- Comandos - Queries ---------

    

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

