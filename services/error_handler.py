import tkinter as tk
from tkinter import messagebox
import traceback

class ErrorHandler:
    @staticmethod
    def handle_error(exception, query=None):
        """
        Captura el error y lo muestra en un messagebox de Tkinter.
        
        Parámetros:
        - exception: La excepción capturada
        - query: La query que se intentó ejecutar, si existe
        
        Muestra una ventana emergente con el mensaje de error.
        """
        error_message = f"Error: {str(exception)}"
        if query:
            error_message += f"\nQuery: {query}"

        # Obtener la traza de la pila para saber en qué función ocurrió el error
        stack_trace = traceback.format_exc()
        print(f"ERROR:\n{error_message}\n")
        # Mostrar el error en una ventana emergente
        messagebox.showerror("Error", f"{error_message}\n\nStack Trace:\n{stack_trace}", fg="red")

        return error_message