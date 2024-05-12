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


#include "freertos/task.h"
#include "esp_netif.h"
#include "esp_transport.h"

typedef struct {
    uint8_t transport_layer;
    uint8_t id_protocol; 
} InitialConfig;

typedef struct {
    uint16_t id;
    uint8_t transport_layer;
    uint8_t id_protocol;
    uint16_t length;
} Client;
//Credenciales de WiFi
#define WIFI_SSID "VTR-4871545"   //"VTR-4871545" wifipancho" 
#define WIFI_PASSWORD "ky3shTsxSthp"   //"ky3shTsxSthp" "pituca4061" 
#define SERVER_IP     "192.168.0.4" // IP del servidor "192.168.0.4" "192.168.43.20"
#define SERVER_PORT   1234


// Variables de WiFi
#define WIFI_CONNECTED_BIT BIT0
#define WIFI_FAIL_BIT BIT1
static const char* TAG = "WIFI";
static int s_retry_num = 0;
static EventGroupHandle_t s_wifi_event_group;

//CODIGO WIFI
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
//-------------------------------------------------TERMINA CODIGO WIFI------------------------------------------------------
/* 
char * pack(Header h, Body b) {
    char * packet = malloc(sizeof(Header) + sizeof(Header));
    memcpy(packet, &h, sizeof(Header));
    memcpy(packet + sizeof(Header), &b,sizeof(Body))
    return packet;
}
*/

void header_message( Client * self, uint8_t* buffer, int body_lenght){
    //por mientras no estamos mandando MAC  
    // el tamaño riginal de size debiese ser size = 12 + body_lenght 
    int size = 6 + body_lenght;
    memcpy(buffer,&(self->id),2);
    memcpy(buffer+2, &(self->transport_layer),1);
    memcpy(buffer+3,&(self->id_protocol),1);
    memcpy(buffer+4,&(size),2);
    
}

uint8_t* create_message(Client * self){
    if (self == NULL) {
        return NULL; // Si self es NULL, no podemos proceder
    }
    uint8_t* message; 
    int id_protocol = self->id_protocol;
    int body_size = 0;
    switch (id_protocol)
    {
    case 0:
        body_size = 1;
        break;
    case 1:
        body_size = 5;
        break;
    case 2:
        body_size = 15;
        break;
    case 3:
        body_size = 15 + 7*4;
        break;
    case 4:
        body_size = 15 + 12000*sizeof(float);
        break;   
    default:
        break;
    }
    message = (uint8_t*) malloc(12 + body_size * sizeof(uint8_t));
    if (message == NULL) {
            return NULL; // Si malloc falló, devolvemos NULL
        }
    header_message(self, message,body_size);

    char batt = 2;
    memcpy(message + 6 , &batt,1);

    return message; 
}

InitialConfig unpack_initial_conf(char *packet) {
    InitialConfig config;

    memcpy(&(config.transport_layer), packet, 1);
    memcpy(&(config.id_protocol), packet + 1, 1);

    printf("Transport Layer: %d\n", config.transport_layer);
    printf("ID Protocol: %d\n", config.id_protocol);
    return config;
}

void initial_socket_tcp(Client* c){
    //  estructura para alamcenar la direccion ip y el puerto del servidor al que se quiere conectar. 
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
    send(sock, "GET_INITIAL_CONFIG", strlen("GET_INITIAL_CONFIG"), 0);
    // Recibir respuesta
    char rx_buffer[128];
    int rx_len = recv(sock, rx_buffer, sizeof(rx_buffer) - 1, 0);
    if (rx_len < 0) {
        ESP_LOGE(TAG, "Error al recibir datos");
        return;
    }
    ESP_LOGI(TAG, "Datos recibidos: %s", rx_buffer);

    InitialConfig config = unpack_initial_conf(rx_buffer);
    c->id = 0; //partimos con un id igual a 0 , la idea es que a medida que se vayan mandandando paquetes este valor tiene que ir cambiando, esto se tiene que setear en header_message. 
    c->transport_layer = config.transport_layer;
    c->id_protocol = config.id_protocol;

    // Cerrar el socket
    close(sock);
}


void socket_tcp(uint8_t* message, int message_length){
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
    //ahora enviamos el primer mensaje 
    char *request = "GET_INITIAL_CONFIG";
    send(sock, request, strlen(request), 0);

    //send(sock, message, message_length, 0);

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
    // lógica para conectarse a red wifi
    nvs_init();
    wifi_init_sta(WIFI_SSID, WIFI_PASSWORD);
    ESP_LOGI(TAG,"Conectado a WiFi!\n");
   
    Client client_instance;

    uint8_t* message = create_message(&client_instance);

    /*  
    if (message != NULL) {
        // Enviar mensaje
        
        socket_tcp(message, 6 + 1); // El mensaje tiene 12 bytes de cabecera y 1 byte de datos (batt)
        free(message); // Liberar la memoria asignada para el mensaje
    } else {
        ESP_LOGE(TAG, "Error al crear el mensaje");
    }*/
    initial_socket_tcp(&client_instance);


}

