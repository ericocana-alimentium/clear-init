from services.query_builder import QueryBuilder
from services.error_handler import ErrorHandler

class ConnectaAlimentiumModel:
    def __init__(self, cursor):
        self.cursor = cursor
        self.query_builder = QueryBuilder(cursor)
        self.queries = []

    def crear_tabla_temporal(self, idcAgente, modulo):
        """
        Crea la tabla temporal en la base de datos `Connecta_Alimentium` utilizando el query_builder.
        """
        # Imprimir los parámetros para asegurarnos de que son correctos

        try:
            # Construir la query utilizando el query_builder
            query = self.query_builder.build_query(
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

            # Imprimir la query generada para ver el resultado
            print(f"Query generada: {query}")

            # Añadir la query a la lista y ejecutarla
            self.queries.append(query)
            #result = self.execute_query(query)
            print("Tabla temporal creada exitosamente.")
            #return result

        except Exception as e:
            # Manejo de errores
            print(f"Error al crear la tabla temporal: {str(e)}")
            ErrorHandler.handle_error(e, "Error al crear la tabla temporal en Connecta_Alimentium")
            return None

    def obtener_productos_agentes(self, codigos_productos):

        """
        Obtiene todos los registros de la tabla dbo.ProductosAgentes en Connecta_Alimentium usando el query_builder.
        """

        try:
            # Construir la query para obtener registros de la tabla dbo.ProductosAgentes
            query = self.query_builder.build_query(
                action="SELECT",
                table="dbo.ProductosAgentes",
                attributes=["Id", "NombreProducto", "Codigo", "FechaCreacion"]
            )

            # Ejecutar la consulta y obtener resultados
            registros = self.query_builder.execute_query(query)
            return registros

        except Exception as e:
            ErrorHandler.handle_error(e, "Error al obtener registros de dbo.ProductosAgentes")
            return None

    def __getattribute__(self, name):
        return super().__getattribute__(name)