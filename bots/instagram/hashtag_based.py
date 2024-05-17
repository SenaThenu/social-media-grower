from selenium.webdriver.common.keys import Keys  # provides keyboard elements
from selenium.webdriver.common.by import By  # locates elements within a web page

from .user_related_actions import perform_action_on_n_users

# hashtag based post xpaths (these are in respect to the row number (i))
HASHTAG_BASED_FIRST_POST_XPATH = (
    lambda i: f"/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/article/div/div[2]/div/div[{i}]/div[1]/a"
)
HASHTAG_BASED_SECOND_POST_XPATH = (
    lambda i: f"/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/article/div/div[2]/div/div[{i}]/div[2]/a"
)

# other xpaths used for this module
LIKERS_CONTAINER_OF_A_POST = "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div[1]/div"

# global vars used for the GUI (these are automatically filled when like_follow_by_hashtag() is called)
UPDATE_PROGRESS_BAR = None
CANCEL_FLAG = None  # flag object indicating whether to cancel the process


def _get_post_urls(
    driver: object, hashtag: str, start_progress: float, end_progress: float, n: int = 5
) -> tuple:
    """
    Grabbing URLs of upto n posts under specified hashtag to follow and like.

    Args:
        driver (object): gateway to interact with instagram.com
        hashtag (str)
        start_progress (float): the start percentage for the progress bar
        end_progress (float): the end percentage for the progress bar
        n (int, optional): the number of posts to query (10 is the maximum; limited by Instagram)
    Returns:
        tuple: 2 lists of post urls (0 -> to_follow_urls, 1 -> to_like_urls)
    """
    # returns a list whose 1st index would be a list of posts to follow and the 2nd index is a list of posts to like
    driver.get(f"https://instagram.com/explore/tags/{hashtag}")
    to_follow_urls = []
    to_like_urls = []

    # 2 queries for each iteration!
    progress_per_query = (end_progress - start_progress) / (n * 2)

    try:
        for i in range(1, n + 1):
            # checking whether we are commanded to cancel the process
            if CANCEL_FLAG.check():
                raise Exception("User terminated the process!")

            to_follow = driver.find_element(
                By.XPATH,
                HASHTAG_BASED_FIRST_POST_XPATH(i),
            )
            to_follow_urls.append(to_follow.get_attribute("href"))
            start_progress += progress_per_query
            UPDATE_PROGRESS_BAR.emit(round(start_progress))

            to_like = driver.find_element(
                By.XPATH,
                HASHTAG_BASED_SECOND_POST_XPATH(i),
            )
            to_like_urls.append(to_like.get_attribute("href"))
            start_progress += progress_per_query
            UPDATE_PROGRESS_BAR.emit(round(start_progress))
    except:
        pass

    return to_follow_urls, to_like_urls


def _perform_action_on_likers(
    action: str,
    config: dict,
    driver: object,
    n: int,
    post_url: str,
    today_actions: dict,
    today_actions_updater: object,
    start_progress: float,
    end_progress: float,
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
        start_progress (float): the start percentage for the progress bar
        end_progress (float): the end percentage for the progress bar

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
        UPDATE_PROGRESS_BAR,
        CANCEL_FLAG,
        start_progress,
        end_progress,
    )

    return n_done


