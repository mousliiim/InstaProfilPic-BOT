import requests
import json

response = requests.request(
"POST", 
"https://techhk.aoscdn.com/api/tasks/visual/scale", 
headers= {'X-API-KEY': 'YOUR-API-KEY'}, 
data={'sync': '1','type':'clean','image_url' : 'https://www.1min30.com/wp-content/uploads/2017/05/Samsung-logo.jpg'},
)

data = response.text
json_data = json.loads(data)
img_url = json_data['data']['image']
print(img_url)
