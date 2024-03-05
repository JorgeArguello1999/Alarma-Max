FROM python:3.11

# Establezca el directorio de trabajo en /app
WORKDIR /app

# Copie todo el contenido de la carpeta actual al directorio /app en el contenedor
COPY . /app

# Instale las dependencias de Python desde requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto 8000 en el contenedor
EXPOSE 8000

# Iniciar la aplicación FastAPI con Uvicorn cuando el contenedor se ejecute
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
