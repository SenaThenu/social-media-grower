import math

from selenium.webdriver.common.keys import Keys  # provides keyboard elements
from selenium.webdriver.common.by import By  # locates elements within a web page

from .user_related_actions import perform_action_on_n_users

import time


def get_post_urls(driver: object, hashtag: str, n: int = 4) -> tuple:
    """
    Grabbing URLs of upto n posts under specified hashtag.

    Args:
        driver (object): gateway to interact with instagram.com
        hashtag (str)
        n (int, optional): the number of posts to query (10 is the maximum) [greater this is, more time it takes!]

    Returns:
        tuple: 2 lists of post urls
    """
    # we are grabbing urls of up to 10 posts to like and follow people (10 is the max number of posts it has per hashtag)
    # returns a list whose 1st index would be a list of posts to follow and the 2nd index is a list of posts to like
    driver.get(f"https://instagram.com/explore/tags/{hashtag}")

    to_follow_urls = []
    to_like_urls = []
    try:
        for i in range(1, n + 1):
            to_follow = driver.find_element(
                By.XPATH,
                f"/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/article/div/div/div/div[{i}]/div[1]/a",
            )
            to_follow_urls.append(to_follow.get_attribute("href"))
            to_like = driver.find_element(
                By.XPATH,
                f"/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/article/div/div/div/div[{i}]/div[2]/a",
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
) -> int:
    """
    follow the likers of the given post url

    Args:
        action (str): name of the action to perform
        config (dict): configurations
        driver (object): gateway to interact with Instagram
        n (int): number of people to follow
        post_url (str): URL of the post (e.g. https://instagram.com/p/id)
        today_actions (dict): the record of actions performed today

    Returns:
        int: number of people we have successfully followed
    """
    driver.get(post_url + "liked_by/")

    user_elements_container = driver.find_element(
        By.XPATH,
        "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div[1]/div",
    )

    n_done = perform_action_on_n_users(
        action, config, driver, user_elements_container, n, today_actions
    )
    return n_done


def iterate_post_urls(
    config: dict,
    driver: object,
    n_actions_to_do: int,
    urls: list,
    action: str,
    today_actions: dict,
) -> int:
    """
    Iterates over the urls given and performs the action up to n_actions_to_do times for those who have liked that particular post.
    Supported actions:
        * like - like the last post of the user
        * follow - follow the user

    Returns:
        int: number of excess actions in case we don't have enough likers!
    """
    print(f"Boom! We are iterating these posts: {urls}")
    current_index = 0
    n_done = 0
    while n_actions_to_do > 0:
        n_done = perform_action_on_likers(
            action, config, driver, n_actions_to_do, urls[current_index], today_actions
        )
        n_actions_to_do -= n_done
        current_index += 1
        if current_index >= len(urls):
            break

    return n_actions_to_do


def like_follow_by_hashtag(
    driver, config, today_actions, only_follow=False, additional_hashtags=[]
):
    hashtags = config["user_preferences"]["hashtags"] + additional_hashtags
    n_follows_per_hashtag = math.floor(
        (config["restrictions"]["instagram"]["n_follows"] - today_actions["n_follows"])
        / len(hashtags)
    )
    n_likes_per_hashtag = math.floor(
        (config["restrictions"]["instagram"]["n_likes"] - today_actions["n_likes"])
        / len(hashtags)
    )

    for i, hashtag in enumerate(hashtags):
        to_follow_urls, to_like_urls = get_post_urls(driver, hashtag)

        if len(to_follow_urls) > 0:
            excess_follows = iterate_post_urls(
                config,
                driver,
                n_follows_per_hashtag,
                to_follow_urls,
                "follow",
                today_actions,
            )

            n_remaining_hashtags = len(hashtags) - i + 1
            get_updated_count_per_hashtag = lambda excess: math.floor(
                ((n_follows_per_hashtag * n_remaining_hashtags) + excess)
                / n_remaining_hashtags
            )

            if excess_follows > 0:
                n_follows_per_hashtag = get_updated_count_per_hashtag(excess_follows)

        if not only_follow and len(to_like_urls):
            excess_likes = iterate_post_urls(
                config, driver, n_likes_per_hashtag, to_like_urls, "like", today_actions
            )
            if excess_likes > 0:
                n_likes_per_hashtag = get_updated_count_per_hashtag(excess_likes)
        else:
            continue
