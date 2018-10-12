import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

import Image2Text

WINDOW_TITLE = 'Image2Text'
APP_ICON_URL = './asset/myicon.ico'


def run_with_titlebar():
    app = QApplication(sys.argv)
    imageFrame = Image2Text.Image2Text()
    imageFrame.setWindowTitle(WINDOW_TITLE)
    imageFrame.setWindowIcon(QIcon(APP_ICON_URL))
    imageFrame.mainwidget.setFocus()
    imageFrame.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    run_with_titlebar()
