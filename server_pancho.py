import socket
import select
import threading
from packet_parser import *

HEADER_FORMAT = '<2sBBH'  # Formato del encabezado (ID, Device MAC, Transport Layer, ID Protocol, Length) '<2s6sBBH'
BODY_FORMAT = '<B'          # Formato del cuerpo (Batt level)

# Define la longitud de cada parte del paquete
HEADER_LENGTH = struct.calcsize(HEADER_FORMAT)
BODY_LENGTH = struct.calcsize(BODY_FORMAT)

# For data races
db_lock = threading.Lock()

def unpack(packet: bytes) -> tuple:
    
    # Desempaqueta el encabezado
    header_data = packet[:HEADER_LENGTH]
    header = struct.unpack(HEADER_FORMAT, header_data)
    packet_id, transport_layer, id_protocol, length = header #packet_id, device_mac, transport_layer, id_protocol, length = header

    headers =  {
        "packet_id": packet_id,
        #"mac": mac,
        "transport_layer": transport_layer,
        "id_protocol": id_protocol,
        "length": length,
    }

    data = ['batt_level','timestamp','temp','press','hum','co','rms','amp_x','frec_x','amp_y','frec_y','amp_z','frec_z']
    datos_dict = {}

    if id_protocol == 0:
        BODY_FORMAT = '<B'
        BODY_LENGTH = struct.calcsize(BODY_FORMAT)
        body_data = packet[HEADER_LENGTH:HEADER_LENGTH + BODY_LENGTH]
        parsed_data=struct.unpack(BODY_FORMAT, body_data)
        #Estructura del protocolo 0
        #Batt_level
        pass
    elif id_protocol == 1:
        BODY_FORMAT = '<BL'
        BODY_LENGTH = struct.calcsize(BODY_FORMAT)
        body_data = packet[HEADER_LENGTH:HEADER_LENGTH + BODY_LENGTH]
        parsed_data=struct.unpack(BODY_FORMAT, body_data)
        #Estructura del protocolo 1
        #Batt_level+Timestamp
        pass

    elif id_protocol == 2:
        BODY_FORMAT = '<BLBiBi'
        BODY_LENGTH = struct.calcsize(BODY_FORMAT)
        body_data = packet[HEADER_LENGTH:HEADER_LENGTH + BODY_LENGTH]
        parsed_data=struct.unpack(BODY_FORMAT, body_data)
        #Estructura del protocolo 2
        #Batt_level+Timestamp+Temp+Press+Hum+Co

    elif id_protocol == 3:
        BODY_FORMAT = '<BLBiBifffffff'
        BODY_LENGTH = struct.calcsize(BODY_FORMAT)
        body_data = packet[HEADER_LENGTH:HEADER_LENGTH + BODY_LENGTH]
        parsed_data=struct.unpack(BODY_FORMAT, body_data)

    else:
        BODY_FORMAT = '<BLBiBi2000f2000f2000f2000f2000f2000f2000f'
        BODY_LENGTH = struct.calcsize(BODY_FORMAT)
        body_data = packet[HEADER_LENGTH:HEADER_LENGTH + BODY_LENGTH]
        parsed_data = struct.unpack(BODY_FORMAT, body_data)

    length = len(parsed_data)
    for i in range(length):
        datos_dict[data[i]] = parsed_data[i]

    return headers ,datos_dict
   




# Función para manejar la conexión TCP con el cliente
def handle_client_tcp(client_tcp, addr):
    print(f"Conexión TCP establecida desde {addr}")
    # Receive packet
    while True:
        values_db = handle_packet(client_tcp)
        print(values_db)
        break
    client_tcp.close()
    print(f"Conexión TCP cerrada desde {addr}")

# Función para manejar la conexión UDP con el cliente
def handle_client_udp(udp_socket):
    print(f"Paquete UDP recibido desde {addr}")
    while True:
        values_db, addr = handle_packet(udp_socket)
        print(values_db)
        break

def handle_packet(client_socket):
    # Check request for config
    CONF = 4
    addr = None
    data = b""
    # Recibe datos del cliente
    if client_socket.type == socket.SOCK_STREAM:
        data = client_socket.recv(CONF)
    elif client_socket.type == socket.SOCK_DGRAM:
        data, addr = client_socket.recvfrom(CONF)

    # Maneja el mensaje de solicitud inicial
    if data == b"CONF":
        # Envía la configuración inicial al cliente
        if addr:# UDP
            initial_config = send_conf(client_socket, addr)
        else:   # TCP
            initial_config = send_conf(client_socket)
        return "Config sent"

    # Header
    N = 12 - CONF
    if client_socket.type == socket.SOCK_STREAM:
        header = client_socket.recv(N)
    elif client_socket.type == socket.SOCK_DGRAM:
        header, addr = client_socket.recvfrom(N)
    if not header:
        print("Not header data")
        return

    data += header
    print(data)
    header_dict = unpack(data)
    print(header_dict)
    
    
    
    return header_dict

def send_conf(client_socket, addr=None):
    id_protocol, transport_layer = (0,0)
    print(id_protocol, transport_layer)
    conf_packet = pack_conf(id_protocol, transport_layer)
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
    tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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