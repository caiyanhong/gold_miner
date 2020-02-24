import sqlite3
import logging
from util import *
from data_description import *

# ----------------------------------------------------------------------------------------
ROOT_DIR = 'D:/data/'
DB_PATH = ROOT_DIR + 'gold_miner.db'
TBL_STOCK_LIST = 'stock_list'
TBL_INDEX_WEIGHT = 'index_weight'
TBL_PRICE = 'price'
TBL_INCOME = 'income'
TBL_BALANCE = 'balance'
TBL_CASH_FLOW = 'cash_flow'
TBL_DIVIDEND = 'dividend'


# --------------------------------------------------------------------------------------
# CACHES
ALL_STOCK_LIST = None       # 全股票列表
SCI = None                  # 上证指数行情, shanghai composite index
HS300 = None                # 沪深300行情
SCI_SID = '000001.SH'
HS300_SID = '399300.SZ'

INTERESTED_FUND = {
    '50ETF': '510050.SH',
    '300ETF': '159919.SZ',
    '500ETF': '159922.SZ',
}

INTERESTED_INDEX = {
    '上证综指': '000001.SH',
    '上证50': '000016.SH',
    '沪深300': '399300.SZ',
    # '中证500': '399905.SZ',  # 没有数据
    '中小板指': '399005.SZ',
    '创业板指': '399006.SZ',
}


