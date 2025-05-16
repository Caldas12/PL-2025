import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from interpreter import Interpreter

interpreter = Interpreter()

examples = [
    'IMPORT TABLE observacoes FROM "examples/observacoes.csv";',
    'IMPORT TABLE estacoes FROM "examples/estacoes.csv";',
    "SELECT * FROM observacoes;",
    "SELECT Temperatura FROM observacoes;",
    "SELECT * FROM observacoes WHERE Temperatura > 15;",
    "SELECT * FROM observacoes WHERE Temperatura > 15 AND Temperatura < 20;",
    "SELECT * FROM observacoes LIMIT 3;",
    "SELECT Temperatura FROM observacoes LIMIT 2;",
    "CREATE TABLE Temp SELECT Temperatura FROM observacoes LIMIT 2;",
    "PRINT TABLE Temp;",
    'EXPORT TABLE Temp AS "Temp.csv";',
    "DISCARD TABLE Temp;",
    "RENAME TABLE estacoes station;",
    "PRINT TABLE station;",
    "PROCEDURE Teste DO CREATE TABLE Testetemp SELECT * FROM observacoes WHERE Temperatura > 22; END;",
    "CALL Teste;",
]

for example in examples:
    print("Input:", example)
    output = interpreter.start(example)
    if output:
        print(output)
    print("-" * 40)