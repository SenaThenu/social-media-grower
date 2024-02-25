from bots.config import load_config
from bots.instagram import InstagramBot
import time

config = load_config()

instabot = InstagramBot(config)
time.sleep(1)
instabot.whitelist_following_users()
print("Done")
time.sleep(100)
