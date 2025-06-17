#!/bin/bash
PORT=${PORT:-8000}
URL="http://localhost:$PORT/index.html"

python3 -m http.server "$PORT" &
SERVER_PID=$!

sleep 1

if command -v xdg-open >/dev/null 2>&1; then
  xdg-open "$URL" >/dev/null 2>&1
elif command -v open >/dev/null 2>&1; then
  open "$URL" >/dev/null 2>&1
fi

echo "Serving KB at $URL (Ctrl+C to stop)"
wait $SERVER_PID
