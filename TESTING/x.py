import requests

# URL for the request
url = "https://hwachong.padlet.org/api/5/reactions"

# Headers
headers = {
    "accept": "application/json, application/vnd.api+json",
    "accept-language": "en-GB,en;q=0.5",
    "authorization": "Bearer b09faf6adadd3a4901f9e169b434ce1071da72cd947afa72f0c6f93031f62c65",
    "content-type": "application/json; charset=utf-8",
    "priority": "u=1, i",
    "sec-ch-ua": '"Chromium";v="124", "Brave";v="124", "Not-A.Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "same-origin",
    "sec-fetch-site": "same-origin",
    "sec-gpc": "1",
    "x-csrf-token": "lKA1A8peWqjp2Jq7/u5SHvLnsuLzY5tOwkR1PDyGU8MfjsmjkfsmiNUoFLYtnS4iR1Q/Li0C+Uu1GsyKBZKahQ==",
    "x-uid": "171513527500503606771700458269",
    "cookie": "ww_d=d12213a7ae99063385c4d90888785c2d; ww_s=c37a45ec7d66f201ee6716c222a6a830; ww_f=beta%3Dfalse; __cf_bm=MLeJMMO4qcNrSxCmVXe4VE79tmj2qcoEfmlsmZJlvG0-1715135274-1.0.1.1-tj0X64f210xHN2rKi.s3O5iYRgUh1uMglNRPc5xg3uKH0njY4o2cOwEuIfO2pW4g3PvASj7Dk8Nd9SpY0HVe_Q; ww_dpr=1; ww_tz=Asia/Singapore; ww_l=en-GB; ww_p=TjBOODJ4cHg3MmMyenpadmtnblB0QVVSdGsveGNLVzYyVDl6NFlGclhDY0s5Y1lYcllJNlZaUU9uSHRvczZXaWZUbVVkRW9kSzB1SE13MWptRmZEQ0pwcW9KVUczM1BUWXF0UUxHaG9EbXhIRlVUNjBZQTVaMkcxZUV3S1FHWFo5dXMwT0IwMGpQRUhCdHUrblljc3lEdUJkSHFxTG1IamRacmdWVVlDM0duSm1oeFFWeGNaOEhwUjJIekZ0aUZqOERiTEJUeFNZZHVsZGp3UEhITmpIc0dsdUM1cW1ZN3QvcU10Z2R5VHg4aWxwb3VXUXI2c1I2OGFNRzJGVG9vZENuU3NpaWI0KzZqRS84eWN0cDJ0VlJ3RG9EV0NqbnVlN0JFRDB5NzZib2FjMmRVcyt5RDBmOHFMY0lLQWZYaFhXMWx5MVdJNUdDOXRCS09xTjZDeUl3SmF5dW9QTWhnOUdjQ0dNczBBRk5JeWNkWU12NmkyNU16TEVQRGllcFpULS0zU1hJdndWSW13VHFBSFJVQnlEY0pnPT0%3D--605bf79d14afaee8835eeda80a15d16eddceb15c",
    "Referer": "https://hwachong.padlet.org/chungal2/2a3-artistic-showcase-gthnvmnzp4nngp4",
    "Referrer-Policy": "strict-origin-when-cross-origin"
}

# Body of the POST request
data = {
    "wish_id": 2959242360,
    "value": 1,
    "reaction_type": "like"
}

# Sending POST request
response = requests.post(url, headers=headers, json=data)

# Output the response text
print(response.text)
