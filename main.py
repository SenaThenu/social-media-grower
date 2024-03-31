import sys
from PyQt6.QtWidgets import QApplication

import gui
from bots.config import load_config
from bots.instagram import InstagramBot

config = load_config()
insta_bot = InstagramBot(config)

if __name__ == "__main__":
    # configuring lower level stuff
    app = QApplication(sys.argv)

    # binding the ui
    main_gui = gui.create_gui(config, insta_bot)

    # showing it to the users
    main_gui.show()

    # closing the browser window when quitting
    app.aboutToQuit.connect(insta_bot.quit)
    sys.exit(app.exec())
