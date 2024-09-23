import socket
import sys
import re
import ssl
from urllib.parse import urlparse

# Function to send an HTTP GET request to a server through a proxy or directly
def send_http_request(host, port, path):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))

        request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\n\r\n"
        client_socket.send(request.encode())

        response = client_socket.recv(1024)
        print(response)
        client_socket.close()
        return response.decode()
    except Exception as e:
        print(f"Error: {e}")
        return None
    
# Function to fetch URL content
def fetch_url(url):
    try:
        parsed_url = urlparse(url)

        if not parsed_url.netloc:
            print("Invalid URL format")
            return

        host = parsed_url.netloc
        path = parsed_url.path if parsed_url.path else "/"

        if parsed_url.scheme == "https":
            port = 443
        else:
            port = 80

        base_html = send_http_request(host, port, path)

        if base_html:
            print(base_html)
            fetch_referenced_objects(base_html, host, port)

    except Exception as e:
        print(f"Error: {e}")

# Function to parse HTML for references to other objects and fetch them
def fetch_referenced_objects(html, host, port):
    references = re.findall(r'href=["\'](https?://[^"\']+)["\']', html)

    for reference in references:
        url_parts = urlparse(reference)
        path = url_parts.path if url_parts.path else "/"

        print(f"Fetching: {reference}")
        response = send_http_request(url_parts.netloc, port, path)
        if response:
            print(response)

# Main function to handle command-line arguments
def main():
    if len(sys.argv) < 2:
        print("Usage: python3 <File_Name>.py <URL or IP>")
        sys.exit(1)

    target = sys.argv[1]

    if target.startswith("http://") or target.startswith("https://"):
        fetch_url(target)
    else:
        if len(sys.argv) < 4:
            print("Usage: python <File_Name>.py <web_server_ip> <web_server_port> <path>")
            sys.exit(1)

        host = sys.argv[1]
        port = int(sys.argv[2])
        path = sys.argv[3]
        # Assuming target is an IP address
        base_html = send_http_request(host, port, path)

        if base_html:
            print(base_html)
            fetch_referenced_objects(base_html, host, port)

if __name__ == '__main__':
    main()