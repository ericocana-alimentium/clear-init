# LIMPIEZA DE PROYECTOS

## Índice

1. [Introducción](#introducción)
2. [Requisitos previos](#requisitos-previos)
3. [Instalación y configuración](#instalación-y-configuración)
4. [Estructura del proyecto](#estructura-del-proyecto)
5. [Uso del sistema](#uso-del-sistema)
6. [Detalles Técnicos](#detalles-técnicos)
   - [QueryBuilder](#querybuilder)
   - [Conexión a la base de datos](#conexión-a-la-base-de-datos)

## Introducción

En los proyectos actuales, se han estado realizando pruebas directamente en el entorno de producción. Esto permite validar el funcionamiento de las integraciones antes del arranque oficial. Sin embargo, como estas pruebas generan datos y procesos temporales, es fundamental realizar una limpieza exhaustiva justo antes de la puesta en marcha definitiva. 

El objetivo de este proyecto es desarrollar un script de limpieza que deje la cuenta completamente vacía de procesos y datos de prueba. La limpieza debe contemplar lo siguiente:

- **Procesos de WorkFlow (wfl)**: Eliminar todos los procesos de workflows, independientemente de su estado (incluidos los cerrados), tanto de clientes como de proveedores.
- **Productos**: Borrar cualquier información asociada a workflows de prueba para todos los productos, así como workflows específicos de proveedores y certificados.
- **Archivos y registros**: Eliminar todos los archivos y registros asociados a los datos de prueba generados durante las validaciones.
- **Aplicación**: La limpieza se debe aplicar tanto en la base de datos de **Aeme** como en la de **Connect**, garantizando que ambos entornos queden completamente libres de datos de prueba.

Este enfoque garantiza un entorno de producción limpio y preparado para su uso oficial sin interferencias de datos temporales.

### Objetivos del programa

- Automatizar la generación de scripts SQL para la limpieza de datos.
- Proveer una interfaz fácil de usar para la configuración y ejecución de dicha limpieza.
- Facilitar la conexión y manejo de datos de múltiples bases de datos.

## Requisitos previos

Antes de ejecutar el script de limpieza, asegúrate de cumplir con los siguientes requisitos:

1. **Acceso a la base de datos**:
   - Se requiere acceso a las bases de datos **Aeme** y **Connect** con privilegios para ejecutar al menos **consultas de selección**.

2. **Python instalado**:
   - Asegúrate de tener **Python 3.8** o superior instalado.
   - Recomendación: usar [Anaconda](https://www.anaconda.com/) para gestionar entornos y paquetes de Python. (esto para los devs)

3. **Bibliotecas necesarias**:
   - Instala las siguientes bibliotecas adicionales para ejecutar el proyecto:
     - **`pyodbc`**: para conectarse y ejecutar consultas en bases de datos SQL Server.
     - **`tkinter`**: (incluido en Python) para la interfaz gráfica de usuario (GUI) utilizada en el programa.
4. **Conexión estable al servidor de base de datos**:
   - El sistema desde el cual se ejecutará el script debe estar conectado a la red VPN.

5. **Permisos para modificar archivos**:
   - El sistema debe tener permisos para crear y modificar archivos en el directorio donde se guardarán los **scripts SQL** generados en caso que se quieran guardar fuera del PC.

## Instalación y Configuración

Sigue los pasos a continuación para instalar y configurar el entorno necesario para ejecutar el proyecto:

### 1. Clona el repositorio

Clona el repositorio del proyecto en tu sistema local usando el siguiente comando:

```bash
git clone https://github.com/ericocana-alimentium/clear-init.git
```

### 2. Configura un entorno virtual (opcional pero recomendado para devs)

Crea un entorno virtual para evitar conflictos con otras bibliotecas instaladas en tu sistema:

```bash
python -m venv entorno-limpieza
```

Activa el entorno virtual:

- **En Windows**:

  ```bash
  entorno-limpieza\Scripts\activate
  ```

- **En macOS y Linux**:

  ```bash
  source entorno-limpieza/bin/activate
  ```

### 3. Navega al directorio del proyecto

Antes de instalar las bibliotecas, asegúrate de que estás en el directorio raíz del proyecto. Usa el siguiente comando:

```bash
cd clear-init
```

### 4. Instala las bibliotecas necesarias

Ejecuta el siguiente comando para instalar las bibliotecas requeridas enumeradas en el archivo **`requisitos.txt`**:

```bash
pip install -r requisitos.txt
```

Este comando se encargará de instalar todos los paquetes necesarios para que el proyecto funcione correctamente. Asegúrate de que el archivo **`requisitos.txt`** esté en el directorio raíz del proyecto.

### 5. Configuración de la conexión a la base de datos

Asegúrate de que las credenciales de conexión a la base de datos estén correctamente configuradas:

- Verifica que el archivo de configuración **`db_connection.py`** contenga los detalles de conexión adecuados para las bases de datos **Aeme** y **Connect**.
- Para cambiar de entorno solo debes cambiar a la variable db_hosts

### 6. Ejecuta la aplicación

Una vez completados los pasos anteriores, puedes ejecutar la aplicación desde el directorio raíz del proyecto usando el siguiente comando:

```bash
python main.py
```


### Estructura del proyecto

En este apartado, se detallará la organización de los directorios y archivos principales para comprender cómo está estructurado el proyecto. Esto ayudará a entender la ubicación y propósito de cada componente.

#### Directorios y archivos principales

- **`controllers/`**: Contiene los controladores de la aplicación. Se encargan de gestionar la lógica de negocio, interactuar con los modelos y coordinar las vistas.
  - **`WorkFlowController.py`**: Controlador principal que gestiona la lógica relacionada con los flujos de trabajo.
  
- **`models/`**: Incluye los modelos de datos. Los modelos se encargan de la comunicación con la base de datos y la ejecución de consultas SQL a través del QueryBuilder.
  - **`WorkFlowAgenteModel.py`**: Modelo que interactúa con las tablas relacionadas a los agentes de trabajo y sus flujos.

- **`views/`**: Almacena las vistas de la aplicación, que son las interfaces gráficas con las que interactúa el usuario.
  - **`first.py`**: Primera ventana de inicio donde pide la información para poder empezar
  - **`LimpiezaWindow.py`**: Vista principal donde se realiza la limpieza de datos para el módulo específico.
  - **`LimpiarAemeDbWindow.py`**: Vista para la limpieza específica de la base de datos Aeme.

- **`services/`**: Contiene servicios auxiliares utilizados por los controladores y modelos.
  - **`query_builder.py`**: Servicio que construye consultas SQL dinámicamente en base a los parámetros proporcionados.
  - **`error_handler.py`**: Servicio encargado de gestionar los errores y mostrar mensajes en la interfaz.

- **`db_connection.py`**: Módulo que gestiona la conexión a la base de datos, permitiendo abrir y cerrar conexiones de forma centralizada.

- **`main.py`**: Punto de entrada de la aplicación donde se inicializan los controladores y las vistas.

Los archivos `.ipynb` son para poder depurar y hacer pruebas, solo se usan a modo de debugación para el programador.

### Uso del sistema

En esta sección, se explica cómo interactuar con el sistema para realizar las principales acciones disponibles: credenciales, limpieza de datos y generación de scripts SQL.

#### Credenciales

Antes de realizar cualquier operación, es necesario que el usuario use las credenciales para la base de datos para validar su acceso y permisos.

- **db_user y db_pass**: en el archivo `db_connection.py`.

#### Limpieza de datos

El sistema permite limpiar datos de las bases AemeDB y Connect. Para cada base, se pueden realizar las siguientes acciones:

- **Escribir módulos y agentes**: El usuario debe elegir el módulo y el ID del agente para especificar el contexto de la limpieza.
- **Visualización previa**: Se muestra un resumen de los procesos y productos que serán afectados. Esto incluye:
  - Procesos totales y productos totales asociados.
  - Visualización de las tablas que se van a limpiar en cada base de datos.
- **Ejecución de la limpieza**: Al confirmar, se genera un script SQL de limpieza basado en los productos y procesos seleccionados.
- **Multimedia**:

#### Generación de scripts SQL

El sistema permite generar scripts SQL de limpieza para ejecutarlos en producción:

- **Selección de carpeta**: El usuario puede elegir la ubicación donde se guardará el archivo SQL. Si no se selecciona una, el archivo se guardará en la carpeta de descargas predeterminada.
- **Personalización**: El nombre del archivo se compone dinámicamente con la fecha, ID de tarea, módulo y autor.

### Detalles Técnicos

En esta sección, se profundiza en algunos aspectos técnicos clave del sistema, como el funcionamiento del `QueryBuilder` y la conexión a la base de datos.

#### QueryBuilder

El `QueryBuilder` es una clase esencial que se encarga de construir las queries SQL de manera dinámica para las operaciones del sistema. (Esta lo más generalizado posible, puedes usuarlo para otro proyecto que te interese construir queries, para ejecutarla o solo generar el texto de la query)

- **Funciones soportadas**: Soporta acciones como `SELECT`, `INSERT`, `UPDATE`, y `DELETE`.
- **Estructura**: Permite añadir joins (`INNER JOIN`, `LEFT JOIN`, etc.) y condiciones (`WHERE`, `AND`, `OR`), permitiendo construir queries complejas de manera programática.
- **Uso de funciones SQL**: Se soporta el uso de funciones SQL como `wfl.GetModuloAgenteId` directamente en las condiciones, sin necesidad de comillas.
- **Generación de queries**: El `QueryBuilder` genera las queries sin placeholders para asegurar compatibilidad con las particularidades del sistema de bases de datos utilizado (Microsoft SQL Server). Además, se encarga de manejar correctamente las listas en las condiciones, transformándolas en operaciones `IN`.
No hago uso de placeholders porque al final solo se lanzan selects el resto solo construye la querie y aparte he puesto un "seguro" para que solo se ejecuten selects

```python
if query.strip().upper().startswith("SELECT"):
```

#### Conexión a la base de datos

El sistema gestiona las conexiones a las bases de datos mediante una clase especializada para garantizar la integridad y la eficiencia de las operaciones.

- **Clase de conexión**: La clase `DBConnection` se encarga de abrir y cerrar conexiones a las bases de datos AemeDB y Connect.
- **Uso del ODBC Driver**: El sistema utiliza el driver ODBC para conectar con Microsoft SQL Server, asegurando compatibilidad con las bases de datos SQL Server en producción.
- **Manejo de errores**: Se ha integrado un sistema de manejo de errores que captura cualquier excepción relacionada con la conexión y las queries, mostrando mensajes detallados para ayudar a depurar y resolver problemas rápidamente.
