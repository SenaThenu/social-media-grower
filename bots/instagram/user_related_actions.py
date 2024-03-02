from selenium.webdriver.common.by import By  # locates elements within a web page
import time
import datetime
import math
import yaml
import os


def _read_the_follow_history() -> dict:
    with open(os.path.join("bots/instagram", "_follow_history.yaml"), "r") as f:
        follow_history = yaml.safe_load(f)
        f.close()
    return follow_history


FOLLOW_HISTORY = _read_the_follow_history()
TODAY = datetime.datetime.now().strftime("%d-%m-%Y")
if TODAY not in FOLLOW_HISTORY.keys():
    FOLLOW_HISTORY[TODAY] = []
else:
    pass

# Common XPATHs
LANDSCAPE_FOLLOW_BTN_XPATH = "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/div[1]/div[1]/div/div[1]/button"
PORTRAIT_FOLLOW_BTN_XPATH = "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/div[3]/div/div[1]/button"


def _update_the_follow_history():
    with open(os.path.join("bots/instagram", "_follow_history.yaml"), "w") as f:
        yaml.dump(FOLLOW_HISTORY, f)
        f.close()


def _update_whitelist(new_whitelist):
    with open(os.path.join("bots/config", "whitelist.yaml"), "w") as f:
        yaml.dump(new_whitelist, f)
        f.close()


def _convert_count(str_count: str) -> int:
    """
    Converts the readable numbers (e.g. 1,000, 100K, 10M) to integers!

    Args:
        str_count (str): readable number

    Returns:
        int: integer equivalent
    """
    str_count = str_count.replace(",", "")
    if "M" in str_count:
        return int(str_count[:-1]) * 1000000
    elif "K" in str_count:
        return int(str_count[:-1]) * 1000
    else:
        return int(str_count)


def _meets_the_accepted_ratio(driver: object, accepted_ratio, is_not_private):
    # Since Instagram is responsive to resolution, there are 2 possible xpaths for each element (portrait & landscape)
    if is_not_private:
        n_followers_landscape_xpath = "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[2]/a/span/span"
        n_following_landscape_xpath = "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[3]/a/span/span"
        n_followers_portrait_xpath = "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/ul/li[2]/a/span/span/span"
        n_following_portrait_xpath = "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/ul/li[3]/a/span/span/span"
    else:
        n_followers_landscape_xpath = "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[2]/span/span"
        n_following_landscape_xpath = "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[3]/span/span"
        n_followers_portrait_xpath = "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/ul/li[2]/span/span/span"
        n_following_portrait_xpath = "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/ul/li[3]/span/span/span"

    try:
        n_followers = _convert_count(
            driver.find_element(By.XPATH, n_followers_landscape_xpath).get_attribute(
                "innerHTML"
            )
        )
        n_following = _convert_count(
            driver.find_element(By.XPATH, n_following_landscape_xpath).get_attribute(
                "innerHTML"
            )
        )
    except:
        n_followers = _convert_count(
            driver.find_element(By.XPATH, n_followers_portrait_xpath).get_attribute(
                "innerHTML"
            )
        )
        n_following = _convert_count(
            driver.find_element(By.XPATH, n_following_portrait_xpath).get_attribute(
                "innerHTML"
            )
        )

    current_ratio = n_following / (n_followers + 1)

    return current_ratio >= accepted_ratio


def _follow_button_includes(keyword: str, driver: object) -> bool:
    """
    Checks whether the keyword is included in the follow_button!

    Args:
        keyword (str): _description_
        driver (object): _description_

    Returns:
        bool: _description_
    """
    try:
        # there are 2 possibilities for the follow button
        follow_btn_landscape_xpath = f"{LANDSCAPE_FOLLOW_BTN_XPATH}/div/div[1]"
        follow_btn_portrait_xpath = f"{PORTRAIT_FOLLOW_BTN_XPATH}/div/div"

        # finding the element
        try:
            follow_button = driver.find_element(By.XPATH, follow_btn_landscape_xpath)
        except:
            follow_button = driver.find_element(By.XPATH, follow_btn_portrait_xpath)

        # retrieving innerHTML
        if follow_button.get_attribute("innerHTML").lower() == keyword.lower():
            return True
        else:
            return False
    except:
        return False


def _user_has_posts(driver: object) -> bool:
    """
    Checks whether the user has at least one post
    """
    post_count = driver.find_element(
        By.XPATH,
        "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[1]/span/span",
    ).get_attribute("innerHTML")
    post_count = _convert_count(post_count)
    return post_count > 0


def _not_private_account(driver: object) -> bool:
    try:
        private_statement = driver.find_element(
            By.XPATH,
            "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/div[1]/div/h2",
        ).get_attribute("innerHTML")
        if "private" in private_statement.lower():
            return False
        else:
            return True
    except:
        return True


