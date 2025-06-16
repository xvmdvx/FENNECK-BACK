# 🦙 Mistral 7B Local Server (con FastAPI y llama.cpp)

Este proyecto expone un asistente ligero mediante `fastapi` y `llama.cpp`.  
Para mantener el repositorio limpio no se incluye el entorno virtual ni los binarios
que genera. Al clonar simplemente recrea el entorno usando `requirements.txt`.

## 🚀 Cómo iniciar

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
./start.sh
```

Puedes personalizar la ruta del modelo y el puerto exportando las
variables de entorno `MODEL_PATH` y `PORT` antes de arrancar:

```bash
export MODEL_PATH=/ruta/al/modelo.gguf
export PORT=9000
./start.sh
```

## 🧪 Cómo probar

Desde consola del navegador:

```js
fetch("http://localhost:8000/api/chat", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ prompt: "¿Qué es una LLC?" })
}).then(res => res.json()).then(console.log);
```

Modelo usado: `mistral-7b-instruct-v0.1.Q4_K_M.gguf`

## 📄 Licencia

Este proyecto está bajo la [Licencia MIT](LICENSE).

## 🐳 Docker

Para construir la imagen ejecuta:

```bash
docker build -t fennec-back .
```

Y para iniciar el contenedor mapea el puerto 8000:

```bash
docker run -p 8000:8000 fennec-back
```
## Abrir la interfaz

Con el servidor en marcha abre `fennec_assistant.html` en tu navegador.
Por defecto busca la API en `http://localhost:8000`, por lo que si cambiaste
el puerto asegúrate de modificar la URL en el código o ajustar la variable
`PORT` antes de abrir el archivo.
