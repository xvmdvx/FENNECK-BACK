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

Puedes personalizar la ruta del modelo, el puerto, los orígenes permitidos y el archivo de reglas exportando las
variables de entorno `MODEL_PATH`, `PORT`, `ALLOWED_ORIGINS` y `RULES_FILE` antes de arrancar:

```bash
export MODEL_PATH=/ruta/al/modelo.gguf
export PORT=9000
export RULES_FILE=/ruta/a/mis_reglas.txt
export ALLOWED_ORIGINS=http://localhost:3000
./start.sh
```
Puedes indicar varios orígenes separándolos con comas.

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

## ✅ Ejecutar pruebas

Para correr las pruebas unitarias usa `pytest`:

```bash
pytest
```
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

Además se incluye la página `index.html` que muestra un asistente por pasos.
Su lógica se encuentra en `script.js` y la estructura de datos en
`data/stepsData.json`, los cuales se cargan de forma externa cuando se abre
la página. Mantén estos archivos en el mismo directorio para que el navegador
pueda localizarlos sin problemas.

Para evitar errores al cargar los archivos JSON, ejecuta `index.html` con el
script `serve_index.py`. Esta utilidad inicia un servidor HTTP sencillo y abre
la página automáticamente:

```bash
python3 serve_index.py
```

Puedes cambiar el puerto estableciendo la variable `PORT` antes de ejecutarlo.

Si utilizas macOS y prefieres contar con una aplicación `.app`, puedes generar
una con `pyinstaller`:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed serve_index.py
```

El paquete resultante se ubicará en `dist/` y podrás lanzarlo con doble clic.

## 🛠️ Automatizar el servidor

Si deseas evitar los pasos manuales cada vez que inicias el sistema,
puedes registrar el script `start.sh` como un servicio `systemd` (Linux).

1. Crea el archivo `/etc/systemd/system/fennec.service` con el siguiente contenido:

```ini
[Unit]
Description=Servidor Fennec AI
After=network.target

[Service]
User=<TU_USUARIO>
WorkingDirectory=/ruta/a/FENNECK-BACK
ExecStart=/ruta/a/FENNECK-BACK/start.sh
Restart=always

[Install]
WantedBy=multi-user.target
```

Reemplaza `<TU_USUARIO>` y las rutas según tu entorno.
Luego ejecuta:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now fennec.service
```

El servidor quedará activo en segundo plano y podrás abrir
`fennec_assistant.html` directamente cuando lo necesites.
