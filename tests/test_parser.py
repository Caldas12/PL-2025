import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from parser import Parser

parser = Parser()

examples = [
    'IMPORT TABLE obs FROM "observacoes.csv";',
    "SELECT IntensidadeVentoKM,Temperatura FROM obs;",
    "SELECT * FROM obs WHERE Temperatura > 15;",
    "CREATE TABLE Tempmaior SELECT * FROM obs WHERE Temperatura > 15;",
    "PROCEDURE atualizar DO CREATE TABLE Tempmaior SELECT * FROM obs WHERE Temperatura > 20 ; END",
    '-- comment\nEXPORT TABLE obs AS "obs.csv";',
]

for example in examples:
    print("Input:", example)
    result = parser.parse_input(example)
    print("AST:", result)
    print("-" * 40)