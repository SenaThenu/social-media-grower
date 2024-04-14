from selenium import webdriver

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By  # locates elements within a web page

import time
import yaml
import datetime
from os import path
from notifypy import Notify

from .hashtag_based import like_follow_by_hashtag
from .user_related_actions import (
    perform_action_on_n_users,
    unfollow_a_user,
    get_user_url_list,
)

# XPATHs stored in global variables

# following users container (3 possibilities)
FOLLOWING_USERS_CONTAINER_LANDSCAPE_1 = "/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[4]/div[1]/div"
FOLLOWING_USERS_CONTAINER_LANDSCAPE_2 = "/html/body/div[5]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[4]/div[1]/div"
FOLLOWING_USERS_CONTAINER_PORTRAIT = "/html/body/div[7]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[4]/div[1]/div"

# followers container (3 possibilities)
FOLLOWERS_CONTAINER_LANDSCAPE_1 = "/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div"
FOLLOWERS_CONTAINER_LANDSCAPE_2 = "/html/body/div[5]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div"
FOLLOWERS_CONTAINER_PORTRAIT = "/html/body/div[7]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div"


class InstagramBot:
    def __init__(self, config):
        self.config = config

        # loading today's actions
        self._today_actions = self._load_today_actions()

        self.driver = (
            None  # this is only configured once in login(). so always perform it first!
        )

    def _load_today_actions(self) -> dict:
        """
        Reads _today_actions.yaml. Updates the date to today if it's not the case.

        Returns:
            dict: actions done today
        """
        # using the absolute path since this is being called from main.py
        with open(
            path.abspath(path.join(path.dirname(__file__), "_today_actions.yaml")),
            "r",
        ) as f:
            actions = yaml.safe_load(f)
            f.close()

        today = datetime.datetime.now().strftime("%d-%m-%Y")
        if actions["date"] != today:
            actions = {"date": today, "n_likes": 0, "n_follows": 0, "n_comments": 0}

        self._update_today_actions(actions)

        return actions

    def _update_today_actions(self, today_actions):
        self._today_actions = today_actions
        with open(
            path.abspath(path.join(path.dirname(__file__), "_today_actions.yaml")),
            "w",
        ) as f:
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

        # there are 3 possibilities
        try:
            following_list = self.driver.find_element(
                By.XPATH,
                FOLLOWING_USERS_CONTAINER_LANDSCAPE_1,
            )
        except:
            try:
                following_list = self.driver.find_element(
                    By.XPATH,
                    FOLLOWING_USERS_CONTAINER_PORTRAIT,
                )
            except:
                following_list = self.driver.find_element(
                    By.XPATH,
                    FOLLOWING_USERS_CONTAINER_LANDSCAPE_2,
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

        # there are 3 possibilities
        try:
            followers_list = self.driver.find_element(
                By.XPATH,
                FOLLOWERS_CONTAINER_LANDSCAPE_1,
            )
        except:
            try:
                followers_list = self.driver.find_element(
                    By.XPATH,
                    FOLLOWERS_CONTAINER_PORTRAIT,
                )
            except:
                followers_list = self.driver.find_element(
                    By.XPATH,
                    FOLLOWERS_CONTAINER_LANDSCAPE_2,
                )

        return followers_list

    def _perform_dynamic_unfollow(
        self,
        n: int,
        update_progress_bar: object,
        cancel_flag: object,
        start_progress: float,
        end_progress: float,
    ):
        """
        Reads the follow history and dynamically unfollows n number of users who don't follow back!

        Args:
        n (int): number of users to unfollow
        update_progress_bar (object): the signal to emit to update the progress bar (accepts an integer argument between 0 and 100 (percentage))
        cancel_flag (object): flag object indicating whether to cancel the process
        start_progress (float): the start percentage for the progress bar
        end_progress (float): the end percentage for the progress bar
        """
        _delta_progress = end_progress - start_progress
        _current_progress = start_progress

        # progress percentage allocated for the querying part
        _query_progress = _delta_progress * 0.4
        # progress percentage per action performed
        _per_action_progress = (_delta_progress * 0.6) / n

        def _update_follow_history(his):
            with open(
                path.abspath(path.join(path.dirname(__file__), "_follow_history.yaml")),
                "w",
            ) as f:
                yaml.dump(his, f)
                f.close()

        with open(
            path.abspath(path.join(path.dirname(__file__), "_follow_history.yaml")),
            "r",
        ) as f:
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
            cancel_flag,
        )

        _current_progress += _query_progress
        update_progress_bar.emit(round(_current_progress))

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
                            _current_progress += _per_action_progress
                            update_progress_bar.emit(round(_current_progress))

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

                try:
                    # if this can be found, the user has enabled 2 factor authentication!
                    two_factor_auth_statement = self.driver.find_element(
                        By.XPATH,
                        "/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/div/div/div[1]/div[2]/div",
                    ).get_attribute("innerHTML")

                    request_to_verify_notification = Notify()
                    request_to_verify_notification.title = "Verify Login!"
                    request_to_verify_notification.message = "You have enabled two-factor authentication. You'll be given 30 seconds to verify!"
                    request_to_verify_notification.send()
                    time.sleep(30)
                except:
                    pass

                try:
                    save_login_info_button = self.driver.find_element(
                        By.XPATH,
                        "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div/div/section/div/button",
                    )
                    save_login_info_button.click()
                except:
                    pass

                return True
            except:
                self.driver.close()
        return False

    def like_and_follow_by_hashtag(
        self,
        n_likes: int,
        n_follows: int,
        update_progress_bar: object,
        cancel_flag: object,
    ):
        """
        Likes/follows n number of users!

        Args:
            n_likes (int): number of users whose posts should be liked
            n_follows (int): number of users to follow
            update_progress_bar (object): the signal to emit to update the progress bar (accepts an integer argument between 0 and 100 (percentage))
            cancel_flag (object): flag object indicating whether to cancel the process
        """
        like_follow_by_hashtag(
            self,
            n_likes,
            n_follows,
            update_progress_bar,
            cancel_flag,
            0,
            100,
        )
        update_progress_bar.emit(100)

    def unfollow_users(
        self,
        n: int,
        mode: str,
        update_progress_bar: object,
        cancel_flag: object,
    ):
        """
        Unfollows the specified number of users.

        Args:
            n (int): number of users to unfollow
            mode (str): mode used to unfollow users (either dynamic or all)
            update_progress_bar (object): the signal to emit to update the progress bar (accepts an integer argument between 0 and 100 (percentage))
            cancel_flag (object): flag object indicating whether to cancel the process
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
                update_progress_bar,
                cancel_flag,
                0,
                100,
            )
        else:
            # mode should be "dynamic" as there are only 2 modes
            self._perform_dynamic_unfollow(
                n,
                update_progress_bar,
                cancel_flag,
                0,
                100,
            )

    def whitelist_following_users(
        self,
        update_progress_bar: object,
        cancel_flag: object,
    ):
        """
        Adds all the "following" users to the whitelist.

        Args:
            update_progress_bar (object): the signal to emit to update the progress bar (accepts an integer argument between 0 and 100 (percentage))
            cancel_flag (object): flag object indicating whether to cancel the process
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
            update_progress_bar,
            cancel_flag,
            0,
            100,
        )

        update_progress_bar.emit(100)

    def quit(self):
        """
        Quits the browser
        """
        if self.driver:
            self.driver.close()
