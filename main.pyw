from PyQt6.QtGui import *
from PyQt6.QtGui import QMouseEvent
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import downloader
import sys

import time

DEFAULT_SAVE_PATH = "./downloads"
DEFAULT_TYPE = "video" # TODO move this over to a number or smth ( do enums exist in python ?? ) as using strings for this is bad 
DEFAULT_QUALITY = "best" # TODO save as above

# i fogot how to codein p ython so here


class DownloadInformation():
    def __init__(self):
        self.progress = 0
        self.started = False

    def isFinished(self):
        return self.progress == 100
    
    def updateFromData(self, data):
        print(self.progress)

        if (data['status'] == 'finished'):
            self.progress = 100
            return

        elapsed = data['elapsed']
        eta = data['eta']

        if eta == None:
            return

        if eta == 0:
            self.progress = 0
            return

        self.progress = (elapsed / (elapsed + eta)) * 100

        if (self.progress > 0 and not self.started):
            self.started = True

class EnqueuedDownload():
    def __init__(self, url: str, save_path: str = DEFAULT_SAVE_PATH, type: str = DEFAULT_TYPE, quality: str = DEFAULT_QUALITY):
        self.url = url
        self.save_path = save_path
        self.type = type
        self.quality = quality
        self.info = DownloadInformation()
        self.worker = None

    def getWorker(self):
        if (self.worker is None):
            self.worker = DownloadWorker(self)

        return self.worker

    def isFinished(self):
        return self.info.isFinished()
    def hasStarted(self):
        return self.info.started

    def downloadHook(self, data):
        if (data['status'] == 'error'):
            print("Error! - Abandoning download")
            self.info.progress = 100
            return

        self.info.updateFromData(data)

    def download(self):
        """ Only call this in a separate thread or the window will freeze, use the DownloadWorker """
        downloader.download(self.url, self.save_path, self.type, self.quality, self.downloadHook) 
        self.info.started = True

class DownloadQueue():
    def __init__(self):
        self.queue = []
        self.threadpool = QThreadPool()

    # i forot why i made a queue system, its useless, im not going to implement playlists. FUck meeeeeee

    def queueIsEmpty(self):
        return len(self.queue) == 0
    def hasNextInQueue(self):
        return len(self.queue) > 0
    
    def getCurrentDownload(self) -> EnqueuedDownload:
        if self.queueIsEmpty():
            print("No download in queue!")
            return None
        return self.queue[0]
    
    def addToQueue(self, download: EnqueuedDownload):
        self.queue.append(download)

    def tick(self):
        if (self.queueIsEmpty()): return

        current = self.getCurrentDownload()

        if (not current.hasStarted()):
            self.threadpool.start(current.getWorker())
            return
        
        if (current.isFinished()):
            self.queue.pop(0)
            return

class DownloadWorker(QRunnable):
    def __init__(self, download : EnqueuedDownload):
        super(DownloadWorker, self).__init__()
        self.download = download

    def getDownload(self) -> EnqueuedDownload:
        return self.download

    @pyqtSlot()
    def run(self):
        self.getDownload().download()

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.queue = DownloadQueue()

        self.setWindowTitle("YTDL")
        self.setMinimumWidth(200)
        # self.setMinimumHeight(250)

        layout = QVBoxLayout()

        w = QWidget()
        w.setLayout(layout)

        self.setCentralWidget(w)

        self.url = QLineEdit()
        self.url.setFixedWidth(150)
        layout.addWidget(self.url, alignment= Qt.AlignmentFlag.AlignCenter)

        self.progress = QProgressBar()
        self.progress.setMaximum(100)
        self.progress.setMinimum(0)
        self.progress.setFixedWidth(150)
        layout.addWidget(self.progress, alignment=Qt.AlignmentFlag.AlignCenter)

        self.save_path = QLineEdit()
        self.save_path.setFixedWidth(150)
        # layout.addWidget(self.save_path, alignment= Qt.AlignmentFlag.AlignCenter)

 
        button = QPushButton("Download")
        button.clicked.connect(self.download)
        layout.addWidget(button)
 
        button = QPushButton("Clear")
        button.clicked.connect(self.clear)
        layout.addWidget(button)

        self.show()

        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        self.timer.start()

    def download(self):
        # convert all our text stuff into an EnqueuedDownload
        self.queue.addToQueue(EnqueuedDownload(self.url.text()))

    def clear(self):
        self.url.clear()
        self.save_path.clear()

    def tick(self):
        if (self.queue.getCurrentDownload() is not None):
            self.progress.setValue(int(self.queue.getCurrentDownload().info.progress))

        self.queue.tick()



app = QApplication([])
window = MainWindow()
sys.exit(app.exec())