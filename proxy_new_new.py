import socket
import threading
from urllib.parse import urlparse
import ssl

def handle_client_url(client_socket):
    try:
        # Receive data from the client (web browser)
        request_data = client_socket.recv(4096)

        if not request_data:
            client_socket.close()
            return
        #print(request_data)

        # Parse the request to extract the host and port
        request_lines = request_data.split(b'\n')
        first_line = request_lines[0].decode('utf-8')
        method, url, protocol  = first_line.split(' ')
        #host, port = url.split(':')[0], 80  # Default to HTTP port
        print('client Connecting with', url)

        print('req_data: ', request_data)
        server_response=fetch_url(url,request_data)
        client_socket.send(server_response)

    except Exception as e:
        print(f"Error handling client: {e}")

    client_socket.close()
    #server_socket.close()
def fetch_url(url,request_data):
    parsed_url = urlparse(url)

    if not parsed_url.netloc:
            print("Invalid URL format")
            return

    host = parsed_url.netloc
    path = parsed_url.path if parsed_url.path else "/"

        # Create a socket to connect to the web server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Check if it's an HTTPS connection and adjust the port
    if parsed_url.scheme == "https":
        port = 443
        server_socket = ssl.wrap_socket(server_socket, ssl_version=ssl.PROTOCOL_SSLv23)

    else:
        port = 80

    server_socket.connect((host, port))
    print('sending request')

        # Forward the client's request to the web server
    server_socket.send(request_data)
        # Receive data from the web server and forward it to the client
    while True:
        server_response = server_socket.recv(4096)
        if len(server_response) == 0:
            break
        print('Response received and sending to client')
        return(server_response)
       


def main():
    # Create a listening socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 8080))
    server.listen(5)
    print("[*] Listening on 127.0.0.1:8080")

    while True:
        client_socket, addr = server.accept()
        print()
        print(f"[*] Accepted connection from client address: {addr[0]}:{addr[1]}")
        client_handler = threading.Thread(target=handle_client_url, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    main()
