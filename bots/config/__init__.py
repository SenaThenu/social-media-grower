import yaml
import os
from dotenv import load_dotenv

# user logins should be stored in .env in the config directory for privacy!
load_dotenv()

def _get_filename(file):
    i_of_period = file.find(".")
    return file[:i_of_period]

def load_config() -> dict:
    """
    Reads the configuration files in the config folder!
    Note: this is intended to be called from main.py! (otherwise, paths wouldn't work!)

    Returns:
        a dict whose keys are the filenames & values are the content in the corresponding file!
    """
    config = {}
    
    for file in os.listdir("bots/config"):
        if file[0] != "_" and file[0] != ".":
            with open(os.path.join("bots/config", file), "r") as f:
                data = yaml.safe_load(f)
                config[_get_filename(file)] = data
                f.close()
    
    return config