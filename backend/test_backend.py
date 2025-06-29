import requests

# This assumes your FastAPI app is running at localhost:8000
response = requests.post("http://localhost:8000/api/generate", json={
    "url": "https://linkedin.com/in/example"
})

print(response.status_code)
print(response.json())
