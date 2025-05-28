import socket
import os
import time

def handle_client(sock, addr):
    print(f"[+] {addr} terhubung")
    try:
        req = sock.recv(1024).decode()
        print(f"[REQ] {req.strip()}")
        if not req:
            return

        print(f"[INFO] Menunggu 5 detik sebelum respon ke {addr}")
        time.sleep(5)

        path = req.split()[1]
        path = '/index.html' if path == '/' else path
        file = '.' + path

        if os.path.isfile(file):
            with open(file, 'rb') as f:
                content = f.read()
            header = b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n"
        else:
            content = b"<h1>404 Not Found</h1>"
            header = b"HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n"

        header += f"Content-Length: {len(content)}\r\n\r\n".encode()
        sock.sendall(header + content)
    except Exception as e:
        print(f"[ERR] {e}")
    finally:
        sock.close()
        print(f"[-] {addr} ditutup")

def start_server(host='127.0.0.1', port=8080):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"[START] Server berjalan di {host}:{port}")
        while True:
            c, a = s.accept()
            handle_client(c, a) 

if __name__ == "__main__":
    start_server()
