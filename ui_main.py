import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from ui_util import *
import data_source as ds
from gold_db import *
from util import *
# import logging
import pandas as pd
from ui_statement import StatementWindow


class MainWindow(QWidget):
    def __init__(self):
        # properties --------------------
        self.db: GoldDb = None
        self.main_layout = QHBoxLayout()
        self.horizon_splitter = QSplitter(Qt.Horizontal)
        self.group_list_wgt = QListWidget()     # stock groups
        self.stock_table_wgt = QTableWidget()       # stock table
        self.group_stocks_data: pd.DataFrame = None
        self.current_group = None

        # self.statement_window: StatementWindow = None
        self.child_windows = list()

        # init function --------------------
        super(MainWindow, self).__init__(flags=Qt.WindowFlags())
        self.init_db()
        self.init_ui()

    def display_stock_table(self, interested_fields):
        self.stock_table_wgt.clearContents()
        self.stock_table_wgt.setColumnCount(len(interested_fields))
        self.stock_table_wgt.setRowCount(len(self.group_stocks_data))
        self.stock_table_wgt.setHorizontalHeaderLabels(interested_fields)

        print(self.group_stocks_data.dtypes)
        for x in range(len(self.group_stocks_data)):
            for y in range(len(interested_fields)):
                data = self.group_stocks_data.iloc[x, y]
                # print(type(data))
                if type(data) != str:
                    self.stock_table_wgt.setItem(x, y, QCustomTableWidgetItem(data))
                else:
                    self.stock_table_wgt.setItem(x, y, QTableWidgetItem(data))

        pass

    def update_stock_table(self, group):
        if group in INTERESTED_INDEX:
            index_code = INTERESTED_INDEX[group]
            self.group_stocks_data = self.db.query_index_weight(index_code)
            # print(self.group_stocks_data)
        else:
            pass

        all_stocks = self.db.query_all_stock_list()
        self.group_stocks_data = self.group_stocks_data.merge(all_stocks, on='sid', how='left')
        interested_fields = ['sid', 'weight', 'name', 'industry']
        self.group_stocks_data = self.group_stocks_data[interested_fields]

        # display on table
        self.display_stock_table(interested_fields)

    def on_clicked_group_list(self, index: QModelIndex):
        item: QListWidgetItem = self.group_list_wgt.item(index.row())
        group = item.text()
        print("index: %d, text: %s" % (index.row(), group))

        if self.current_group == group:
            return
        if group == '上证综指':
            return
        if group == '全市场':
            return

        self.current_group = group
        self.update_stock_table(self.current_group)

    def create_left_layout(self):
        left_layout = QVBoxLayout()
        for idx in INTERESTED_INDEX.keys():
            if idx == '上证综指':
                continue
            self.group_list_wgt.addItem(idx)

        self.group_list_wgt.addItem('全市场')
        self.group_list_wgt.clicked.connect(self.on_clicked_group_list)

        # default selection
        self.current_group = '沪深300'
        self.group_list_wgt.setCurrentRow(1)
        self.update_stock_table(self.current_group)

        group_edit_layout = QHBoxLayout()
        btn_add = QPushButton("+")
        btn_del = QPushButton("-")
        btn_edit = QPushButton("E")

        btn_add.setFixedWidth(30)
        btn_del.setFixedWidth(30)
        btn_edit.setFixedWidth(30)

        group_edit_layout.addWidget(btn_add)
        group_edit_layout.addWidget(btn_del)
        group_edit_layout.addWidget(btn_edit)

        left_layout.addWidget(QLabel('Groups'))
        left_layout.addWidget(self.group_list_wgt)
        left_layout.addLayout(group_edit_layout)
        self.horizon_splitter.addWidget(wrap_layout(left_layout))

    def on_double_clicked_stock_table_widget(self, x, y):
        # print("x %d, y %d" % (x, y))
        sw = StatementWindow(parent=self, sid=self.group_stocks_data['sid'][x], name=self.group_stocks_data['name'][x])
        sw.show()
        # sw.destroyed.connect(lambda _w: self.child_windows.remove(_w))
        self.child_windows.append(sw)    # keep in memory
        pass

    def init_stock_table_widget(self):
        self.stock_table_wgt.setSortingEnabled(True)
        self.stock_table_wgt.setSelectionMode(QAbstractItemView.ExtendedSelection)  # 可多选（Ctrl、Shift、  Ctrl + A）
        self.stock_table_wgt.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.stock_table_wgt.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 设置不可编辑
        self.stock_table_wgt.cellDoubleClicked.connect(self.on_double_clicked_stock_table_widget)

    def create_middle_layout(self):
        # search bar
        middle_layout = QVBoxLayout()
        search_layout = QHBoxLayout()

        search_layout.addWidget(QLabel("Search"))
        search_layout.addWidget(QLineEdit())

        search_next = QPushButton("Next")
        search_prev = QPushButton("Prev")
        search_layout.addWidget(search_prev)
        search_layout.addWidget(search_next)

        middle_layout.addLayout(search_layout)

        self.init_stock_table_widget()
        middle_layout.addWidget(self.stock_table_wgt)
        self.horizon_splitter.addWidget(wrap_layout(middle_layout))

    def create_splitter(self):
        self.horizon_splitter.setStyleSheet("QSplitter::handle { background-color: gray }")
        self.horizon_splitter.setHandleWidth(2)   # 设置分界线的宽度
        self.horizon_splitter.setSizes([200, 800])
        self.main_layout.addWidget(self.horizon_splitter)

    def init_ui(self):
        self.resize(1024, 720)
        self.setWindowTitle('Hard working')
        self.create_left_layout()
        self.create_middle_layout()

        self.create_splitter()
        self.setLayout(self.main_layout)
        self.show()

    def init_db(self):
        init_logging()
        self.db = GoldDb()
        ds.set_db(self.db)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())

