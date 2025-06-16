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
