import socket
import os

def handle_client(client_socket, client_address):
    print(f"[+] Terhubung dengan {client_address}")

    try:
        request = client_socket.recv(1024).decode()
        print(f"[REQUEST] {request}")

        if not request:
            client_socket.close()
            return

        headers = request.split('\n')
        filename = headers[0].split()[1]

        if filename == '/':
            filename = '/index.html'

        filepath = '.' + filename
        if os.path.isfile(filepath):
            with open(filepath, 'rb') as f:
                content = f.read()
            response = b"HTTP/1.1 200 OK\r\n"
            response += b"Content-Type: text/html\r\n"
            response += b"Content-Length: " + str(len(content)).encode() + b"\r\n"
            response += b"\r\n" + content
        else:
            content = b"<html><body><h1>404 Not Found</h1></body></html>"
            response = b"HTTP/1.1 404 Not Found\r\n"
            response += b"Content-Type: text/html\r\n"
            response += b"Content-Length: " + str(len(content)).encode() + b"\r\n"
            response += b"\r\n" + content

        client_socket.sendall(response)
    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        client_socket.close()
        print(f"[-] Koneksi dengan {client_address} ditutup")

def start_server(host='127.0.0.1', port=6789):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"[START] Server berjalan di {host}:{port}")

    while True:
        client_socket, client_address = server.accept()
        handle_client(client_socket, client_address)

if __name__ == "__main__":
    start_server()