def follow_a_user(
    driver: object, accepted_ratio: int, mute: bool, follow_private_accounts: bool
) -> bool:
    """
    Checks whether the user meets the accepted ratio. If so, follows and mutes them.

    Args:
        driver (object): gateway to interact with instagram.com
        accepted_ratio (int): n(following)/n(followers) threshold to perform the action
        mute (bool): whether to mute the user after following
        follow_private_accounts (bool): whether to follow private accounts

    Returns:
        bool: whether the user was followed
    """
    try:
        is_not_private = _not_private_account(driver)
        if _meets_the_accepted_ratio(
            driver, accepted_ratio, is_not_private
        ) and _follow_button_includes("Follow", driver):

            if not is_not_private and not follow_private_accounts:
                return False

            # checking both the possibilities for the follow button
            try:
                follow_button = driver.find_element(
                    By.XPATH,
                    LANDSCAPE_FOLLOW_BTN_XPATH,
                )
            except:
                follow_button = driver.find_element(
                    By.XPATH,
                    PORTRAIT_FOLLOW_BTN_XPATH,
                )
            follow_button.click()

            time.sleep(3)
            if mute and is_not_private:
                try:
                    following_button = driver.find_element(
                        By.XPATH,
                        LANDSCAPE_FOLLOW_BTN_XPATH,
                    )
                except:
                    following_button = driver.find_element(
                        By.XPATH,
                        PORTRAIT_FOLLOW_BTN_XPATH,
                    )
                following_button.click()

                mute_button = driver.find_element(
                    By.XPATH,
                    "/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div/div[6]",
                )
                mute_button.click()

                mute_posts = driver.find_element(
                    By.XPATH,
                    "/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div/div[2]/div[1]",
                )
                mute_posts.click()

                mute_stories = driver.find_element(
                    By.XPATH,
                    "/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div/div[2]/div[2]",
                )
                mute_stories.click()

                save_button = driver.find_element(
                    By.XPATH,
                    "/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div/div[2]/div[4]/div",
                )
                save_button.click()

            return True

        else:
            return False
    except:
        return False


def unfollow_a_user(driver: object, user_url: str) -> bool:
    """
    Unfollows the given user.

    Args:
        driver (object): gateway to interact with the browser
        user_url (str): link to the profile of the user

    Returns:
        bool: whether the user was unfollowed
    """
    driver.get(user_url)

    try:
        is_following = _follow_button_includes("following", driver)
        is_requested = _follow_button_includes("requested", driver)
        if is_following or is_requested:
            try:
                following_btn = driver.find_element(
                    By.XPATH,
                    LANDSCAPE_FOLLOW_BTN_XPATH,
                )
            except:
                following_btn = driver.find_element(
                    By.XPATH,
                    PORTRAIT_FOLLOW_BTN_XPATH,
                )

            following_btn.click()

            if is_following:
                unfollow_btn_xpath = "/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div/div[8]"
            else:
                unfollow_btn_xpath = "/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div/div/button[1]"

            unfollow_btn = driver.find_element(By.XPATH, unfollow_btn_xpath)
            unfollow_btn.click()

            time.sleep(3)
            return True
        else:
            return False
    except:
        return False


def like_the_last_post_of_a_user(driver: object, accepted_ratio: int) -> bool:
    """
    Checks whether the user meets the accepted ratio. If so, likes their first post.

    Args:
        accepted_ratio (int): n(following)/n(followers) threshold to perform the action

    Returns:
        bool: _description_
    """
    try:
        is_not_private = _not_private_account(driver)
        if (
            _meets_the_accepted_ratio(driver, accepted_ratio, is_not_private)
            and _follow_button_includes("follow", driver)
        ) and (_user_has_posts(driver) and is_not_private):
            try:
                last_post_link = driver.find_element(
                    By.XPATH,
                    "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/div[2]/div/div[1]/div[1]/a",
                ).get_attribute("href")
            except:
                # dealing with pinned posts!
                time.sleep(1.5)
                last_post_link = driver.find_element(
                    By.XPATH,
                    "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/div[3]/div/div[1]/div[1]/a",
                ).get_attribute("href")

            driver.get(last_post_link)

            like_button = driver.find_element(
                By.XPATH,
                "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[3]/div[1]/div[1]/span[1]/div",
            )
            like_button.click()

            return True
        else:
            return False
    except:
        return False


