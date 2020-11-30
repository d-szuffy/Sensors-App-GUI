import requests
import json

api_call_response = requests.get('http://188.168.0.173:5000/get_points/')
api_call_json = json.loads(api_call_response.text)
# responses = json.dumps(api_call_json, indent=4)
# print(api_call_json['points'][0]['iess'])
i = 1

temperature = 'wbu1_sensor' + str(i) + "_temperature"

for points in api_call_json['points']:
    temperature = 'wbu1_sensor' + str(i) + "_temperature"
    if points['iess'] == temperature:
        print(points['iess'], points['av'])
        i += 1
