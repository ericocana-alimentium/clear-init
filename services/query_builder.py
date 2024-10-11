import pyodbc
from services.error_handler import ErrorHandler

class QueryBuilder:
    def __init__(self, cursor):
        self.cursor = cursor

    def build_query(self, action, table, attributes=None, into = None ,conditions=None, values=None, joins=None):

        """
        Construye la query basada en los parámetros proporcionados, pero no la ejecuta.
        """

        query = ""

        # SELECT y SELECT INTO
        if action == "SELECT" or action == "SELECT INTO":
            columns = ", ".join(attributes) if attributes else "*"
            query = f"SELECT {columns}"
            
            # Añadimos la cláusula INTO si está presente y si la acción es "SELECT INTO"
            if action == "SELECT INTO" and into:
                query += f" INTO {into}"

            query += f" FROM {table}"

            if joins:
                for join in joins:
                    query += f" {join['type']} {join['table']} ON {join['on']}"

            if conditions:
                where_clauses = []
                for key, value in conditions.items():
                    # Si el valor parece una función SQL, no lo envuelvas en comillas
                    if isinstance(value, str) and "(" in value and ")" in value:
                        where_clauses.append(f"{key} = {value}")
                    elif isinstance(value, list):  # Manejo de listas con IN
                        value_list = ", ".join(f"'{item}'" if isinstance(item, str) else str(item) for item in value)
                        where_clauses.append(f"{key} IN ({value_list})")
                    else:
                        where_clauses.append(f"{key} = '{value}'" if isinstance(value, str) else f"{key} = {value}")

                where_clause = " AND ".join(where_clauses)
                query += f" WHERE {where_clause}"

        # UPDATE (SQL Server con JOIN)
        elif action == "UPDATE":
            set_clause = ", ".join([f"{k} = '{v}'" if isinstance(v, str) else f"{k} = {v}" for k, v in values.items()])
            query = f"UPDATE {table} SET {set_clause}"

            # Para SQL Server, al hacer un UPDATE con JOIN, necesitamos especificar el FROM para las tablas relacionadas
            if joins:
                query += f" FROM {table}"  # Especificamos que el UPDATE es en esta tabla
                for join in joins:
                    query += f" {join['type']} {join['table']} ON {join['on']}"

            if conditions:
                where_clauses = []
                for key, value in conditions.items():
                    if isinstance(value, list):  # Handle lists with IN
                        value_list = ", ".join(f"'{item}'" if isinstance(item, str) else str(item) for item in value)
                        where_clauses.append(f"{key} IN ({value_list})")
                    elif isinstance(value, str) and (value.startswith("wfl.") or value.startswith("dbo.") or value.startswith("ftc.")):
                        where_clauses.append(f"{key} = {value}")
                    else:
                        where_clauses.append(f"{key} = '{value}'" if isinstance(value, str) else f"{key} = {value}")

                where_clause = " AND ".join(where_clauses)
                query += f" WHERE {where_clause}"

        # DELETE (SQL Server con JOIN)
        elif action == "DELETE":
            query = f"DELETE {table} FROM {table}"  # Aquí se repite la tabla para SQL Server

            if joins:
                for join in joins:
                    query += f" {join['type']} {join['table']} ON {join['on']}"

            if conditions:
                where_clauses = []
                for key, value in conditions.items():
                    if isinstance(value, list):  # Handle lists with IN
                        value_list = ", ".join(f"'{item}'" if isinstance(item, str) else str(item) for item in value)
                        where_clauses.append(f"{key} IN ({value_list})")
                    elif isinstance(value, str) and (value.startswith("wfl.") or value.startswith("dbo.") or value.startswith("ftc.")):
                        where_clauses.append(f"{key} = {value}")
                    else:
                        where_clauses.append(f"{key} = '{value}'" if isinstance(value, str) else f"{key} = {value}")

                where_clause = " AND ".join(where_clauses)
                query += f" WHERE {where_clause}"

        return query

    def execute_query(self, query, allow_modifications=False):
        try:
            print(f"Query construida: {query}")
            
            # Validar si la query es una modificación y si está permitida
            if not allow_modifications and not query.strip().upper().startswith("SELECT"):
                raise ValueError("Las modificaciones no están permitidas con esta configuración.")
            
            self.cursor.execute(query)  # Ejecutar la query
            
            # Verificar si es un SELECT para intentar obtener resultados
            if query.strip().upper().startswith("SELECT") and "INTO" not in query.strip().upper():
                return self.cursor.fetchall()
            else:
                # Si no es un SELECT que devuelva resultados, confirmar la transacción
                self.cursor.connection.commit()
                print("Modificación ejecutada exitosamente")
                return None

        except Exception as e:
            ErrorHandler.handle_error(e, query)
            return None