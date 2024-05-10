import socket

HOST = '0.0.0.0'  # Escucha en todas las interfaces disponibles
PORT = 1234       # Puerto en el que se escucha

def server_program():
    # Create a UDP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind the socket to the host and port
    server_socket.bind((HOST, PORT))

    print("El servidor está esperando conexiones en el puerto", PORT)

    while True:
        # Receive data from a client
        data, addr = server_socket.recvfrom(1024)  # 1024 is the buffer size
        print(f"Recibido por {addr}: {data.decode()}")

        # Send data back to the client
        server_socket.sendto(b"Hello from the server!", addr)

if __name__ == "__main__":
    server_program()