# ----------------------------------------------------------------------------------------
class GoldDb:
    def __init__(self, db_name=DB_PATH):
        self.name = db_name
        self.con = None
        self.cursor = None
        self.connect()

    def __del__(self):
        self.close()

    def connect(self):
        if self.con is not None and self.cursor is not None:
            return True

        try:
            self.con = sqlite3.connect(self.name, check_same_thread=False)  # enable multi-thread
            self.cursor = self.con.cursor()
        except Exception as e:
            logging.warning(e)
            return False

        logging.info("db connected: " + self.name)
        return True

    def close(self):
        self.cursor.close()
        self.con.close()
        self.con = None
        self.cursor = None
        logging.info("db closed: " + self.name)

    def execute(self, sql):
        try:
            res = self.cursor.execute(sql)
            self.con.commit()
            return res
        except Exception as e:
            logging.warning(e)
            return False

    def query(self, sql):
        return pandas.read_sql(sql, self.con)

    def select(self, table, field=None, condition=None):
        sql = 'select '
        if field is not None:
            sql += field
        else:
            sql += "*"

        sql += ' from ' + table
        if condition is not None:
            sql += ' where ' + condition

        return pandas.read_sql(sql, self.con)

    def insert_data_frame(self, table, df):
        tuples = list(df.itertuples(index=False, name=None))
        columns_list = df.columns.tolist()
        marks = ['?' for _ in columns_list]
        columns_list = f'({(",".join(columns_list))})'
        marks = f'({(",".join(marks))})'
        try:
            self.cursor.executemany(f'INSERT OR REPLACE INTO {table}{columns_list} VALUES {marks}', tuples)
            self.con.commit()
            return True
        except Exception as e:
            logging.warning(e)
            return False

    def create_stock_list(self):
        create_table = 'create table ' + TBL_STOCK_LIST \
                       + '(sid int not null primary key, ' \
                         'name text not null, ' \
                         'area text, ' \
                         'industry text, ' \
                         'fullname text, ' \
                         'enname text, ' \
                         'market text, ' \
                         'exchange text, ' \
                         'curr_type text, ' \
                         'list_status text, ' \
                         'list_date text, ' \
                         'delist_date text, ' \
                         'is_hs text' \
                         ')'
        insert_value = 'insert into ' + TBL_STOCK_LIST + ' values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
        remove_value = 'delete from ' + TBL_STOCK_LIST + ' where sid like "TEST%"'
        prices = list()
        prices.append(('TEST', "Devil inc.", None, None, None, None, None, None, None, None, None, None, None))
        prices.append(('TEST-2', "Cai inc.", None, None, None, None, None, None, None, None, None, None, None))

        try:
            logging.info("create " + TBL_STOCK_LIST)
            self.cursor.execute(create_table)
            logging.info('try insert' + TBL_STOCK_LIST)
            for price_record in prices:
                self.cursor.execute(insert_value, price_record)
            self.con.commit()
            logging.debug('\n' + str(self.select(TBL_STOCK_LIST)))
            logging.info("remove test prices")
            self.cursor.execute(remove_value)
            self.con.commit()
            logging.debug('\n' + str(self.select(TBL_STOCK_LIST)))

        except Exception as e:
            logging.warning(str(e))
        pass

    def create_price_table(self):
        # date, open, high, low, close, volume, amount
        create_price = 'create table ' + TBL_PRICE + '(' \
                                                     'sid text not null, ' \
                                                     'asset_type tinyint not null, ' \
                                                     'date int not null, ' \
                                                     'time int not null, ' \
                                                     'open float, ' \
                                                     'high float, ' \
                                                     'low float, ' \
                                                     'close float, ' \
                                                     'volume float, ' \
                                                     'amount float ,' \
                                                     'constraint asset_date_price primary key(sid, asset_type, date, time)' \
                                                     ')'
        create_index = 'CREATE INDEX price_date ON price (date)'
        create_index_sid = 'CREATE INDEX price_sid ON price (sid)'
        insert_price = 'insert into ' + TBL_PRICE + ' values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
        remove_price = 'delete from ' + TBL_PRICE + ' where sid="TEST"'
        prices = list()

        prices.append(('TEST', AssetType.stock, 20021105, 0,
                       3.0167, 3.1092, 2.9987, 3.0618, 217887.72, 294514.312))
        prices.append(('TEST', AssetType.stock, 20021105, 1,
                       3.0167, 3.1092, 2.9987, 3.0618, 217887.72, 294514.312))

        # unique test
        # prices.append(('TEST', 0, '2002-11-05T15:00:00.000Z', 3.0167, 3.1092, 2.9987, 3.0618, 217887.72, 294514.312))

        try:
            logging.info("create price table")
            self.cursor.execute(create_price)

            logging.info(create_index)
            self.cursor.execute(create_index)
            self.cursor.execute(create_index_sid)

            logging.info("try insert price table")
            for price_record in prices:
                self.cursor.execute(insert_price, price_record)
            self.con.commit()
            logging.debug('\n' + str(self.select(TBL_PRICE)))

            logging.info("remove test prices")
            self.cursor.execute(remove_price)
            self.con.commit()
            logging.debug('\n' + str(self.select(TBL_PRICE)))

        except Exception as e:
            logging.warning(str(e))

    def create_dividend_table(self):
        table = TBL_DIVIDEND
        statement_description = DIVIDEND_DESCRIPTION

        sql_fields = ''
        fields = statement_description.split('\n')
        for line_no in range(len(fields)):
            if fields[line_no] == '':
                continue
            structs = fields[line_no].split('\t')
            sql_fields += structs[0]
            sql_fields += ' %s, ' % structs[1]

        create_table = 'create table ' + table \
                       + '(sid text not null, ' \
                       + sql_fields \
                       + 'constraint sid_ex_date primary key(sid, ex_date)' \
                       + ')'
        create_index = 'CREATE INDEX %s_ex_date ON %s (ex_date)' % (table, table)
        create_index_sid = 'CREATE INDEX %s_sid ON %s (sid)' % (table, table)

        print(create_table)
        try:
            logging.info("create " + table)
            self.cursor.execute(create_table)
            self.cursor.execute(create_index)
            self.cursor.execute(create_index_sid)
            self.con.commit()
            logging.debug('\n' + str(self.select(table)))

        except Exception as e:
            logging.warning(str(e))
        pass

    def create_statement_index(self):
        for table in [TBL_BALANCE, TBL_CASH_FLOW, TBL_INCOME]:
            with Timer("create  index"):
                create_index_sid = 'CREATE INDEX %s_sid ON %s (sid)' % (table, table)
                self.cursor.execute(create_index_sid)
                self.con.commit()

    def create_statement_tables(self):
        self.create_statement_table(INCOME_STATEMENT_DESCRIPTION, TBL_INCOME)
        self.create_statement_table(BALANCE_STATEMENT_DESCRIPTION, TBL_BALANCE)
        self.create_statement_table(CASH_FLOW_STATEMENT_DESCRIPTION, TBL_CASH_FLOW)

    def create_statement_table(self, statement_description, table):
        # get fields
        # industry = pro.income(ts_code='600009.SH')
        # print(industry.columns.values)
        # print(industry.dtypes)

        sql_fields = ''
        fields = statement_description.split('\n')
        for line_no in range(len(fields)):
            if fields[line_no] == '':
                continue
            structs = fields[line_no].split('\t')
            sql_fields += structs[0]
            sql_fields += ' %s, ' % structs[1]
        print(sql_fields)

        create_table = 'create table ' + table \
                       + '(sid text not null, ' \
                       + sql_fields \
                       + 'constraint sid_end_date primary key(sid, end_date)' \
                       + ')'
        create_index = 'CREATE INDEX %s_f_ann_date ON %s (f_ann_date)' % (table, table)
        create_index_sid = 'CREATE INDEX %s_sid ON %s (sid)' % (table, table)

        try:
            logging.info("create " + table)
            self.cursor.execute(create_table)
            self.cursor.execute(create_index)
            self.cursor.execute(create_index_sid)
            self.con.commit()
            logging.debug('\n' + str(self.select(table)))

        except Exception as e:
            logging.warning(str(e))
        pass

    @Timer('test_database')
    def test_database(self):
        with Timer("Test select distinct sid"):
            logging.info(self.select('price', field='distinct sid').head())

        with Timer("Test select distinct date"):
            logging.info(self.select('price', field='distinct date').head())

        with Timer('Test select max'):
            logging.info(self.select('price', field='max(date)').head())

        with Timer('Test select by date'):
            logging.info(self.select('price', condition=' date>20200101 and date<20200202 ').head())

        with Timer('Test select by sid'):
            logging.info(self.select('price', condition='sid="600000.SH"').head())

    def rebuild_database(self):
        self.create_price_table()
        self.create_statement_tables()
        self.create_dividend_table()

    # ----------------------------------------------------------------------------------------
    # specified functions
    def query_all_stock_list(self):
        global ALL_STOCK_LIST
        if ALL_STOCK_LIST is None:
            ALL_STOCK_LIST = self.select(TBL_STOCK_LIST)
        return ALL_STOCK_LIST

    def query_price(self, sid):
        return self.select(TBL_PRICE, condition="sid='%s'" % sid)

    def query_sci(self):
        global SCI
        if SCI is None:
            SCI = self.select(TBL_PRICE, condition="sid='%s'" % SCI_SID)
        return SCI

    def query_hs300(self):
        global HS300
        if HS300 is None:
            HS300 = self.select(TBL_PRICE, condition="sid='%s'" % SCI_SID)
        return HS300

    def query_index_weight(self, index_code):
        max_date = self.select(TBL_INDEX_WEIGHT, field="max(date)",
                               condition='index_code="%s"' % index_code)
        max_date = max_date.iloc[0, 0]
        # print(max_date)

        index_weights = self.select(TBL_INDEX_WEIGHT, field="sid, date, weight",
                                    condition='index_code="%s"' % index_code + ' and date=' + str(max_date))
        index_weights.sort_values('weight', ascending=False, inplace=True)
        index_weights.reset_index(drop=True, inplace=True)
        # print(index_weights)
        return index_weights

    def query_statement(self, sid, table):

        pass


