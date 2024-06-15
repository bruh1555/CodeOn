import requests

def check():
    'Checks if you have an internet connection'
    try:
        response = requests.get("https://www.google.com", timeout=5)
        if response.status_code == 200:
            return "True"
        else:
            return "False"
    except requests.exceptions.RequestException:
        return "False"
