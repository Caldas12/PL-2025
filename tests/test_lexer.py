import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from lexer import Lexer

lexer = Lexer()
lexer.build()

examples = [
    'IMPORT TABLE estacoes FROM "estacoes.csv";',
    "SELECT * FROM observacoes WHERE Temperatura > 22;",
    "-- Comentario teste\nSELECT Id FROM estacoes;",
    '{- Comentario teste\n Comentario teste-}\nEXPORT TABLE estacoes AS "station.csv";',
]

for example in examples:
    print("Input:", example)
    lexer.lexer.input(example)
    for token in lexer.lexer:
        print(token)
    print("-" * 40)