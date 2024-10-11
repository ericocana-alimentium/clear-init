from services.query_builder import QueryBuilder
from services.error_handler import ErrorHandler

class ConnectaAlimentiumModel:
    def __init__(self, cursor):
        self.cursor = cursor
        self.query_builder = QueryBuilder(cursor)
        self.queries = []
        self.datos_aeme = []

    def crear_tabla_temporal(self, idcAgente, modulo):

        """
        Crea la tabla temporal en la base de datos `Connecta_Alimentium` utilizando el query_builder.
        """
        # Imprimir los parámetros para asegurarnos de que son correctos
        # Query para eliminar la tabla temporal si existe

        try:
            drop_query = "DROP TABLE IF EXISTS Connecta_Alimentium..#tpAemeDatos"
            self.query_builder.execute_query(drop_query, allow_modifications=True)

            # Construir la query utilizando el query_builder
            create_query = self.query_builder.build_query(
                action="SELECT INTO",

                table="AeMeDb..ProductoOrganizacion",

                attributes=[
                    "AeMeDb..ProductoOrganizacion.Id AS ProductoOrganizacionId",
                    "AeMeDb..ProductoOrganizacion.Codigo"
                ],

                into="Connecta_Alimentium..#tpAemeDatos",

                joins=[
                    {
                        "type": "INNER JOIN",
                        "table": "AeMeDb.wfl.ProcesoWorkFlow",
                        "on": "AeMeDb..ProductoOrganizacion.Id = AeMeDb.wfl.ProcesoWorkFlow.ProductoOrganizacionId"
                    }
                ],

                conditions={
                    "AeMeDb..ProductoOrganizacion.idcAgente": idcAgente,
                    "AeMeDb.wfl.ProcesoWorkFlow.WorkflowId": f"AeMeDb.wfl.GetModuloAgenteId('{modulo}')"
                }

            )

            # Añadir la query a la lista y ejecutarla
            self.queries.append(create_query)
            # Ejecutar la query en el contexto adecuado
            self.query_builder.execute_query(create_query, allow_modifications=True)

            select_query = self.query_builder.build_query(
                        action="SELECT",
                        table="#tpAemeDatos",
                        attributes=["*"]
                    )
                    
                    # Ejecutar la query para seleccionar los datos de la tabla temporal
            self.datos_aeme = self.query_builder.execute_query(select_query)
            return create_query
        except Exception as e:

            print(f"Error al crear la tabla temporal: {str(e)}")
            ErrorHandler.handle_error(e, "Error al crear la tabla temporal en Connecta_Alimentium")
            return None

    def obtener_productos_agentes(self):

        """
        Obtiene los productos de la tabla `dbo.ProductosAgentes` usando los códigos obtenidos 
        de la tabla temporal almacenada en `self.datos_aeme`.
        """

        try:
            # Validamos que `self.datos_aeme` tenga datos antes de iterar
            if not self.datos_aeme or len(self.datos_aeme) == 0:
                print("Error: self.datos_aeme está vacía o no se llenó correctamente.")
                return None

            # Extraer los códigos de la segunda posición de cada tupla en self.datos_aeme
            codigos_productos = [dato[1] for dato in self.datos_aeme]

            # Construir la query para obtener los productos agentes
            query = self.query_builder.build_query(
                action="SELECT",
                table="dbo.ProductosAgentes",
                attributes=[
                    "IdcAgente",
                    "IdcProducto",
                    "Codigo",
                    "Status",
                    "IdcFabricante"
                ],

                conditions={
                    "Codigo": codigos_productos  # Usamos la lista de códigos
                }
            )

            result = self.query_builder.execute_query(query)

            return result

        except Exception as e:
            # Manejo de errores
            print(f"Error al obtener productos agentes: {str(e)}")
            ErrorHandler.handle_error(e, "Error al obtener productos agentes de Connecta_Alimentium")
            return None



    def __getattribute__(self, name):
        return super().__getattribute__(name)