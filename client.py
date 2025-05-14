from operator import index
import socket
import sys

def run_client(server_host, server_port, filename):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_host, int(server_port)))

        request_line = f"GET /{filename} HTTP/1.1\r\nHost: {server_host}\r\n\r\n"
        client_socket.send(request_line.encode())

        response = b""
        while True:
            chunk = client_socket.recv(1024)
            if not chunk:
                break
            response += chunk

        print("[RESPONSE]")
        print(response.decode(errors='ignore'))  # ignore untuk menghindari crash saat ada karakter non-UTF-8

        client_socket.close()
    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python client.py server_host server_port filename")
        sys.exit(1)

    _, server_host, server_port, filename = sys.argv
    run_client(server_host, server_port, filename)
