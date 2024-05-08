import time
from datetime import datetime
import random

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver

#################################################
MODE = "like" # "comment" or "like"
#################################################

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

with open("link.txt", "r") as f:
    link = f.readline()
    print(link)

chrome_options = Options()
chrome_options.add_argument("--log-level=3")

driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()


count = 0 # for tracking added likes

print("--- AUTOPADLET LOG ---")
while 1:
    driver.get(link)

    wait = WebDriverWait(driver, 300)

    if MODE == "like":
        like_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="surface-container"]/div[4]/div[2]/div/div[2]/div/div[3]/button')))
        like_button.click()
        
        count += 1
        print(f"{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} Total Likes Added: {count}") 
    
    else:
        comment_box = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="surface-container"]/div[4]/div[2]/div/div[2]/div/div[4]/div[2]/div/div/div/div/div/p')))
        comment_box.send_keys(random.choice(comments))
        
        comment_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="surface-container"]/div[4]/div[2]/div/div[2]/div/div[4]/div[2]/div/button')))
        comment_button.click()

        count += 1
        print(f"{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} Total Comments Added: {count}") 

    
    driver.delete_all_cookies()