import math

from selenium.webdriver.common.keys import Keys # provides keyboard elements
from selenium.webdriver.common.by import By # locates elements within a web page

def get_user_url_list(driver:object, user_list_container:object, max_users:int, n:int) -> list:
    """
    Scrolls down the list of users displayed as a floating panel in Instagram.
    Returns a list urls of n number of users from that!

    Args:
        driver (object): the gateway to interact with instagram.com
        user_list_container (object): div that contains the every user element as a child
        max_users (int): the maximum number of children user elements in the user_list_container
        n (int): _description_
    """

    user_elements = user_list_container.find_elements(By.XPATH, "./div")
    user_urls = []

    def _scrape_url_from_user_elements(user_elements, user_urls):
        for user_element in user_elements:
            anchor = user_element.find_element(By.XPATH, "./div/div/div/div[2]/div/div/div/div/div/a")
            user_url = anchor.get_attribute("href")
            if user_url not in user_urls:
                user_urls.append(user_url)

        return user_urls
    
    user_urls = _scrape_url_from_user_elements(user_elements, user_urls)

    # the maximum number of user_elements that are available at a given time is 17
    # when you scroll a particular element into view, it becomes the middle one!
    while (len(user_urls) < n) and (len(user_urls) < max_users):
        driver.execute_script("arguments[0].scrollIntoView(true);", user_elements[-1])
        user_elements = user_list_container.find_elements(By.XPATH, "./div")
        if len(user_elements) == 17:
            user_elements = user_elements[-10:]
        else:
            pass

        user_urls = _scrape_url_from_user_elements(user_elements, user_urls)

    return user_urls

def get_post_urls(driver:object, hashtag:str) -> tuple:
    """
    Grabbing URLs of upto 10 posts under specified hashtag.

    Args:
        driver (object): _description_
        hashtag (str): _description_

    Returns:
        tuple: 2 lists of post urls
    """
    # we are grabbing urls of up to 10 posts to like and follow people (10 is the max number of posts it has per hashtag)
    # returns a list whose 1st index would be a list of posts to follow and the 2nd index is a list of posts to like
    driver.get(f"https://instagram.com/explore/tags/{hashtag}")
    
    to_follow_urls = []
    to_like_urls = []
    try:
        for i in range(1, 11):
            to_follow = driver.find_element(By.XPATH, f"/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/article/div/div/div/div[{i}]/div[1]/a")
            to_follow_urls.append(to_follow.get_attribute("href"))
            to_like = driver.find_element(By.XPATH, f"/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/article/div/div/div/div[{i}]/div[2]/a")
            to_like_urls.append(to_like.get_attribute("href"))
    except:
        pass
    
    return to_follow_urls, to_like_urls


def follow_likers(driver:object, n:int, post_url:str) -> int:
    """
    follow the likers of the given post url

    Args:
        driver (object): gateway to interact with Instagram
        n (int): number of people to follow
        post_url (str): URL of the post (e.g. https://instagram.com/p/id)

    Returns:
        int: number of people we have successfully followed
    """
    driver.get(post_url)
    likers = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[3]/section/div/div/span/a")
    max_users = likers.find_element(By.XPATH, "./span/span").get_attribute("innerHTML")
    max_users = int(max_users.replace(",", ""))
    likers.click()

    user_elements_container = driver.find_element(By.XPATH, "/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div/div[2]/div/div")
    print(get_user_url_list(driver, user_elements_container, max_users, n))
    return n

def like_the_latest_post_of_likers(driver, post_url):
    pass


def iterate_post_urls(driver:object, n_actions_to_do:int, urls:list, action:object) -> int:
    """
    Iterates over the urls given and performs the action function up to n_actions_to_do times for those who have liked that particular post.

    Returns:
        int: number of excess actions in case we don't have enough likers!
    """
    print(f"Boom! We are iterating these posts: {urls}")
    current_index = 0
    n_done = 0
    while n_actions_to_do > 0:
        n_done = action(driver, n_actions_to_do, urls[current_index])
        n_actions_to_do -= n_done
        current_index += 1
        if current_index >= len(urls):
            break
    
    return n_actions_to_do


def like_follow_by_hashtag(driver, config, today_actions, only_follow=True, additional_hashtags=[]):
    hashtags = config["user_preferences"]["hashtags"] + additional_hashtags
    n_follows_per_hashtag = math.floor((config["restrictions"]["instagram"]["n_follows"] - today_actions["n_follows"]) / len(hashtags))
    n_likes_per_hashtag = math.floor((config["restrictions"]["instagram"]["n_likes"] - today_actions["n_likes"]) / len(hashtags))

    for i, hashtag in enumerate(hashtags):
        to_follow_urls, to_like_urls = get_post_urls(driver, hashtag)
        
        excess_follows = iterate_post_urls(driver, n_follows_per_hashtag, to_follow_urls, follow_likers)

        n_remaining_hashtags = len(hashtags) - i + 1
        get_updated_count_per_hashtag = lambda excess: math.floor(((n_follows_per_hashtag * n_remaining_hashtags) + excess) / n_remaining_hashtags)
                
        if excess_follows > 0:    
            n_follows_per_hashtag = get_updated_count_per_hashtag(excess_follows)

        if not only_follow:
            excess_likes = iterate_post_urls(driver, n_likes_per_hashtag, to_like_urls, like_the_latest_post_of_likers)
            if excess_likes > 0:
                n_likes_per_hashtag = get_updated_count_per_hashtag(excess_likes)
        else:
            pass