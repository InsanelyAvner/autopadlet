from datetime import datetime
import random
import json
import concurrent.futures

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver

# Config checking
with open("config.json") as f:
    config = json.load(f)

if not "link" in config or not "mode" in config:
    raise Exception("Invalid config file")

if "threads" in config:
    if type(config["threads"]) != int:
        raise Exception("Invalid config file")
    THREADS = config["threads"]
else:
    THREADS = 2

TARGET_URL = config["link"]
MODE = config["mode"]

comments = [
    "Great job!",
    "Well done!",
    "Fantastic work!",
    "Impressive effort!",
    "Keep it up!",
    "Brilliant!",
    "You nailed it!",
    "That's exactly right!",
    "Outstanding performance!",
    "You're doing a great job!",
    "That was first-class work!",
    "You've got this!",
    "Amazing progress!",
    "Superb!",
    "You exceeded expectations!"
]

chrome_options = Options()
chrome_options.add_argument("--log-level=3")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")

print("--- AUTOPADLET LOG ---")

def slave(n):
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()

    count = 0 # for tracking added likes
    while 1:
        driver.get(TARGET_URL)

        wait = WebDriverWait(driver, 10)

        if MODE.lower() == "like":
            like_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="surface-container"]/div[4]/div[2]/div/div[2]/div/div[3]/button')))
            like_button.click() 
        else:
            comment_box = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="surface-container"]/div[4]/div[2]/div/div[2]/div/div[4]/div[2]/div/div/div/div/div/p')))
            comment_box.send_keys(random.choice(comments))
            
            comment_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="surface-container"]/div[4]/div[2]/div/div[2]/div/div[4]/div[2]/div/button')))
            comment_button.click()

        count += 1
        
        print(f"[INSTANCE {n}] {datetime.now().strftime("%d/%m/%Y %H:%M:%S")} Total Likes Added: {count}") 

        driver.delete_all_cookies() # reset


with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = [executor.submit(slave, i + 1) for i in range(THREADS)]
    for future in concurrent.futures.as_completed(futures):
        result = future.result()  