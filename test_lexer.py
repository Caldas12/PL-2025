from lexer import Lexer

def dump_tokens(s):
    lx = Lexer()
    lx.build()
    lx.lexer.input(s)
    print(f"\nTokens for: {s!r}")
    while True:
        tok = lx.lexer.token()
        if not tok: break
        print(f"  {tok.type!r:12} {tok.value!r}")

if __name__ == "__main__":
    dump_tokens('SELECT * FROM T WHERE x > 10;')
    dump_tokens('SELECT * FROM T WHERE x = 1 AND y <> 2 AND z <= 5;')