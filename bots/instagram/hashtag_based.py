import math

from selenium.webdriver.common.keys import Keys  # provides keyboard elements
from selenium.webdriver.common.by import By  # locates elements within a web page

from .user_related_actions import perform_action_on_n_users

import time

# hashtag based post xpaths (these are in respect to the row number (i))
HASHTAG_BASED_FIRST_POST_XPATH = (
    lambda i: f"/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/article/div/div/div/div[{i}]/div[1]/a"
)
HASHTAG_BASED_SECOND_POST_XPATH = (
    lambda i: f"/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/article/div/div/div/div[{i}]/div[2]/a"
)

# other xpaths used for this module
LIKERS_CONTAINER_OF_A_POST = "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div[1]/div"


def get_post_urls(driver: object, hashtag: str, n: int = 4) -> tuple:
    """
    Grabbing URLs of upto n posts under specified hashtag to follow and like.

    Args:
        driver (object): gateway to interact with instagram.com
        hashtag (str)
        n (int, optional): the number of posts to query (10 is the maximum; limited by Instagram) [greater this is, more time it takes!]

    Returns:
        tuple: 2 lists of post urls (0 -> to_follow_urls, 1 -> to_like_urls)
    """
    # returns a list whose 1st index would be a list of posts to follow and the 2nd index is a list of posts to like
    driver.get(f"https://instagram.com/explore/tags/{hashtag}")

    to_follow_urls = []
    to_like_urls = []
    try:
        for i in range(1, n + 1):
            to_follow = driver.find_element(
                By.XPATH,
                HASHTAG_BASED_FIRST_POST_XPATH(i),
            )
            to_follow_urls.append(to_follow.get_attribute("href"))
            to_like = driver.find_element(
                By.XPATH,
                HASHTAG_BASED_SECOND_POST_XPATH(i),
            )
            to_like_urls.append(to_like.get_attribute("href"))
    except:
        pass

    return to_follow_urls, to_like_urls


def perform_action_on_likers(
    action: str,
    config: dict,
    driver: object,
    n: int,
    post_url: str,
    today_actions: dict,
    today_actions_updater: object,
) -> int:
    """
    either follow the likers of the given post url or like their latest post!

    Args:
        action (str): name of the action to perform
        config (dict): configurations
        driver (object): gateway to interact with Instagram
        n (int): number of people to follow
        post_url (str): URL of the post (e.g. https://instagram.com/p/id)
        today_actions (dict): the record of actions performed today
        today_actions_updater (function): a function to write today_actions to _today_actions.yaml

    Returns:
        int: number of people we have successfully followed
    """
    driver.get(post_url + "liked_by/")

    user_elements_container = driver.find_element(
        By.XPATH,
        LIKERS_CONTAINER_OF_A_POST,
    )

    n_done = perform_action_on_n_users(
        action,
        config,
        driver,
        user_elements_container,
        n,
        today_actions,
        today_actions_updater,
    )
    return n_done


def iterate_post_urls(
    config: dict,
    driver: object,
    n_actions_to_do: int,
    urls: list,
    action: str,
    today_actions: dict,
    today_actions_updater: object,
) -> int:
    """
    Iterates over the urls given and performs the action up to n_actions_to_do times for those who have liked that particular post.
    Supported actions:
        * like - like the last post of the user
        * follow - follow the user

    Returns:
        int: number of excess actions in case we don't have enough likers!
    """
    current_index = 0
    n_done = 0
    while n_actions_to_do > 0:
        n_done = perform_action_on_likers(
            action,
            config,
            driver,
            n_actions_to_do,
            urls[current_index],
            today_actions,
            today_actions_updater,
        )
        n_actions_to_do -= n_done
        current_index += 1
        if current_index >= len(urls):
            break

    return n_actions_to_do


def like_follow_by_hashtag(bot: object, n_likes: int, n_follows: int):
    """
    Follows and likes the last post of n users!

    Args:
        bot (object): an instance of the instagram bot class
        n_likes (int): number of users whose posts should be liked
        n_follows (int): number of users to follow
        * NOTE: n_likes & n_follows have to be greater than the number of hashtags!
    """
    # defining a few backbone variables
    driver = bot.driver
    config = bot.config
    today_actions = bot._today_actions
    today_actions_updater = bot._update_today_actions

    only_follow = config["user_preferences"]["only_follow"]

    hashtags = config["user_preferences"]["hashtags"]
    n_follows_per_hashtag = n_follows // len(hashtags)
    n_likes_per_hashtag = n_likes // len(hashtags)

    for i, hashtag in enumerate(hashtags):
        n_remaining_hashtags = len(hashtags) - i + 1

        # a function to automatically update the number of remaining actions
        get_updated_count_per_hashtag = (
            lambda excess: ((n_follows_per_hashtag * n_remaining_hashtags) + excess)
            // n_remaining_hashtags
        )

        try:
            to_follow_urls, to_like_urls = get_post_urls(driver, hashtag)

            if len(to_follow_urls) > 0:
                excess_follows = iterate_post_urls(
                    config,
                    driver,
                    n_follows_per_hashtag,
                    to_follow_urls,
                    "follow",
                    today_actions,
                    today_actions_updater,
                )

                if excess_follows > 0:
                    n_follows_per_hashtag = get_updated_count_per_hashtag(
                        excess_follows
                    )

            if not only_follow and len(to_like_urls):
                excess_likes = iterate_post_urls(
                    config,
                    driver,
                    n_likes_per_hashtag,
                    to_like_urls,
                    "like",
                    today_actions,
                    today_actions_updater,
                )
                if excess_likes > 0:
                    n_likes_per_hashtag = get_updated_count_per_hashtag(excess_likes)
            else:
                continue
        except:
            n_follows_per_hashtag = get_updated_count_per_hashtag(n_follows_per_hashtag)
            n_likes_per_hashtag = get_updated_count_per_hashtag(n_likes_per_hashtag)
            continue
