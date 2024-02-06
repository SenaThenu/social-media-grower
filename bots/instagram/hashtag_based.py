import math

def follow_likers(driver, hashtag, n):
    for i in range(n):
        # follow n amount of people who have liked the first post under the hashtag!
        pass

def like_latest_post_of_likers(driver, hashtag, n):
    for i in range(n):
        # like n amount of people who have liked the 2nd post under the hashtag!
        pass


def like_and_follow_by_hashtag(driver, config, today_actions):
    hashtags = config["user_preferences"]["hashtags"]
    n_follows_per_hashtag = math.floor((config["restrictions"]["instagram"]["n_follows"] - today_actions["n_follows"]) / len(hashtags))
    n_likes_per_hashtag = math.floor((config["restrictions"]["instagram"]["n_likes"] - today_actions["n_likes"]) / len(hashtags))

    for hashtag in hashtags:
        follow_likers(driver, hashtag, n_follows_per_hashtag)
        like_latest_post_of_likers(driver, hashtag, n_likes_per_hashtag)