from selenium import webdriver

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By  # locates elements within a web page

from PyQt6 import QtGui
from PyQt6.QtWidgets import QMessageBox

import time
import os
import yaml
import datetime

from .hashtag_based import like_follow_by_hashtag
from .user_related_actions import (
    perform_action_on_n_users,
    unfollow_a_user,
    get_user_url_list,
)

# Logo
LOGO_PATH = "readme_assets/logo.png"  # from the root directory


class InstagramBot:
    def __init__(self, config):
        self.config = config
        self.last_action_time = time.time()

        # loading today's actions
        self._today_actions = self._load_today_actions()

    def _show_error_message(self, title, explanation):
        error_box = QMessageBox()
        error_box.setIcon(QMessageBox.Icon.Warning)
        error_box.setWindowIcon(QtGui.QIcon(LOGO_PATH))

        error_box.setText(title)
        error_box.setInformativeText(explanation)
        error_box.setWindowTitle("Error")
        error_box.exec()

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

    def _get_following_users_container(self) -> object:
        """
        Goes to "https://www.instagram.com/logged_in_username/following"

        Returns:
            object -> The div container which contains the list of users.
        """
        username = self.config["login"]["insta_username"]
        following_link = f"https://www.instagram.com/{username}/following/"

        self.driver.get(following_link)

        time.sleep(self.config["user_preferences"]["base_waiting_time"] * 0.8)

        # there are 2 possibilities
        try:
            following_list = self.driver.find_element(
                By.XPATH,
                "/html/body/div[5]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[4]/div[1]/div",
            )
        except:
            following_list = self.driver.find_element(
                By.XPATH,
                "/html/body/div[7]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[4]/div[1]/div",
            )

        return following_list

    def _get_followers_container(self) -> object:
        """
        Goes to "https://www.instagram.com/logged_in_username/followers"

        Returns:
            object -> The div container which contains the list of users.
        """
        username = self.config["login"]["insta_username"]
        followers_link = f"https://www.instagram.com/{username}/followers/"

        self.driver.get(followers_link)

        time.sleep(self.config["user_preferences"]["base_waiting_time"] * 0.8)

        # there are 2 possibilities
        try:
            followers_list = self.driver.find_element(
                By.XPATH,
                "/html/body/div[5]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div",
            )
        except:
            followers_list = self.driver.find_element(
                By.XPATH,
                "/html/body/div[7]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div",
            )

        return followers_list

    def _perform_dynamic_unfollow(self, n: int):
        """
        Reads the follow history and dynamically unfollows n number of users who don't follow back!
        """

        def _update_follow_history(his):
            with open(os.path.join("bots/instagram", "_follow_history.yaml"), "w") as f:
                yaml.dump(his, f)
                f.close()

        with open("bots/instagram/_follow_history.yaml", "r") as f:
            follow_history = yaml.safe_load(f)
            f.close()

        # sorting the follow history in the ascending order so that we can focus on the first element!
        follow_history = {
            k: v
            for k, v in sorted(
                follow_history.items(),
                key=lambda item: datetime.datetime.strptime(list(item)[0], "%d-%m-%Y"),
            )
        }

        # retrieving the links of users who are currently being followed
        following_list = get_user_url_list(
            self.driver,
            self._get_followers_container(),
            # we pass in the maximum following to ensure we get all the users!
            self.config["restrictions"]["instagram"]["max_following"],
        )

        if len(follow_history) > 0:
            n_done = 0
            while n_done < n:
                # checking if there are users followed under the oldest date
                oldest_date = list(follow_history.keys())[0]

                if len(follow_history[oldest_date]) > 0:
                    user_link = follow_history[oldest_date][0]

                    if user_link not in following_list:
                        was_successful = unfollow_a_user(self.driver, user_link)
                        if was_successful:
                            self._today_actions["n_follows"] += 1
                            self._update_today_actions(self._today_actions)
                            n_done += 1

                    # removing this user_link because there's no further use of it!
                    follow_history[oldest_date].pop(0)
                else:
                    follow_history.pop(oldest_date)

                _update_follow_history(follow_history)

                # we can't keep the _follow_history.yaml empty! So, we're gonna add an easter egg account!
                if len(follow_history) <= 0:
                    easter_egg_follow = {
                        "14-03-2024": ["https://www.instagram.com/senathenu_bot/"]
                    }
                    _update_follow_history(easter_egg_follow)
                    break

    def login(self) -> bool:
        """
        Opens Instagram and logs in!

        Returns:
            bool: whether the logging in was successful
        """
        if (
            self.config["login"]["insta_username"]
            and self.config["login"]["insta_password"]
        ):
            try:
                # configuring the driver
                self.driver = webdriver.Chrome(
                    service=Service(ChromeDriverManager().install()), options=Options()
                )
                self.driver.implicitly_wait(
                    self.config["user_preferences"]["base_waiting_time"]
                )  # configuring waiting time period till elements appear

                self.driver.get("https://instagram.com")
                username_field = self.driver.find_element(
                    By.XPATH, "//*[@id='loginForm']/div/div[1]/div/label/input"
                )
                username_field.clear()
                username_field.send_keys(self.config["login"]["insta_username"])

                password_field = self.driver.find_element(
                    By.XPATH, "//*[@id='loginForm']/div/div[2]/div/label/input"
                )
                password_field.clear()
                password_field.send_keys(self.config["login"]["insta_password"])

                login_button = self.driver.find_element(
                    By.XPATH, "//*[@id='loginForm']/div/div[3]/button"
                )
                login_button.click()

                time.sleep(self.config["user_preferences"]["base_waiting_time"])

                save_login_info_button = self.driver.find_element(
                    By.XPATH,
                    "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div/div/section/div/button",
                )
                save_login_info_button.click()

                return True
            except:
                self._show_error_message(
                    "Error Logging In!",
                    "Check whether your credentials are valid! \nIf the error persists, try changing Base Waiting Time (in Preferences) or updating the application!",
                )
                self.driver.close()
        else:
            self._show_error_message(
                "Error Logging In!", "Instagram login details are missing!"
            )
        return False

    def like_and_follow_by_hashtag(self, n_likes: int, n_follows: int):
        """
        Likes/follows n number of users!

        Args:
            n_likes (int): number of users whose posts should be liked
            n_follows (int): number of users to follow
        """
        like_follow_by_hashtag(self, n_likes, n_follows)

    def unfollow_users(self, n: int, mode: str):
        """
        Unfollows the specified number of users.

        Args:
            n (int): number of users to unfollow
            mode (str): mode used to unfollow users (either dynamic or all)
        """
        if mode == "all":
            following_list = self._get_following_users_container()
            perform_action_on_n_users(
                "unfollow",
                self.config,
                self.driver,
                following_list,
                n,
                self._today_actions,
                self._update_today_actions,
            )
        else:
            # mode should be "dynamic" as there are only 2 modes
            self._perform_dynamic_unfollow(n)

    def whitelist_following_users(self):
        """
        Adds all the "following" users to the whitelist.
        """
        following_list = self._get_following_users_container()
        perform_action_on_n_users(
            "set_whitelist",
            self.config,
            self.driver,
            following_list,
            self.config["restrictions"]["instagram"]["max_following"],
            self._today_actions,
            self._update_today_actions,
        )

    def quit(self):
        """
        Quits the browser
        """
        self.driver.close()
