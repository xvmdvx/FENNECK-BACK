# 🦙 Mistral 7B Local Server (con FastAPI y llama.cpp)

## 🚀 Cómo iniciar

```bash
source venv/bin/activate
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

## 📦 Reinstalación

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Modelo usado: `mistral-7b-instruct-v0.1.Q4_K_M.gguf`