def get_user_url_list(driver: object, user_elements_container: object, n: int) -> list:
    """
    Scrolls down the list of users displayed as a floating panel in Instagram.
    Returns a list urls of n number of users from that!

    Args:
        driver (object): the gateway to interact with instagram.com
        user_list_container (object): div that contains the every user element as a child
        n (int): _description_
    """

    user_elements = user_elements_container.find_elements(By.XPATH, "./div")
    user_urls = []

    def _scrape_url_from_user_elements(user_elements, user_urls):
        for user_element in user_elements:
            anchor = user_element.find_element(
                By.XPATH, "./div/div/div/div[2]/div/div/div/div/div/a"
            )
            user_url = anchor.get_attribute("href")
            # making sure there are no duplicates
            if user_url not in user_urls:
                user_urls.append(user_url)

        return user_urls

    user_urls = _scrape_url_from_user_elements(user_elements, user_urls)

    get_last_username = (
        lambda user_elements: user_elements[-1]
        .find_element(
            By.XPATH, "./div/div/div/div[2]/div/div/div/div/div/a/div/div/span"
        )
        .get_attribute("innerHTML")
    )
    last_username = get_last_username(user_elements)

    # the maximum number of user_elements that are available at a given time is 17
    # when you scroll a particular element into view, it becomes the middle one!
    while len(user_urls) < n:
        driver.execute_script("arguments[0].scrollIntoView(true);", user_elements[-1])
        time.sleep(2)
        user_elements = user_elements_container.find_elements(By.XPATH, "./div")

        # making sure we haven't reached the end of the document
        if last_username == get_last_username(user_elements):
            break
        else:
            last_username = get_last_username(user_elements)

        if len(user_elements) == 17:
            user_elements = user_elements[-10:]
        else:
            pass

        user_urls = _scrape_url_from_user_elements(user_elements, user_urls)

    return user_urls


def perform_action_on_n_users(
    action: str,
    config: dict,
    driver: object,
    user_elements_container: object,
    n: int,
    today_actions: dict,
    today_actions_updater: object,
) -> int:
    """
    Performs the defined action on n users in the user_elements_container.
    Supported actions:
        * like - like the last post of the user
        * follow - follow the user
        * unfollow - unfollows the user
        * set_whitelist - whitelists all the "following" users

    Args:
        action (str): name of the action to perform (defined above!)
        config (dict): configuration dictionary
        driver (object): gateway to interact with instagram.com
        user_elements_container (object): the container which holds all the user elements
        n (int): number of users to perform the action on
        today_actions (dict): the record of actions performed today
        today_actions_updater (function): a function that writes the today_actions to _today_actions.yaml

    Returns:
        int: number of users the action was successfully done to
    """
    if action != "unfollow" and action != "set_whitelist":
        # we query 2 times the n number of users for backup!
        user_urls = get_user_url_list(driver, user_elements_container, n * 2)
    else:
        # when it comes to unfollowing users, we can't rely on n*2...
        user_urls = get_user_url_list(
            driver,
            user_elements_container,
            config["restrictions"]["instagram"]["max_following"],
        )
    n_done = 0

    last_action_time = time.time()

    # removing the whitelisted user_urls
    user_urls = list(set(user_urls) - set(config["whitelist"]["instagram"]))

    for user_url in user_urls:
        # we can perform some actions (set_whitelist) without navigating to the user_url
        # plus, they don't even involve following/liking
        # they don't have to go through the bot-masking security layers :)
        if action == "set_whitelist":
            if user_url not in config["whitelist"]["instagram"]:
                config["whitelist"]["instagram"].append(user_url)
            _update_whitelist(config["whitelist"])
            continue

        elapsed_time = math.floor(time.time() - last_action_time)
        required_waiting_time = config["restrictions"]["instagram"][
            "min_time_between_actions"
        ]
        if elapsed_time < required_waiting_time:
            time.sleep(required_waiting_time - elapsed_time)
        else:
            last_action_time = time.time()
            if n_done >= n:
                # breaking the loop once we have done the specified number of actions
                break
            else:
                # navigating to the user_url
                driver.get(user_url)

                if action == "like":
                    was_successful = like_the_last_post_of_a_user(
                        driver, config["user_preferences"]["accepted_follow_ratio"]
                    )
                elif action == "unfollow":
                    was_successful = unfollow_a_user(driver, user_url)
                else:
                    was_successful = follow_a_user(
                        driver,
                        config["user_preferences"]["accepted_follow_ratio"],
                        config["user_preferences"]["automatic_muting"],
                        config["user_preferences"]["follow_private_accounts"],
                    )
                    # updating the follow history
                    if was_successful:
                        FOLLOW_HISTORY[TODAY].append(user_url)
                        _update_the_follow_history()

                # updating the actions quota for today
                if was_successful:
                    n_done += 1
                    if action != "unfollow":
                        today_actions[f"n_{action}s"] += 1
                    else:
                        # the number of unfollows goes under n_follows
                        today_actions["n_follows"] += 1
                    today_actions_updater(today_actions)
    return n_done
