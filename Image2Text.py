from PyQt5.QtCore import pyqtSlot, QFileInfo, pyqtSignal
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QWidget, QFileDialog, QLabel
from qss_ui_theme.green_theme import green_decorator

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

    def get_ocr_str(self, file_path):
        return ocr_util.get_ocr_str(file_path)

    def job_ocr(self, img_path):
        result = self.get_ocr_str(img_path)
        self.signal_response.emit(result)

    @pyqtSlot()
    def on_pushButtonOpen_clicked(self):
        img_full_path = QFileDialog.getOpenFileName()[0]
        if img_full_path is None or img_full_path == '':
            return
        self.loadingLabel.setVisible(True)
        threading.Thread(target=self.job_ocr, args=(img_full_path,)).start()

    @pyqtSlot(str)
    def __slot_http_response(self, result):
        self.ui.textEdit.setText(result)
        self.loadingLabel.setVisible(False)

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
            self.loadingLabel.setVisible(True)
            threading.Thread(target=self.job_ocr, args=(img_full_path,)).start()
            event.acceptProposedAction()
