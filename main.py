import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from screen_capture import CaptureScreen

import Image2Text

WINDOW_TITLE = 'Image2Text'


def run_with_titlebar():
    app = QApplication(sys.argv)
    imgeFrame = Image2Text.Image2Text()
    imgeFrame.setWindowTitle(WINDOW_TITLE)
    imgeFrame.setWindowIcon(QIcon('myicon.ico'))
    imgeFrame.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    run_with_titlebar()
