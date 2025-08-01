import requests
res = requests.post("http://127.0.0.1:8000/predict", json={"text": "This is an example sentence."})
print(res.json())