from services.query_builder import QueryBuilder
from services.error_handler import ErrorHandler

class WorkFlowAgenteModel:
    def __init__(self, cursor):
        self.query_builder = QueryBuilder(cursor)
        self.idcAgente = None
        self.modulo = None
        self.workflow_id_function = None 


    def check_agente_modulo(self, idcAgente, modulo):
        try:

            query = self.query_builder.build_query(
                action="SELECT",
                table="wfl.WorkFlowAgente",
                attributes=["idcAgente", "Codigo"],
                conditions={"idcAgente": idcAgente, "Codigo": modulo}
            )

            result = self.query_builder.execute_query(query)
            
            return len(result) > 0
        
        except Exception as e:
            ErrorHandler.handle_error(e, query)
            return False


    def get_total_procesos(self, modulo):
        """
        Obtiene todos los procesos asociados con un módulo específico.
        Retorna todos los campos relevantes: Id, WorkflowId, ProductoOrganizacionId.
        """
        self.modulo = modulo
        self.workflow_id_function = f"wfl.GetModuloAgenteId('{self.modulo}')"

        result = self.query_builder.build_query(
            action="SELECT",
            table="wfl.ProcesoWorkFlow",
            attributes=["Id", "WorkflowId", "ProductoOrganizacionId"],
            conditions={"WorkFlowId": self.workflow_id_function}
        )

        return self.query_builder.execute_query(result)

    def get_total_productos(self, idcAgente):

        """
        Obtiene los productos necesarios usando el QueryBuilder modificado.
        El modelo construye y ejecuta la query.
        """
        self.idcAgente = idcAgente
        try:

            query = self.query_builder.build_query(
                action="SELECT",
                table="ProductoOrganizacion",
                attributes=["Id", "Codigo", "FichaTecnicaPrincipalId"],
                conditions={"IdcAgente": idcAgente}
            )

            result = self.query_builder.execute_query(query)
            return result
        except Exception as e:
            ErrorHandler.handle_error(e, query)
            return None

    def get_ficha_tecnica_ids(self, producto_organizacion_ids, modulo_agente_id):

        """
        Obtiene los FichaTecnicaId basados en los ProductoOrganizacionId y ModuloAgenteId usando QueryBuilder.
        El modelo construye y ejecuta la query.
        """

        self.workflow_id_function = f"wfl.GetModuloAgenteId('{modulo_agente_id}')"
        try:

            query = self.query_builder.build_query(
                action="SELECT",
                table="ftc.FichaTecnica",
                attributes=["Id AS FichaTecnicaId", "Codigo", "ProductoOrganizacionId", "ProcesoWorkFlowId"],
                conditions={"ProductoOrganizacionId": producto_organizacion_ids, "ModuloAgenteId": self.workflow_id_function}
            )

            result = self.query_builder.execute_query(query)
            return result
        except Exception as e:
            ErrorHandler.handle_error(e, query)
            return None

    def get_productos_procesados(self, producto_organizacion_ids, idcAgente):
        
        """
        Obtiene los productos procesados que coinciden con los ProductoOrganizacionId y el idcAgente proporcionado.
        """
        self.idcAgente = idcAgente
        try:
            
            print(f"get_productos_procesados: {producto_organizacion_ids}")
            query = self.query_builder.build_query(
                action="SELECT",
                table="ProductoOrganizacion",
                attributes=["Id", "Codigo"],
                conditions={"idcAgente": self.idcAgente, "Id": producto_organizacion_ids}
            )

            result=self.query_builder.execute_query(query)
            return result
        except Exception as e:
            ErrorHandler.handle_error(e, query)
            return None


    def generar_queries(self, idcAgente, modulo):
        """
        Genera las queries de limpieza basadas en productos que estén en ProductoOrganizacion y relacionados con ProcesoWorkFlow.
        """
        
        self.idcAgente = idcAgente
        self.workflow_id_function = f"wfl.GetModuloAgenteId('{modulo}')"
        
        queries = []
        try:
            # UPDATE para ProductoOrganizacion usando INNER JOIN con ProcesoWorkFlow
            update_query = self.query_builder.build_query(
                action="UPDATE",
                table="ProductoOrganizacion",
                values={"FichaTecnicaPrincipalId": None, "LastFichaTecnicaPrincipalId": None},
                joins=[
                    {"type": "INNER JOIN", "table": "wfl.ProcesoWorkFlow", "on": "ProductoOrganizacion.Id = wfl.ProcesoWorkFlow.ProductoOrganizacionId"}
                ],
                conditions={"ProductoOrganizacion.idcAgente": idcAgente, "wfl.ProcesoWorkFlow.WorkflowId": f"wfl.GetModuloAgenteId('{modulo}')"}
            )
            queries.append(update_query)

            # DELETE para AtributoValorFichaTecnica con INNER JOIN
            delete_atributo_valor = self.query_builder.build_query(
                action="DELETE",
                table="ftc.AtributoValorFichaTecnica",
                joins=[
                    {"type": "INNER JOIN", "table": "ftc.FichaTecnica", "on": "ftc.AtributoValorFichaTecnica.FichaTecnicaId = ftc.FichaTecnica.Id"},
                    {"type": "INNER JOIN", "table": "ProductoOrganizacion", "on": "ftc.FichaTecnica.ProductoOrganizacionId = ProductoOrganizacion.Id"},
                    {"type": "INNER JOIN", "table": "wfl.ProcesoWorkFlow", "on": "ProductoOrganizacion.Id = wfl.ProcesoWorkFlow.ProductoOrganizacionId"}
                ],
                conditions={"ProductoOrganizacion.idcAgente": idcAgente, "wfl.ProcesoWorkFlow.WorkflowId": f"wfl.GetModuloAgenteId('{modulo}')"}
            )
            queries.append(delete_atributo_valor)

            # DELETE para TechnicalData con INNER JOIN
            delete_technical_data = self.query_builder.build_query(
                action="DELETE",
                table="ftc.TechnicalData",
                joins=[
                    {"type": "INNER JOIN", "table": "ftc.FichaTecnica", "on": "ftc.TechnicalData.FichaTecnicaId = ftc.FichaTecnica.Id"},
                    {"type": "INNER JOIN", "table": "ProductoOrganizacion", "on": "ftc.FichaTecnica.ProductoOrganizacionId = ProductoOrganizacion.Id"},
                    {"type": "INNER JOIN", "table": "wfl.ProcesoWorkFlow", "on": "ProductoOrganizacion.Id = wfl.ProcesoWorkFlow.ProductoOrganizacionId"}
                ],
                conditions={"ProductoOrganizacion.idcAgente": idcAgente, "wfl.ProcesoWorkFlow.WorkflowId": f"wfl.GetModuloAgenteId('{modulo}')"}
            )
            queries.append(delete_technical_data)

            # DELETE para RegistrosDeCambios con INNER JOIN
            delete_registros_cambios = self.query_builder.build_query(
                action="DELETE",
                table="ftc.RegistrosDeCambios",
                joins=[
                    {"type": "INNER JOIN", "table": "ftc.FichaTecnica", "on": "ftc.RegistrosDeCambios.FichaTecnicaId = ftc.FichaTecnica.Id"},
                    {"type": "INNER JOIN", "table": "ProductoOrganizacion", "on": "ftc.FichaTecnica.ProductoOrganizacionId = ProductoOrganizacion.Id"},
                    {"type": "INNER JOIN", "table": "wfl.ProcesoWorkFlow", "on": "ProductoOrganizacion.Id = wfl.ProcesoWorkFlow.ProductoOrganizacionId"}
                ],
                conditions={"ProductoOrganizacion.idcAgente": idcAgente, "wfl.ProcesoWorkFlow.WorkflowId": f"wfl.GetModuloAgenteId('{modulo}')"}
            )
            queries.append(delete_registros_cambios)

            # DELETE para FichaTecnica con INNER JOIN
            delete_ficha_tecnica = self.query_builder.build_query(
                action="DELETE",
                table="ftc.FichaTecnica",
                joins=[
                    {"type": "INNER JOIN", "table": "ProductoOrganizacion", "on": "ftc.FichaTecnica.ProductoOrganizacionId = ProductoOrganizacion.Id"},
                    {"type": "INNER JOIN", "table": "wfl.ProcesoWorkFlow", "on": "ProductoOrganizacion.Id = wfl.ProcesoWorkFlow.ProductoOrganizacionId"}
                ],
                conditions={"ProductoOrganizacion.idcAgente": idcAgente, "wfl.ProcesoWorkFlow.WorkflowId":f"wfl.GetModuloAgenteId('{modulo}')"}
            )
            queries.append(delete_ficha_tecnica)

            # Añadir los nuevos DELETEs según la estructura que has indicado:

            # DELETE wfl.ResolucionTransaccion
            delete_resolucion_transaccion = self.query_builder.build_query(
                action="DELETE",
                table="wfl.ResolucionTransaccion",
                joins=[
                    {"type": "INNER JOIN", "table": "wfl.Transaccion", "on": "wfl.Transaccion.Id = wfl.ResolucionTransaccion.TransaccionId"},
                    {"type": "INNER JOIN", "table": "wfl.ProcesoWorkFlow", "on": "wfl.ProcesoWorkFlow.Id = wfl.Transaccion.ProcesoWorkFlowId"}
                ],
                conditions={"wfl.ProcesoWorkFlow.WorkFlowId": f"wfl.GetModuloAgenteId('{modulo}')"}
            )
            queries.append(delete_resolucion_transaccion)

            # DELETE wfl.Transaccion
            delete_transaccion = self.query_builder.build_query(
                action="DELETE",
                table="wfl.Transaccion",
                joins=[
                    {"type": "INNER JOIN", "table": "wfl.ProcesoWorkFlow", "on": "wfl.ProcesoWorkFlow.Id = wfl.Transaccion.ProcesoWorkFlowId"}
                ],
                conditions={"wfl.ProcesoWorkFlow.WorkFlowId": f"wfl.GetModuloAgenteId('{modulo}')"}
            )
            queries.append(delete_transaccion)

            # DELETE wfl.ProcesoWorkFlow
            delete_proceso_workflow = self.query_builder.build_query(
                action="DELETE",
                table="wfl.ProcesoWorkFlow",
                conditions={"wfl.ProcesoWorkFlow.WorkFlowId": f"wfl.GetModuloAgenteId('{modulo}')"}
            )
            queries.append(delete_proceso_workflow)

            return queries

        except Exception as e:
            ErrorHandler.handle_error(e, "Error generando las queries de limpieza con INNER JOIN para productos en procesos")
            return None

