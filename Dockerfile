FROM python:3.11-slim

# Instala Node.js
RUN apt-get update && apt-get install -y curl \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean

WORKDIR /app

# Copia los archivos necesarios
COPY package*.json ./
COPY requirements.txt ./

# Instala las dependencias de Node.js y Python
RUN npm install
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de los archivos de la aplicación
COPY . .

# Expone el puerto de la aplicación
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["sh", "-c", "npx tailwindcss -i ./static/src/styles.css -o ./static/public/output.css --watch & uvicorn app.main:app --host 0.0.0.0 --port 8000"]
