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

'''
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
'''
def handle_client(client_socket):
    # Recibe datos del cliente
    data = client_socket.recv(1024)

    # Maneja el mensaje de solicitud inicial
    if data == b"GET_INITIAL_CONFIG":
        # Envía la configuración inicial al cliente
        initial_config = pack_conf(0,0) # Ejemplo de configuración inicial (transport_layer = 1, id_protocol = 0)
        client_socket.sendall(initial_config)
    else:
        packet = client_socket.recv(HEADER_LENGTH+BODY_LENGTH)
        unpack_header(packet)
        # Maneja otro tipo de mensaje (datos)
        # Haz lo que necesites con los datos recibidos aquí
        print("Mensaje de datos recibido:", data)


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
        
            data = client_socket.recv(1024) #recibimos pa cabecera 
            #client_socket.send()
            print(data)
            if data == b"GET_INITIAL_CONFIG":

                paquete_inicial = pack_conf(0,0) # la idea es que los valores realmente los saquemos de 
                print(paquete_inicial)
                client_socket.send(paquete_inicial)
                #print("enviado")
            else:
                print("entramos aca")
                
                #headers_values = unpack_header(data)
                #datos = parse_body(headers_values,data)
                header, body = unpack(data)
                print(header)
                print(body)
                

