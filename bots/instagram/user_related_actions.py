from selenium.webdriver.common.by import By  # locates elements within a web page
from selenium.webdriver.common.action_chains import ActionChains
import time
import datetime
import yaml
from os import path


def _read_the_follow_history() -> dict:
    with open(
        path.abspath(path.join(path.dirname(__file__), "_follow_history.yaml")),
        "r",
    ) as f:
        follow_history = yaml.safe_load(f)
        f.close()
    return follow_history


FOLLOW_HISTORY = _read_the_follow_history()
TODAY = datetime.datetime.now().strftime("%d-%m-%Y")
if TODAY not in FOLLOW_HISTORY.keys():
    FOLLOW_HISTORY[TODAY] = []
else:
    pass

LAST_ACTION_TIME = None  # the last time an action was performed

# general user account xpaths (note: some xpaths depend on the resolution)
LANDSCAPE_FOLLOW_BTN_XPATH = "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[2]/section/main/div/header/section[2]/div/div/div[2]/div/div[1]/button"
PORTRAIT_FOLLOW_BTN_XPATH = "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[2]/section/main/div/header/section[2]/div/div[2]/div/div[1]/button"

LIKE_BUTTON_OF_A_POST = "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[3]/section[1]/div[1]/span[1]/div"
POST_COUNT_OF_A_USER = "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[2]/section/main/div/header/section[3]/ul/li[1]/span/span"

TOP_LEFT_POST_OF_A_USER_LANDSCAPE = "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[2]/section/main/div/div[2]/div/div[1]/div[1]/a"
TOP_LEFT_POST_OF_A_USER_PORTRAIT = "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[2]/section/main/div/div[2]/div/div[1]/div[1]/a"

PRIVATE_ACCOUNT_STATEMENT = "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[2]/section/main/div/div[1]/div/div[1]/div[2]/div/div/span"

UNFOLLOW_BUTTON_WHEN_FOLLOWING = "/html/body/div[8]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div/div[8]"
UNFOLLOW_BUTTON_WHEN_REQUESTED_TO_FOLLOW = "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[2]/section/main/div/header/section[2]/div/div/div[2]/div/div/button"

# dynamic xpaths
n_count_base = "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[2]/section/main/div/"  # just a repetitive path :)
N_FOLLOWERS_LANDSCAPE = lambda is_not_private: (
    n_count_base + "header/section[3]/ul/li[2]/a/span/span"
    if is_not_private
    else n_count_base + "header/section[3]/ul/li[2]/span/span"
)
N_FOLLOWING_LANDSCAPE = lambda is_not_private: (
    n_count_base + "header/section[3]/ul/li[3]/a/span/span"
    if is_not_private
    else n_count_base + "header/section[3]/ul/li[3]/span/span"
)

N_FOLLOWERS_PORTRAIT = lambda is_not_private: (
    n_count_base + "header/section[3]/ul/li[2]/a/span/span/span"
    if is_not_private
    else n_count_base + "header/section[3]/ul/li[2]/span/span/span"
)
N_FOLLOWING_PORTRAIT = lambda is_not_private: (
    n_count_base + "header/section[3]/ul/li[3]/a/span/span/span"
    if is_not_private
    else n_count_base + "header/section[3]/ul/li[3]/span/span/span"
)

# muting related xpaths
USER_MUTE_BUTTON_XPATH = "/html/body/div[7]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div/div[6]"
MUTE_POSTS_BUTTON = "/html/body/div[7]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div/div[2]/div[1]"
MUTE_STORIES_BUTTON = "/html/body/div[7]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div/div[2]/div[2]"
MUTE_SETTINGS_SAVE_BUTTON_XPATH = "/html/body/div[7]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div/div[2]/div[4]/div"


def _update_the_follow_history():
    with open(
        path.abspath(path.join(path.dirname(__file__), "_follow_history.yaml")),
        "w",
    ) as f:
        yaml.dump(FOLLOW_HISTORY, f)
        f.close()


