# Imagen base
FROM python:3.10

# Directorio de trabajo
WORKDIR /code

# Copia de archivo requirements.txt
COPY ./requirements.txt /code/requirements.txt

# Instalación de dependencias
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copia de archivos al contenedor
COPY ./app /code/app
COPY ./data /code/data

# Comando para iniciar la aplicación
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

# Exponer puerto de la aplicación
EXPOSE 80