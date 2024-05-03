from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from datetime import datetime

import random
import json
import time

with open('link.txt', 'r') as f:
    url = f.readline()
    
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
# chrome_options.add_argument('--headless')
chrome_options.add_argument("--log-level=3")

driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()

while True:
    try:
        driver.get(url)

        wait = WebDriverWait(driver, 3)
        
        comment_box = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="surface-container"]/div[4]/div[2]/div/div[2]/div/div[4]/div[2]/div/div/div/div/div/p')))
        random_comment = random.choice(comments)
        comment_box.send_keys(random_comment)
        
        comment_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="surface-container"]/div[4]/div[2]/div/div[2]/div/div[4]/div[2]/div/button')))
        comment_button.click()

        driver.delete_all_cookies()
        print(f"{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} Comment: '{random_comment}'")
    except: pass