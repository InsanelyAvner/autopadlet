from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime

"""
PADLET LIKES BOT

How to use:
- Go to your padlet post
- Right click > copy link to post
- Put link inside link.txt
- Run this python file
"""

driver = webdriver.Chrome()

with open("link.txt", "r") as f:
    link = f.readline()
    print(link)

count = 0
print("--- PADLET SPAMMER LOG ---")
while 1:
    driver.get(link)

    wait = WebDriverWait(driver, 300) 

    like_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="surface-container"]/div[3]/div[2]/div/div[2]/div[2]/div[3]/button')))
    like_button.click()

    like_count = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="surface-container"]/div[3]/div[2]/div/div[2]/div[2]/div[3]/button/span[1]')))
    
    driver.delete_all_cookies()
    count += 1

    print(f"{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} Total Added: {count} Total Likes: {like_count.text}")
    time.sleep(1)