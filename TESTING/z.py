import requests

# URL for the request
url = "https://hwachong.padlet.org/chungal2/2a3-artistic-showcase-gthnvmnzp4nngp4"

# Headers for the GET request
headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "accept-language": "en-GB,en;q=0.8",
    "cache-control": "max-age=0",
    "priority": "u=0, i",
    "sec-ch-ua": "\"Chromium\";v=\"124\", \"Brave\";v=\"124\", \"Not-A.Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-gpc": "1",
    "upgrade-insecure-requests": "1"
}

# Sending the GET request
response = requests.get(url, headers=headers)

# Output the response text
print(response.text)
