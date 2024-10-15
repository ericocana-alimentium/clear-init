from models.ConnectaAlimentiumModel import ConnectaAlimentiumModel
from controllers.BaseController import BaseController
from services.error_handler import ErrorHandler
import os
from datetime import datetime

class ConnectaAlimentiumController(BaseController):
    def __init__(self, db_name):
        super().__init__(db_name)
        self.codigos_aeme = None
        self.productos_agentes = []
        self.queries = []
        self.datos = []

    def cambiar_base_datos(self, nueva_bd):
        """
        Cambia la base de datos actual.
        """
        if not self.db or not self.db.cursor:
            self.connect_to_db()

        self.db.cambiar_base_datos(nueva_bd)

    def crear_tabla_temporal(self, idcAgente, modulo):
        """
        Llama a la función del modelo para crear la tabla temporal y guarda la query generada.
        """
        self.cambiar_base_datos("Connecta_Alimentium")

        try:
            connecta_model = ConnectaAlimentiumModel(self.db.cursor)

            self.idcAgente = idcAgente
            self.modulo = modulo

            self.datos, create_query = connecta_model.crear_tabla_temporal(idcAgente, modulo)
            
            if create_query:
                # Guardar la query en la lista de queries del controlador
                self.queries.append(create_query)
                print(f"Query de creación de tabla temporal almacenada: {create_query}")
                return self.datos, create_query
            else:
                print("No se generó ninguna query para la creación de la tabla temporal.")
                return None


        except Exception as e:
            print(f"Error al crear la tabla temporal desde el controlador: {str(e)}")
            ErrorHandler.handle_error(e, "Error al crear la tabla temporal en el controlador Connecta_Alimentium")
            return None

    def obtener_productos_agentes(self, datos):
        """
        Llama a la función del modelo para obtener productos agentes basados en la tabla temporal.
        """
        try:
            print(f"{self.datos}")
            connecta_model = ConnectaAlimentiumModel(self.db.cursor)
            self.codigos_aeme = [dato[1] for dato in datos]
            if not self.codigos_aeme:
                print("Error controller: self.datos_aeme está vacía o no se llenó correctamente en el modelo.")
            else:
                print(f"Datos de self.datos_aeme en el controlador: {self.codigos_aeme}")

            result = connecta_model.obtener_productos_agentes(self.codigos_aeme, self.idcAgente)

            return result

        except Exception as e:
            print(f"Error al obtener productos agentes desde el controlador: {str(e)}")
            ErrorHandler.handle_error(e, "Error al obtener productos agentes en el controlador Connecta_Alimentium")
            return None
        
    
        
    def generar_queries(self,tarea_id, folder_path, autor):
        """
        Genera el archivo SQL con las queries almacenadas.
        """
        fecha_actual = datetime.now().strftime("%Y%m%d")
        tarea_id_num = tarea_id.split('-')[1]
        filename = f"{fecha_actual}-{tarea_id_num}-000-DAT-limpieza-{self.modulo}.sql"
        full_path = os.path.join(folder_path, filename)

        # Generar el encabezado del archivo
        header = f"""
/*
* LINK TAREA: https://app.clickup.com/t/36671967/{tarea_id}
* DESCRIPCIÓN: Script de limpieza para {self.modulo} - {self.idcAgente}
*
* AUTOR: {autor}
* FECHA CREACIÓN: {fecha_actual}
* FECHA DESPLIEGUE DESARROLLO:
* FECHA DESPLIEGUE PRE-PRODUCCIÓN:
* FECHA DESPLIEGUE PRODUCCIÓN:
*/
-------------------------------------------------------------------------------------
--- 
-------------------------------------------------
--- 
-------------------------------------------------
BEGIN TRAN
"""       
        try:
            #connecta_model = ConnectaAlimentiumModel(self.db.cursor)
            #self.queries.append(connecta_model.generar_query_update_productos(self.idcAgente))
            #self.queries.append(connecta_model.generar_query_delete_multimedia(self.idcAgente))
            #self.queries.append(connecta_model.generar_query_delete_productos_agentes(self.idcAgente))


            # Abrir el archivo SQL para escribir
            with open(full_path, 'w') as sql_file:
                # Escribir el encabezado en el archivo
                sql_file.write(header)

                # Formatear y escribir cada query en el archivo
                for query in self.queries:
                    # Reemplazos para darle formato a la query
                    formatted_query = query.replace(" FROM ", "\nFROM ")
                    formatted_query = formatted_query.replace(" WHERE ", "\nWHERE ")
                    formatted_query = formatted_query.replace(" AND ", "\nAND ")
                    formatted_query = formatted_query.replace(" OR ", "\nOR ")

                    # Mantener JOIN y ON en la misma línea
                    formatted_query = formatted_query.replace(" INNER JOIN ", "\nINNER JOIN ")
                    formatted_query = formatted_query.replace(" LEFT JOIN ", "\nLEFT JOIN ")
                    formatted_query = formatted_query.replace(" RIGHT JOIN ", "\nRIGHT JOIN ")
                    formatted_query = formatted_query.replace(" ON ", " ON ")

                    # Escribir la query formateada con GO al final
                    sql_file.write(formatted_query + ";\nGO\n\n")

                # Agregar el final del script
                sql_file.write("GO\n--COMMIT\nROLLBACK\n")

                print(f"Archivo SQL generado correctamente en: {full_path}")
                return full_path

        except Exception as e:
            print(f"Error al generar el archivo SQL: {str(e)}")
            return str(e)
    def close_connection(self):
        self.close_db()
