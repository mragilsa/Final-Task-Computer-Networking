import socket, threading, os

def handle_client(sock, addr):
    print(f"[+] {addr} terhubung")
    try:
        req = sock.recv(1024).decode()
        print(f"[REQ] {req}")
        if not req: return

        path = req.split()[1]
        path = '/index.html' if path == '/' else path
        full_path = '.' + path

        if os.path.isfile(full_path):
            with open(full_path, 'rb') as f:
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

def start_server(host='127.0.0.1', port=1234):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"[START] {host}:{port}")
        while True:
            c, a = s.accept()
            threading.Thread(target=handle_client, args=(c, a)).start()

if __name__ == "__main__":
    start_server()
