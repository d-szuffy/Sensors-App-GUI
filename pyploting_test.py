import requests
import json
api_call_response = requests.get('http://188.168.0.173:5000/get_points/')
api_call_json = json.loads(api_call_response.text)
print(json.dumps(api_call_json, indent=4))
