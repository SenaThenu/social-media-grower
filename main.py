import sys
from bots.config import load_config
from PyQt6.QtWidgets import QApplication, QMainWindow
import gui

config = load_config()

if __name__ == "__main__":
    # configuring lower level stuff
    app = QApplication(sys.argv)

    # binding the ui
    main_gui = gui.create_gui(config)

    # showing it to the users
    main_gui.show()
    sys.exit(app.exec())