def _iterate_post_urls(
    config: dict,
    driver: object,
    n_actions_to_do: int,
    urls: list,
    action: str,
    today_actions: dict,
    today_actions_updater: object,
    start_progress: float,
    end_progress: float,
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
    current_progress = start_progress

    progress_increment_per_action = (end_progress - start_progress) / n_actions_to_do

    while n_actions_to_do > 0:
        if not CANCEL_FLAG.check():
            n_done = _perform_action_on_likers(
                action,
                config,
                driver,
                n_actions_to_do,
                urls[current_index],
                today_actions,
                today_actions_updater,
                current_progress,
                current_progress + (progress_increment_per_action * n_actions_to_do),
            )

            n_actions_to_do -= n_done

            current_progress += progress_increment_per_action * n_done
            UPDATE_PROGRESS_BAR.emit(round(current_progress))

            current_index += 1
            if current_index >= len(urls):
                UPDATE_PROGRESS_BAR.emit(round(end_progress))
                break
        else:
            break

    return n_actions_to_do


def like_follow_by_hashtag(
    bot: object,
    n_likes: int,
    n_follows: int,
    update_progress_bar: object,
    cancel_flag: object,
    start_progress: float,
    end_progress: float,
):
    """
    Follows and likes the last post of n users!

    Args:
        bot (object): an instance of the instagram bot class
        n_likes (int): number of users whose posts should be liked
        n_follows (int): number of users to follow
        UPDATE_PROGRESS_BAR (object): PyQt progress bar object
        cancel_flag (object): flag object indicating whether to cancel the process
        start_progress (float): the start percentage for the progress bar
        end_progress (float): the end percentage for the progress bar
            * NOTE: n_likes & n_follows have to be greater than the number of hashtags!
    """
    # filling some global GUI-related variables
    global UPDATE_PROGRESS_BAR, CANCEL_FLAG
    UPDATE_PROGRESS_BAR = update_progress_bar
    CANCEL_FLAG = cancel_flag

    # defining a few backbone variables
    driver = bot.driver
    config = bot.config
    today_actions = bot._today_actions
    today_actions_updater = bot._update_today_actions

    only_follow = config["user_preferences"]["only_follow"]

    hashtags = config["user_preferences"]["hashtags"]
    n_follows_per_hashtag = n_follows // len(hashtags)
    n_likes_per_hashtag = n_likes // len(hashtags)

    current_percentage = start_progress
    progress_per_hashtag = (end_progress - start_progress) / len(hashtags)
    # assumes equal percentages for querying and performing the actions

    for i, hashtag in enumerate(hashtags):
        n_remaining_hashtags = (
            len(hashtags) - i - 1 if i != len(hashtags) - 1 else 1
        )  # to prevent the ZeroDivisionError

        # a function to automatically update the number of remaining actions
        get_updated_count_per_hashtag = (
            lambda excess: ((n_follows_per_hashtag * n_remaining_hashtags) + excess)
            // n_remaining_hashtags
        )

        try:
            to_follow_urls, to_like_urls = _get_post_urls(
                driver,
                hashtag,
                current_percentage,
                current_percentage + (progress_per_hashtag / 2),
            )

            current_percentage += (
                progress_per_hashtag / 2
            )  # 50% for querying and 50% for performing
            UPDATE_PROGRESS_BAR.emit(round(current_percentage))

            # if just follow, the remaining 50% is taken. If it's both like and follow, it should be split into 2
            progress_increment_for_each_action_type = (
                progress_per_hashtag / 2 if only_follow else progress_per_hashtag / 4
            )

            if len(to_follow_urls) > 0:
                excess_follows = _iterate_post_urls(
                    config,
                    driver,
                    n_follows_per_hashtag,
                    to_follow_urls,
                    "follow",
                    today_actions,
                    today_actions_updater,
                    current_percentage,
                    current_percentage + progress_increment_for_each_action_type,
                )

                current_percentage += progress_increment_for_each_action_type
                UPDATE_PROGRESS_BAR.emit(round(current_percentage))

                if excess_follows > 0:
                    n_follows_per_hashtag = get_updated_count_per_hashtag(
                        excess_follows
                    )

            if not only_follow and len(to_like_urls):
                excess_likes = _iterate_post_urls(
                    config,
                    driver,
                    n_likes_per_hashtag,
                    to_like_urls,
                    "like",
                    today_actions,
                    today_actions_updater,
                    current_percentage,
                    current_percentage + progress_increment_for_each_action_type,
                )

                current_percentage += progress_increment_for_each_action_type
                UPDATE_PROGRESS_BAR.emit(round(current_percentage))

                if excess_likes > 0:
                    n_likes_per_hashtag = get_updated_count_per_hashtag(excess_likes)
            else:
                continue
        except:
            n_follows_per_hashtag = get_updated_count_per_hashtag(n_follows_per_hashtag)
            n_likes_per_hashtag = get_updated_count_per_hashtag(n_likes_per_hashtag)
            continue
