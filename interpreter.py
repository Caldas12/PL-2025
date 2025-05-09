from parser import Parser

class Interpreter:
    def __init__(self):
        self.parser = Parser()

    def start(self, input_string):
        parser = self.parser.parse_input(input_string)
        if parser is None:
            raise print("Parser error")
            return None
        for statement in parser:
            print(statement)
            if statement[0] == 'import':
                self.import_table(statement[1], statement[2])
        




    def import_table(self, table_name, file_path):
        