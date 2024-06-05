from peewee import (
    PostgresqlDatabase,
    Model,
    IntegerField,
    CharField,
    FloatField,
    TimestampField,
    DateTimeField,
    ForeignKeyField,
)

# Database configuration
db_config = {
    "host": "localhost",
    "port": 5432,
    "user": "postgres",
    "password": "postgres",
    "database": "iot_db",
}

# Initialize the database connection
db = PostgresqlDatabase(**db_config)

# Connect to the database and set the schema search path
db.connect()
db.execute_sql("SET search_path TO ble_db;")
db.close()


# Base model class to use the database connection
class BaseModel(Model):
    class Meta:
        database = db


# Define the models
class Configuration(BaseModel):
    Id_device = IntegerField(primary_key=True)
    Status_conf = IntegerField(null=True)
    Protocol_conf = IntegerField(null=True)
    Acc_sampling = IntegerField(null=True)
    Acc_sensibility = IntegerField(null=True)
    Gyro_sensibility = IntegerField(null=True)
    BME688_sampling = IntegerField(null=True)
    Discontinuos_time = IntegerField(null=True)
    TCP_PORT = IntegerField(null=True)
    UDP_port = IntegerField(null=True)
    Host_ip_addr = IntegerField(null=True)
    Ssid = CharField(max_length=45, null=True)
    Pass = CharField(max_length=45, null=True)


class Log(BaseModel):
    Id_device = IntegerField(primary_key=True)
    Status_report = IntegerField(null=True)
    Protocol_report = IntegerField(null=True)
    Battery_Level = IntegerField(null=True)
    Conf_peripheral = IntegerField(null=True)
    Time_client = DateTimeField(null=True)
    Time_server = TimestampField(default="CURRENT_TIMESTAMP", null=True)
    configuration_Id_device = ForeignKeyField(
        Configuration, backref="logs", on_delete="NO ACTION", on_update="NO ACTION"
    )


class Data_1(BaseModel):
    Id_device = IntegerField(primary_key=True)
    Temperature = IntegerField(null=True)
    Press = IntegerField(null=True)
    Hum = IntegerField(null=True)
    Co = FloatField(null=True)
    RMS = FloatField(null=True)
    Amp_x = FloatField(null=True)
    Freq_x = FloatField(null=True)
    Amp_y = FloatField(null=True)
    Freq_y = FloatField(null=True)
    Amp_z = FloatField(null=True)
    Freq_z = FloatField(null=True)
    Time_client = DateTimeField(null=True)
    Log_Id_device = ForeignKeyField(
        Log, backref="data_1", on_delete="NO ACTION", on_update="NO ACTION"
    )


class Data_2(BaseModel):
    Id_device = IntegerField(primary_key=True)
    Racc_x = FloatField(null=True)
    Racc_y = FloatField(null=True)
    Racc_z = FloatField(null=True)
    Rgyr_x = FloatField(null=True)
    Rgyr_y = FloatField(null=True)
    Rgyr_z = FloatField(null=True)
    Time_client = DateTimeField(null=True)
    Log_Id_device = ForeignKeyField(
        Log, backref="data_2", on_delete="NO ACTION", on_update="NO ACTION"
    )


def add_data_1_to_db(datos_data: list, log_data: list):
    try:
        with db.atomic():
            # Log
            id_device = log_data[0]
            status_report = log_data[1]
            protocol_report = log_data[2]
            battery_level = log_data[3]
            conf_peripheral = log_data[4]
            time_client = log_data[5]
            time_server = log_data[6]
            configuration_id_device = log_data[7]

            # Data_1
            battery_Level = datos_data[0]
            timestamp = datos_data[1]
            temperature = datos_data[2]
            press = datos_data[3]
            hum = datos_data[4]
            co = datos_data[5]
            rms = datos_data[6]
            amp_x = datos_data[7]
            freq_x = datos_data[8]
            amp_y = datos_data[9]
            freq_y = datos_data[10]
            amp_z = datos_data[11]
            freq_z = datos_data[12]

            log = Log.create(
                id_device,
                status_report,
                protocol_report,
                battery_level,
                conf_peripheral,
                time_client,
                time_server,
                configuration_id_device,
            )

            datos = Data_1.create(
                id_device,
                battery_Level,
                timestamp,
                temperature,
                press,
                hum,
                co,
                rms,
                amp_x,
                freq_x,
                amp_y,
                freq_y,
                amp_z,
                freq_z,
                time_client,
                log.Id_device,
            )
            Log.create()
    except Exception as error:
        print("Error al agregar datos a la base de datos:", error)


def add_data_2_to_db(datos_data: list, log_data: list):
    try:
        with db.atomic():
            # Log
            id_device = log_data[0]
            status_report = log_data[1]
            protocol_report = log_data[2]
            battery_level = log_data[3]
            conf_peripheral = log_data[4]
            time_client = log_data[5]
            time_server = log_data[6]
            configuration_id_device = log_data[7]

            # Data_2
            battery_Level = datos_data[0]
            timestamp = datos_data[1]
            temperature = datos_data[2]
            press = datos_data[3]
            hum = datos_data[4]
            co = datos_data[5]
            acc_x = datos_data[6]
            acc_y = datos_data[7]
            acc_z = datos_data[8]

            log = Log.create(
                id_device,
                status_report,
                protocol_report,
                battery_level,
                conf_peripheral,
                time_client,
                time_server,
                configuration_id_device,
            )

            datos = Data_2.create(
                id_device,
                battery_Level,
                timestamp,
                temperature,
                press,
                hum,
                co,
                acc_x,
                acc_y,
                acc_z,
                time_client,
                log.Id_device,
            )
            Log.create()
    except Exception as error:
        print("Error al agregar datos a la base de datos:", error)


def get_conf() -> list:
    query = Configuration.select()
    # Must be only one row
    values = []
    for row in query:
        for e in row:
            values.append(e)
    values = values[1::]  # Delete first element (id_device)
    return values


def update_conf(conf_data: list):
    query = Configuration.update(
        Id_device=conf_data[0],
        Status_conf=conf_data[1],
        Protocol_conf=conf_data[2],
        Acc_sampling=conf_data[3],
        Acc_sensibility=conf_data[4],
        Gyro_sensibility=conf_data[5],
        BME688_sampling=conf_data[6],
        Discontinuos_time=conf_data[7],
        TCP_PORT=conf_data[8],
        UDP_port=conf_data[9],
        Host_ip_addr=conf_data[10],
        Ssid=conf_data[11],
        Pass=conf_data[12],
    )


if __name__ == "__main__":
    # Create the tables
    db.create_tables([Configuration, Timestamp, Log, Data_1, Data_2])

    # Example query to test the setup
    config = Configuration.get_or_none(Configuration.Id_device == 1)
    if config:
        print(f"Configuration for device {config.Id_device}: SSID = {config.Ssid}")
7
