from bots.config import load_config
from bots.instagram import InstagramBot
import time

config = load_config()

instabot = InstagramBot(config)
time.sleep(1)
instabot.like_and_follow_by_hashtag()
time.sleep(100)
