import socket
import struct 
from packet_parser import * 
HOST = '0.0.0.0'  # Escucha en todas las interfaces disponibles
PORT = 1234       # Puerto en el que se escucha

# Define la estructura del encabezado y el cuerpo
HEADER_FORMAT = '<2sBBH'  # Formato del encabezado (ID, Device MAC, Transport Layer, ID Protocol, Length) '<2s6sBBH'
BODY_FORMAT = '<B'          # Formato del cuerpo (Batt level)

# Define la longitud de cada parte del paquete
HEADER_LENGTH = struct.calcsize(HEADER_FORMAT)
BODY_LENGTH = struct.calcsize(BODY_FORMAT)

def unpack(packet: bytes) -> tuple:
    if len(packet) < HEADER_LENGTH + BODY_LENGTH:
        raise ValueError("Packet is too short")

    # Desempaqueta el encabezado
    header_data = packet[:HEADER_LENGTH]
    header = struct.unpack(HEADER_FORMAT, header_data)
    packet_id, transport_layer, id_protocol, length = header #packet_id, device_mac, transport_layer, id_protocol, length = header
    print(packet_id)
    print(transport_layer)
    print(id_protocol)
    print(length)
    # Desempaqueta el cuerpo
    body_data = packet[HEADER_LENGTH:HEADER_LENGTH + BODY_LENGTH]
    body = struct.unpack(BODY_FORMAT, body_data)

    return header, body


def handle_client(client_socket):
    packet = client_socket.recv(HEADER_LENGTH+BODY_LENGTH)
    if packet:
        header, body = unpack(packet)
        # Imprime los datos del paquete
        print("Paquete recibido:")
        print("Header:", header)
        print("Body:", body)
    # Cierra el socket del cliente
    #client_socket.close()


#header_struct = struct.Struct("!HBBH") 

# Crea un socket para IPv4 y conexión TCP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    print("El servidor está esperando conexiones en el puerto", PORT)

    while True:
        client_socket, addr  = s.accept()  # Espera una conexión
        with client_socket:
            print('Conectado por', addr)
            #data = conn.recv(1024)  # Recibe hasta 1024 bytes del cliente
            #handle_client(client_socket)
            data = client_socket.recv(1024)
            #client_socket.send()
            print(data)
            if data == b"GET_INITIAL_CONFIG":
                paquete_inicial = pack_conf(0,0)
                print(paquete_inicial)
                client_socket.send(paquete_inicial)
                #print("enviado")








'''
HOST = '0.0.0.0'  # Escucha en todas las interfaces disponibles
PORT = 1234       # Puerto en el que se escucha

header_struct = struct.Struct("!HBBH") 

# Crea un socket para IPv4 y conexión TCP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    print("El servidor está esperando conexiones en el puerto", PORT)

    while True:
        conn, addr = s.accept()  # Espera una conexión
        with conn:
            
            print('Conectado por', addr)
            #data = conn.recv(1024)  # Recibe hasta 1024 bytes del cliente
            expected_bytes = 12 + 1 
            #data = conn.recv(expected_bytes)
            header_data = conn.recv(header_struct.size) 
            if header_data:             
                # Desempaqueta el encabezado
                id, transport_layer, id_protocol, length = header_struct.unpack(header_data)
                print("ID:", id)
                print("Transport Layer:", transport_layer)
                print("ID Protocol:", id_protocol)
                print("Length:", length)

                # Recibe el cuerpo (de longitud 'length')
                body_data = conn.recv(length)
                if body_data:
                    print("Body:", body_data)
'''


