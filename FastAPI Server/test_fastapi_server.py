import requests
res = requests.post("http://127.0.0.1:8000/predict", json={"text": "I really liked The colour out of Space starting slow, "
"but reeeeaally gave me the shivers in the end."
" I think it was the first time I got scared reading a story."})
print(res.json())