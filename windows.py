from PyQt5.QtWidgets import QWidget, QMessageBox

from map import *


class Widget(QWidget):
    finish_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.initialize()
        self.map = Map(self)

    def initialize(self):
        self.setGeometry(100, 100, 500, 500)
        self.setWindowTitle('Pynake')
        self.setFixedSize(self.rect().size())
        self.finish_signal.connect(self.end_game)

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.map.draw(qp)
        qp.end()

    def keyPressEvent(self, e):
        self.map.keypress(e.key())

    def end_game(self):
        result = QMessageBox.information(self, 'GAME OVER', 'Restart game?', QMessageBox.Yes | QMessageBox.No)

        if result == QMessageBox.Yes:
            self.map.restart()
        else:
            self.close()
