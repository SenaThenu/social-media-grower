import yaml
from os import path
from functools import partial
from PyQt6.QtCore import QThread, pyqtSignal
from notifypy import Notify

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
                # making sure there's a key in the configs to save login details
                if type(INSTA_BOT.config["login"]) == dict:
                    pass
                else:
                    INSTA_BOT.config["login"] = {}
            except:
                # if not, we are gonna create a new key!
                INSTA_BOT.config["login"] = {}
            INSTA_BOT.config["login"]["insta_username"] = self.username
            INSTA_BOT.config["login"]["insta_password"] = self.password

            if self.save_credentials:
                with open(
                    path.abspath(
                        # accessing the parent directory through 2 dirnames
                        path.join(
                            path.dirname(path.dirname(__file__)),
                            "bots/config/login.yaml",
                        )
                    ),
                    "w",
                ) as f:
                    yaml.dump(INSTA_BOT.config["login"], f)
                    f.close()

            try:
                # starting the logging process
                login_successful = INSTA_BOT.login()

                if login_successful:
                    _set_state_to_logged_in()
                    logged_in_notification = Notify()
                    logged_in_notification.title = "Successfully Logged In!"
                    logged_in_notification.message = "You can now perform any action!"
                    logged_in_notification.send()
                else:
                    self._set_login_btn_to_retry(
                        "⚠️Check whether your credentials are valid! \nIf the error persists, try changing Base Waiting Time (in Preferences) or updating the application!"
                    )
            except:
                self._set_login_btn_to_retry(
                    "⚠️Oops! You closed the browser window! \nIf the error persists, make sure you have Chrome installed on your device!"
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
        try:
            if self.callback_args:
                self.insta_callback(**self.callback_args)
            else:
                if self.insta_callback:
                    self.insta_callback()
                else:
                    raise (
                        "You have to call the configure_insta_func function before starting the thread!"
                    )

            self.update_progress.emit(100)
            self._display_message("🍀Success!", "success")
            success_notification = Notify()
            success_notification.title = "Successfully Completed the Task!"
            success_notification.message = "Why not give a go at another one?"
            success_notification.send()
        except:
            self._display_message(
                "⚠️Error Occurred :(\nPossible Reasons:\n1. You've closed or interacted with the program's browser window (if you have, reopen the app)\n2. You haven't specified the hashtags (in hashtag based actions)\n3. You don't have the latest version",
                "error",
            )
            error_notification = Notify()
            error_notification.title = "An Error Occurred!"
            error_notification.message = (
                "Have a look at the possible reasons in the interface!"
            )
            error_notification.send()

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
    _set_up_unfollow_tab()
    _set_up_whitelist_tab()


def _set_up_hashtag_based_tab():
    """
    Makes the hashtag based liking/following tab functional
    """
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
    # the step should be equal to the number of hashtags (because actions are divided into them)
    if n_follows_min:
        MAIN_GUI.nInstaFollowsSlider.setSingleStep(n_follows_min)
        MAIN_GUI.nInstaFollowsSlider.setPageStep(n_follows_min)
        MAIN_GUI.nInstaFollowsSpinBox.setSingleStep(n_follows_min)

    # n_likes input handling
    MAIN_GUI.nInstaLikesSlider.setMaximum(n_likes_max)
    MAIN_GUI.nInstaLikesSlider.setMinimum(n_likes_min)
    MAIN_GUI.nInstaLikesSpinBox.setMaximum(n_likes_max)
    MAIN_GUI.nInstaLikesSpinBox.setMinimum(n_likes_min)
    # the step should be equal to the number of hashtags (because actions are divided into them)
    if n_likes_min:
        MAIN_GUI.nInstaLikesSlider.setSingleStep(n_likes_min)
        MAIN_GUI.nInstaLikesSlider.setPageStep(n_likes_min)
        MAIN_GUI.nInstaLikesSpinBox.setSingleStep(n_likes_min)

    def _execute():
        n_follows_left, n_likes_left = _get_remaining_actions()
        n_follows = MAIN_GUI.nInstaFollowsSpinBox.value()
        n_likes = MAIN_GUI.nInstaLikesSpinBox.value()

        # if there are remaining actions,
        if n_follows_left or n_likes_left:
            _execute_action(
                "HashtagBased",
                INSTA_BOT.like_and_follow_by_hashtag,
                {
                    "n_likes": n_likes,
                    "n_follows": n_follows,
                },
            )
        else:
            MAIN_GUI.instaHashtagBasedMessage.setText(
                "😢Instagram has limits on the number of people you can follow and the posts you can like :("
            )
            MAIN_GUI.instaHashtagBasedMessage.setStyleSheet(MAIN_GUI.error_style)

    MAIN_GUI.instaHashtagBasedStart.clicked.connect(_execute)


def _set_up_unfollow_tab():
    """
    Makes the user unfollowing tab functional
    """
    n_unfollows_left, n_likes_left = _get_remaining_actions()

    # limits for the input values
    if n_unfollows_left > 0:
        n_unfollows_min = 1
        n_unfollows_max = n_unfollows_left
    else:
        n_unfollows_max = 0
        n_unfollows_min = 0

    # n_follows input handling
    MAIN_GUI.nInstaUnfollowsSlider.setMaximum(n_unfollows_max)
    MAIN_GUI.nInstaUnfollowsSlider.setMinimum(n_unfollows_min)
    MAIN_GUI.nInstaUnfollowsSpinBox.setMaximum(n_unfollows_max)
    MAIN_GUI.nInstaUnfollowsSpinBox.setMinimum(n_unfollows_min)
    # the step should be equal to the number of hashtags (because actions are divided into them)
    if n_unfollows_min:
        MAIN_GUI.nInstaUnfollowsSlider.setSingleStep(n_unfollows_min)
        MAIN_GUI.nInstaUnfollowsSlider.setPageStep(n_unfollows_min)
        MAIN_GUI.nInstaUnfollowsSpinBox.setSingleStep(n_unfollows_min)

    def _execute():
        n_unfollows_left, n_likes_left = _get_remaining_actions()
        n_unfollows = MAIN_GUI.nInstaUnfollowsSpinBox.value()

        # mode_indices: 0th = dynamic & 1st = unfollow all
        mode_index = MAIN_GUI.instaUnfollowModeComboBox.currentIndex()
        mode = "dynamic" if mode_index == 0 else "all"

        if n_unfollows_left:
            _execute_action(
                "Unfollow",
                INSTA_BOT.unfollow_users,
                {
                    "n": n_unfollows,
                    "mode": mode,
                },
            )
        else:
            MAIN_GUI.instaUnfollowMessage.setText(
                "😢Instagram has limits on the number of people you can unfollow :("
            )
            MAIN_GUI.setStyleSheet(MAIN_GUI.error_style)

    MAIN_GUI.instaUnfollowStart.clicked.connect(_execute)


def _set_up_whitelist_tab():
    """
    Makes the set_whitelist_following_users tab functional.
    """
    # passing the arguments for _execute_action using functools.partial
    MAIN_GUI.instaSetWhitelistStart.clicked.connect(
        partial(
            _execute_action, "SetWhitelist", INSTA_BOT.whitelist_following_users, {}
        )
    )


def _execute_action(process_name: str, insta_func: object, insta_func_args_dict: dict):
    """
    Executes the follow/unfollow/like actions through the given insta_func

    Args:
        process_name (str): the name of the process (either Unfollow or HashtagBased)
        insta_func (object): the function that executes the action
        insta_func_args_dict (dict): arguments for the function (don't include the cancel flag and update_progress bar signals since they are automatically added)
    """
    global CURRENT_PROCESS
    CURRENT_PROCESS = process_name

    # unhiding the progress bar
    MAIN_GUI.__getattribute__(f"insta{CURRENT_PROCESS}ProgressBar").setValue(0)
    MAIN_GUI.__getattribute__(f"insta{CURRENT_PROCESS}ProgressBar").setHidden(False)

    # executing the function in a separate thread
    MAIN_GUI.worker_thread = WorkerThread()
    MAIN_GUI.worker_thread.update_progress.connect(
        MAIN_GUI.__getattribute__(f"insta{CURRENT_PROCESS}ProgressBar").setValue
    )

    MAIN_GUI.cancel_flag = CancelFlag()

    # adding default args to the dictionary
    insta_func_args_dict["update_progress_bar"] = MAIN_GUI.worker_thread.update_progress
    insta_func_args_dict["cancel_flag"] = MAIN_GUI.cancel_flag

    MAIN_GUI.worker_thread.configure_insta_func(
        insta_func,
        insta_func_args_dict,
    )

    MAIN_GUI.instaHashtagBasedCancel.clicked.connect(MAIN_GUI.cancel_flag.set)
    _set_state_to_in_progress()
    MAIN_GUI.worker_thread.start()


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
        # custom start button texts
        if func == "SetWhitelist":
            MAIN_GUI.__getattribute__(f"insta{func}Start").setText(
                "Whitelist all the users you follow right now!"
            )

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
