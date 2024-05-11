import socket
import threading
import psycopg2
import modelos

# Bloqueo para sincronizar el acceso a la base de datos
db_lock = threading.Lock()

# Función para manejar la conexión TCP con el cliente
def handle_client_tcp(client_tcp, addr):
    print(f"Conexión TCP establecida desde {addr}")
    while True:
        data = client_tcp.recv(1024).decode()
        if not data:
            break
        # Agregar datos a la base de datos de manera segura
        with db_lock:
            modelos.add_data_to_database(data)
        # Aquí puedes implementar la lógica para comunicarte con el cliente a través de TCP
    client_tcp.close()
    print(f"Conexión TCP cerrada desde {addr}")

# Función para manejar la conexión UDP con el cliente
def handle_client_udp(data, addr, udp_socket):
    print(f"Paquete UDP recibido desde {addr}: {data.decode()}")
    # Agregar datos a la base de datos de manera segura
    with db_lock:
        add_data_to_database(data.decode())
    # Aquí puedes implementar la lógica para comunicarte con el cliente a través de UDP
    udp_socket.sendto("Respuesta UDP".encode(), addr)

def main():
    host = '0.0.0.0'
    port = 1234

    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    tcp_socket.bind((host, port))
    udp_socket.bind((host, port))

    tcp_socket.listen(5)
    print("Servidor esperando conexiones...")

    while True:
        client_tcp, addr = tcp_socket.accept()
        client_handler_tcp = threading.Thread(target=handle_client_tcp, args=(client_tcp, addr))
        client_handler_tcp.start()

        data, addr = udp_socket.recvfrom(1024)
        client_handler_udp = threading.Thread(target=handle_client_udp, args=(data, addr, udp_socket))
        client_handler_udp.start()

if __name__ == "__main__":
    main()
