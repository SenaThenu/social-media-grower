from bots.config import load_config
from bots.instagram import InstagramBot
import time

config = load_config()

instabot = InstagramBot()
time.sleep(1)
instabot.like_and_follow_by_hashtag(config)
time.sleep(100)