def _update_whitelist(new_whitelist):
    with open(
        # accessing the parent directory through 2 dirnames
        path.abspath(
            path.join(path.dirname(path.dirname(__file__)), "config/whitelist.yaml")
        ),
        "w",
    ) as f:
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
    n_followers_landscape_xpath = N_FOLLOWERS_LANDSCAPE(is_not_private)
    n_following_landscape_xpath = N_FOLLOWING_LANDSCAPE(is_not_private)
    n_followers_portrait_xpath = N_FOLLOWERS_PORTRAIT(is_not_private)
    n_following_portrait_xpath = N_FOLLOWING_PORTRAIT(is_not_private)

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
        POST_COUNT_OF_A_USER,
    ).get_attribute("innerHTML")
    post_count = _convert_count(post_count)
    return post_count > 0


def _not_private_account(driver: object) -> bool:
    try:
        private_statement = driver.find_element(
            By.XPATH,
            PRIVATE_ACCOUNT_STATEMENT,
        ).get_attribute("innerHTML")
        return False
    except:
        return True


def follow_a_user(
    driver: object,
    accepted_ratio: int,
    mute: bool,
    follow_private_accounts: bool,
    time_to_wait: float,
) -> bool:
    """
    Checks whether the user meets the accepted ratio. If so, follows and mutes them.

    Args:
        driver (object): gateway to interact with instagram.com
        accepted_ratio (int): n(following)/n(followers) threshold to perform the action
        mute (bool): whether to mute the user after following
        follow_private_accounts (bool): whether to follow private accounts
        time_to_wait (float): the amount of time to wait before performing the action

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

            try:
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

                    time.sleep(time_to_wait)

                    following_button.click()

                    mute_button = driver.find_element(
                        By.XPATH,
                        USER_MUTE_BUTTON_XPATH,
                    )
                    mute_button.click()

                    mute_posts = driver.find_element(
                        By.XPATH,
                        MUTE_POSTS_BUTTON,
                    )
                    mute_posts.click()

                    mute_stories = driver.find_element(
                        By.XPATH,
                        MUTE_STORIES_BUTTON,
                    )
                    mute_stories.click()

                    save_button = driver.find_element(
                        By.XPATH,
                        MUTE_SETTINGS_SAVE_BUTTON_XPATH,
                    )
                    save_button.click()
            except:
                pass

            return True

        else:
            return False
    except:
        return False


def unfollow_a_user(driver: object, user_url: str, time_to_wait: float) -> bool:
    """
    Unfollows the given user.

    Args:
        driver (object): gateway to interact with the browser
        user_url (str): link to the profile of the user
        time_to_wait (float): the amount of time to wait before performing the action

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
                unfollow_btn_xpath = UNFOLLOW_BUTTON_WHEN_FOLLOWING
            else:
                unfollow_btn_xpath = UNFOLLOW_BUTTON_WHEN_REQUESTED_TO_FOLLOW

            unfollow_btn = driver.find_element(By.XPATH, unfollow_btn_xpath)

            time.sleep(time_to_wait)
            unfollow_btn.click()

            time.sleep(3)
            return True
        else:
            return False
    except:
        return False


