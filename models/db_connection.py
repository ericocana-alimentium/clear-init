import pyodbc

class DBConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.db_host = "10.0.3.5,1433"
        self.connection = None
        self.cursor = None
        self.db_user = "cproject_developer"
        self.db_pass = "10549971ea#E32!!"

    def connect(self):
        try:
            self.connection = pyodbc.connect(
                f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.db_host};DATABASE={self.db_name};UID={self.db_user};PWD={self.db_pass}'
            )
            
            self.cursor = self.connection.cursor()
            print(f"Conectado a la base de datos: {self.db_name}")

        except pyodbc.Error as e:
            print(f"Error al conectar a la base de datos: {e}")

    def cambiar_base_datos(self, db_name):
        try:
            self.cursor.execute(f"USE {db_name}")
            print(f"Cambiado a la base de datos: {db_name}")
        except pyodbc.Error as e:
            print(f"Error al cambiar de base de datos: {e}")

    def close(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()
            print("Conexión cerrada")