import os
import yaml

LOGGED_IN = False

# these will be automatically updated when setup_instagram_ui is called
MAIN_GUI = None
INSTA_BOT = None


def setup_instagram_ui(main_gui: object, instabot: object):
    global MAIN_GUI, INSTA_BOT
    MAIN_GUI = main_gui
    INSTA_BOT = instabot

    # filling in saved login details
    MAIN_GUI.instaUsernameInput.setText(INSTA_BOT.config["login"]["insta_username"])
    MAIN_GUI.instaPasswordInput.setText(INSTA_BOT.config["login"]["insta_password"])

    # disabling other functionality until logged in
    disabled_tool_tip = "Log In to Enable!"

    MAIN_GUI.instaHashtagBasedStart.setToolTip(disabled_tool_tip)
    MAIN_GUI.instaHashtagBasedStart.setEnabled(False)

    MAIN_GUI.instaUnfollowStart.setToolTip(disabled_tool_tip)
    MAIN_GUI.instaUnfollowStart.setEnabled(False)

    MAIN_GUI.instaSetWhitelistBtn.setToolTip(disabled_tool_tip)
    MAIN_GUI.instaSetWhitelistBtn.setEnabled(False)

    # hiding the logged in message
    MAIN_GUI.instaLoggedInMessage.setHidden(True)

    # connecting functions to required elements
    MAIN_GUI.instaLoginBtn.clicked.connect(_save_credentials_and_login)


def _set_state_to_logged_in():
    # enabling functionality
    start_tool_tip = "Start the Process!"

    MAIN_GUI.instaHashtagBasedStart.setEnabled(True)
    MAIN_GUI.instaHashtagBasedStart.setToolTip(start_tool_tip)

    MAIN_GUI.instaUnfollowStart.setEnabled(True)
    MAIN_GUI.instaUnfollowStart.setToolTip(start_tool_tip)

    MAIN_GUI.instaSetWhitelistBtn.setEnabled(True)
    MAIN_GUI.instaSetWhitelistBtn.setToolTip(start_tool_tip)

    # displaying the logged in state
    MAIN_GUI.instaLoggedInMessage.setHidden(False)
    MAIN_GUI.instaLoginBtn.setText("Logged In!")


def _save_credentials_and_login():
    # disabling the log in button
    MAIN_GUI.instaLoginBtn.setEnabled(False)
    MAIN_GUI.instaLoginBtn.setText("Logging In!")

    save_credentials = bool(MAIN_GUI.instaLoginsSaveCheckBox.isChecked())
    username = MAIN_GUI.instaUsernameInput.text()
    password = MAIN_GUI.instaPasswordInput.text()

    INSTA_BOT.config["login"]["insta_username"] = username
    INSTA_BOT.config["login"]["insta_password"] = password

    if save_credentials:
        with open(os.path.join("bots/config", "login.yaml"), "w") as f:
            yaml.dump(INSTA_BOT.config["login"], f)
            f.close()

    login_successful = INSTA_BOT.login()
    if login_successful:
        _set_state_to_logged_in()
    else:
        MAIN_GUI.instaLoginBtn.setEnabled(True)
        MAIN_GUI.instaLoginBtn.setText("Try Logging In Again!")
