import requests
import json
import datetime
import time
import csv

fieldnames = [
    'humidity',
    'timeout',
    'temp',
    'co2',
    'time',
]

sensors_temp = []
sensors_humidity = []
sensors_co2 = []
sensors_timeout = []
SENSORS_TYPES = [
    'temp',
    'humidity',
    'co2',
    'timeout'
]
sensors_readings = {
    sensor_name: [] for sensor_name in SENSORS_TYPES
}
PARAMETER_NAMES = [
    'av',
    'av',
    'av',
    'ipv'
]

SENSORS_NUMBER = 8


SENSORS_NAMES = [
    '_temperature',
    '_humidity',
    '_co2',
    '_timeout'
]


def read_sensors(sensor_type: str, sensor_name: str, parameter_name) -> dict:
    assert sensor_type in SENSORS_TYPES
    assert sensor_name in SENSORS_NAMES
    assert parameter_name in PARAMETER_NAMES
    i = 1
    for points in api_call_json['points']:
        value = 'wbu1_sensor' + str(i) + sensor_name
        if points['iess'] == value:
            sensors_readings[sensor_type].append(points[parameter_name])
            i += 1

    info = [
        float(sensors_readings[sensor_type][counter+i-1]) for i in range(1, SENSORS_NUMBER + 1)
    ]
    return info


def time_counter():
    return datetime.datetime.now().strftime("%H:%M:%S")

# with open('new_data.csv', 'w') as csv_file:
#     csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
#     csv_writer.writeheader()


counter = 0
while True:

    with open('new_data.csv', 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        api_call_response = requests.get('http://188.168.0.173:5000/get_points/')
        api_call_json = json.loads(api_call_response.text)
        whole_info = {
            sensor_type: read_sensors(sensor_type, sensor_name, parameter_name) for sensor_type, sensor_name, parameter_name in zip(SENSORS_TYPES, SENSORS_NAMES, PARAMETER_NAMES)
        }
        whole_info['time'] = time_counter()
        csv_writer.writerow(whole_info)
        print(whole_info)
        counter += 8
        time.sleep(1)
