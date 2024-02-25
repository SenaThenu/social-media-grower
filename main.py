from bots.config import load_config
from bots.instagram import InstagramBot
import time

config = load_config()

instabot = InstagramBot(config)
time.sleep(1)
instabot.unfollow_users(3, "all")
print("Done")
time.sleep(100)
