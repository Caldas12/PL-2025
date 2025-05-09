from parser import Parser
import csv

class Interpreter:
    def __init__(self):
        self.parser = Parser()
        self.dictionary = {}

    def start(self, input_string):
        parser = self.parser.parse_input(input_string)
        if parser is None:
            raise ValueError("Parser error")
        for statement in parser:
            print(statement)
            if statement[0] == 'import':
                self.import_table(statement[1], statement[2])
            elif statement[0] == 'export':
                self.write_file(statement[1], statement[2])
            elif statement[0] == 'discard':
                self.discard_table(statement[1])
            elif statement[0] == 'rename':
                self.rename_table(statement[1], statement[2])
            elif statement[0] == 'print':
                self.print_table(statement[1])

    def read_file(self, file_path):
        data = []
        header = None
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0].startswith('#'):
                    continue
                if header is None:
                    header = row
                    continue
                data.append(row)
            print(header, data)
            return {"header": header, "data": data}

    def write_file(self, table_name, file_path):
        if table_name not in self.dictionary:
            raise ValueError("Table does not exist")
        table = self.dictionary[table_name]
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(table["header"])
            for row in table["data"]:
                writer.writerow(row)

    def import_table(self, table_name, file_path):
        if table_name in self.dictionary:
            raise ValueError("Table already exists")
        data = self.read_file(file_path)
        self.dictionary[table_name] = data

    def rename_table(self, old_name, new_name):
        if old_name not in self.dictionary:
            raise ValueError("Table does not exist")
        self.dictionary[new_name] = self.dictionary.pop(old_name)

    def discard_table(self, table_name):
        if table_name not in self.dictionary:
            raise ValueError("Table does not exist")
        del self.dictionary[table_name]

    def print_table(self, table_name):
        if table_name not in self.dictionary:
            raise ValueError("Table does not exist")
        table = self.dictionary[table_name]
        print(table["header"])
        for row in table["data"]:
            print(row)