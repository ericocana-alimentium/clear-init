from models.ConnectaAlimentiumModel import ConnectaAlimentiumModel
from controllers.BaseController import BaseController

class ConnectaAlimentiumController(BaseController):
    def __init__(self, db_name):
        super().__init__(db_name)
        self.codigos_aeme = None
        self.productos_agentes = []

    def cambiar_base_datos(self, nueva_bd):
        """
        Cambia la base de datos actual.
        """
        if not self.db or not self.db.cursor:
            self.connect_to_db()

        self.db.cambiar_base_datos(nueva_bd)

    def crear_tabla_temporal(self, idcAgente, modulo):
        """
        Crea la tabla temporal en la base de datos `Connecta_Alimentium`.
        """
        if not self.db or not self.db.cursor:
            self.connect_to_db()
        
        connecta_model = ConnectaAlimentiumModel(self.db.cursor)
        self.datos_aeme = connecta_model.crear_tabla_temporal(idcAgente, modulo)
        self.codigos_aeme = [dato[1] for dato in self.datos_aeme]
        return self.codigos_aeme
    def obtener_productos_agentes(self):

        """
        Obtiene los productos de la tabla `dbo.ProductosAgentes` usando la tabla temporal.
        """

        if not self.db or not self.db.cursor:
            self.connect_to_db()
        
        connecta_model = ConnectaAlimentiumModel(self.db.cursor)
        self.productos_agentes = connecta_model.obtener_productos_agentes(self.codigos_aeme)

        return self.productos_agentes

    def generar_queries_connecta(self):
        """
        Genera las queries necesarias para limpiar los datos en la base de datos Connecta_Alimentium.
        Usa las listas y las queries generadas previamente.
        """
        if not self.productos_agentes:
            raise ValueError("No se encontraron productos agentes. Asegúrese de haber ejecutado `obtener_productos_agentes` primero.")
        
        connecta_model = ConnectaAlimentiumModel(self.db.cursor)
        queries = connecta_model.generar_queries(self.productos_agentes)
        return queries

    def close_connection(self):
        self.close_db()
