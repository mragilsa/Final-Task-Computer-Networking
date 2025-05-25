import socket
import os
import time

HOST = '127.0.0.1'
PORT = 6789

def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}")

def get_content_type(filename):
    if filename.endswith(".html"): return "text/html"
    if filename.endswith(".css"):  return "text/css"
    if filename.endswith(".js"):   return "application/javascript"
    return "text/plain"

def handle_client(sock):
    try:
        request = sock.recv(1024).decode()
        if not request:
            sock.close()
            return

        log("[REQUEST]")
        print(request.strip())

        line = request.splitlines()[0]
        method, path, _ = line.split()

        if method != "GET":
            response = "HTTP/1.1 405 Method Not Allowed\r\n\r\nMethod Not Allowed"
            sock.sendall(response.encode())
            return

        if path == "/generate":
            log("Simulating QR generation...")
            time.sleep(10)
            html = "QR Generated ✅"
            response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/html\r\n"
                f"Content-Length: {len(html)}\r\n"
                "Connection: close\r\n\r\n"
            ) + html
            sock.sendall(response.encode())
            return

        # Serve file
        filepath = "." + (path if path != "/" else "/index.html")
        if os.path.isfile(filepath):
            with open(filepath, "rb") as f:
                content = f.read()
            header = (
                "HTTP/1.1 200 OK\r\n"
                f"Content-Type: {get_content_type(filepath)}\r\n"
                f"Content-Length: {len(content)}\r\n"
                "Connection: close\r\n\r\n"
            ).encode()
            sock.sendall(header + content)
        else:
            response = "HTTP/1.1 404 Not Found\r\n\r\n404 Not Found"
            sock.sendall(response.encode())

    except Exception as e:
        log(f"Error: {e}")
    finally:
        sock.close()
        log("Client disconnected")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(1)
    log(f"Server listening on http://{HOST}:{PORT}")

    while True:
        client_sock, client_addr = server.accept()
        log(f"Client connected from {client_addr}")
        handle_client(client_sock)

if __name__ == "__main__":
    start_server()
