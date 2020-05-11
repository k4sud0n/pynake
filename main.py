import sys

from PyQt5.QtWidgets import QApplication

from windows import *

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Widget()
    w.show()
    sys.exit(app.exec_())
