import requests

file_path = input("Enter the file path: ")

url = 'http://127.0.0.1:8000/process_file' 

response = requests.post(url, json={'file_path': file_path})

if response.status_code == 200:
    print(response.json()["message"])
else:
    print("Error processing file.")
