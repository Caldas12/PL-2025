from parser import Parser
import csv

class Interpreter:
    """
    Interpretador para uma linguagem simples de consultas baseada em tabelas.

    Esta classe fornece métodos para importar, exportar, manipular e consultar dados tabulares armazenados em ficheiros CSV.
    Suporta operações básicas semelhantes a SQL, como SELECT, WHERE, LIMIT, JOIN e procedimentos.
    """

    def __init__(self):
        """
        Atributos:
            parser (Parser): Instância da classe Parser para analisar comandos de entrada.
            dictionary (dict): Armazena tabelas por nome, cada uma como um dicionário com as chaves 'header' e 'data'.
            procedures (dict): Armazena procedimentos definidos pelo utilizador por nome.
        """
        self.parser = Parser()
        self.dictionary = {}
        self.procedures = {}

    def start(self, input_string):
        """
        Analisa e executa uma sequência de comandos a partir da string de entrada.
        """
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
            elif stmt in ('select_table', 'select_columns', 'select_where', 'select_where_and', 'select_limit', 'select_limit_columns'):
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
        """
        Lê um ficheiro CSV e devolve o seu conteúdo como um dicionário com 'header' e 'data'.
        """
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
        """
        Escreve a tabela especificada num ficheiro CSV.
        """
        if table_name not in self.dictionary:
            raise ValueError("Table does not exist")
        table = self.dictionary[table_name]
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(table["header"])
            for row in table["data"]:
                writer.writerow(row)

    def import_table(self, table_name, file_path):
        """
        Importa uma tabela de um ficheiro CSV e armazena-a com o nome dado.
        """
        if table_name in self.dictionary:
            raise ValueError("Table already exists")
        data = self.read_file(file_path)
        self.dictionary[table_name] = data

    def rename_table(self, old_name, new_name):
        """
        Altera o nome de uma tabela existente.
        """
        if old_name not in self.dictionary:
            raise ValueError("Table does not exist")
        self.dictionary[new_name] = self.dictionary.pop(old_name)

    def discard_table(self, table_name):
        """
        Remove uma tabela do dicionário.
        """
        if table_name not in self.dictionary:
            raise ValueError("Table does not exist")
        del self.dictionary[table_name]

    def print_table(self, table_name):
        """
        Imprime o cabeçalho e as linhas da tabela especificada.
        """
        if table_name not in self.dictionary:
            raise ValueError("Table does not exist")
        table = self.dictionary[table_name]
        print(table["header"])
        for row in table["data"]:
            print(row)

    # --------- Comandos - Queries ---------

    def select_table(self, table_name, columns, conditions=None, limit=None):
        """
        Seleciona colunas e linhas de uma tabela, podendo filtrar por condições e limitar o número de linhas.
        """
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
        """
        Avalia uma lista de condições numa linha da tabela.
        """
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
        """
        Aplica um operador de comparação entre o valor de uma célula e um valor dado.
        """
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
        """
        Executa uma instrução SELECT analisada e devolve o resultado.
        """
        kind = statement[0]

        if kind == 'select_table':
            _, cols, table = statement
            return self.select_table(table, cols)
        
        elif kind == 'select_columns':
            _, cols, table = statement
            return self.select_table(table, cols)

        elif kind == 'select_where':
            _, table, cond = statement
            return self.select_table(table, '*', cond)

        elif kind == 'select_where_and':
            _, table, cond = statement
            return self.select_table(table, '*', cond)
        
        elif kind == 'select_limit':
            _, table, limit = statement
            return self.select_table(table, '*', None, limit)
        
        elif kind == 'select_limit_columns':
            _, cols, table, limit = statement
            return self.select_table(table, cols, None, limit)
        
        else:
            raise ValueError(f"Unknown select kind: {kind}")
        
    def print_result(self, result):
        """
        Imprime o cabeçalho e as linhas de um resultado de consulta.
        """
        print(result["header"])
        for row in result["data"]:
            print(row)

    # --------- Comandos - Criação ---------

    def create_join_table(self, new_table, table1, table2, join_key):
        """
        Cria uma nova tabela juntando duas tabelas por uma chave especificada.
        """
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
        """
        Cria uma nova tabela selecionando colunas específicas de uma tabela existente.
        """
        result = self.select_table(source_table, columns)
        self.dictionary[new_table] = result

    # --------- Procedimentos ---------

    def create_procedure(self, name, statements):
        """
        Cria um procedimento guardado pelo nome.
        """
        if name in self.procedures:
            raise ValueError("Procedure already exists")
        self.procedures[name] = statements
        return f"Procedure {name} created"
    
    def call_procedure(self, name):
        """
        Executa um procedimento guardado pelo nome.
        """
        if name not in self.procedures:
            raise ValueError("Procedure does not exist")
        
        statements = self.procedures[name]
        for statement in statements:
            print(statement)
            stmt_type = statement[0]

            if stmt_type == 'print':
                self.print_table(statement[1])
            elif stmt_type in ('select_table', 'select_columns', 'select_where', 'select_where_and', 'select_limit', 'select_limit_columns'):
                result = self.execute_select(statement)
                self.print_result(result)
            elif stmt_type == 'import':
                self.import_table(statement[1], statement[2])
            elif stmt_type == 'export':
                self.write_file(statement[1], statement[2])
            elif stmt_type == 'discard':
                self.discard_table(statement[1])
            elif stmt_type == 'rename':
                self.rename_table(statement[1], statement[2])
            elif stmt_type == 'create_from_query':
                result = self.execute_select(statement[2])
                self.dictionary[statement[1]] = result
            elif stmt_type == 'create_join':
                self.create_join_table(*statement[1:])
            elif stmt_type == 'create_select_columns':
                self.create_select_columns(*statement[1:])
            elif stmt_type == 'procedure':
                self.procedures[statement[1]] = statement[2]
            elif stmt_type == 'call':
                self.call_procedure(statement[1])
            else:
                raise ValueError(f"Unknown statement type: {stmt_type}")

    def statement_to_string(self, stmt):
        kind = stmt[0]
        
        if kind == 'print':
            return f"PRINT TABLE {stmt[1]}"
        
        elif kind == 'import':
            return f"IMPORT TABLE {stmt[1]} FROM '{stmt[2]}'"
        
        elif kind == 'export':
            return f"EXPORT TABLE {stmt[1]} AS '{stmt[2]}'"
        
        elif kind == 'discard':
            return f"DISCARD TABLE {stmt[1]}"
        
        elif kind == 'rename':
            return f"RENAME TABLE {stmt[1]} TO {stmt[2]}"
        
        elif kind == 'select_table':
            return f"SELECT * FROM {stmt[2]}"
        
        elif kind == 'select_columns':
            cols = ', '.join(stmt[1])
            return f"SELECT {cols} FROM {stmt[2]}"
        
        elif kind == 'select_where':
            cond = self.condition_to_string(stmt[2])
            return f"SELECT * FROM {stmt[1]} WHERE {cond}"
        
        elif kind == 'select_where_and':
            cond = ' AND '.join(self.condition_to_string(c) for c in stmt[2])
            return f"SELECT * FROM {stmt[1]} WHERE {cond}"
        
        elif kind == 'select_limit':
            return f"SELECT * FROM {stmt[1]} LIMIT {stmt[2]}"
        
        elif kind == 'select_limit_columns':
            cols = ', '.join(stmt[1])
            return f"SELECT {cols} FROM {stmt[2]} LIMIT {stmt[3]}"
        
        elif kind == 'call':
            return f"CALL {stmt[1]}"
        
        else:
            raise NotImplementedError(f"statement_to_string not implemented for '{kind}'")