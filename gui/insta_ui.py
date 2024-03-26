import os
import yaml
from PyQt6.QtCore import QThread, pyqtSignal, pyqtSlot

LOGGED_IN = False

# these will be automatically updated when setup_instagram_ui is called
MAIN_GUI = None
INSTA_BOT = None

# to keep track of stuff
FUNCTIONS_SUPPORTED = ["HashtagBased", "Unfollow", "SetWhitelist"]  # title case (PyQt)
CURRENT_PROCESS = None  # can be hashtag_based, unfollow, set_whitelist


# defining a flag class that's used to make the cancel button functional
class CancelFlag:
    def __init__(self):
        self.flag = False

    def set(self):
        self.flag = True

    def check(self):
        return self.flag


class LoginThread(QThread):
    def __init__(self, username, password, save_credentials):
        super().__init__()
        self.username = username
        self.password = password
        self.save_credentials = save_credentials

        self.finished.connect(self.deleteLater)

    def _set_login_btn_to_retry(self, error_message):
        # renaming the login button
        MAIN_GUI.instaLogInBtn.setEnabled(True)
        MAIN_GUI.instaLogInBtn.setText("Try Logging In Again!")

        # displaying the error message
        MAIN_GUI.instaLogInMessage.setText(error_message)
        MAIN_GUI.instaLogInMessage.setStyleSheet(MAIN_GUI.error_style)
        MAIN_GUI.instaLogInMessage.setHidden(False)

    def run(self):
        # checking whether they are empty
        if self.username and self.password:
            try:
                # making sure there's n key in the configs to save login details
                INSTA_BOT.config["login"]
            except:
                # if not, we are gonna create a new key!
                INSTA_BOT.config["login"] = {}
            INSTA_BOT.config["login"]["insta_username"] = self.username
            INSTA_BOT.config["login"]["insta_password"] = self.password

            if self.save_credentials:
                with open(os.path.join("bots/config", "login.yaml"), "w") as f:
                    yaml.dump(INSTA_BOT.config["login"], f)
                    f.close()

            # starting the logging process
            login_successful = INSTA_BOT.login()

            if login_successful:
                _set_state_to_logged_in()
            else:
                self._set_login_btn_to_retry(
                    "⚠️Check whether your credentials are valid! \nIf the error persists, try changing Base Waiting Time (in Preferences) or updating the application!"
                )
        else:
            self._set_login_btn_to_retry("⚠️Instagram login details are missing!")


# this is used to concurrently run the browser automation processes
class WorkerThread(QThread):
    update_progress = pyqtSignal(int)  # defining inside __init__() results in an error!

    def __init__(self):
        super().__init__()

    def configure_insta_func(
        self, insta_callback: object, callback_args_dict: dict = None
    ):
        self.insta_callback = insta_callback
        self.callback_args = callback_args_dict

    def _display_message(self, message: str, message_type: str):
        MAIN_GUI.__getattribute__(f"insta{CURRENT_PROCESS}Message").setText(message)
        if message_type == "success":
            MAIN_GUI.__getattribute__(f"insta{CURRENT_PROCESS}Message").setStyleSheet(
                MAIN_GUI.success_style
            )
        else:
            MAIN_GUI.__getattribute__(f"insta{CURRENT_PROCESS}Message").setStyleSheet(
                MAIN_GUI.error_style
            )
        MAIN_GUI.__getattribute__(f"insta{CURRENT_PROCESS}Message").setHidden(False)

    def run(self):
        if self.callback_args:
            self.insta_callback(**self.callback_args)
        else:
            if self.insta_callback:
                try:
                    self.insta_callback()
                    self.update_progress.emit(100)
                    self._display_message("🍀Success!", "success")
                except:
                    self._display_message(
                        "⚠️Error Occurred :(\nMake sure you have the latest version and haven't accidentally closed the browser window (if you have, reopen the app)!",
                        "error",
                    )
            else:
                raise (
                    "You have to call the configure_insta_func function before starting the thread!"
                )
        _set_state_to_logged_in()
        # updating the tabs since we have consumed some of the quota
        _set_up_instabot_function_tabs()


