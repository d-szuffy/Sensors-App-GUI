import requests
import json
import datetime, time, csv

i = 0
time_list = []

fieldnames = [
    'time',
    'sensor1_temp',
    'sensor1_humidity',
    'sensor1_co2',
    'sensor2_temp',
    'sensor2_humidity',
    'sensor2_co2',
    'sensor3_temp',
    'sensor3_humidity',
    'sensor3_co2',
    'sensor4_temp',
    'sensor4_humidity',
    'sensor4_co2',
]

sensor1_temp = []
sensor1_humidity = []
sensor1_co2 = []

sensor2_temp = []
sensor2_humidity = []
sensor2_co2 = []

sensor3_temp = []
sensor3_humidity = []
sensor3_co2 = []

sensor4_temp = []
sensor4_humidity = []
sensor4_co2 = []

with open('data.csv', 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()

while True:

    with open('data.csv', 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        current_time = datetime.datetime.now()
        current_hour = str(current_time.hour) + ':' + str(current_time.minute) + ':' + str(current_time.second)

        api_call_response = requests.get('http://188.168.0.173:5000/get_points/wbu1_sensor1_temperature')
        api_call_json = json.loads(api_call_response.text)
        y_value = json.dumps(float(api_call_json['points'][0]['av']), indent=4)

        time.sleep(1)

        info = {
            "x_val": current_hour,
            'y_val': y_value
        }

        csv_writer.writerow(info)
