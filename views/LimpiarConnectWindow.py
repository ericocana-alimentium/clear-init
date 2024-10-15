import tkinter as tk
from tkinter import filedialog
import os
from datetime import datetime
from tkinter import messagebox
from controllers.ConnectaAlimentiumController import ConnectaAlimentiumController

class LimpiarConnectWindow(tk.Toplevel):
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
        self.title("Limpiar Connecta")
        self.geometry("500x300")


    def init_window(self):

        # Campo de texto para mostrar el total de productos encontrados
        self.productos_count_var = tk.StringVar()
        self.productos_count_label = tk.Label(self, textvariable=self.productos_count_var)
        self.productos_count_label.pack(pady=10)

        # Cargar el conteo de productos encontrados en la vista
        self.cargar_productos()

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
        self.generate_button = tk.Button(self, text="Generar SQL", command=self.generar_sql)
        self.generate_button.pack(pady=10)
    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.filepath.set(folder_selected)

    def cargar_productos(self):
        """
        Carga la cantidad de productos encontrados en la vista.
        """
        #self.controller.cambiar_base_datos("Connecta_Alimentium")
        datos, self.query_s = self.controller.crear_tabla_temporal(self.idcAgente, self.modulo)
        #print(f"estoy aquí: {self.query_s}, fin")
        productos_agentes = self.controller.obtener_productos_agentes(datos)
        if productos_agentes:
            total_productos = len(productos_agentes)
            self.productos_count_var.set(f"Total de productos encontrados: {total_productos}")
        else:
            self.productos_count_var.set("No se encontraron productos en Connecta.")

    def generar_sql(self):
        folder_path = self.filepath.get()
        if not folder_path:
            messagebox.showerror("Error", "Por favor, selecciona una carpeta primero.")
            return

        if folder_path:
            # Llamar al controlador para generar el archivo SQL
            archivo_generado = self.controller.generar_queries(self.tarea_id,folder_path, self.autor)
            if archivo_generado:
                messagebox.showinfo("Éxito", f"Archivo SQL generado: {archivo_generado}")
            else:
                messagebox.showerror("Error", f"Hubo un problema generando el archivo.\n {archivo_generado}")