import tkinter as tk
from tkinter import messagebox
from controllers.WorkFlowController import WorkFlowController
from views.LimpiezaWindow import LimpiezaWindow

class Application(tk.Frame):
    def __init__(self, master=None, controller=None):
        super().__init__(master)
        self.master = master
        self.controller = controller
        self.pack(padx=50, pady=20)  # Añadimos espacio alrededor de los widgets
        self.create_widgets()

    def create_widgets(self):
        # Fila 0 - IdcAgente
        self.idcAgente_label = tk.Label(self, text="IdcAgente")
        self.idcAgente_label.grid(row=0, column=0, sticky="e", padx=10, pady=5)  # Justificar a la derecha
        self.idcAgente_entry = tk.Entry(self, width=30)
        self.idcAgente_entry.grid(row=0, column=1, sticky="w", padx=10, pady=5)

        # Fila 1 - Modulo
        self.modulo_label = tk.Label(self, text="Modulo (WorkflowAgenteId)")
        self.modulo_label.grid(row=1, column=0, sticky="e", padx=10, pady=5)  # Justificar a la derecha
        self.modulo_entry = tk.Entry(self, width=50)  # Más espacio para escribir
        self.modulo_entry.grid(row=1, column=1, sticky="w", padx=10, pady=5)

        # Fila 2 - Autor
        self.autor_label = tk.Label(self, text="Autor")
        self.autor_label.grid(row=2, column=0, sticky="e", padx=10, pady=5)  # Justificar a la derecha
        self.autor_entry = tk.Entry(self, width=30)
        self.autor_entry.grid(row=2, column=1, sticky="w", padx=10, pady=5)

        self.tarea_id_label = tk.Label(self, text="ID tarea:")
        self.tarea_id_label.grid(row=3, column=0, sticky="e", padx=10, pady=5)  # Justificar a la derecha
        self.tarea_id_entry = tk.Entry(self, width=30)
        self.tarea_id_entry.grid(row=3, column=1, sticky="w", padx=10, pady=5)

        # Botón de Validar (centrado)
        self.validate_button = tk.Button(self, text="Validar", command=self.validate_fields)
        self.validate_button.grid(row=4, column=0, columnspan=2, pady=10)

        # Botón de Salir (centrado)
        self.quit = tk.Button(self, text="Salir", fg="red", command=self.master.destroy)
        self.quit.grid(row=5, column=0, columnspan=2, pady=5)

    def validate_fields(self):
        # Obtener los valores de entrada
        idcAgente = self.idcAgente_entry.get()
        modulo = self.modulo_entry.get()
        autor = self.autor_entry.get()
        tarea_id = self.tarea_id_entry.get()

        # Comprobar que los campos no estén vacíos
        if not idcAgente or not modulo or not autor:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        # Validamos la relación usando el controlador
        if self.controller.validate_agente_modulo(idcAgente, modulo):
            messagebox.showinfo("Resultado", f"Validación exitosa: Existe una relación entre el agente {idcAgente} y el módulo {modulo}.")
            
            # Cambiar de ventana, pero la conexión sigue abierta
            self.master.destroy()

            # Crear la nueva ventana de Limpieza, pasando idcAgente y Modulo
            new_window = tk.Tk()
            new_window.geometry("800x600")
            new_window.title(f"ClearInit - Limpieza del cliente {idcAgente}")
            limpieza_app = LimpiezaWindow(master=new_window, controller=self.controller, idcAgente=idcAgente, modulo=modulo, autor=autor, tarea_id = tarea_id)
            limpieza_app.mainloop()

            # Cerrar la conexión después de la segunda ventana
            self.controller.close_connection()

        else:
            messagebox.showerror("Resultado", f"No se encontró relación para idcAgente {idcAgente} y Modulo {modulo}.")



def main():
    # Inicializamos el controlador
    workflow_controller = WorkFlowController(db_name="AemeDb")

    # Creamos la ventana usando el controlador
    root = tk.Tk()
    root.geometry("600x300")
    root.title(f"ClearInit")
    app = Application(master=root, controller=workflow_controller)
    app.mainloop()

# Solo ejecutamos main si este archivo es ejecutado directamente
if __name__ == "__main__":
    main()