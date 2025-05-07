from parser import parser

entrada = '''
IMPORT TABLE estacoes FROM "estacoes.csv";
EXPORT TABLE estacoes AS "saida.csv";
SELECT * FROM estacoes;
SELECT Id,Local FROM estacoes;
'''

resultado = parser.parse(entrada)
for comando in resultado:
    print(comando)