def setup_instagram_ui(main_gui: object, instabot: object):
    """
    Sets up the whole UI to interact with the instagram bot.

    Args:
        main_gui (object): an instance of the main window where you can find the instagram bot tab
        instabot (object): instabot object instance
    """
    global MAIN_GUI, INSTA_BOT
    MAIN_GUI = main_gui
    INSTA_BOT = instabot

    # filling in saved login details
    try:
        MAIN_GUI.instaUsernameInput.setText(INSTA_BOT.config["login"]["insta_username"])
        MAIN_GUI.instaPasswordInput.setText(INSTA_BOT.config["login"]["insta_password"])
    except:
        pass

    disabled_tool_tip = "Log In to Enable!"
    cancel_btn_tooltip = "Start a process to cancel"

    # disabling the access to other functionality until logged in
    for func in FUNCTIONS_SUPPORTED:
        # disabling the start buttons
        MAIN_GUI.__getattribute__(f"insta{func}Start").setToolTip(disabled_tool_tip)
        MAIN_GUI.__getattribute__(f"insta{func}Start").setEnabled(False)

        # disabling the cancel buttons
        MAIN_GUI.__getattribute__(f"insta{func}Cancel").setToolTip(cancel_btn_tooltip)
        MAIN_GUI.__getattribute__(f"insta{func}Cancel").setEnabled(False)

        # hiding the progress bars
        MAIN_GUI.__getattribute__(f"insta{func}ProgressBar").setHidden(True)

        # hiding the message
        MAIN_GUI.__getattribute__(f"insta{func}Message").setHidden(True)

    # hiding the logged in message
    MAIN_GUI.instaLogInMessage.setHidden(True)

    # connecting functions to required elements
    MAIN_GUI.instaLogInBtn.clicked.connect(_save_credentials_and_login)

    # configuring the instabot functionality
    _set_up_instabot_function_tabs()


def _save_credentials_and_login():
    """
    Accepts the user inputs and login in them
    """
    # disabling the log in button
    MAIN_GUI.instaLogInBtn.setEnabled(False)
    MAIN_GUI.instaLogInBtn.setText("Logging In!")
    MAIN_GUI.instaLogInMessage.setHidden(True)

    # accessing form information
    save_credentials = bool(MAIN_GUI.instaLoginsSaveCheckBox.isChecked())
    username = MAIN_GUI.instaUsernameInput.text()
    password = MAIN_GUI.instaPasswordInput.text()

    MAIN_GUI.login_thread = LoginThread(username, password, save_credentials)
    MAIN_GUI.login_thread.start()


def _set_up_instabot_function_tabs():
    _set_up_hashtag_based_tab()


def _set_up_hashtag_based_tab():
    n_follows_left, n_likes_left = _get_remaining_actions()

    # limits for the input values
    if n_follows_left > 0:
        n_follows_min = len(INSTA_BOT.config["user_preferences"]["hashtags"])
        n_follows_max = n_follows_left
    else:
        n_follows_min = 0
        n_follows_max = 0

    if n_likes_left > 0:
        n_likes_min = len(INSTA_BOT.config["user_preferences"]["hashtags"])
        n_likes_max = n_likes_left
    else:
        n_likes_min = 0
        n_likes_max = 0

    # n_follows input handling
    MAIN_GUI.nInstaFollowsSlider.setMaximum(n_follows_max)
    MAIN_GUI.nInstaFollowsSlider.setMinimum(n_follows_min)
    MAIN_GUI.nInstaFollowsSpinBox.setMaximum(n_follows_max)
    MAIN_GUI.nInstaFollowsSpinBox.setMinimum(n_follows_min)

    # n_likes input handling
    MAIN_GUI.nInstaLikesSlider.setMaximum(n_likes_max)
    MAIN_GUI.nInstaLikesSlider.setMinimum(n_likes_min)
    MAIN_GUI.nInstaLikesSpinBox.setMaximum(n_likes_max)
    MAIN_GUI.nInstaLikesSpinBox.setMinimum(n_likes_min)

    def _execute():
        n_follows_left, n_likes_left = _get_remaining_actions()
        n_follows = MAIN_GUI.nInstaFollowsSpinBox.value()
        n_likes = MAIN_GUI.nInstaLikesSpinBox.value()

        if n_follows_left or n_likes_left:
            # if there are remaining actions,
            global CURRENT_PROCESS
            CURRENT_PROCESS = "HashtagBased"

            # unhiding the progress bar
            MAIN_GUI.instaHashtagBasedProgressBar.setValue(0)
            MAIN_GUI.instaHashtagBasedProgressBar.setHidden(False)

            # executing the function in a separate thread
            MAIN_GUI.worker_thread = WorkerThread()
            MAIN_GUI.worker_thread.update_progress.connect(
                MAIN_GUI.instaHashtagBasedProgressBar.setValue
            )

            MAIN_GUI.cancel_flag = CancelFlag()

            MAIN_GUI.worker_thread.configure_insta_func(
                INSTA_BOT.like_and_follow_by_hashtag,
                {
                    "n_likes": n_likes,
                    "n_follows": n_follows,
                    "update_progress_bar": MAIN_GUI.worker_thread.update_progress,
                    "cancel_flag": MAIN_GUI.cancel_flag,
                },
            )

            MAIN_GUI.instaHashtagBasedCancel.clicked.connect(MAIN_GUI.cancel_flag.set)
            _set_state_to_in_progress()
            MAIN_GUI.worker_thread.start()
        else:
            MAIN_GUI.instaLogInMessage.setText(
                "😢Instagram has limits on the number of people you can follow/unfollow and the number of posts you can like :("
            )
            MAIN_GUI.instaLogInMessage.setStyleSheet(MAIN_GUI.error_style)

    MAIN_GUI.instaHashtagBasedStart.clicked.connect(_execute)


