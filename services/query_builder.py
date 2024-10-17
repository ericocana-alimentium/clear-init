import pyodbc
from services.error_handler import ErrorHandler

class QueryBuilder:
    def __init__(self, cursor):
        self.cursor = cursor

    def build_query(self, action, table, attributes=None, conditions=None, values=None, joins=None, into=None, from_table=None, delete_from_alias = None):
        """
        Construye la query basada en los parámetros proporcionados, pero no la ejecuta.
        """
        query = ""

        # SELECT o SELECT INTO
        if action == "SELECT" or action == "SELECT INTO":
            columns = ", ".join(attributes) if attributes else "*"

            # Si el parámetro into está presente, significa que es un SELECT INTO
            if into:
                query = f"SELECT {columns} INTO {into} FROM {table}"
            else:
                query = f"SELECT {columns} FROM {table}"

            if joins:
                for join in joins:
                    query += f" {join['type']} {join['table']} ON {join['on']}"

            if conditions:
                where_clauses = []
                for key, value in conditions.items():
                    # Detectar funciones SQL o columnas con ciertos prefijos
                    if isinstance(value, str) and ("(" in value and ")" in value):
                        where_clauses.append(f"{key} = {value}")  # No agregar comillas si es una función
                    elif isinstance(value, str) and (value.startswith("wfl.") or value.startswith("ftc.") or value.startswith("dbo.") or value.startswith("atr.")):
                        where_clauses.append(f"{key} = {value}")  # No agregar comillas si tiene estos prefijos
                    elif isinstance(value, list):  # Handle lists with IN
                        value_list = ", ".join(f"'{item}'" if isinstance(item, str) else str(item) for item in value)
                        where_clauses.append(f"{key} IN ({value_list})")
                    else:
                        where_clauses.append(f"{key} = '{value}'" if isinstance(value, str) else f"{key} = {value}")

                where_clause = " AND ".join(where_clauses)
                query += f" WHERE {where_clause}"

        # UPDATE y DELETE siguen la misma lógica, con sus propias cláusulas.
        elif action == "UPDATE":
            table_name = table.split()[0]  # Obtener solo el nombre de la tabla sin alias

            # Comenzar la query de actualización sin alias en la parte del UPDATE
            query = f"UPDATE {table_name} SET " + ", ".join(f"{k} = '{v}'" for k, v in values.items())

            if joins:
                query += f" FROM {from_table if from_table else table}"  # Usar from_table si está presente
                for join in joins:
                    query += f" {join['type']} {join['table']} ON {join['on']}"

            if conditions:
                where_clauses = []
                for key, value in conditions.items():
                    if isinstance(value, dict) and 'not_in' in value:  # Manejar NOT IN
                        value_list = ", ".join(f"'{item}'" if isinstance(item, str) else str(item) for item in value['not_in'])
                        where_clauses.append(f"{key} NOT IN ({value_list})")
                    elif isinstance(value, list):  # Manejar listas con IN
                        value_list = ", ".join(f"'{item}'" if isinstance(item, str) else str(item) for item in value)
                        where_clauses.append(f"{key} IN ({value_list})")
                    elif isinstance(value, str) and ("(" in value and ")" in value):  # No agregar comillas si es una función
                        where_clauses.append(f"{key} = {value}")
                    else:
                        where_clauses.append(f"{key} = '{value}'" if isinstance(value, str) else f"{key} = {value}")

                where_clause = " AND ".join(where_clauses)
                query += f" WHERE {where_clause}"

        elif action == "DELETE":
            table_name = table.split()[0]  # Obtener solo el nombre de la tabla sin alias
        
            if delete_from_alias and from_table:
                query = f"DELETE {delete_from_alias} FROM {from_table}"  # Usar el alias en el DELETE y una tabla diferente en el FROM
            elif from_table:
                query = f"DELETE {table_name} FROM {from_table}"
            elif delete_from_alias:
                query = f"DELETE {delete_from_alias} FROM {table}"  # Usar el alias en el DELETE y la tabla en el FROM
            else:
                query = f"DELETE {table_name} FROM {table}"  # Usar el nombre de la tabla en el DELETE y el FROM
            

            if joins:
                for join in joins:
                    query += f" {join['type']} {join['table']} ON {join['on']}"

            if conditions:
                where_clauses = []
                for key, value in conditions.items():
                    if isinstance(value, dict) and 'not_in' in value:  # Manejar NOT IN
                        if isinstance(value['not_in'], str):  # Si es una subconsulta, no agregar comillas
                            where_clauses.append(f"{key} NOT IN {value['not_in']}")
                        else:  # Si es una lista de valores, formatear correctamente
                            value_list = ", ".join(f"'{item}'" if isinstance(item, str) else str(item) for item in value['not_in'])
                            where_clauses.append(f"{key} NOT IN ({value_list})")
                    elif isinstance(value, list):  # Manejar listas con IN
                        value_list = ", ".join(f"'{item}'" if isinstance(item, str) else str(item) for item in value)
                        where_clauses.append(f"{key} IN ({value_list})")
                    elif isinstance(value, str) and ("(" in value and ")" in value):  # No agregar comillas si es una función o subconsulta
                        where_clauses.append(f"{key} = {value}")
                    else:
                        where_clauses.append(f"{key} = '{value}'" if isinstance(value, str) else f"{key} = {value}")

                where_clause = " AND ".join(where_clauses)
                query += f" WHERE {where_clause}"

        print(f"Query final: {query}")
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