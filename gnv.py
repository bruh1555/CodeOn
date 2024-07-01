import sys
import requests
import checkinternet
def gnv():
    returncheck = checkinternet.check()
    if returncheck == "False":
        print("Error: You are not connected to the internet. CodeOn requires an internet connection. Please try again later when you have one.")
        sys.exit()
    else:
        response = requests.get("https://raw.githubusercontent.com/bruh1555/CodeOn/main/latest_version.txt")

        if response.status_code == 200:
            content = response.text
            return content
        else:
            return f'Error: {response.status_code}'
