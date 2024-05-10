#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

#include <stdio.h>
#include <string.h>


#include "esp_event.h"
#include "esp_log.h"
#include "esp_system.h"
#include "esp_wifi.h"
#include "freertos/FreeRTOS.h"
#include "freertos/event_groups.h"
#include "lwip/err.h"
#include "lwip/sys.h"
#include "nvs_flash.h"
#include "lwip/sockets.h" // Para sockets

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////7
// Funciones para generar datos
// Acceloremeter_kpi
// Función para generar un número aleatorio en un rango dado
float randomInRange(float min, float max) {
    return min + ((float)rand() / RAND_MAX) * (max - min);
}
// Función para generar Ampx
float generateAmpx() {
    return randomInRange(0.0059, 0.12);
}
// Función para generar Freqx
float generateFreqx() {
    return randomInRange(29.0, 31.0);
}
// Función para generar Ampy
float generateAmpy() {
    return randomInRange(0.0041, 0.11);
}
// Función para generar Freqy
float generateFreqy() {
    return randomInRange(59.0, 61.0);
}
// Función para generar Ampz
float generateAmpz() {
    return randomInRange(0.008, 0.15);
}
// Función para generar Freqz
float generateFreqz() {
    return randomInRange(89.0, 91.0);
}
// Función para generar el RMS
float generateRMS(float Ampx, float Ampy, float Ampz) {
    return sqrtf(powf(Ampx, 2) + powf(Ampy, 2) + powf(Ampz, 2));
}
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Funciones para generar HEADERS
// Función para generar un ID único del mensaje (2 bytes)
uint16_t generateMessageID() {
    return (uint16_t)rand(); // Genera un ID aleatorio de 2 bytes
}
// Función para generar una dirección MAC aleatoria (6 bytes)
void generateMACAddress(uint8_t *mac_address) {
    for (int i = 0; i < 6; i++) {
        mac_address[i] = rand() % 256; // Genera un byte aleatorio
    }
}
////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Función para empaquetar los datos del encabezado y el cuerpo en un paquete
//Credenciales de WiFi

#define WIFI_SSID "Negras"
#define WIFI_PASSWORD "adaclaraflora"
#define SERVER_IP     "192.168.1.91" // IP del servidor
#define SERVER_PORT   1234
#define PACKET_SIZE 14 // Tamaño del paquete a enviar al servidor

char *pack(int ID_protocol, int Transport_Layer, uint16_t message_id, uint16_t Length) {
    char *packet = malloc(PACKET_SIZE);
    if (packet == NULL) {
        fprintf(stderr, "Error: No se pudo asignar memoria para el paquete\n");
        return NULL;
    }

    // Empaquetar los datos en el paquete
    memcpy(packet, &ID_protocol, sizeof(ID_protocol));
    memcpy(packet + sizeof(ID_protocol), &Transport_Layer, sizeof(Transport_Layer));
    memcpy(packet + sizeof(ID_protocol) + sizeof(Transport_Layer), &message_id, sizeof(message_id));
    memcpy(packet + sizeof(ID_protocol) + sizeof(Transport_Layer) + sizeof(message_id), &Length, sizeof(Length));

    return packet;
}




// Variables de WiFi
#define WIFI_CONNECTED_BIT BIT0
#define WIFI_FAIL_BIT BIT1
static const char* TAG = "WIFI";
static int s_retry_num = 0;
static EventGroupHandle_t s_wifi_event_group;


void event_handler(void* arg, esp_event_base_t event_base,
                          int32_t event_id, void* event_data) {
    if (event_base == WIFI_EVENT && event_id == WIFI_EVENT_STA_START) {
        esp_wifi_connect();
    } else if (event_base == WIFI_EVENT &&
               event_id == WIFI_EVENT_STA_DISCONNECTED) {
        if (s_retry_num < 10) {
            esp_wifi_connect();
            s_retry_num++;
            ESP_LOGI(TAG, "retry to connect to the AP");
        } else {
            xEventGroupSetBits(s_wifi_event_group, WIFI_FAIL_BIT);
        }
        ESP_LOGI(TAG, "connect to the AP fail");
    } else if (event_base == IP_EVENT && event_id == IP_EVENT_STA_GOT_IP) {
        ip_event_got_ip_t* event = (ip_event_got_ip_t*)event_data;
        ESP_LOGI(TAG, "got ip:" IPSTR, IP2STR(&event->ip_info.ip));
        s_retry_num = 0;
        xEventGroupSetBits(s_wifi_event_group, WIFI_CONNECTED_BIT);
    }
}

