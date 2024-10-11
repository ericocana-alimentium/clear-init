import tkinter as tk
from tkinter import filedialog
import os
from datetime import datetime
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


    def init_window(self):
        # Configurar la ventana
        self.title("Limpiar Connect")
        self.geometry("500x300")

        # Etiqueta para mostrar el string de la tabla temporal
        self.temporal_query_label = tk.Label(self, text="Query de la tabla temporal:")
        self.temporal_query_label.pack(pady=10)

        # Campo de texto para mostrar el resultado de la query temporal
        self.temporal_query_text = tk.Text(self, wrap="word", width=50, height=10)
        self.temporal_query_text.pack(padx=10, pady=10)

        # Botón para generar y mostrar la query
        self.generate_button = tk.Button(self, text="Generar Query Temporal", command=self.show_temporal_query)
        self.generate_button.pack(pady=10)

    def show_temporal_query(self):
        try:
            # Llamada al controller correcto para obtener la query temporal
            temporal_query = self.controller.crear_tabla_temporal(self.idcAgente, self.modulo)
            self.temporal_query_text.delete(1.0, tk.END)  # Limpiar el campo de texto
            self.temporal_query_text.insert(tk.END, temporal_query)  # Insertar la query generada
        except Exception as e:
            # Mostrar el error en el campo de texto si algo falla
            self.temporal_query_text.delete(1.0, tk.END)
            self.temporal_query_text.insert(tk.END, f"Error: {e}")