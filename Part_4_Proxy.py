from socket import *
import re
import threading
from datetime import datetime
import time

PROXY_IP = "127.0.0.1"
PROXY_PORT = 8082

PROXY_ADDR = (PROXY_IP, PROXY_PORT)
CACHE_TIMEOUT = 300

print("Proxy server listening on", PROXY_ADDR)

# Create a TCP socket
proxyServerSocket = socket(AF_INET, SOCK_STREAM)
proxyServerSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
proxyServerSocket.bind(PROXY_ADDR)
proxyServerSocket.listen(100)

# Create a dictionary to store cached URLs and their timestamps
cached_urls = {}

def handle_client(client_socket, client_address):
    try:
        # Initialize the response_message variable
        response_message = None

        # Receive the client's request along with the address it is coming from
        request_message = client_socket.recv(104857)

        if not request_message:
            return

        # Extract the Host header from the request using 'ISO-8859-1' encoding
        host_header = re.search('Host: (.)+(:[0-9]{1,5})?', request_message.decode('ISO-8859-1'))
        host = host_header.group(0)[6:-1]

        if host in cached_urls:
            cached_time = int(cached_urls[host])
            current_time = int(time.time())

            if current_time - cached_time <= CACHE_TIMEOUT:
                print("Serving from cache:", host, "Timestamp:", time.ctime(cached_time))
            else:
                print("Cache timeout exceeded for", host)
                del cached_urls[host]
        else:
            # Make sure to assign response_message here
            response_message = request_message

            try:
                host_ip, host_port = host.split(':')
                host_addr = (host_ip, int(host_port))
            except ValueError as e:
                host_addr = (host.replace("\r", ""), 80)

            server_socket = socket(AF_INET, SOCK_STREAM)

            try:
                server_socket.connect(host_addr)
            except Exception as e:
                print("Error connecting to", host_addr, "error:", e)

            server_socket.sendall(response_message)

        response_payload = None

        # Check if the URL is cached and display its timestamp
        if host in cached_urls:
            print(f"Serving from cache: {host} Timestamp: {cached_urls[host]}")

        while True:
            try:
                while True:
                    response_payload = server_socket.recv(104857)

                    if not response_payload:
                        break

                    # Forward the response payload to the client
                    client_socket.sendall(response_payload)

                client_socket.close()
                server_socket.close()
                break

            except timeout:
                if host[-3:] != "443":
                    print("Timeout occurred for", host)
                pass

    except ConnectionResetError as e:
        if host[-3:] != "443":
            print("Connection reset for", host)
    else:
        # Add or update the cached URL and its timestamp
        cached_urls[host] = datetime.now().strftime("%c")

# Print cached URLs and their timestamps
def print_cached_urls():
    while True:
        time.sleep(10)  # Adjust this interval as needed
        print("Cached URLs:")
        for url, timestamp in cached_urls.items():
            print(f"Url: {url}, Timestamp: {timestamp}")

# Create a separate thread to periodically print cached URLs
cache_thread = threading.Thread(target=print_cached_urls)
cache_thread.start()

# Main thread to handle incoming client connections
try:
    while True:
        # Accept a connection from a client
        client_socket, client_address = proxyServerSocket.accept()

        # Create a thread to handle the multiple connections
        thread = threading.Thread(target=handle_client, args=(client_socket, client_address))

        # Start the thread using the start function
        thread.start()

except KeyboardInterrupt:
    proxyServerSocket.close()
    print("KeyboardInterrupt occurred, socket shutdown")