def convert_statement_date():
    db = GoldDb()
    #
    # # --1.将表名改为临时表
    # # ALTER TABLE "Student" RENAME TO "_Student_old_20140409";
    # for table in [TBL_BALANCE, TBL_CASH_FLOW, TBL_INCOME]:
    #     sql = 'ALTER TABLE "%s" RENAME TO "%s_temp" ' % (table, table)
    #     logging.info(sql)
    #     db.execute(sql)
    #
    # # --2.创建新表
    # # CREATE TABLE "Student" ("Id"  INTEGER PRIMARY KEY AUTOINCREMENT, "Name"  Text);
    # db.create_statement_tables()
    #
    # # --3.导入数据
    # # ;INSERT INTO "Student" ("Id", "Name") SELECT "Id", "Title" FROM "_Student_old_20140409"
    # for table in [TBL_BALANCE, TBL_CASH_FLOW, TBL_INCOME]:
    #     sql = 'INSERT INTO "%s" SELECT * FROM "%s_temp"' % (table, table)
    #     logging.info(sql)
    #     db.execute(sql)
    #     pass

    # --4.更新sqlite_sequence
    # UPDATE "sqlite_sequence" SET seq = 3 WHERE name = 'Student';
    # 由于在Sqlite中使用自增长字段,引擎会自动产生一个sqlite_sequence表,用于记录每个表的自增长字段的已使用的最大值，所以要一起更新下。如果有没有设置自增长，则跳过此步骤。

    # --5.删除临时表(可选)
    # DROP TABLE _Student_old_20140409;
    # for table in [TBL_BALANCE, TBL_CASH_FLOW, TBL_INCOME]:
    #     sql = 'DROP TABLE %s_temp' % table
    #     logging.info(sql)
    #     db.execute(sql)
    #     pass

    # 重建索引
    for table in [TBL_BALANCE, TBL_CASH_FLOW, TBL_INCOME]:
        sql = 'CREATE INDEX %s_f_ann_date ON %s (f_ann_date)' % (table, table)
        logging.info(sql)
        db.execute(sql)

        sql = 'CREATE INDEX %s_sid ON %s (sid)' % (table, table)
        logging.info(sql)
        db.execute(sql)

    df = db.select(TBL_BALANCE, condition="sid='600000.SH'")
    print(df.head())
    print(df.dtypes)
    logging.info("Done")