void wifi_init_sta(char* ssid, char* password) {
    s_wifi_event_group = xEventGroupCreate();

    ESP_ERROR_CHECK(esp_netif_init());

    ESP_ERROR_CHECK(esp_event_loop_create_default());
    esp_netif_create_default_wifi_sta();

    wifi_init_config_t cfg = WIFI_INIT_CONFIG_DEFAULT();
    ESP_ERROR_CHECK(esp_wifi_init(&cfg));

    esp_event_handler_instance_t instance_any_id;
    esp_event_handler_instance_t instance_got_ip;
    ESP_ERROR_CHECK(esp_event_handler_instance_register(
        WIFI_EVENT, ESP_EVENT_ANY_ID, &event_handler, NULL, &instance_any_id));
    ESP_ERROR_CHECK(esp_event_handler_instance_register(
        IP_EVENT, IP_EVENT_STA_GOT_IP, &event_handler, NULL, &instance_got_ip));

    wifi_config_t wifi_config;
    memset(&wifi_config, 0, sizeof(wifi_config_t));

    // Set the specific fields
    strcpy((char*)wifi_config.sta.ssid, WIFI_SSID);
    strcpy((char*)wifi_config.sta.password, WIFI_PASSWORD);
    wifi_config.sta.threshold.authmode = WIFI_AUTH_WPA2_PSK;
    wifi_config.sta.pmf_cfg.capable = true;
    wifi_config.sta.pmf_cfg.required = false;
    ESP_ERROR_CHECK(esp_wifi_set_mode(WIFI_MODE_STA));
    ESP_ERROR_CHECK(esp_wifi_set_config(WIFI_IF_STA, &wifi_config));
    ESP_ERROR_CHECK(esp_wifi_start());

    ESP_LOGI(TAG, "wifi_init_sta finished.");

    EventBits_t bits = xEventGroupWaitBits(s_wifi_event_group,
                                           WIFI_CONNECTED_BIT | WIFI_FAIL_BIT,
                                           pdFALSE, pdFALSE, portMAX_DELAY);

    if (bits & WIFI_CONNECTED_BIT) {
        ESP_LOGI(TAG, "connected to ap SSID:%s password:%s", ssid,
                 password);
    } else if (bits & WIFI_FAIL_BIT) {
        ESP_LOGI(TAG, "Failed to connect to SSID:%s, password:%s", ssid,
                 password);
    } else {
        ESP_LOGE(TAG, "UNEXPECTED EVENT");
    }

    ESP_ERROR_CHECK(esp_event_handler_instance_unregister(
        IP_EVENT, IP_EVENT_STA_GOT_IP, instance_got_ip));
    ESP_ERROR_CHECK(esp_event_handler_instance_unregister(
        WIFI_EVENT, ESP_EVENT_ANY_ID, instance_any_id));
    vEventGroupDelete(s_wifi_event_group);
}

void nvs_init() {
    esp_err_t ret = nvs_flash_init();
    if (ret == ESP_ERR_NVS_NO_FREE_PAGES ||
        ret == ESP_ERR_NVS_NEW_VERSION_FOUND) {
        ESP_ERROR_CHECK(nvs_flash_erase());
        ret = nvs_flash_init();
    }
    ESP_ERROR_CHECK(ret);
}



void socket_tcp(){
    struct sockaddr_in server_addr;
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(SERVER_PORT);
    inet_pton(AF_INET, SERVER_IP, &server_addr.sin_addr.s_addr);

    // Crear un socket
    int sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (sock < 0) {
        ESP_LOGE(TAG, "Error al crear el socket");
        return;
    }

    // Conectar al servidor
    if (connect(sock, (struct sockaddr *)&server_addr, sizeof(server_addr)) != 0) {
        ESP_LOGE(TAG, "Error al conectar");
        close(sock);
        return;
    }



    // Enviar mensaje "Hola mundo"
    //send(sock, float ampx, sizeof(ampx), 0);
    send(sock, "Hola mundo", strlen("Hola mundo"), 0);

    // Recibir respuesta

    char rx_buffer[128];
    int rx_len = recv(sock, rx_buffer, sizeof(rx_buffer) - 1, 0);
    if (rx_len < 0) {
        ESP_LOGE(TAG, "Error al recibir datos");
        return;
    }
    ESP_LOGI(TAG, "Datos recibidos: %s", rx_buffer);
    
    // Cerrar el socket
    close(sock);
}



void app_main(void){
    nvs_init();
    wifi_init_sta(WIFI_SSID, WIFI_PASSWORD);
    ESP_LOGI(TAG,"Conectado a WiFi!\n");

    //Primera parte
    //Consulta a DB sobre ID_protocol y Transport_Layer
    uint8_t ID_protocol = 3; //1 bytes
    uint8_t Transport_Layer = 1; //1bytes
    //Printeamos en terminal ID_protocol y Transport_Layer
    printf("Consulta DB:\n");
    printf("ID_protocol: %.2d\n", ID_protocol);
    printf("Transport_Layer: %.2d\n", Transport_Layer);
    
    //Headers
    uint16_t ID = generateMessageID(); //2bytes
    uint16_t Length=10; //2bytes
    //Imprime los datos de encabezado
    printf("Header Data:\n");
    printf("Message ID: %u\n", ID);
    //printf("Device MAC: ");
    //for (int i = 0; i < 6; i++) {
    //    printf("%02X ", mac_address[i]);
    //}
    printf("Transport Layer: %u\n", Transport_Layer);
    printf("ID_protocol: %u\n", ID_protocol);
    printf("Length: %u\n", Length);

    printf("Header Data Sizes:\n");
    printf("Message ID: %zu bytes\n", sizeof(ID));
    //printf("Device MAC: %zu bytes\n", sizeof(mac_address));
    printf("Transport Layer: %zu bytes\n", sizeof(Transport_Layer));
    printf("ID_protocol: %zu bytes\n", sizeof(ID_protocol));
    printf("Length: %zu bytes\n", sizeof(Length));

    // Generación datos
    
    float ampx=generateAmpx(); 
    float freqx=generateFreqx();
    float ampy=generateAmpy();
    float freqy=generateFreqy();
    float ampz=generateAmpz();
    float freqz = generateFreqz();
    float rms=generateRMS(ampx,ampy,ampz); 

    // Mostrar el dato generado en la terminal
    printf("Cuerpo:\n");
    printf("AMPX: %.2f\n", ampx);
    printf("FrecX: %.2f\n", freqx);
    printf("AMPY: %.2f\n", ampy);
    printf("FrecY: %.2f\n", freqy);
    printf("AMPZ: %.2f\n", ampz);
    printf("FrecZ: %.2f\n", freqz);
    printf("Rms: %.2f\n", rms);
    
    socket_tcp();
    //socket_tcp();
}