def like_the_last_post_of_a_user(
    driver: object, accepted_ratio: int, time_to_wait: float
) -> bool:
    """
    Checks whether the user meets the accepted ratio. If so, likes their their post. Here, the last post means the top-left post of a user.

    Args:
        accepted_ratio (int): n(following)/n(followers) threshold to perform the action
        time_to_wait (float): the amount of time to wait before performing the action

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
                    TOP_LEFT_POST_OF_A_USER_LANDSCAPE,
                ).get_attribute("href")
            except:
                time.sleep(1.5)
                last_post_link = driver.find_element(
                    By.XPATH,
                    TOP_LEFT_POST_OF_A_USER_PORTRAIT,
                ).get_attribute("href")

            driver.get(last_post_link)

            like_button = driver.find_element(
                By.XPATH,
                LIKE_BUTTON_OF_A_POST,
            )

            time.sleep(time_to_wait)

            # simulating a human click
            action = ActionChains(driver)
            action.click_and_hold(like_button)
            action.release(like_button)
            action.perform()

            return True
        else:
            return False
    except:
        return False


def get_user_url_list(
    driver: object,
    user_elements_container: object,
    n: int,
    cancel_flag: object,
) -> list:
    """
    Scrolls down the list of users displayed as a floating panel in Instagram.
    Returns a list urls of n number of users from that!

    Args:
        driver (object): the gateway to interact with instagram.com
        user_list_container (object): div that contains the every user element as a child
        n (int): number of users whose urls should be queried
        cancel_flag (object): flag object indicating whether to cancel the process
    """
    user_elements = user_elements_container.find_elements(By.XPATH, "./div")
    user_urls = []

    def _scrape_url_from_user_elements(user_elements, user_urls):
        # user_urls list is constant updated after each scroll.
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
        if not cancel_flag.check():
            driver.execute_script(
                "arguments[0].scrollIntoView(true);", user_elements[-1]
            )

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
        else:
            break

    return user_urls


def perform_action_on_n_users(
    action: str,
    config: dict,
    driver: object,
    user_elements_container: object,
    n: int,
    today_actions: dict,
    today_actions_updater: object,
    update_progress_bar: object,
    cancel_flag: object,
    start_progress: float,
    end_progress: float,
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
        update_progress_bar (object): PyQt progress bar object
        cancel_flag (object): flag object indicating whether to cancel the process
        start_progress (float): the start percentage for the progress bar
        end_progress (float): the end percentage for the progress bar

    Returns:
        int: number of users the action was successfully done to
    """
    global LAST_ACTION_TIME

    _delta_progress = end_progress - start_progress
    _current_progress = start_progress

    # progress percentage allocated for the querying part
    _query_progress = _delta_progress * 0.4
    # progress percentage per action performed
    _per_action_progress = (_delta_progress * 0.6) / n

    if action != "unfollow" and action != "set_whitelist":
        # we query 4 times the n number of users for backup!
        user_urls = get_user_url_list(
            driver,
            user_elements_container,
            n * 4,
            cancel_flag,
        )
    else:
        # when it comes to unfollowing users, we can't rely on n*2...
        user_urls = get_user_url_list(
            driver,
            user_elements_container,
            config["restrictions"]["instagram"]["max_following"],
            cancel_flag,
        )

    _current_progress += _query_progress
    update_progress_bar.emit(round(_current_progress))

    n_done = 0

    # removing the whitelisted user_urls
    user_urls = list(set(user_urls) - set(config["whitelist"]["instagram"]))

    for user_url in user_urls:
        if not cancel_flag.check():
            # we can perform some actions (set_whitelist) without navigating to the user_url
            # plus, they don't even involve following/liking
            # so, they don't have to go through the bot-masking security layers :)
            if action == "set_whitelist":
                config["whitelist"]["instagram"].append(user_url)
                _update_whitelist(config["whitelist"])
                continue

            if LAST_ACTION_TIME == None:
                # the first action is deployed immediately
                elapsed_time = 1
                required_waiting_time = 0
            else:
                elapsed_time = time.time() - LAST_ACTION_TIME
                required_waiting_time = config["restrictions"]["instagram"][
                    "min_time_between_actions"
                ]

            if n_done >= n:
                # breaking the loop once we have done the specified number of actions
                break
            else:
                # navigating to the user_url
                driver.get(user_url)

                if elapsed_time < required_waiting_time:
                    time_to_wait = required_waiting_time - elapsed_time
                else:
                    time_to_wait = 0

                if action == "like":
                    was_successful = like_the_last_post_of_a_user(
                        driver,
                        config["user_preferences"]["accepted_follow_ratio"],
                        time_to_wait,
                    )
                elif action == "unfollow":
                    was_successful = unfollow_a_user(driver, user_url, time_to_wait)
                else:
                    was_successful = follow_a_user(
                        driver,
                        config["user_preferences"]["accepted_follow_ratio"],
                        config["user_preferences"]["automatic_muting"],
                        config["user_preferences"]["follow_private_accounts"],
                        time_to_wait,
                    )
                    # updating the follow history
                    if was_successful:
                        FOLLOW_HISTORY[TODAY].append(user_url)
                        _update_the_follow_history()

                # updating the actions quota for today
                if was_successful:
                    n_done += 1
                    LAST_ACTION_TIME = time.time()

                    # updating the progress
                    _current_progress += _per_action_progress
                    update_progress_bar.emit(round(_current_progress))

                    if action != "unfollow":
                        today_actions[f"n_{action}s"] += 1
                    else:
                        # the number of unfollows goes under n_follows
                        today_actions["n_follows"] += 1
                    today_actions_updater(today_actions)
        else:
            break
    return n_done
