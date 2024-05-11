
import struct # Libreria muy util para codificar y decodificar datos


"""

--- Packing en C ---



char * pack(int packet_id, float value_float, char * text) {
    char * packet = malloc(12 + strlen(text));
    memcpy(packet, &packet_id, 4);
    memcpy(packet + 4, &value_float, 4);
    memcpy(packet + 8, &largo_text, 4);
    memcpy(packet + 12, text, largo_text);
    return packet;
}

//Luego mandan el paquete por el socket


--- Unpacking en C ---


void unpack(char * packet) {
    int packet_id;
    float value_float;
    int largo_text;
    char * text;

    memcpy(&packet_id, packet, 4);
    memcpy(&value_float, packet + 4, 4);
    memcpy(&largo_text, packet + 8, 4);

    text = malloc(largo_text + 1); // +1 for the null-terminator
    if (text == NULL) {
        // Handle memory allocation failure
        return;
    }
    
    memcpy(text, packet + 12, largo_text);
    text[largo_text] = '\0'; // Null-terminate the string

    printf("Packet ID: %d\n", packet_id);
    printf("Float Value: %f\n", value_float);
    printf("Text: %s\n", text);

    free(text); 
}


"""

def pack(packet_id: int, value_float: float, text: str) -> bytes:
    largo_text = len(text)
    """
     '<' significa que se codifica en little-endian
     'i' significa que el primer dato es un entero de 4 bytes
     'f' significa que el segundo dato es un float de 4 bytes
     'i' significa que el tercer dato es un entero de 4 bytes
     '{}s'.format(largo_text) (ej: 10s para un string de largo 10) significa que el string tiene largo variable,

            Documentacion de struct: https://docs.python.org/3/library/struct.html

    """
    return struct.pack('<ifi{}s'.format(largo_text), packet_id, value_float, largo_text, text.encode('utf-8'))

def pack_conf(id_protocol, transport_layer):
    return struct.pack('<i3s', id_protocol, transport_layer.encode('utf-8'))

def unpack(packet: bytes) -> list:
    packet_id,value_float,largo_text = struct.unpack('<ifi', packet[:12])
    text = struct.unpack('<{}s'.format(largo_text), packet[12:])[0].decode('utf-8')
    return [packet_id, value_float, text]

# def unpack_body():
#     data = unpack()
#     datos_data = {
#         'id_device': ,
#         'mac': ,
#         'timestamp': ,
#         'batt_level': ,
#         'temp': ,
#         'press': ,
#         'hum': ,
#         'co': ,
#         'rms': ,
#         'amp_x': ,
#         'freq_x': ,
#         'amp_y': ,
#         'freq_y': ,
#         'amp_z': ,
#         'freq_z': ,
#         'acc_x': ,
#         'acc_y': ,
#         'acc_z': ,
#         'rgyr_x': ,
#         'rgyr_y': ,
#         'rgyr_z': ,
#     }

#     logs_data = {
#         'id_device': ,
#         'id_protocol': ,
#         'transport_layer': ,
#         'timestamp': ,
#     }

#     loss_data = {
#         'delay': ,
#         'packet_loss': ,
#     }

#     return datos_data, logs_data, loss_data

if __name__ == "__main__":
    mensage = pack(1, 3.20, "Hola mundo")
    print(mensage)
    print(unpack(mensage))
