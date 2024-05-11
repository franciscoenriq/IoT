import socket
import select
import threading
from packet_parser import pack, unpack, pack_conf
from modelos import add_data_to_database, get_conf

# For data races
db_lock = threading.Lock()

# Función para manejar la conexión TCP con el cliente
def handle_client_tcp(client_tcp, addr):
    print(f"Conexión TCP establecida desde {addr}")
    # Receive packet
    while True:
        header = client_tcp.recv(12).decode()
        if not header:
            break
        # with db_lock:
        #     add_data_to_database()
    client_tcp.close()
    print(f"Conexión TCP cerrada desde {addr}")

# Función para manejar la conexión UDP con el cliente
def handle_client_udp(data, addr, udp_socket):
    print(f"Paquete UDP recibido desde {addr}: {data.decode()}")
    # with db_lock:
    #     add_data_to_database(data.decode())
    udp_socket.sendto("Respuesta UDP".encode(), addr)

def parse_header(client_tcp):
    N = 12
    # Helper function to recv n bytes or return None if EOF is hit
    data = bytearray()
    while len(data) < N:
        packet = sock.recv(N - len(data))
        if not packet:
            return None
        data.extend(packet)
    # data = sock.recv(N)
    return data

def send_conf(client_socket, addr):
    conf_packet = pack_conf(get_conf())
    if client_socket.type == socket.SOCK_STREAM:
        client_socket.send(conf_packet)
    elif client_socket.type == socket.SOCK_DGRAM:
        client_socket.sendto(conf_packet, addr)
    else:
        print("Unknown socket type")

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
        sockets_list = [tcp_socket, udp_socket]

        read_sockets, _, _ = select.select(sockets_list, [], [])

        for sock in read_sockets:
            if sock == tcp_socket:
                client_tcp, addr = tcp_socket.accept()
                client_handler_tcp = threading.Thread(target=handle_client_tcp, args=(client_tcp, addr))
                client_handler_tcp.start()
            elif sock == udp_socket:
                data, addr = udp_socket.recvfrom(1024)
                client_handler_udp = threading.Thread(target=handle_client_udp, args=(data, addr, udp_socket))
                client_handler_udp.start()


if __name__ == "__main__":
    main()
