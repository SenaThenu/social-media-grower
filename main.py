from bots.config import load_config
from bots.instagram import instagram_bot

config = load_config()

instagram_bot(config)