from selenium import webdriver

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.keys import Keys  # provides keyboard elements
from selenium.webdriver.common.by import By  # locates elements within a web page

import time
import os
import yaml
import datetime

from .hashtag_based import like_follow_by_hashtag


class InstagramBot:
    def __init__(self, config):
        self.config = config
        self.last_action_time = time.time()

        print("Initialising the Driver!")
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=Options()
        )
        self.driver.implicitly_wait(6)  # 6-second waiting till elements appear

        print("Going to instagram.com")
        self.driver.get("https://instagram.com")

        print("Logging in!")
        self._login()

        # loading today's actions
        self._today_actions = self._load_today_actions()

    def like_and_follow_by_hashtag(self):
        like_follow_by_hashtag(self)

    def _login(self):
        username_field = self.driver.find_element(
            By.XPATH, "//*[@id='loginForm']/div/div[1]/div/label/input"
        )
        username_field.clear()
        username_field.send_keys(os.getenv("INSTAGRAM_USERNAME"))

        password_field = self.driver.find_element(
            By.XPATH, "//*[@id='loginForm']/div/div[2]/div/label/input"
        )
        password_field.clear()
        password_field.send_keys(os.getenv("INSTAGRAM_PASSWORD"))

        login_button = self.driver.find_element(
            By.XPATH, "//*[@id='loginForm']/div/div[3]/button"
        )
        login_button.click()

        save_login_info_button = self.driver.find_element(
            By.XPATH,
            "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div/div/section/div/button",
        )
        save_login_info_button.click()

    def _load_today_actions(self) -> dict:
        """
        Reads _today_actions.yaml. Updates the date to today if it's not the case.

        Returns:
            dict: actions done today
        """
        # using the absolute path since this is being called from main.py
        with open(os.path.join("bots/instagram", "_today_actions.yaml"), "r") as f:
            actions = yaml.safe_load(f)
            f.close()

        today = datetime.datetime.now().strftime("%d-%m-%Y")
        if actions["date"] != today:
            actions = {"date": today, "n_likes": 0, "n_follows": 0, "n_comments": 0}

            with open(os.path.join("bots/instagram", "_today_actions.yaml"), "w") as f:
                yaml.dump(actions, f)
                f.close()

        return actions

    def _update_today_actions(self, today_actions):
        self._today_actions = today_actions
        with open(os.path.join("bots/instagram", "_today_actions.yaml"), "w") as f:
            yaml.dump(self._today_actions, f)
            f.close()

    def quit(self):
        """
        Quits the browser
        """
        self.driver.close()
