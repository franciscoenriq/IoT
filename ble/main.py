import asyncio
import struct
import socket
import sys
from bleak import BleakClient, BleakScanner

ESP_MAC = '3C:61:05:65:9D:BA'


# Used to convert a 16-bit UUID to 128-bit UUID
def convert_to_128bit_uuid(short_uuid):
    base_uuid = "00000000-0000-1000-8000-00805F9B34FB"
    short_uuid_hex = "{:04X}".format(short_uuid)
    return base_uuid[:4] + short_uuid_hex + base_uuid[8:]


CHARACTERISTIC_UUID = convert_to_128bit_uuid(0xFF01)


# Notification callback function
async def handle_notification(client, sender, value):
    print("recibiendo datos..")
    print("Data: {}".format(value.hex()))
    print("Handle: {}".format(sender))

    try:
        ascii_message = value.decode('ascii')
        print('Notificación recibida (ASCII):', ascii_message)
        if value == b'CONFIG':
            packet = config_packet_example()
            # Write to the characteristic when 'CONFIG' is received
            await client.write_gatt_char(CHARACTERISTIC_UUID, packet)
    except UnicodeDecodeError:
        pass


# Define the data structure
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
        status=1,
        id_protocol=2,
        bmi270_sampling=100,
        bmi270_acc_sensibility=4,
        bmi270_gyro_sensibility=250,
        bme688_sampling=2,
        discontinuous_time=60,
        port_tcp=1234,
        port_udp=5678,
        host_ip_addr="192.168.1.1",
        ssid="tu_ssid",
        password="tu_passwor"
    )
    print("Paquete de configuración creado: ", config_packet.hex())
    print("Size: ", sys.getsizeof(config_packet))
    return config_packet


async def connect_and_subscribe():
    device = await BleakScanner.find_device_by_address(ESP_MAC, timeout=5.0)
    if device is None:
        print("No se pudo encontrar el dispositivo")
        return

    async with BleakClient(device) as client:
        try:
            print("Conectado al dispositivo")
            await client.start_notify(CHARACTERISTIC_UUID, lambda sender, value: asyncio.create_task(handle_notification(client, sender, value)))
            print("Suscrito a las notificaciones")

            while True:
                await asyncio.sleep(1) # Revisar

        except Exception as e:
            print(f"Ocurrió un error: {e}")

        finally:
            await client.stop_notify(CHARACTERISTIC_UUID)
            print("Notificaciones detenidas")


if __name__ == "__main__":
    while True:
        try:
            asyncio.run(connect_and_subscribe())
        except KeyboardInterrupt:
            print("Programa interrumpido por el usuario.")
            break
