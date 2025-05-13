from parser import Parser
import csv

class Interpreter:
    def __init__(self):
        self.parser = Parser()
        self.dictionary = {}
        self.procedures = {}

    def start(self, input_string):
        parser = self.parser.parse_input(input_string)
        if parser is None:
            raise ValueError("Parser error")
        for statement in parser:
            print(statement)
            stmt = statement[0]
            if stmt == 'import':
                self.import_table(statement[1], statement[2])
            elif stmt == 'export':
                self.write_file(statement[1], statement[2])
            elif stmt == 'discard':
                self.discard_table(statement[1])
            elif stmt == 'rename':
                self.rename_table(statement[1], statement[2])
            elif stmt == 'print':
                self.print_table(statement[1])
            elif stmt in ('select_table', 'select_columns', 'select_where', 'select_where_and', 'select_limit'):
                result = self.execute_select(statement)
                self.print_result(result)
            elif stmt == 'create_from_query':
                table_name, query = statement[1], statement[2]
                result = self.execute_select(query)
                self.dictionary[table_name] = result
            elif stmt == 'create_join':
                self.create_join_table(*statement[1:])
            elif stmt == 'create_select_columns':
                self.create_select_columns(*statement[1:])
            elif stmt == 'procedure':
                self.procedures[statement[1]] = statement[2]
            elif stmt == 'call':
                self.call_procedure(statement[1])

    # --------- Comandos - Tabela de dados ---------

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

    # --------- Comandos - Queries ---------

    def select_table(self, table_name, columns, conditions=None, limit=None):
        if table_name not in self.dictionary:
            raise ValueError("Table does not exist")
        table = self.dictionary[table_name]
        header = table["header"]
        data = table["data"]

        if columns == "*":
            selected_columns = header
        elif isinstance(columns, list):
            selected_columns = columns
        else:
            selected_columns = [col.strip() for col in columns.split(",")]

        if conditions:
            data = [row for row in data if self.evaluate_conditions(row, header, conditions)]

        if limit:
            data = data[:int(limit)]

        selected_data = []
        for row in data:
            selected_row = [row[header.index(col)] for col in selected_columns]
            selected_data.append(selected_row)

        return {"header": selected_columns, "data": selected_data}

    def evaluate_conditions(self, row, header, conditions):
        for cond in conditions:
            if cond[0] == 'AND':
                _, col, op, val = cond
            else:
                col, op, val = cond

            idx = header.index(col)
            cell = row[idx]
            if not self.apply_operator(cell, op, val):
                return False
        return True

    def apply_operator(self, cell, op, val):
        try:
            cell = float(cell)
            val = float(val)
        except ValueError:
            pass

        if op == '=': return cell == val
        elif op == '<>': return cell != val
        elif op == '<': return cell < val
        elif op == '>': return cell > val
        elif op == '<=': return cell <= val
        elif op == '>=': return cell >= val
        return False

    def execute_select(self, statement):
        kind = statement[0]
        if kind == 'select:_table':
            _, table = statement
            return self.select_table(table, '*')
        elif kind == 'select_columns':
            _, cols, table = statement
            return self.select_table(table, cols)
        elif kind == 'select_where':
            _, table, cond = statement
            return self.select_table(table, '*', [cond])
        elif kind == 'select_where_and':
            _, table, cond, conds = statement
            return self.select_table(table, '*', [cond] + conds)
        elif kind == 'select_limit':
            _, table, limit = statement
            return self.select_table(table, '*', None, limit)
        elif kind == 'select_limit_columns':
            _, cols, table, limit = statement
            return self.select_table(table, cols, None, limit)

    def print_result(self, result):
        print(result["header"])
        for row in result["data"]:
            print(row)

    # --------- Comandos - Criação ---------

    def create_join_table(self, new_table, table1, table2, join_key):
        if table1 not in self.dictionary or table2 not in self.dictionary:
            raise ValueError("One or both tables do not exist")
        t1 = self.dictionary[table1]
        t2 = self.dictionary[table2]
        idx1 = t1["header"].index(join_key)
        idx2 = t2["header"].index(join_key)

        header = t1["header"] + [col for col in t2["header"] if col != join_key]
        data = []
        for row1 in t1["data"]:
            for row2 in t2["data"]:
                if row1[idx1] == row2[idx2]:
                    joined_row = row1 + [row2[i] for i in range(len(row2)) if i != idx2]
                    data.append(joined_row)
        self.dictionary[new_table] = {"header": header, "data": data}

    def create_select_columns(self, new_table, columns, source_table):
        result = self.select_table(source_table, columns)
        self.dictionary[new_table] = result

    # --------- Procedimentos ---------

    def call_procedure(self, name):
        if name not in self.procedures:
            raise ValueError("Procedure does not exist")
        statements = self.procedures[name]
        for statement in statements:
            self.start(';'.join([self.statement_to_string(stmt) for stmt in statements]))

    def statement_to_string(self, stmt):
        # Simplified for demo purposes — you can improve this
        return str(stmt)
