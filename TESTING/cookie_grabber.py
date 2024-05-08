from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

import time
import requests

headers = {
    "accept": "application/json, application/vnd.api+json",
    "accept-language": "en-GB,en;q=0.5",
    "authorization": "Bearer 6725a620b23de92924fd0f7cf2e6eb9ce5df18bda89ffa194f02104a0a88ba0f",
    "content-type": "application/json; charset=utf-8",
    "priority": "u=1, i",
    "sec-ch-ua": '"Chromium";v="124", "Brave";v="124", "Not-A.Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "same-origin",
    "sec-fetch-site": "same-origin",
    "sec-gpc": "1",
    "x-csrf-token": "KSrhLzJ9Kw+UMJTr86O7JXmfV/mutXeY4zmuD2OwU63MzwbflWV+a+aHg2GOvNiFMjD0oRyi5hof0qYRFBcwiQ==",
    "x-uid": "1715132822183031857683632590983",
    "cookie": "ww_d=ef36b5e49e547505b2889163aecfb3ba; ww_f=beta%3Dfalse; ww_dpr=1; ww_l=en; ww_s=b1766121d39b835026f4053014e99091; __cf_bm=UWNIgo7C0XT.YgtcR7RHTK.QmmfQhY4YI6QYLDECSsU-1715132463-1.0.1.1-fQaJ7.2WXaI600xjcOdZgSaRzZJCbsgyDjG29uuxjXWuXlffaxtTI1Bqj5w6nHhnH5H3I5ZMSrK678luGxo_5g; ww_tz=Asia/Singapore; ww_p=SDdld1RmcUxqYUJPRUxSLzdOdERueTZUc0NTYkNqT05TYjVkUFZXVzhMcWFaUGd3R3BYUGp6OXYraEt3N3pVNzkwTS9Bb205Vlc2WHVFZEgvYzFYTUNpWkkvQWxUQytJWmg3UnAzUmZNYnpxNUJxYWRTTU8yQWRnMEJ3eWN5cUorZUp6QzN0ekVPY0NUTXdZWEVxTkZBK09WU0tKNlZKSWx6VmhmbTQ3RGlrWTRKcFJiSFZSck5FUkZnZU5PS0svc0ZTd0hHNkhiOXlmS2E1MXIvVXBxdUluZkxUWVR6QWZvU0R4dGdpTUNvTGtmNmlXd3BYN0hxMFUxY3VyMko5SzI1RlE2RU1leHpzM25HL1VGWEROY3V5WGNjNlBuWmhOSk9Ea0xqa04vU1l0TUJhaFpEL2tpdWFHUXJycmV4RmxXc1ZQT2hwVnJPNkdKK3ZvRzdhMVhvL0d5SjQ1UlpETVo0aWRsM1B1dWhwcnY4bXdvYmg2UDZsUjM3YWFvQkM0MGRzWC9HaExHZUthQ0JZWXQveWdyc0tCVFlaa1NlSUJsSC94QXo4eWp3WGpVVmk0L1BoSStYSDdtc2FpV3pNUjg3T0ZFSUJLNG1ZaUptMVdhWGZ6QnBGbUQ0SmorYnp5ZUlZRnpMc0lxZjlsNE1PamNFeWhrYm1nQW0rcmVIQkNOanUxWDlja3QyVUxhTUNwcWVCbmxBPT0tLThXVmx6bWlxbzhtVnRQT3BHdi9Bd3c9PQ%3D%3D--1ea78e0c5065386d957e085ff66f233de389e09b",
    "Referer": "https://hwachong.padlet.org/chungal2/2a3-artistic-showcase-gthnvmnzp4nngp4",
    "Referrer-Policy": "strict-origin-when-cross-origin"
}

# List of cookie names you want to capture and the order in which they should be saved
desired_cookies = ['ww_d', 'ww_f', 'ww_dpr', 'ww_l', 'ww_s', '__cf_bm', 'ww_tz', 'ww_p']

# Setting up Chrome options for headless mode
options = Options()
options.headless = True
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Setting up the Chrome driver
driver = webdriver.Chrome(options=options)

# URL to navigate to
url = "https://hwachong.padlet.org/chungal2/2a3-artistic-showcase-gthnvmnzp4nngp4"

while 1:
    # Navigate to the page
    driver.get(url)

    # Wait for the necessary cookies to be loaded (Checking continuously)
    start_time = time.time()
    timeout = 10  # seconds
    cookies_captured = False

    while not cookies_captured and time.time() - start_time < timeout:
        cookies = driver.get_cookies()
        cookie_dict = {cookie['name']: cookie['value'] for cookie in cookies}
        # Check if all desired cookies are present
        if all(name in cookie_dict for name in desired_cookies):
            cookies_captured = True
            # Format and save the desired cookies in order
            cookie_header_str = '; '.join(f"{name}={cookie_dict[name]}" for name in desired_cookies if name in cookie_dict)
            with open('cookies.txt', 'a') as f:
                f.write(f"{cookie_header_str}\n")
            print("Cookies saved to cookies.txt")
        time.sleep(0.1)  # Small delay to prevent excessive CPU usage

    # Output result
    if not cookies_captured:
        print("Timeout reached. Not all desired cookies were captured.")
        continue


    # COOKIES WERE CAPTURED, ADD A LIKE
    # api_url = "https://hwachong.padlet.org/api/5/reactions"
    # headers["cookie"] = cookie_header_str

    # data = {
    #     "wish_id": 2959242360,
    #     "value": 1,
    #     "reaction_type": "like"
    # }

    # # Sending POST request
    # response = requests.post(api_url, headers=headers, json=data)

    # # Output the response text
    # print(response.text)

    driver.delete_all_cookies()