def _get_remaining_actions() -> tuple:
    """
    Returns the remaining number of actions based on how many has performed from the quota.

    Returns:
        tuple: (n_follows_left, n_likes_left)
    """
    # remaining actions based on the quotes
    n_follows_left = (
        INSTA_BOT.config["restrictions"]["instagram"]["n_follows"]
        - INSTA_BOT._today_actions["n_follows"]
    )
    n_likes_left = (
        INSTA_BOT.config["restrictions"]["instagram"]["n_likes"]
        - INSTA_BOT._today_actions["n_likes"]
    )
    return n_follows_left, n_likes_left


def _set_state_to_in_progress():
    """
    Configures the UI so that the user can only cancel the current process.
    """
    for func in FUNCTIONS_SUPPORTED:
        if func == CURRENT_PROCESS:
            MAIN_GUI.__getattribute__(f"insta{func}Cancel").setEnabled(True)
            MAIN_GUI.__getattribute__(f"insta{func}Cancel").setToolTip(
                "Cancel Process!"
            )

            MAIN_GUI.__getattribute__(f"insta{func}Start").setEnabled(False)
            MAIN_GUI.__getattribute__(f"insta{func}Start").setText("Started")
            MAIN_GUI.__getattribute__(f"insta{func}Start").setToolTip(
                "Already Started!"
            )

            MAIN_GUI.__getattribute__(f"insta{func}Message").setHidden(True)

            MAIN_GUI.__getattribute__(f"insta{func}ProgressBar").setHidden(False)
        else:
            MAIN_GUI.__getattribute__(f"insta{func}Cancel").setEnabled(False)
            MAIN_GUI.__getattribute__(f"insta{func}Start").setEnabled(False)


def _set_state_to_logged_in():
    # resetting the current_process global var
    global CURRENT_PROCESS
    CURRENT_PROCESS = None

    # enabling functionality
    start_tool_tip = "Start the Process!"
    cancel_tool_tip = "Start a process to cancel"

    for func in FUNCTIONS_SUPPORTED:
        # start button
        MAIN_GUI.__getattribute__(f"insta{func}Start").setEnabled(True)
        MAIN_GUI.__getattribute__(f"insta{func}Start").setText("Start")
        MAIN_GUI.__getattribute__(f"insta{func}Start").setToolTip(start_tool_tip)

        # cancel button
        MAIN_GUI.__getattribute__(f"insta{func}Cancel").setEnabled(False)
        MAIN_GUI.__getattribute__(f"insta{func}Cancel").setText("Cancel")
        MAIN_GUI.__getattribute__(f"insta{func}Cancel").setToolTip(cancel_tool_tip)

        # progress bar
        MAIN_GUI.__getattribute__(f"insta{func}ProgressBar").setHidden(True)

    # displaying the logged in state
    MAIN_GUI.instaLogInBtn.setText("Logged In!")

    MAIN_GUI.instaLogInMessage.setHidden(False)
    MAIN_GUI.instaLogInMessage.setText("👍Logged In!")
    MAIN_GUI.instaLogInMessage.setStyleSheet(MAIN_GUI.success_style)
