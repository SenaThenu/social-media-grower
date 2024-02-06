from selenium import webdriver

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.keys import Keys # provides keyboard elements
from selenium.webdriver.common.by import By # locates elements within a web page

import time
import os

def login(driver):      
    username_field = driver.find_element(By.XPATH, "//*[@id='loginForm']/div/div[1]/div/label/input")
    username_field.clear()
    username_field.send_keys(os.getenv("INSTAGRAM_USERNAME"))

    password_field = driver.find_element(By.XPATH, "//*[@id='loginForm']/div/div[2]/div/label/input")
    password_field.clear()
    password_field.send_keys(os.getenv("INSTAGRAM_PASSWORD"))

    login_button = driver.find_element(By.XPATH, "//*[@id='loginForm']/div/div[3]/button")
    login_button.click()

    save_login_info_button = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div/div/section/div/button")
    save_login_info_button.click()

    turn_off_notifications_button = driver.find_element(By.XPATH, "/html/body/div[3]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]")
    turn_off_notifications_button.click()

def instagram_bot(config):
    last_action_time = time.time()

    print("Triggering the browser window!")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=Options())

    driver.implicitly_wait(30) # 30 second waiting

    # going to instagram.com
    driver.get("https://instagram.com")

    login(driver)

    time.sleep(100)

    driver.close() # quits the browser!