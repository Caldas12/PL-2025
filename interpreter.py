from parser import Parser
import csv

class Interpreter:
    def __init__(self):
        self.parser = Parser()
        self.dictionary = {} 

    def start(self, input_string):
        parser = self.parser.parse_input(input_string)
        if parser is None:
            raise print("Parser error")
            return None
        for statement in parser:
            print(statement)
            if statement[0] == 'import':
                self.import_table(statement[1], statement[2])
            elif statement[0] == 'export':
                self.write_file(statement[1], statement[2])
        
# ---------------------

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
            print (header, data)
            return {header, data}
    
    def write_file(self, table_name, file_path):
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(table_name)
            for row in table_name:
                writer.writerow(row)

    def import_table(self, table_name, file_path):
        if self.dictionary [table_name]:
            raise print("Table already exists")
            return None
        data = self.read_file(file_path)
        self.dictionary[table_name].append(data)
