from socket import *
import re
import threading
from urllib.parse import urlparse

PROXY_IP = "127.0.0.1"
PROXY_PORT = 8080  # Proxy server port

TARGET_IP = "127.0.0.1"
TARGET_PORT = 9000  # Target server port

PROXY_ADDR = (PROXY_IP, PROXY_PORT)
TARGET_ADDR = (TARGET_IP, TARGET_PORT)

print("Proxy server listening on", PROXY_ADDR)

# Create a TCP socket for the proxy server
proxyServerSocket = socket(AF_INET, SOCK_STREAM)
proxyServerSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
proxyServerSocket.bind(PROXY_ADDR)
proxyServerSocket.listen(100)

http_status_codes = {
    200: "OK",
    404: "Not Found",
    301: "Moved Permanently",
    # Add more status codes as needed
}

# Function to handle client requests and forward them to the target server
def handle_client(client_socket):
    try:
        # Connect to the target server
        target_server_socket = socket(AF_INET, SOCK_STREAM)
        target_server_socket.connect(TARGET_ADDR)

        while True:
            # Receive data from the client
            data = client_socket.recv(4096)
            
            if not data:
                break

            # Forward the client's request to the target server
            target_server_socket.send(data)

            # Receive the response from the target server
            response = target_server_socket.recv(4096)
            
            if not response:
                break

            # Parse the response to understand the status code
            response_lines = response.decode('utf-8').split('\r\n')
            status_line = response_lines[0]
            match = re.match(r'HTTP/\d+\.\d+ (\d+) (.+)', status_line)
            if match:
                status_code = int(match.group(1))
                reason_phrase = match.group(2)

                # Handle different HTTP status codes
                if status_code == 200:
                    print(f"Received a 200 (OK) response from the target server for {target_server_socket}")
                    pass
                elif status_code == 404:
                    # Handle 404 Not Found response
                    print(f"Received a 404 (Not Found) response from the target server for {target_server_socket}")
                    pass


            # Send the response back to the client
            client_socket.send(response)
    except Exception as e:
        print("Error:", e)

    finally:
        client_socket.close()
        target_server_socket.close()
# Existing functionality for handling HTTP requests
def handle_http_requests(client_socket, client_address):
    target_server_socket = None  # Initialize the variable with None
    try:
        # Receive the client's HTTP request
        request_message = client_socket.recv(4096).decode('utf-8')
        # print("request message: ", request_message)
        if not request_message:
            return

        # Extract the requested URL from the request
        request_lines = request_message.split('\n')
        request_line = request_lines[0].strip()
        method, url, protocol = request_line.split(' ')

        # Forward the original request to the target server
        target_server_socket = socket(AF_INET, SOCK_STREAM)
        target_server_socket.connect(TARGET_ADDR)
        target_server_socket.send(request_message.encode('utf-8'))

        # Receive the response from the target server
        response_message = b""
        while True:
            data = target_server_socket.recv(4096)
            if not data:
                break
            response_message += data

        # Forward the response to the client
        client_socket.send(response_message)

    except Exception as e:
        print("Error:", e)

    finally:
        if target_server_socket is not None:
            target_server_socket.close()  # Close the socket if it was created

    client_socket.close()  # Always close the client socket

while True:
    # Accept client connections
    client_socket, client_address = proxyServerSocket.accept()
    
    # Create a thread to handle the client request
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()

    # Existing functionality: Handle HTTP requests in a separate thread
    http_thread = threading.Thread(target=handle_http_requests, args=(client_socket, client_address))
    http_thread.start()
