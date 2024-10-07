import tkinter as tk
from tkinter import font
from views.LimpiarAemeDbWindow import LimpiarAemeDbWindow  # Importamos la nueva ventana


class LimpiezaWindow(tk.Frame):
    def __init__(self, master=None, controller=None, idcAgente=None, modulo=None, autor=None, tarea_id = None):
        super().__init__(master)
        self.master = master
        self.controller = controller
        self.idcAgente = idcAgente
        self.modulo = modulo
        self.autor = autor
        self.tarea_id = tarea_id
        self.tablas_a_borrar_aemedb = []  # Lista para almacenar las tablas de AemeDB
        self.tablas_a_borrar_connect = []  # Lista para almacenar las tablas de Connect
        self.check_vars_aemedb = {}  # Diccionario para almacenar las variables de las checkboxes de AemeDB
        self.check_vars_connect = {}  # Diccionario para almacenar las variables de las checkboxes de Connect
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # Crear fuente en negrita y más grande
        bold_font = font.Font(weight="bold", size=10)

        # Mostrar procesos totales en negrita
        self.procesos_label = tk.Label(self, text="Procesos totales (wfl.ProcesoWorkflow): Cargando...", font=bold_font)
        self.procesos_label.pack()

        # Mostrar productos totales en negrita
        self.productos_label = tk.Label(self, text="Productos totales: Cargando...", font=bold_font)
        self.productos_label.pack()

        # Actualizar procesos y productos
        self.update_procesos()
        self.update_productos()

        # Crear un frame para organizar las columnas
        self.columns_frame = tk.Frame(self)
        self.columns_frame.pack(pady=10)  # Añadir separación vertical para mejor organización

        # Título en negrita y más grande para "Tablas que se van a borrar datos"
        self.tablas_label = tk.Label(self.columns_frame, text="Tablas que se van a borrar datos:", font=("Helvetica", 12, "bold"))
        self.tablas_label.grid(row=0, column=0, columnspan=2, sticky="n", pady=5)  # Mostrar sobre ambas columnas con separación

        # Columna 1: AemeDB en negrita
        self.aeme_label = tk.Label(self.columns_frame, text="AemeDB:", font=bold_font)
        self.aeme_label.grid(row=1, column=0, sticky="nw", padx=10)

        # Columna 2: Connect en negrita, con más espacio entre las columnas
        self.connect_label = tk.Label(self.columns_frame, text="Connect:", font=bold_font)
        self.connect_label.grid(row=1, column=1, sticky="nw", padx=50)  # Más padding horizontal entre columnas

        # Listado de tablas para AemeDB
        tablas_aemedb = [
            "ftc.AtributoValorFichaTecnica",
            "ftc.TechnicalData",
            "ftc.RegistrosDeCambios",
            "ftc.FichaTecnica",
            "wfl.ProcesoWorkflow",
            "wfl.Transaccion",
            "wfl.ResolucionTransaccion",
        ]

        # Agregamos las tablas de AemeDB a la primera columna
        for index, tabla in enumerate(tablas_aemedb):
            var = tk.BooleanVar(value=True)  # Checkbox seleccionado por defecto
            checkbox = tk.Checkbutton(self.columns_frame, text=tabla, variable=var, state=tk.DISABLED)  # Deshabilitar
            checkbox.grid(row=index+2, column=0, sticky="w")
            self.check_vars_aemedb[tabla] = var  # Almacenar la variable en el diccionario
            self.tablas_a_borrar_aemedb.append(tabla)  # Añadir la tabla a la lista de tablas a borrar en AemeDB

        # Reservar espacio para Connect (columna vacía por ahora)
        for index in range(len(tablas_aemedb)):
            empty_label = tk.Label(self.columns_frame, text="")  # Espacio vacío
            empty_label.grid(row=index+2, column=1)

        # Crear un frame para los botones "Limpiar AemeDb" y "Limpiar Connect"
        self.buttons_frame = tk.Frame(self)
        self.buttons_frame.pack(pady=10)

        self.limpiar_aemedb_button = tk.Button(self.buttons_frame, text="Limpiar AemeDb", command=self.abrir_ventana_aemedb)
        self.limpiar_aemedb_button.grid(row=0, column=0, padx=10)

        # Botón para limpiar Connect
        self.limpiar_connect_button = tk.Button(self.buttons_frame, text="Limpiar Connect", command=self.abrir_ventana_connect)
        self.limpiar_connect_button.grid(row=0, column=1, padx=10)

        # Botón para gestionar productos y multimedia
        self.productos_button = tk.Button(self, text="Productos - Multimedia", command=self.gestionar_multimedia)
        self.productos_button.pack()

    def update_procesos(self):
        try:
            total_procesos = self.controller.get_total_procesos(self.modulo)
            self.procesos_label.config(text=f"Procesos totales (ProcesoWorkFlow): {len(total_procesos)}", fg="black")
        except Exception as e:
            self.procesos_label.config(text=f"Error en la consulta: {e}", fg="red")

    def update_productos(self):
        try:
            productos_lista = self.controller.get_total_productos(self.idcAgente)
            total_productos = len(productos_lista)
            self.productos_label.config(text=f"Productos totales: {total_productos}")
        except Exception as e:
            self.productos_label.config(text=f"Error obteniendo productos: {e}")

    def crear_ventana(self, clase_ventana, title, size, **kwargs):
        new_window = clase_ventana(master=self.master, **kwargs)
        new_window.title(title)
        new_window.geometry(size)
        new_window.grab_set()  # Bloquear la ventana principal hasta que se cierre la nueva
        return new_window


    def abrir_ventana_aemedb(self):
        self.crear_ventana(LimpiarAemeDbWindow, "Limpiar AemeDb", "500x400", controller=self.controller, idcAgente=self.idcAgente, autor=self.autor, modulo=self.modulo, tarea_id= self.tarea_id)

    def abrir_ventana_connect(self):
        # Crear nueva ventana para Connect
        new_window = tk.Toplevel(self)
        new_window.title("Limpiar Connect")
        new_window.geometry("400x300")
        label = tk.Label(new_window, text="Ventana para limpiar Connect")
        label.pack(pady=20)

    def gestionar_multimedia(self):
        print("Gestionar productos y multimedia")
