# UISP Analytics API

Este repositorio contiene el código fuente de la API en FastAPI para interactuar con el sistema UISP de Ubiquiti. La aplicación proporciona funcionalidades para analizar datos relacionados con clientes, dispositivos y servicios.

## Configuración
Antes de ejecutar el proyecto, asegúrate de seguir estos pasos:

1. **Variables de Entorno:**
   Crea un archivo llamado **.env** en la raíz del proyecto y configura las siguientes variables de entorno:

   `uisp_url=URL_DEL_SISTEMA_UISP`
   `x_auth_token=TU_TOKEN_DE_AUTENTICACION`

   Sustituye **URL_DEL_SISTEMA_UISP** y **TU_TOKEN_DE_AUTENTICACION** con la URL del sistema UISP de Ubiquiti y tu token de autenticación respectivamente.
2. **Archivos YAML:**
   Crea los siguientes archivos vacíos en la raíz del proyecto:
    `data/clients.yaml`
    `data/devices.yaml`
    `data/services.yaml`
3.  **Ambiente Virtual:**
    Se recomienda utilizar un entorno virtual para gestionar las dependencias del proyecto. Ejecuta los siguientes comandos para crear un entorno virtual e instalar las dependencias:
    `$ python -m venv venv`
    `$ source venv/bin/activate  # Para Linux/Mac`
    `$ pip install -r requirements.txt`

## Ejecutar la Aplicación:
Una vez configurado el entorno, puedes ejecutar la aplicación con el siguiente comando:
`$ uvicorn main:app --host 0.0.0.0 --port 8000 --reload`
La aplicación estará disponible en http://localhost:8000.

## Docker
Para desplegar la aplicación utilizando Docker, ejecuta los siguientes comandos:

`$ docker build -t uisp-analytics-api .`
`$ docker run -p 8000:80 -e uisp_url=URL_DEL_SISTEMA_UISP -e x_auth_token=TU_TOKEN_DE_AUTENTICACION uisp-analytics-api`

Reemplaza **URL_DEL_SISTEMA_UISP** y **TU_TOKEN_DE_AUTENTICACION** con la URL del sistema UISP de Ubiquiti y tu token de autenticación respectivamente.

La aplicación estará disponible en http://localhost:8000

## Contribuciones
Si encuentras algún problema o tienes sugerencias, por favor crea un issue. ¡Las contribuciones son bienvenidas!