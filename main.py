# VERSION=1
# https://github.com/ageorge95/ag95_repo_base

import ctypes
import os
import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (QApplication,
                               QLabel,
                               QMainWindow,
                               QPushButton,
                               QVBoxLayout,
                               QWidget)

APP_NAME = 'Python GUI Base'
APP_ID = 'AG95.PythonGUIBase'  # Windows taskbar identity; rename for a new project
ICON_FILE = 'icon.ico'
VERSION_FILE = 'version.txt'


def get_running_path(relative_path):
    """Return a bundled file's path in both source and PyInstaller builds."""
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def set_windows_app_id():
    """Give the app its own Windows taskbar identity.

    When run as python.exe, Windows groups the window under Python's taskbar
    entry and uses Python's icon. An explicit AppUserModelID makes the taskbar
    use the window icon instead, matching the compiled executable.
    """
    if sys.platform != 'win32':
        return
    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(APP_ID)
    except (AttributeError, OSError):
        pass


def read_version():
    """Return the version from version.txt, or 'dev' if it is missing."""
    try:
        with open(get_running_path(VERSION_FILE), 'r', encoding='utf-8') as file:
            return file.read().strip()
    except OSError:
        return 'dev'


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f'{APP_NAME} v{read_version()}')
        self.resize(900, 600)
        self.setWindowIcon(QIcon(get_running_path(ICON_FILE)))

        self.clicks = 0

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)
        layout.addStretch()

        self.label = QLabel('Hello, PySide6!')
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        self.button = QPushButton('Click me')
        self.button.setFixedWidth(180)
        self.button.clicked.connect(self.on_button_clicked)
        layout.addWidget(self.button, 0, Qt.AlignHCenter)

        layout.addStretch()

    def on_button_clicked(self):
        self.clicks += 1
        self.label.setText(f'Button clicked {self.clicks} time(s).')


def main():
    set_windows_app_id()
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(get_running_path(ICON_FILE)))

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
