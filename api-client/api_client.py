import requests

response = requests.get('http://anayasa-scraper-container:5000/get-data')
data = response.json()

print(data)
