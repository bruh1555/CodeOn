import requests
def check():
  'Checks if you have an internet connection'
  try:
    requests.get("www.google.com")
    tempstatus = "True"
  except:
    tempstatus = "False"
  if tempstatus == "True":
    return "True"
  else:
    return "False"
