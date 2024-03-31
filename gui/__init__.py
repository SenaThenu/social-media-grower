import sys
from os import path
import yaml
from functools import partial

# PyQt imports
from PyQt6 import QtGui, QtWidgets

# importing the prebuilt UI designs (using QtDesigner)
from ._main_ui import Ui_MainWindow
from ._list_editor_ui import Ui_listEdit
from ._preferences_ui import Ui_Preferences

# importing the functional UIs in modules of the current directory
from .insta_ui import setup_instagram_ui

MAIN_GUI = Ui_MainWindow()
HASHTAGS_GUI = Ui_listEdit()
WHITELIST_GUI = Ui_listEdit()
PREFERENCES_GUI = Ui_Preferences()


# Configurations Object (automatically filled when create_functional_gui is called)
CONFIG = None

# Logo (by going to the parent directory!)
LOGO_PATH = path.abspath(
    path.join(path.dirname(path.dirname(__file__)), "readme_assets/logo.png")
)

# Styles
ERROR_STYLE = "color: red;\nfont-weight: bold;"
SUCCESS_STYLE = "color: green;\nfont-weight: bold;"


def create_gui(config: dict, insta_bot: object) -> object:
    """
    Creates and returns a functional main GUI

    Args:
        config (dict): global configuration folder
        insta_bot (object): instance of the InstagramBot class

    Returns:
        object: main window of the functional GUI
    """
    # making configurations globally accessible
    global CONFIG
    CONFIG = config  # only referencing the dict (so, automatically updated)

    # binding the qt-generated UI
    main_window = QtWidgets.QMainWindow()
    MAIN_GUI.setupUi(main_window)

    # attaching the styles to the MAIN_GUI
    MAIN_GUI.error_style = ERROR_STYLE
    MAIN_GUI.success_style = SUCCESS_STYLE

    # making UI static elements functional
    _setup_menubar()
    _map_interface_btns_with_menu_actions()
    setup_instagram_ui(MAIN_GUI, insta_bot)

    # basic main window configurations
    main_window.setWindowIcon(QtGui.QIcon(LOGO_PATH))
    return main_window


def snake_to_camel(snake_case_str: str) -> str:
    """
    Converts snake case to came case

    Args:
        snake_case_str (str): the string to be converted to camel case

    Returns:
        str: camel case converted string
    """
    parts = snake_case_str.split("_")
    camel_case_str = parts[0] + "".join(word.title() for word in parts[1:])
    return camel_case_str


def _setup_menubar():
    """
    Makes the menu bar of the main window functional
    """
    # File Menu
    MAIN_GUI.actionExit.triggered.connect(sys.exit)
    MAIN_GUI.actionOpenInstaBot.triggered.connect(
        lambda: MAIN_GUI.mainTabsWidget.setCurrentIndex(0)
    )

    # Edit Menu
    MAIN_GUI.actionPreferences.triggered.connect(_open_preferences_editor)
    MAIN_GUI.actionHashtags.triggered.connect(_open_hashtags_editor)
    MAIN_GUI.actionWhitelistInstaBot.triggered.connect(
        partial(_open_whitelist_editor, "instagram")
    )


def _map_interface_btns_with_menu_actions():
    """
    Maps menu bar actions with buttons in the interface
    """
    # edit hashtags
    MAIN_GUI.instaEditHashtagsBtn.clicked.connect(_open_hashtags_editor)


