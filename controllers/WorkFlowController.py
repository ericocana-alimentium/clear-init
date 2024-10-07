from models.WorkFlowAgenteModel import WorkFlowAgenteModel 
from controllers.BaseController import BaseController

class WorkFlowController(BaseController):
    def __init__(self, db_name):
        super().__init__(db_name)
        self.list_productos = []
        self.list_procesos = []
        self.ficha_tecnica_ids = []
        self.list_productos_procesados = []
        
    def validate_agente_modulo(self, idcAgente, modulo):
        
        if not self.db or not self.db.cursor:
            self.connect_to_db()

        workflow_model = WorkFlowAgenteModel(self.db.cursor)
        result = workflow_model.check_agente_modulo(idcAgente, modulo)

        return result

    def get_db_ip(self):

        if self.db is None:
            self.connect_to_db()

        if self.db and hasattr(self.db, 'db_host'):
            return self.db.db_host
        else:
            raise AttributeError("No se pudo obtener la IP de la base de datos. La conexión no está inicializada.")
    
    def get_total_procesos(self, modulo):
        """
        Actualiza y usa la lista `list_procesos` para almacenar el resultado de `get_total_procesos`.
        """
        workflow_model = WorkFlowAgenteModel(self.db.cursor)
        self.list_procesos = workflow_model.get_total_procesos(modulo)
        return self.list_procesos

    def get_total_productos(self, idcAgente):
        """
        Actualiza y usa la lista `list_productos` para almacenar el resultado de `get_total_productos`.
        """
        if not self.db or not self.db.cursor:
            self.connect_to_db()
        workflow_model = WorkFlowAgenteModel(self.db.cursor)
        self.list_productos = workflow_model.get_total_productos(idcAgente)
        return self.list_productos

    def get_productos_procesados(self, idcAgente):
        """
        Usa la lista `list_procesos` y actualiza `list_productos` con los productos procesados.
        """
        if not self.list_procesos:  
            raise ValueError("La lista de procesos está vacía. Llama a `get_total_procesos` primero.")
        
        workflow_model = WorkFlowAgenteModel(self.db.cursor)
        producto_organizacion_ids = [proceso[2] for proceso in self.list_procesos]
        print(f"Estoy en el controller:{producto_organizacion_ids}")
        self.list_productos_procesados = workflow_model.get_productos_procesados(producto_organizacion_ids, idcAgente)
        return self.list_productos_procesados

    def get_ficha_tecnica_ids(self):

        """
        Usa `list_productos` para obtener los `producto_ids` y actualiza `ficha_tecnica_ids` con los resultados.
        """

        if not self.list_productos: 
            raise ValueError("La lista de productos está vacía. Llama a `get_productos_procesados` primero.")
        
        workflow_model = WorkFlowAgenteModel(self.db.cursor)
        producto_ids = [producto[0] for producto in self.list_productos_procesados]
        self.ficha_tecnica_ids = workflow_model.get_ficha_tecnica_ids(producto_ids)
        return self.ficha_tecnica_ids

    def generar_queries_aemedb(self,  idcAgente, modulo):

    
        """
        Genera las queries de limpieza para AemeDb usando el modelo y aplicando INNER JOIN.
        """
        if not self.db or not self.db.cursor:
            self.connect_to_db()

        # Instanciamos el modelo y delegamos la generación de queries
        workflow_model = WorkFlowAgenteModel(self.db.cursor)
        idcAgente = int(idcAgente)
        # El modelo se encarga de construir las queries con INNER JOIN sin usar listas
        queries = workflow_model.generar_queries(idcAgente, modulo)

        return queries
    
    def close_connection(self):
        self.close_db()