def convert_db_date():
    old_db = GoldDb()
    new_db = GoldDb('d:/data/new.db')
    # new_db.rebuild_database()

    with Timer("all distinct sid"):
        all_stocks = old_db.select(TBL_PRICE, 'distinct sid')

    # # price table
    # for sid in all_stocks['sid'].values.tolist():
    #     prices = old_db.select(TBL_PRICE, condition='sid="%s"' % sid)
    #     prices['date'] = prices['date'].apply(str_date2num)
    #     prices['time'] = [0]*len(prices)
    #     new_db.insert_data_frame(TBL_PRICE, prices)
    #     print(prices.head())
    #     # print(prices.dtypes)
    #     # break
    #     pass

    # # statements
    # for sid in all_stocks['sid'].values.tolist():
    #     for table in [TBL_BALANCE, TBL_CASH_FLOW, TBL_INCOME]:
    #         with Timer("select sheet"):
    #             sheet = old_db.select(table, condition='sid="%s"' % sid)
    #         sheet['ann_date'] = sheet['ann_date'].apply(str_date2num)
    #         sheet['f_ann_date'] = sheet['f_ann_date'].apply(str_date2num)
    #         sheet['end_date'] = sheet['end_date'].apply(str_date2num)
    #         sheet['report_type'] = sheet['report_type'].apply(str2int)
    #         sheet['comp_type'] = sheet['comp_type'].apply(str2int)
    #         print(sheet.head())
    #         new_db.insert_data_frame(table, sheet)
    #
    # # index weight
    # index_weight = old_db.select(TBL_INDEX_WEIGHT)
    # index_weight['date'] = index_weight['date'].apply(str_date2num)
    # index_weight.to_sql(TBL_INDEX_WEIGHT, new_db.con, if_exists='replace', index=False)

    # # stock list
    # stock_list = old_db.select(TBL_STOCK_LIST)
    # stock_list['list_date'] = stock_list['list_date'].apply(str2int)
    # stock_list['delist_date'] = stock_list['delist_date'].apply(str2int)
    # stock_list.to_sql(TBL_STOCK_LIST, new_db.con, if_exists='replace', index=False)

