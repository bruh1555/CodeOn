import urllib
import sys
import requests
def gnv():
    try:
        requests.get("https://www.google.com")
        tempstatus = "Connected"
    except:
        tempstatus = "Not connected"
    if not tempstatus == "Connected":
        print("Error: You are not connected to the internet. CodeOn requires an internet connection. Please try again later when you have one.")
        return 'Error: No Wifi Connection'
    else:
        tempstatus = None
    response = requests.get("https://raw.githubusercontent.com/bruh1555/CodeOn/main/latest_version.txt")

    if response.status_code == 200:
        content = response.text
        return content
    else:
        return f'Error: {response.status_code}'
