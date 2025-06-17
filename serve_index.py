import http.server
import os
import socketserver
import threading
import webbrowser


def serve_index() -> None:
    """Serve index.html on localhost and open it in the default browser."""
    port = int(os.environ.get("PORT", "8000"))
    url = f"http://localhost:{port}/index.html"
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        threading.Timer(1.0, lambda: webbrowser.open(url)).start()
        print(f"Serving KB at {url} (Ctrl+C to stop)")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    serve_index()
