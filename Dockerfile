# Imagen base
FROM python:3.13-alpine

# Directorio de trabajo
WORKDIR /code

# Copia de archivo requirements.txt
COPY ./requirements.txt /code/requirements.txt

# Instalación de dependencias
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copia de archivos al contenedor
COPY ./app /code/app
COPY ./data /code/data

# Establecer PYTHONPATH
ENV PYTHONPATH=/code

# Comando para iniciar la aplicación
CMD ["fastapi", "run", "app/main.py", "--port", "80"]

# Exponer puerto de la aplicación
EXPOSE 80