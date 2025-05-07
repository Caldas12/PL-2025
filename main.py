from parser import parser

while True:
    try:
        s = input('cql> ')
    except EOFError:
        break
    if not s:
        continue
    result = parser.parse(s)
    print(result)