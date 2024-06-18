import pygatt
import struct
import socket 
from time import sleep

# Inicializar la conexión PyGatt 
adapter = pygatt.GATTToolBackend()

ESP_MAC = 'C8:C9:A3:D0:7B:12'

# Usada para convertir un UUID de 16 bits a 128 bits
def convert_to_128bit_uuid(short_uuid):
    base_uuid = "00000000-0000-1000-8000-00805F9B34FB"
    short_uuid_hex = "{:04X}".format(short_uuid)
    return base_uuid[:4] + short_uuid_hex + base_uuid[8:]

CHARACTERISTIC_UUID = convert_to_128bit_uuid(0xFF01) 


# Función callback que se ejecuta cada vez que llega una notificación.
def handle_notification(device,handle, value):
    print("recibiendo datos..")
    print("Data: {}".format(value.hex()))
    print("Handle: {}".format(handle))

    try:
        ascii_message = value.decode('ascii')
        print('Notificación recibida (ASCII):', ascii_message)
        if value == b'CONFIG':
            packet = config_packet_example()
            # Write to the characteristic when 'CONFIG' is received
            
            #device.char_write(CHARACTERISTIC_UUID, b'Some data to send')
            device.char_write(CHARACTERISTIC_UUID, packet)
    except UnicodeDecodeError:
        pass 



    

# Definición de la estructura de datos
def create_config_packet(status, id_protocol, bmi270_sampling, bmi270_acc_sensibility,
                         bmi270_gyro_sensibility, bme688_sampling, discontinuous_time,
                         port_tcp, port_udp, host_ip_addr, ssid, password):
    
    host_ip_bytes = socket.inet_aton(host_ip_addr)
    
    data = struct.pack('<bbiiiiiiii10s10s', status, id_protocol, bmi270_sampling,
                   bmi270_acc_sensibility, bmi270_gyro_sensibility, bme688_sampling,
                   discontinuous_time, port_tcp, port_udp, int.from_bytes(host_ip_bytes, byteorder='little'), 
                   ssid.encode('utf-8'), password.encode('utf-8'))
    return data 

def config_packet_example():
    print("Creando el paquete de configuración...")
    config_packet = create_config_packet(
        status = 1,
        id_protocol = 2,
        bmi270_sampling = 100,
        bmi270_acc_sensibility = 4,
        bmi270_gyro_sensibility = 250,
        bme688_sampling = 2,
        discontinuous_time = 60,
        port_tcp = 1234,
        port_udp = 5678,
        host_ip_addr="192.168.1.1",  
        ssid="tu_ssid",
        password="tu_password"
    )
    print("Paquete de configuración creado: ", config_packet.hex())
    return config_packet
    



def connect_and_subscribe():
    try:
        adapter.start()
        print("Adaptador iniciado, intentando conectar...")
        device = adapter.connect(ESP_MAC, timeout=30)
        print("Conectado al dispositivo")
        
        device.subscribe(CHARACTERISTIC_UUID, callback=lambda handle, value: handle_notification(device, handle, value))
        print("Suscrito a las notificaciones")
                
    except pygatt.exceptions.NotConnectedError:
        print("No se logró conectar, intentando nuevamente en 5 segundos...")
        sleep(5)  # Espera antes de volver a intentar

    except Exception as e:
        print(f"Ocurrió un error: {e}")
    
    finally:
        try:
            adapter.stop()
            print("Adaptador detenido")
        except Exception as e:
            print(f"Error al detener el adaptador: {e}")

connect_and_subscribe()
