# %%
from tkinter import Tk
from controllers.WorkFlowController import WorkFlowController
from views.first import Application

# %%


def main():
    # Inicializar el controlador
    db_name = "AemeDb"  # Nombre de la base de datos
    workflow_controller = WorkFlowController(db_name)

    # Crear la ventana principal de la aplicación
    root = Tk()
    
    # Definir el título de la ventana con la IP de la base de datos
    db_ip = workflow_controller.get_db_ip()
    root.title(f"IP BBDD: {db_ip}")

    # Inicializar la aplicación con la ventana y el controlador
    app = Application(master=root, controller=workflow_controller)
    
    # Ejecutar el bucle principal de Tkinter
    app.mainloop()

if __name__ == "__main__":
    main()




# %%
