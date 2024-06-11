import pygatt
from pygatt.backends import BGAPIBackend
from time import sleep

# Inicializar la conexión PyGatt 
adapter = pygatt.GATTToolBackend()

ESP_MAC = 'C8:C9:A3:D0:7B:12'

# Usada para convertir un UUID de 16 bits a 128 bits
# Los bits fijos son utilizados para BLE ya que todos los UUID de BLE son de 128 bits
# y tiene este formato: 0000XXXX-0000-1000-8000-00805F9B34FB
def convert_to_128bit_uuid(short_uuid):
    base_uuid = "00000000-0000-1000-8000-00805F9B34FB"
    short_uuid_hex = "{:04X}".format(short_uuid)
    return base_uuid[:4] + short_uuid_hex + base_uuid[8:]

CHARACTERISTIC_UUID = convert_to_128bit_uuid(0xFF01) 

#funcion callback , que se ejecuta cada vez que lelga una notificacion.
def handle_notification(handle, value):
    print('Notificación recibida:', value.hex())

while True:
    try:
        adapter.start()
        print("Intentando conectar...")
        device = adapter.connect(ESP_MAC, timeout=30)
        device.subscribe(CHARACTERISTIC_UUID, callback=handle_notification)
        print("Conectado y suscrito a las notificaciones")
        
        # Mantener la conexión activa (puedes ajustar este tiempo según sea necesario)
        while True:
            print("concexion activa")
            sleep(1000)
                
    except pygatt.exceptions.NotConnectedError:
        print("No se logró conectar, intentando nuevamente en 5 segundos...")
        sleep(5)  # Espera antes de volver a intentar

    except Exception as e:
        print(f"Ocurrió un error: {e}")
    
    finally:
        try:
            adapter.stop()
        except Exception as e:
            print(f"Error al detener el adaptador: {e}")

