# Web-Client-with-Proxy-Support
# Part-1: Client

This Python script is designed to send HTTP GET requests to a specified web server or URL and fetch its content. The script can be run with or without a proxy and allows you to specify the target web server's IP address, port, and path, or a full URL.

## Features
- Supports both HTTP and HTTPS requests.
- Can be used to fetch the HTML content of a web page and its referenced objects (e.g., images, stylesheets, scripts).
- Can run with or without a proxy.
- Parses HTML for references to other objects and fetches them.

## Prerequisites
- Python 3
- The `socket`, `sys`, `re`, `ssl`, and `urllib.parse` modules are required.

## How to Run the Script
1. Download the Python script to your local machine.

2. Open a terminal or command prompt.

3. Navigate to the directory where the script is located using the `cd` command.

4. Run the script by using one of the following methods:

   - **To fetch a URL**:
     ```
     python <File_Name>.py <URL>
     ```
     Example:
     ```
     python fetch_web_content.py https://www.example.com
     ```

   - **To specify a web server's IP address, port, and path**:
     ```
     python <File_Name>.py <web_server_ip> <web_server_port> <path>
     ```
     Example:
     ```
     python fetch_web_content.py 192.168.0.1 80 /index.html
     ```

## Important Notes
- When specifying a URL, the script will automatically detect if it's an HTTP or HTTPS URL and set the port accordingly.



# Part-2: Proxy Server for Url

This is a simple proxy server implemented in Python that can forward HTTP and HTTPS requests from clients to web servers. The proxy server listens on `127.0.0.1` at port `8080` and handles incoming connections, forwarding the client's request to the specified URL and relaying the response back to the client.

## Requirements

- Python 3 
- The `socket` and `ssl` libraries are used for socket communication and SSL handling.

## Usage

1. Clone this repository or download the `proxy_server.py` script.

2. Open a terminal and navigate to the directory where the script is located.

3. Run the script using the following command:

   ```shell
   python proxy_server.py
   ```

   You'll see a message indicating that the server is listening on `127.0.0.1:8080`.

4. Configure your web browser to use the proxy server. You can do this by going to your browser's network settings and setting the proxy server to `127.0.0.1` at port `8080`.

5. Once the proxy server is running and your browser is configured to use it, any HTTP or HTTPS requests you make will be intercepted by the proxy server.

6. The proxy server will log incoming connections and the URL requested by the client. It will forward the request to the specified URL, receive the response, and relay it back to the client.

7. To stop the proxy server, press `Ctrl+C` in the terminal.

## Important Notes

- The proxy server only listens on `127.0.0.1` for local testing. 

Here's a `README.md` for your Python proxy server code:

---

# Part-2: Proxy Server for ip Address

This is a basic Python proxy server designed to forward HTTP requests from clients to a target server. It listens on a specific IP and port, and forwards requests and responses between the client and the target server.

## Features

- Listens for incoming client connections.
- Forwards client requests to a target server.
- Receives responses from the target server and sends them back to the client.

## Requirements

- Python 3
- No additional Python packages are required.

## Usage

1. Clone this repository or download the `proxy_server.py` script.

2. Open a terminal and navigate to the directory where the script is located.

3. Customize the following variables in the script to match your requirements:

   - `PROXY_IP`: The IP address where the proxy server will listen.
   - `PROXY_PORT`: The port on which the proxy server will listen.
   - `TARGET_IP`: The IP address of the target server.
   - `TARGET_PORT`: The port of the target server.

4. Run the script using the following command:

   ```shell
   python proxy_server.py
   ```

   You'll see a message indicating that the proxy server is listening on the specified address and port.

5. Configure your web browser or client to use the proxy server by specifying the proxy server's IP address and port.

6. The proxy server will intercept HTTP requests from the client and forward them to the target server.

7. The responses from the target server will be relayed back to the client through the proxy.

8. To stop the proxy server, press `Ctrl+C` in the terminal.





# Part-3: Server

This Python script implements a HTTP server that serves files and images from a specified document root. It listens on a designated IP address and port, and upon receiving an HTTP request, it attempts to serve the requested resource from the document root.

## Features

- Serves static HTML files and images (JPEG, PNG) to clients.
- Supports a simple configuration for setting the server's IP address, port, and document root.
- Multithreaded to handle multiple client requests simultaneously.

## Prerequisites

- Python 3

## How to Run the HTTP Server

1. Download the Python script to your local machine.

2. Open a terminal or command prompt.

3. Navigate to the directory where the script is located using the `cd` command.

4. Adjust the configuration parameters at the beginning of the script if needed:

   - `PROXY_IP`: Set the IP address on which the server should listen.
   - `PROXY_PORT`: Set the port on which the server should listen.
   - `DOC_ROOT`: Set the document root directory where your files are located. By default, it uses the current working directory.

5. Start the HTTP server by running the script with the following command:

   ```
   python <File_Name>.py
   ```

   Example:

   ```
   python http_server.py
   ```

6. The server will start listening on the specified IP address and port (default: 127.0.0.1:9000). Clients can send HTTP requests to this server to request files and images from the document root.

7. To access a file, use a web browser or a tool like `curl` to send an HTTP request to the server. For example:

   ```
   http://127.0.0.1:9000/index.html
   http://127.0.0.1:9000/image.jpg
   ```

8. The server will serve the requested files and images from the document root directory.

9. To stop the server, you can terminate the script by pressing `Ctrl+C` in the terminal.

## Important Notes

- Ensure that the document root directory (`DOC_ROOT`) contains the files and images you want to serve.

- The server listens only on the local machine by default. If you want to make it accessible from other devices on the network, modify the `PROXY_IP` variable to the appropriate IP address.



# Part-4: Proxy Server with Caching

This Python script implements a proxy server with caching functionality. It allows you to intercept and cache HTTP requests made by clients, effectively acting as an intermediary between clients and web servers.

## Features

- Acts as a proxy server to forward HTTP requests from clients to web servers.
- Implements caching of HTTP responses to improve response time and reduce the load on web servers.
- Provides a simple mechanism to print cached URLs and their timestamps periodically.

## Prerequisites

- Python 3

## How to Run the Proxy Server

1. Download the Python script to your local machine.

2. Open a terminal or command prompt.

3. Navigate to the directory where the script is located using the `cd` command.

4. Start the proxy server by running the script with the following command:

   ```
   python <File_Name>.py
   ```
   Example:
   ```
   python proxy_server.py
   ```

5. The proxy server will start listening on the specified IP address and port (default: 127.0.0.1:8081). You can adjust these settings by modifying the `PROXY_IP` and `PROXY_PORT` variables at the beginning of the script.

6. To use the proxy server, configure your web browser or client application to use the proxy settings. Set the proxy address to the one defined in the script (e.g., 127.0.0.1:8081).

7. Once the proxy is configured, your web browser or client application will route its HTTP requests through the proxy server.

8. The proxy server will cache responses for a duration specified by the `CACHE_TIMEOUT` variable (default: 300 seconds). Cached responses will be served from the cache until the timeout is reached.

9. Periodically, the script will print the cached URLs and their timestamps, allowing you to see which resources are in the cache.

## Important Notes



- The proxy server listens only on the local machine by default. If you want to make it accessible from other devices on the network, modify the `PROXY_IP` variable to the appropriate IP address.

- To stop the proxy server, you can terminate the script by pressing `Ctrl+C` in the terminal. The server will clean up and exit gracefully.
