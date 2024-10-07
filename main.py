# %%
import importlib
from views import first 
from controllers import WorkFlowController 

# Si has hecho cambios en first.py, usa importlib para recargar el módulo
importlib.reload(first)
importlib.reload(WorkFlowController)

# %%
# Llamamos a la función main definida en first.py
first.main()



