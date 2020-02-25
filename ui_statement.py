from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from ui_util import *
import data_source as ds
from gold_db import *
from util import *
import pandas as pd


class StatementWindow(QWidget):
    def __init__(self, parent, sid, name):
        # properties --------------------
        self.parent = parent
        self.sid = sid
        self.name = name
        self.db = ds.DB
        self.balance: pd.DataFrame = None
        self.income: pd.DataFrame = None
        self.cash_flow: pd.DataFrame = None
        self.current_statement = None
        self.current_statement_data: pd.DataFrame = None
        self.main_layout = QHBoxLayout()
        self.horizon_splitter = QSplitter(Qt.Horizontal)
        self.statement_list_wgt = QListWidget()  # stock groups
        self.statement_table_wgt = QTableWidget()  # stock table

        # init function --------------------
        super(StatementWindow, self).__init__(flags=Qt.WindowFlags())
        self.init_ui()
        pass


    def create_splitter(self):
        self.horizon_splitter.setStyleSheet("QSplitter::handle { background-color: gray }")
        self.horizon_splitter.setHandleWidth(2)   # 设置分界线的宽度
        self.horizon_splitter.setSizes([200, 800])
        self.main_layout.addWidget(self.horizon_splitter)

    # if self.current_statement == 'balance':
    #     self.current_statement_data = self.balance
    # elif self.current_statement == 'income':
    #     self.current_statement_data = self.income
    # elif self.current_statement == 'income':
    #     self.current_statement_data = self.
    # else:
    #     pass
    def update_statement_table(self, s):
        if self.current_statement == s:
            return
        self.current_statement = s
        self.current_statement_data = getattr(self, s)

        # 时间倒序
        self.current_statement_data.sort_values('end_date', ascending=False, inplace=True)

        # 行列转置
        # print(self.current_statement_data.head())
        self.current_statement_data['end_date'] = self.current_statement_data['end_date'].apply(
            lambda _date: str(_date))
        self.current_statement_data = pd.DataFrame(self.current_statement_data.values.T,
                                                   index=self.current_statement_data.columns,
                                                   columns=self.current_statement_data['end_date'])

        # print(self.current_statement_data.head())

        self.current_statement_data.drop(index='end_date', inplace=True)
        # print(self.current_statement_data.head())

        fields = self.current_statement_data.columns.values.tolist()
        self.statement_table_wgt.clearContents()
        self.statement_table_wgt.setColumnCount(len(fields))
        self.statement_table_wgt.setHorizontalHeaderLabels(fields)
        self.statement_table_wgt.setRowCount(len(self.current_statement_data))
        self.statement_table_wgt.setVerticalHeaderLabels(self.current_statement_data.index.values.tolist())

        for x in range(len(self.current_statement_data)):
            for y in range(len(fields)):
                data = self.current_statement_data.iloc[x, y]
                # print(type(data))
                if type(data) != str:
                    self.statement_table_wgt.setItem(x, y, QCustomTableWidgetItem(data))
                else:
                    self.statement_table_wgt.setItem(x, y, QTableWidgetItem(data))

        pass

    def on_clicked_statement_list(self,  index: QModelIndex):
        item: QListWidgetItem = self.statement_list_wgt.item(index.row())
        self.update_statement_table(item.text())

    def create_left_layout(self):
        left_layout = QVBoxLayout()
        for table in [TBL_BALANCE, TBL_CASH_FLOW, TBL_INCOME]:
            self.statement_list_wgt.addItem(table)
        self.statement_list_wgt.clicked.connect(self.on_clicked_statement_list)
        self.statement_list_wgt.setCurrentRow(0)
        self.update_statement_table(TBL_BALANCE)

        left_layout.addWidget(QLabel('Statements'))
        left_layout.addWidget(self.statement_list_wgt)
        self.horizon_splitter.addWidget(wrap_layout(left_layout))

    def init_statement_table_widget(self):
        self.statement_table_wgt.setSortingEnabled(True)
        self.statement_table_wgt.setSelectionMode(QAbstractItemView.ExtendedSelection)  # 可多选（Ctrl、Shift、  Ctrl + A）
        self.statement_table_wgt.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.statement_table_wgt.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 设置不可编辑
        # self.statement_table_wgt.cellDoubleClicked.connect(self.on_double_clicked_statment_table_widget)

        filters = ['sid', 'ann_date', 'f_ann_date', 'report_type', 'comp_type']
        self.balance = self.db.query_statement(self.sid, TBL_BALANCE, filters)
        self.income = self.db.query_statement(self.sid, TBL_INCOME, filters)
        self.cash_flow = self.db.query_statement(self.sid, TBL_CASH_FLOW, filters)
        print(self.balance.head())

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
        middle_layout.addWidget(self.statement_table_wgt)
        self.horizon_splitter.addWidget(wrap_layout(middle_layout))


    def init_ui(self):
        self.resize(1024, 720)
        self.setWindowTitle(self.name + '-' + self.sid)
        self.init_statement_table_widget()
        self.create_left_layout()
        self.create_middle_layout()
        self.create_splitter()
        self.setLayout(self.main_layout)

