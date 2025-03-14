import socket
import threading
import logging

logging.basicConfig(filename="honeypot.log", level=logging.INFO, format="%(asctime)s - %(message)s") # Log file

PORTS = [22, 80, 4444] # Ports to listen on (e.g., SSH, HTTP, and a custom port)

def honeypot_server(port):
    # Listens on the specified port, captures incoming connections, and logs them.
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a socket for communication (IPv4, TCP)
    server_socket.bind(("0.0.0.0", port)) # Bind the socket to all available network interfaces on the given port
    server_socket.listen(5) ## Start listening for incoming connections (max 5 clients in queue)
    print(f"[INFO] Honeypot is listening on port {port}...")

    while True:
        client_socket, addr = server_socket.accept() # Accept incoming connection from a client
        print(f"[ALERT] Connection attempt: {addr[0]}:{addr[1]} -> Port {port}")
        
        logging.info(f"Connection attempt from {addr[0]}:{addr[1]} -> Port {port}") # Log the connection attempt details (IP, Port, Time)
        
        client_socket.send(b"Connection accepted. \n") # Send a response message to the attacker (pretending to be a real service)

        # Close the client socket after sending the response
        client_socket.close() 

# Start listening on multiple ports using threads
threads = []
for port in PORTS:
    thread = threading.Thread(target=honeypot_server, args=(port,))
    threads.append(thread)
    thread.start()

# Wait for all threads to finish
for thread in threads: 
    thread.join()
