import threading

from PyQt5.QtCore import pyqtSlot, QFileInfo, pyqtSignal, QBuffer, QByteArray, QIODevice, QSize
from PyQt5.QtGui import QMovie, QPixmap, QIcon
from PyQt5.QtWidgets import QWidget, QFileDialog, QLabel
from QCandyUi.CandyWindow import colorful

import ocr_util
from screen_capture import CaptureScreen
from triggerKeyboard import key_trigger
from ui_image2text import Ui_image2textWidget

# 全局截屏快捷键
SCREEN_SHOT_SHORTCUT = 'ctrl+shift+alt+f8'

# 资源路径
SCREEN_SHOT_ICON_URL = './asset/scissors.png'
OPEN_FILE_ICON_URL = './asset/file.png'
LOADING_GIF_URL = './asset/loading.gif'


@colorful('blueGreen')
class Image2Text(QWidget):
    signal_response = pyqtSignal(str)

    def __init__(self):
        QWidget.__init__(self)
        self.ui = Ui_image2textWidget()
        self.ui.setupUi(self)
        self.ui.textEdit.setAcceptDrops(False)
        self.ui.textEdit.setPlaceholderText('1.将待识别图片拖拽到此处...\n' + '2.截屏识图快捷键: ' + SCREEN_SHOT_SHORTCUT)
        self.setAcceptDrops(True)
        self.init_loading_gif()
        self.signal_response.connect(self.__slot_http_response)
        self.beautify_button(self.ui.pushButtonOpen, OPEN_FILE_ICON_URL)
        self.beautify_button(self.ui.pushButtonCapture, SCREEN_SHOT_ICON_URL)
        # 异步运行键盘扫描
        threading.Thread(target=self.run_capture_keyscan).start()

    def beautify_button(self, button, image_url):
        """
        美化按键
        :param button:  QPushButton
        :param image_url: str
        :return: None
        """
        button.setText('')
        button.setIcon(QIcon(image_url))
        icon_width = button.height() >> 1
        button.setIconSize(QSize(icon_width, icon_width))
        button.setFlat(True)

    def init_loading_gif(self):
        """
        初始化loading动画
        :return:
        """
        gif = QMovie(LOADING_GIF_URL)
        gif.start()
        x, y = 275, 110
        self.loadingLabel = QLabel(self)
        self.loadingLabel.setMovie(gif)
        self.loadingLabel.adjustSize()
        self.loadingLabel.setGeometry(x, y, self.loadingLabel.width(), self.loadingLabel.height())
        self.loadingLabel.setVisible(False)

    def job_ocr(self, image_bytes):
        result = ''
        try:
            result = ocr_util.get_ocr_str_from_bytes(image_bytes)
        finally:
            self.signal_response.emit(result)

    def run_ocr_async(self, image_bytes):
        self.loadingLabel.setVisible(True)
        threading.Thread(target=self.job_ocr, args=(image_bytes,)).start()

    def pixmap_to_bytes(self, image, image_format='jpg'):
        """
        Pixmap转字节
        :param image: pixmap
        :param image_format: str
        :return: bytes
        """
        byte_array = QByteArray()
        buffer = QBuffer(byte_array)
        buffer.open(QIODevice.WriteOnly)
        image.save(buffer, image_format)
        return buffer.data()

    @key_trigger(SCREEN_SHOT_SHORTCUT, False)
    def run_capture_keyscan(self):
        """
        快捷键触发截屏信号
        :return:
        """
        self.ui.pushButtonCapture.clicked.emit()

    @pyqtSlot()
    def on_pushButtonOpen_clicked(self):
        img_full_path = QFileDialog.getOpenFileName()[0]
        if img_full_path is None or img_full_path == '':
            return
        with open(img_full_path, 'rb') as fp:
            file_bytes = fp.read()
        self.run_ocr_async(file_bytes)

    @pyqtSlot()
    def on_pushButtonCapture_clicked(self):
        self.capture = CaptureScreen()
        self.capture.signal_complete_capture.connect(self.__slot_screen_capture)

    @pyqtSlot(str)
    def __slot_http_response(self, result):
        self.ui.textEdit.setText(result)
        self.loadingLabel.setVisible(False)

    @pyqtSlot(QPixmap)
    def __slot_screen_capture(self, image):
        image_bytes = self.pixmap_to_bytes(image)
        if image_bytes is None or len(image_bytes) == 0:
            return
        self.run_ocr_async(image_bytes)

    def dragEnterEvent(self, event):
        if (event.mimeData().hasUrls()):
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        if (event.mimeData().hasUrls()):
            event.acceptProposedAction()

    def dropEvent(self, event):
        if (event.mimeData().hasUrls()):
            urlList = event.mimeData().urls()
            fileInfo = QFileInfo(urlList[0].toLocalFile())
            img_full_path = fileInfo.filePath()
            with open(img_full_path, 'rb') as fp:
                file_bytes = fp.read()
            self.run_ocr_async(file_bytes)
            event.acceptProposedAction()
