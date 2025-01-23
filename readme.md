# CRUD con Qdrant y VectorDBApp

Este proyecto utiliza Qdrant, un sistema de gestión de vectores, junto con una interfaz gráfica construida con Tkinter en Python. Permite insertar, eliminar y visualizar vectores en una base de datos de Qdrant mediante un CRUD.

## Requisitos

Antes de ejecutar el proyecto, asegúrate de tener las siguientes dependencias instaladas:

- Python 3.10 o superior
- Tkinter (debería estar incluido con Python)
- Las siguientes bibliotecas de Python:

```bash
pip install sentence-transformers qdrant-client python-dotenv
```

## Configuración de variables de entorno

```bash	
QDRANT_URL=<TU_URL_DE_QDRANT>
QDRANT_API_KEY=<TU_API_KEY_DE_QDRANT>
```

# Descripción del Proyecto

El proyecto permite realizar las siguientes operaciones:

* Añadir un vector: Convierte un texto en un vector utilizando un modelo de Sentence-Transformers y lo inserta en la base de datos de Qdrant.
* Ver los vectores almacenados: Muestra todos los vectores almacenados en la base de datos con su texto asociado.

* Eliminar un vector: Permite eliminar un vector seleccionado por su ID.

# Funcionalidad de la Aplicación

1. Interfaz gráfica: La aplicación usa Tkinter para crear una interfaz gráfica donde puedes agregar texto, visualizar los vectores existentes y eliminarlos.
2. Modelo de Sentence-Transformers: Usa el modelo "sentence-transformers/all-MiniLM-L6-v2" para convertir los textos en vectores de 384 dimensiones.
3. Qdrant: Se usa como base de datos para almacenar los vectores generados.

# Instrucciones de uso 

* Inicialización: Cuando se ejecuta la aplicación por primera vez, se crea la colección en Qdrant si no existe.
* Añadir Vectores: Introduce un texto en el campo de entrada y haz clic en "Añadir Vector" para agregarlo a la base de datos.
* Eliminar Vectores: Selecciona un vector de la tabla y haz clic en "Eliminar" para eliminarlo de la base de datos.
* Actualizar la lista: Haz clic en "Actualizar" para cargar los vectores actuales desde la base de datos y mostrarlos en la tabla.


# Descripción grafica del Proyecto

* Crear
![image](https://github.com/TakizawaXD/CRUD-Vector/blob/main/img/create.png?raw=true)

Resultados ![image](https://github.com/TakizawaXD/CRUD-Vector/blob/main/img/resultcreate.png?raw=true)


* Actualizar
![image](https://github.com/TakizawaXD/CRUD-Vector/blob/main/img/update.png?raw=true)

* Eliminar
![image](https://github.com/TakizawaXD/CRUD-Vector/blob/main/img/Borrar.png?raw=true)



