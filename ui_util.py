from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


def wrap_layout(layout):
    w = QWidget()
    w.setLayout(layout)
    return w


class QCustomTableWidgetItem (QTableWidgetItem):
    def __init__(self, value):
        super(QCustomTableWidgetItem, self).__init__()
        self.setData(Qt.EditRole, value)
        self.setData(Qt.DisplayRole, str(value))

    def __lt__(self, other):
        if isinstance(other, QCustomTableWidgetItem):
            self_data = float(self.data(Qt.EditRole))
            other_data = float(other.data(Qt.EditRole))
            return self_data < other_data
        else:
            return QTableWidgetItem.__lt__(self, other)


