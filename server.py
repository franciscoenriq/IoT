import socket
import threading
import psycopg2
import modelos
from packet_parser import pack, unpack
from modelos import add_data_to_database, get_conf

# For data races
db_lock = threading.Lock()

# Función para manejar la conexión TCP con el cliente
def handle_client_tcp(client_tcp, addr):
    print(f"Conexión TCP establecida desde {addr}")
    # Receive header
    while True:
        header = client_tcp.recv(12).decode()
        size = unpack_header(header)[-1] # body byte size
        if not header:
            break
    # Receive body
    while True:
        body = client_tcp.recv(size).decode()
        if not body:
            break
        parse_packet(body)
        with db_lock:
            add_data_to_database()
    client_tcp.close()
    print(f"Conexión TCP cerrada desde {addr}")

# Función para manejar la conexión UDP con el cliente
def handle_client_udp(data, addr, udp_socket):
    print(f"Paquete UDP recibido desde {addr}: {data.decode()}")
    with db_lock:
        add_data_to_database(data.decode())
    udp_socket.sendto("Respuesta UDP".encode(), addr)

def parse_packet(packet):
    data = unpack()
    datos_data = {
        'id_device': ,
        'mac': ,
        'timestamp': ,
        'batt_level': ,
        'temp': ,
        'press': ,
        'hum': ,
        'co': ,
        'rms': ,
        'amp_x': ,
        'freq_x': ,
        'amp_y': ,
        'freq_y': ,
        'amp_z': ,
        'freq_z': ,
        'acc_x': ,
        'acc_y': ,
        'acc_z': ,
        'rgyr_x': ,
        'rgyr_y': ,
        'rgyr_z': ,
    }

    logs_data = {
        'id_device': ,
        'id_protocol': ,
        'transport_layer': ,
        'timestamp': ,
    }

    loss_data = {
        'delay': ,
        'packet_loss': ,
    }

    return datos_data, logs_data, loss_data

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
