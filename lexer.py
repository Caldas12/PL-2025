import ply.lex as lex


class Lexer:

    # Lista de tokens reconhecidos pelo lexer
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
        'limit': 'LIMIT',
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

    # Constrói o analisador léxico
    def build (self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)
    
    # Reconhece strings entre aspas
    def t_STRING(self, t):
        r'\"[^"\n]*\"'
        t.value = t.value.strip('"')
        return t

    # Reconhece números inteiros e decimais
    def t_NUMBER(self, t):
        r'\d+(\.\d+)?'
        t.value = float(t.value) if '.' in t.value else int(t.value)
        return t

    # Reconhece identificadores e verifica se são palavras reservadas
    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = self.reserved.get(t.value.lower(), 'ID')
        return t

    # Ignora comentários de linha (começam com --)
    def t_comment_line(self, t):
        r'\-\-.*'
        pass  # ignora

    # Ignora comentários de bloco (começam com {- e terminam com -})
    def t_comment_block(self, t):
        r'\{\-.*?\-\}'
        pass

    # Ignora espaços em branco, tabulações e quebras de linha
    t_ignore = ' \t\n'

    # Tratamento de erros
    def t_error(self, t):
        print(f"Token not recognized: {t.value[0]}")
        t.lexer.skip(1)