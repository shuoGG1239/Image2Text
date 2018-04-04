from PyQt5.QtCore import pyqtSlot, QFileInfo, pyqtSignal, QBuffer, QByteArray, QIODevice
from PyQt5.QtGui import QMovie, QPixmap
from PyQt5.QtWidgets import QWidget, QFileDialog, QLabel
from qss_ui_theme.green_theme import green_decorator

from screen_capture import CaptureScreen
from ui_image2text import Ui_image2textWidget
import ocr_util
import threading


@green_decorator
class Image2Text(QWidget):
    signal_response = pyqtSignal(str)

    def __init__(self):
        QWidget.__init__(self)
        self.ui = Ui_image2textWidget()
        self.ui.setupUi(self)
        self.ui.textEdit.setAcceptDrops(False)
        self.ui.textEdit.setPlaceholderText('将待识别图片拖拽到此处...')
        self.setAcceptDrops(True)
        self.init_loading_gif()
        self.signal_response.connect(self.__slot_http_response)

    def init_loading_gif(self):
        gif = QMovie('loading.gif')
        gif.start()
        self.loadingLabel = QLabel(self)
        self.loadingLabel.setMovie(gif)
        self.loadingLabel.setGeometry(275, 50, self.loadingLabel.width(), 200)
        self.loadingLabel.setVisible(False)

    def job_ocr(self, image_bytes):
        result = ''
        try:
            result = ocr_util.get_ocr_str_from_bytes(image_bytes)
        finally:
            self.signal_response.emit(result)

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

    def run_ocr_async(self, image_bytes):
        self.loadingLabel.setVisible(True)
        threading.Thread(target=self.job_ocr, args=(image_bytes,)).start()

    def pixmap_to_bytes(self, image, image_format='jpg'):
        byte_array = QByteArray()
        buffer = QBuffer(byte_array)
        buffer.open(QIODevice.WriteOnly)
        image.save(buffer, image_format)
        return buffer.data()

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
