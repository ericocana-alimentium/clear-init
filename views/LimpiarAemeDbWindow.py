import tkinter as tk
from tkinter import filedialog
import os
from datetime import datetime

class LimpiarAemeDbWindow(tk.Toplevel):
    def __init__(self, master=None, controller=None, idcAgente=None, autor=None, modulo = None, tarea_id = None):
        super().__init__(master)
        self.controller = controller  # Controlador para manejar las queries
        self.idcAgente = idcAgente
        self.autor = autor
        self.filepath = tk.StringVar()  # Ruta del archivo .sql
        self.modulo = modulo
        self.tarea_id = tarea_id
        self.productos_procesados_count = tk.StringVar()  # Guardará el número de productos procesados
        self.init_window()

    def init_window(self):
        # Configurar la ventana
        self.title("Limpiar AemeDb")

        # Título "Productos con workflow asociado"
  
        # Etiqueta para mostrar el número de productos procesados
        self.productos_procesados_label = tk.Label(self, textvariable=self.productos_procesados_count, font=("Arial", 12, "bold"))
        self.productos_procesados_label.pack(pady=10)

        # Actualizar el conteo de productos procesados
        self.update_productos_procesados()

        # Etiqueta para el campo de ruta
        self.label = tk.Label(self, text="Selecciona carpeta donde guardar el archivo SQL:")
        self.label.pack(pady=10)

        # Campo de texto para mostrar la ruta seleccionada
        self.entry = tk.Entry(self, textvariable=self.filepath, width=50)
        self.entry.pack(padx=10)

        # Botón para seleccionar la carpeta
        self.browse_button = tk.Button(self, text="Browse", command=self.browse_folder)
        self.browse_button.pack(pady=10)

        # Botón para generar el SQL
        self.generate_button = tk.Button(self, text="Generar SQL", command=self.generate_sql)
        self.generate_button.pack(pady=10)

    def update_productos_procesados(self):
        # Lógica para obtener el número de productos procesados desde el controlador
        productos_procesados = self.controller.get_productos_procesados(self.idcAgente)  # Llamada al controlador
        total_productos_procesados = len(productos_procesados)  # Contar los productos procesados

        # Actualizar la etiqueta con el número de productos procesados
        self.productos_procesados_count.set(f"Productos con workflow asociado: {total_productos_procesados}")

    def browse_folder(self):
        # Abrir ventana para seleccionar carpeta
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.filepath.set(folder_selected)

    def generate_sql(self):
        # Obtener la carpeta donde se guardará el archivo, o usar "Descargas" por defecto
        folder_path = self.filepath.get() or os.path.expanduser("~/Downloads")
        
        # Crear nombre del archivo .sql
        fecha_actual = datetime.now().strftime("%Y%m%d")
        tarea_id_num = self.tarea_id.split('-')[1]  # Extraer solo la parte numérica de la tarea
        filename = f"{fecha_actual}-{tarea_id_num}-000-DAT-limpieza-{self.modulo}.sql"
        full_path = os.path.join(folder_path, filename)
        
        # Generar el encabezado del archivo SQL
        header = f"""
/*
* LINK TAREA: https://app.clickup.com/t/36671967/{self.tarea_id} 
* DESCRIPCIÓN: Script de limpieza para {self.modulo} - {self.idcAgente} 
*
* AUTOR: {self.autor} 
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

        # Acumulador para todo el contenido del archivo SQL
        content = header + "\n"

        queries = self.controller.generar_queries_aemedb(self.idcAgente, self.modulo)

        for query in queries:
            # Formatear la query
            formatted_query = query

            # Añadir saltos de línea después de ciertas palabras clave, excepto en el caso de JOIN y ON
            formatted_query = formatted_query.replace(" FROM ", "\nFROM ")
            formatted_query = formatted_query.replace(" WHERE ", "\nWHERE ")
            formatted_query = formatted_query.replace(" AND ", "\nAND ")
            formatted_query = formatted_query.replace(" OR ", "\nOR ")

            # Mantener JOIN y ON en la misma línea
            formatted_query = formatted_query.replace(" INNER JOIN ", "\nINNER JOIN ")
            formatted_query = formatted_query.replace(" LEFT JOIN ", "\nLEFT JOIN ")
            formatted_query = formatted_query.replace(" RIGHT JOIN ", "\nRIGHT JOIN ")
            formatted_query = formatted_query.replace(" ON ", " ON ")

            # Agregar la query formateada al contenido
            content += formatted_query + ";\nGO\n\n"

        # Añadir el cierre final
        footer = "GO\n--COMMIT\nROLLBACK\n"
        content += footer

        # Reemplazar todas las ocurrencias de 'None' con NULL en el contenido generado
        content = content.replace("None", "NULL").replace("'NULL'", "NULL")

        # Escribir todo el contenido en el archivo
        with open(full_path, 'w') as sql_file:
            sql_file.write(content)

        # Mensaje de confirmación
        tk.messagebox.showinfo("Éxito", f"Archivo SQL generado en: {full_path}")




