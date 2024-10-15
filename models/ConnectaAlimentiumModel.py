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
        try:
            # Eliminar la tabla temporal si ya existe
            drop_query = "IF OBJECT_ID('tempdb..#tpAemeDatos') IS NOT NULL DROP TABLE #tpAemeDatos"
            self.query_builder.execute_query(drop_query, allow_modifications=True)

            # Construir la query para crear la tabla temporal
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

            # Ejecutar la query para crear la tabla temporal
            self.query_builder.execute_query(query, allow_modifications=True)

            # Query para obtener los datos de la tabla temporal
            select_query = "SELECT * FROM #tpAemeDatos"
            datos_aeme = self.query_builder.execute_query(select_query)

            if datos_aeme:
                return datos_aeme, query
            else:
                raise ValueError("No se encontraron datos en la tabla temporal")

        except Exception as e:
            print(f"Error al crear la tabla temporal: {str(e)}")
            return [], None  # Devolver una lista vacía y None en caso de error
        
    def generar_query_update_productos(self, idcAgente):
        """
        Genera la query de actualización (UPDATE) para la tabla ProductosAgentes sin usar alias.
        """
        try:
            # Construir la query utilizando el query_builder sin alias
            update_query = self.query_builder.build_query(
                action="UPDATE",
                table="dbo.Productos",  
                values={"Status": "AC"},  # SET Status = 'AC'
                joins=[
                    {
                        "type": "INNER JOIN",
                        "table": "#tpAemeDatos",  
                        "on": "#tpAemeDatos.Codigo = dbo.Productos.Codigo"  
                    }
                ],
                conditions={
                    "dbo.Productos.IdcAgente": idcAgente  
                }
            )

            print(f"Query de UPDATE generada: {update_query}")
            return update_query

        except Exception as e:
            print(f"Error al generar la query de UPDATE: {str(e)}")
            return None
            
    def generar_query_delete_multimedia(self, idcAgente):
        """
        Genera la query DELETE para la tabla Multimedia sin alias.
        """
        try:
            # Construir la query utilizando el query_builder sin alias
            delete_query = self.query_builder.build_query(
                action="DELETE",
                table="dbo.Multimedia",  
                joins=[
                    {
                        "type": "INNER JOIN",
                        "table": "#tpAemeDatos",  
                        "on": "#tpAemeDatos.Codigo = dbo.Multimedia.Ejeproducto"  
                    },
                    {
                        "type": "INNER JOIN",
                        "table": "dbo.ProductosAgentes",  
                        "on": "dbo.ProductosAgentes.Codigo = #tpAemeDatos.Codigo"  
                    },
                    {
                        "type": "INNER JOIN",
                        "table": "dbo.Productos",  
                        "on": "dbo.Productos.IdcProducto = dbo.ProductosAgentes.IdcProducto"  
                    },
                    {
                        "type": "INNER JOIN",
                        "table": "dbo.ProductosAgentes",  
                        "on": "dbo.ProductosAgentes.IdcAgente = dbo.Productos.IdcFabricante AND dbo.ProductosAgentes.IdcProducto = dbo.ProductosAgentes.IdcProducto"  
                    }
                ],
                conditions={
                    "dbo.ProductosAgentes.IdcAgente": idcAgente  
                }
            )

            print(f"Query de DELETE generada para Multimedia: {delete_query}")
            return delete_query

        except Exception as e:
            print(f"Error al generar la query de DELETE para Multimedia: {str(e)}")
            return None
    
    def generar_query_delete_productos_agentes(self, idcAgente):
        """
        Genera la query DELETE para la tabla ProductosAgentes sin alias.
        """
        try:
            # Construir la query utilizando el query_builder sin alias
            delete_query = self.query_builder.build_query(
                action="DELETE",
                table="dbo.ProductosAgentes",  
                joins=[
                    {
                        "type": "INNER JOIN",
                        "table": "#tpAemeDatos",  
                        "on": "#tpAemeDatos.Codigo = dbo.ProductosAgentes.Codigo"  
                    }
                ],
                conditions={
                    "dbo.ProductosAgentes.IdcAgente": idcAgente  
                }
            )

            print(f"Query de DELETE generada para ProductosAgentes: {delete_query}")
            return delete_query

        except Exception as e:
            print(f"Error al generar la query de DELETE para ProductosAgentes: {str(e)}")
            return None

    def obtener_productos_agentes(self, codigos_aeme, idcAgente):

        """
        Obtiene los productos de la tabla `dbo.ProductosAgentes` usando los códigos obtenidos 
        de la tabla temporal almacenada en `self.datos_aeme`.
        """

        try:
            # Validamos que `self.datos_aeme` tenga datos antes de iterar
            if not codigos_aeme or len(codigos_aeme) == 0:
                print("Error: self.datos_aeme está vacía o no se llenó correctamente.")
                return None

            # Extraer los códigos de la segunda posición de cada tupla en self.datos_aeme
            # codigos_productos = [dato[1] for dato in codigos_aeme]

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
                    "Codigo": codigos_aeme, "IdcAgente": idcAgente  # Usamos la lista de códigos
                }
            )

            result = self.query_builder.execute_query(query)

            return result

        except Exception as e:
            print(f"Error al obtener productos agentes: {str(e)}")
            ErrorHandler.handle_error(e, "Error al obtener productos agentes de Connecta_Alimentium")
            return None

    
    def debug_datos_aeme(self):
        print(f"Estado actual de self.datos_aeme: {self.datos_aeme}, fin.")

    def __getattribute__(self, name):
        return super().__getattribute__(name)
    
