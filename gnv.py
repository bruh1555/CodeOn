def gnv():
    import requests
    response = requests.get("https://raw.githubusercontent.com/bruh1555/CodeOn/main/latest_version.txt")

    if response.status_code == 200:
        content = response.text
        return content
    else:
        return f'Error: {response.status_code}'