def _setup_preferences_editor():
    """
    Makes the preferences editor functional
    """
    numbers_only = ["accepted_follow_ratio", "base_waiting_time", "unfollow_gap"]
    bool_only = ["automatic_muting", "follow_private_accounts", "only_follow"]

    def _save_preferences():
        # updating the user_preferences using the input values
        for preference in CONFIG["user_preferences"].keys():
            if preference in numbers_only:
                input_field = PREFERENCES_GUI.__getattribute__(
                    f"{snake_to_camel(preference)}Input"
                )
                CONFIG["user_preferences"][preference] = float(input_field.text())
            elif preference in bool_only:
                checkbox = PREFERENCES_GUI.__getattribute__(
                    f"{snake_to_camel(preference)}Checkbox"
                )
                CONFIG["user_preferences"][preference] = bool(checkbox.isChecked())
            else:
                pass

        # saving
        with open(
            path.abspath(
                # accessing the parent directory through 2 dirnames
                path.join(
                    path.dirname(path.dirname(__file__)),
                    "bots/config/user_preferences.yaml",
                )
            ),
            "w",
        ) as f:
            yaml.dump(CONFIG["user_preferences"], f)
            f.close()

        PREFERENCES_GUI.savedMessageLabel.setHidden(False)

    # showing the user current values!
    for preference in CONFIG["user_preferences"].keys():
        if preference in numbers_only:
            input_field = PREFERENCES_GUI.__getattribute__(
                f"{snake_to_camel(preference)}Input"
            )
            # number-only validator with limits
            if preference == "base_waiting_time":
                input_field.setValidator(QtGui.QDoubleValidator(5.0, 100.0, 2))
            else:
                input_field.setValidator(QtGui.QDoubleValidator(0.0, 100.0, 2))

            # setting the current value
            input_field.setText(str(CONFIG["user_preferences"][preference]))
        elif preference in bool_only:
            checkbox = PREFERENCES_GUI.__getattribute__(
                f"{snake_to_camel(preference)}Checkbox"
            )
            checkbox.setChecked(CONFIG["user_preferences"][preference])
        else:
            pass

    PREFERENCES_GUI.savedMessageLabel.setHidden(True)
    PREFERENCES_GUI.saveBtn.clicked.connect(_save_preferences)


def _open_preferences_editor():
    """
    Creates the interface for the user to change their preferences
    """
    # binding the qt-generated UI
    preferences_dialog = QtWidgets.QDialog()
    PREFERENCES_GUI.setupUi(preferences_dialog)

    # configuring UI elements
    _setup_preferences_editor()
    preferences_dialog.setWindowTitle("Preferences Editor")
    preferences_dialog.setWindowIcon(QtGui.QIcon(LOGO_PATH))

    # displaying the UI
    preferences_dialog.exec()
    preferences_dialog.show()


def _setup_list_editor(
    gui: object,
    main_dict: list,
    filename_to_update: str,
    subindex: str,
):
    """
    Sets up the list editor dialogue so that users can manipulate items in lists (e.g. whitelist, hashtags)

    Args:
        gui (object)
        main_dict (dict): dict containing items
        filename_to_update (str): name of the file that should be updated in the config folder (with extension: yaml)
        subindex (str): the keyword to index the main_dict
    """

    focus_list = main_dict[subindex]

    def _update_list():
        with open(
            path.abspath(
                # accessing the parent directory through 2 dirnames
                path.join(
                    path.dirname(path.dirname(__file__)),
                    f"bots/config/{filename_to_update}",
                )
            ),
            "w",
        ) as f:
            yaml.dump(main_dict, f)
            f.close()

    def _add_item():
        item_input = gui.itemInputField.text().lower()
        if item_input and item_input not in focus_list:
            focus_list.append(item_input)
            _update_list()
            gui.itemsList.addItem(item_input)

    def _delete_selected_item():
        current_row = gui.itemsList.currentRow()
        if current_row >= 0:
            focus_list.pop(current_row)
            _update_list()
            gui.itemsList.takeItem(current_row)

    for hashtag in focus_list:
        gui.itemsList.addItem(hashtag)

    gui.addBtn.clicked.connect(_add_item)
    gui.deleteBtn.clicked.connect(_delete_selected_item)


def _open_hashtags_editor():
    """
    Creates the interface for the users to edit hashtags
    """
    # binding the qt-generated UI
    hashtag_dialog = QtWidgets.QDialog()
    HASHTAGS_GUI.setupUi(hashtag_dialog)

    # configuring UI elements
    _setup_list_editor(
        HASHTAGS_GUI, CONFIG["user_preferences"], "user_preferences.yaml", "hashtags"
    )
    hashtag_dialog.setWindowTitle("Hashtags Editor")
    hashtag_dialog.setWindowIcon(QtGui.QIcon(LOGO_PATH))

    # displaying the UI
    hashtag_dialog.exec()
    hashtag_dialog.show()


def _open_whitelist_editor(platform: str):
    """
    Creates the interface for the users to edit the whitelist

    Args:
        platform (str): name of the social media platform
    """
    # binding the qt-generated UI
    whitelist_dialog = QtWidgets.QDialog()
    WHITELIST_GUI.setupUi(whitelist_dialog)

    # configuring UI elements
    _setup_list_editor(WHITELIST_GUI, CONFIG["whitelist"], "whitelist.yaml", platform)
    whitelist_dialog.setWindowTitle("Whitelist Editor")
    whitelist_dialog.setWindowIcon(QtGui.QIcon(LOGO_PATH))

    # displaying the UI
    whitelist_dialog.exec()
    whitelist_dialog.show()
