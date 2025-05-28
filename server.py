import socket, threading

def handle_client(conn, addr):
    print(f"[+] {addr} terhubung")
    try:
        request = conn.recv(1024).decode()
        print(f"[REQ] {request}")
        with open("index.html", "r") as f:
            content = f.read()
        response = f"HTTP/1.1 200 OK\nContent-Type: text/html\nContent-Length: {len(content)}\n\n{content}"
    except:
        response = "HTTP/1.1 404 Not Found\n\nFile not found"
    conn.sendall(response.encode())
    conn.close()
    print(f"[-] {addr} ditutup")

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('127.0.0.1', 5678))
    s.listen(5)
    print("[START] 127.0.0.1:5678")

    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    main()
