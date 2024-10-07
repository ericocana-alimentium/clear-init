import pyodbc

class DBConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.db_host = "10.0.3.5,1433"  # IP del servidor
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = pyodbc.connect(
                f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.db_host};DATABASE={self.db_name};UID=cproject_developer;PWD=10549971ea#E32!!'
            )
            self.cursor = self.connection.cursor()  # Inicializamos el cursor correctamente
            print(f"Conectado a la base de datos: {self.db_name}")
        except pyodbc.Error as e:
            print(f"Error al conectar a la base de datos: {e}")

    def close(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()
            print("Conexión cerrada")

