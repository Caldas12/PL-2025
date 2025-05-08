from parser import parser  

entrada = '''
SELECT * FROM observacoes WHERE Temperatura > 22 AND Humidade < 80;
SELECT Id FROM observacoes WHERE DirecaoVento = "NE";
'''

resultado = parser.parse(entrada)

for comando in resultado:
    print(comando)