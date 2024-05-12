import socket
import select
import threading
from packet_parser import *
from modelos import add_data_to_database, get_conf

# For data races
db_lock = threading.Lock()

# Función para manejar la conexión TCP con el cliente
def handle_client_tcp(client_tcp, addr):
    print(f"Conexión TCP establecida desde {addr}")
    # Receive packet
    while True:
        values_db = parse_packet(client_tcp)
        with db_lock:
            add_data_to_database(values_db)
    client_tcp.close()
    print(f"Conexión TCP cerrada desde {addr}")

# Función para manejar la conexión UDP con el cliente
def handle_client_udp(udp_socket):
    print(f"Paquete UDP recibido desde {addr}")
    values_db, addr = parse_packet(udp_socket, True)
    with db_lock:
        add_data_to_database(values_db)

def parse_packet(client_socket, udp=False):
    # Header
    N = 12
    data = bytearray()
    if client_socket.type == socket.SOCK_STREAM:
        data = client_socket.recv(N)
    elif client_socket.type == socket.SOCK_DGRAM:
        data, addr = client_socket.recvfrom(N)
    if not data:
        return

    header_dict = unpack_header(data)
    length = header_dict["length"]

    # Body
    if client_socket.type == socket.SOCK_STREAM:
        data = client_socket.recv(length - N)
    elif client_socket.type == socket.SOCK_DGRAM:
        data = client_socket.recvfrom(length - N)
    if not data:
        return
    values_db = parse_body(header_dict, data)
    if udp:
        return values_db, addr
    return values_db

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
                client_handler_udp = threading.Thread(target=handle_client_udp, args=(udp_socket))
                client_handler_udp.start()


if __name__ == "__main__":
    main()
