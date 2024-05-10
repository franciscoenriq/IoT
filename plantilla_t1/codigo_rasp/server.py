'''


import socket

HOST = '0.0.0.0'  # Escucha en todas las interfaces disponibles
PORT = 1234       # Puerto en el que se escucha

# Crea un socket para IPv4 y conexión TCP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    print("El servidor está esperando conexiones en el puerto", PORT)

    while True:
        conn, addr = s.accept()  # Espera una conexión
        with conn:
            print('Conectado por', addr)
            data = conn.recv(1024)  # Recibe hasta 1024 bytes del cliente
            if data:
                print("Recibido: ", data.decode('utf-8'))
                respuesta = "tu mensaje es: " + data.decode('utf-8')
                respuesta2 = (1,2)
                conn.sendall(respuesta.encode('utf-8'))  # Envía la respuesta al cliente


'''
import struct 
import socket 
# Define la estructura del encabezado y el cuerpo
HEADER_FORMAT = '<2s6sBBH'  # Formato del encabezado (ID, Device MAC, Transport Layer, ID Protocol, Length)
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
    packet_id, device_mac, transport_layer, id_protocol, length = header

    # Desempaqueta el cuerpo
    body_data = packet[HEADER_LENGTH:HEADER_LENGTH + BODY_LENGTH]
    body = struct.unpack(BODY_FORMAT, body_data)

    return header, body

HOST = '0.0.0.0'  # Escucha en todas las interfaces disponibles
PORT = 1234       # Puerto en el que se escucha

# Crea un socket para IPv4 y conexión TCP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    print("El servidor está esperando conexiones en el puerto", PORT)

    while True:
        conn, addr = s.accept()  # Espera una conexión
        with conn:
            print('Conectado por', addr)
            data = conn.recv(1024)  # Recibe hasta 1024 bytes del cliente
            if data:
                print("Recibido: ", data)
                
                try:
                    # Desempaqueta el paquete recibido
                    header, body = unpack(data)
                    print("Header:", header)
                    print("Body:", body)
                    
                    # Aquí puedes manejar los datos del encabezado y del cuerpo como desees
                    
                    # Envía una respuesta al cliente
                    respuesta = "Paquete recibido correctamente"
                    conn.sendall(respuesta.encode('utf-8'))  # Envía la respuesta al cliente
                except ValueError as e:
                    print("Error al desempaquetar el paquete:", e)
                    respuesta = "Error al procesar el paquete"
                    conn.sendall(respuesta.encode('utf-8'))  # Envía la respuesta de error al cliente