import yaml
import os


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

    for file in os.listdir(os.path.dirname(__file__)):
        # making sure it is a yaml file that's not private (private = an underscore/period at the start)!
        if (file[-4:] == "yaml") and (file[0] != "_" and file[0] != "."):
            with open(
                os.path.abspath(os.path.join(os.path.dirname(__file__), file)),
                "r",
            ) as f:
                data = yaml.safe_load(f)
                config[_get_filename(file)] = data
                f.close()

    return config
