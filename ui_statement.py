from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from ui_util import *
import data_source as ds
from gold_db import *
from util import *
# import logging
import pandas as pd


class StatementWindow(QWidget):
    def __init__(self, parent, sid, name):
        # properties --------------------
        self.parent = parent
        self.sid = sid
        self.name = name
        self.main_layout = QHBoxLayout()
        self.horizon_splitter = QSplitter(Qt.Horizontal)
        self.statement_list_wgt = QListWidget()  # stock groups
        self.statement_table_wgt = QTableWidget()  # stock table

        print(sid)

        # init function --------------------
        super(StatementWindow, self).__init__(flags=Qt.WindowFlags())
        self.init_ui()
        pass


    def create_splitter(self):
        self.horizon_splitter.setStyleSheet("QSplitter::handle { background-color: gray }")
        self.horizon_splitter.setHandleWidth(2)   # 设置分界线的宽度
        self.horizon_splitter.setSizes([200, 800])
        self.main_layout.addWidget(self.horizon_splitter)

    def create_left_layout(self):
        left_layout = QVBoxLayout()
        for table in [TBL_BALANCE, TBL_CASH_FLOW, TBL_INCOME]:
            self.statement_list_wgt.addItem(table)

        # self.statement_list_wgt.clicked.connect(self.on_clicked_group_list)

        left_layout.addWidget(QLabel('Statements'))
        left_layout.addWidget(self.statement_list_wgt)
        self.horizon_splitter.addWidget(wrap_layout(left_layout))

    def init_statement_table_widget(self):
        self.statement_table_wgt.setSortingEnabled(True)
        self.statement_table_wgt.setSelectionMode(QAbstractItemView.ExtendedSelection)  # 可多选（Ctrl、Shift、  Ctrl + A）
        self.statement_table_wgt.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.statement_table_wgt.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 设置不可编辑
        # self.statement_table_wgt.cellDoubleClicked.connect(self.on_double_clicked_statment_table_widget)

    def create_middle_layout(self):
        middle_layout = QVBoxLayout()
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Search"))
        search_layout.addWidget(QLineEdit())

        search_next = QPushButton("Next")
        search_prev = QPushButton("Prev")
        search_layout.addWidget(search_prev)
        search_layout.addWidget(search_next)

        middle_layout.addLayout(search_layout)

        self.init_statement_table_widget()
        middle_layout.addWidget(self.statement_table_wgt)
        self.horizon_splitter.addWidget(wrap_layout(middle_layout))


    def init_ui(self):
        self.resize(1024, 720)
        self.setWindowTitle(self.name + '-' + self.sid)
        self.create_left_layout()
        self.create_middle_layout()
        self.create_splitter()
        self.setLayout(self.main_layout)

