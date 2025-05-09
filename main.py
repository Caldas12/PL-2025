import sys
from interpreter import Interpreter

class main:

    interpreter = Interpreter()

    if len(sys.argv) == 2:
            try:
                with open(sys.argv[1], "r") as file:
                    contents = file.read()
                    resultado = interpreter.start(contents)
            except Exception as e:
                print(e)
    else:
        for expr in iter(lambda: input(">> "), ""):
            try:
                resultado = interpreter.start(expr)
            except Exception as e:
                print(e)