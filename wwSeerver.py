import socket
import threading
import os

# Configuration
PROXY_IP = '127.0.0.1'
PROXY_PORT = 9000
DOC_ROOT = os.getcwd()  # Use the current working directory as the document root

def handle_client(client_socket):
    request = client_socket.recv(1024).decode()  # Receive and decode the HTTP request
    filename = parse_request(request)
    # print(request)
    # print(filename)
    if filename:
        if filename.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
            response = serve_image(filename)
        else:
            response = serve_file(filename)
    else:
        response = "HTTP/1.1 404 Not Found\r\n\r\n404 Not Found"
    # print(response)
    # response_bytes = response.encode()  # Encode the response as bytes

    if isinstance(response, str):
        response = response.encode()  # Encode the response as bytes if it's a string

    client_socket.send(response)
    client_socket.close()
    


def parse_request(request):
    try:
        # Extract the requested filename from the HTTP request
        filename = request.split(' ')[1]
        if filename.startswith("/"):
            filename = filename[1:]
        return filename
    except Exception as e:
        return None

def serve_file(filename):
    try:
        with open(os.path.join(DOC_ROOT, filename), 'r') as file:
            content = file.read()
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n{content}"
            return response.encode()
    except FileNotFoundError:
        return "HTTP/1.1 404 Not Found\r\n\r\n404 Not Found".encode()

def serve_image(filename):
    try:
        with open(os.path.join(DOC_ROOT, filename), 'rb') as file:
            content = file.read()
            content_type = "image/jpeg" if filename.endswith(('.jpg', '.jpeg')) else "image/png"
            response = f"HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\n\r\n".encode() + content
            return response
    except FileNotFoundError:
        return "HTTP/1.1 404 Not Found\r\n\r\n404 Not Found".encode()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((PROXY_IP, PROXY_PORT))
    server.listen(5)
    print(f"Listening on {PROXY_IP}:{PROXY_PORT}")

    while True:
        client, addr = server.accept()
        client_thread = threading.Thread(target=handle_client, args=(client,))
        client_thread.start()

if __name__ == '__main__':
    main()
