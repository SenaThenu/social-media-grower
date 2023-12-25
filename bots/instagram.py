# web-driver related imports
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# web-interacting related imports
from selenium.webdriver.common.by import By

USERNAME = ""
PASSWORD = ""

# login global variables
USERNAME_XPATH = "//*[@id='loginForm']/div/div[1]/div/label/input"
PASSWORD_XPATH = "//*[@id='loginForm']/div/div[2]/div/label/input"
LOGIN_BUTTON_XPATH = "//*[@id='loginForm']/div/div[3]/button"

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=Options())

# going to a specific site
driver.get("https://www.instagram.com/")

driver.implicitly_wait(5)

# fetching the login form elements
username_field = driver.find_element(By.XPATH, USERNAME_XPATH)
password_field = driver.find_element(By.XPATH, PASSWORD_XPATH)
submit_button = driver.find_element(By.XPATH, LOGIN_BUTTON_XPATH)

# filling the form
username_field.send_keys(USERNAME)
password_field.send_keys(PASSWORD)

submit_button.click()

# driver.quit()