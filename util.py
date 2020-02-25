import logging
import pandas
from datetime import date
from datetime import datetime
from contextlib import ContextDecorator


# ----------------------------------------------------------------------------------------
def init_logging():
    logging.basicConfig(level=logging.DEBUG,
                        format='[%(asctime)s %(threadName)s %(funcName)s:%(lineno)d] %(message)s',
                        # filename='gold_miner.log',
                        # filemode='w'
                        )
    pandas.set_option('max_colwidth', 100)  # 设置value的显示长度为100，默认为50
    pandas.set_option('display.width', 10000)  # 表格宽度
    pandas.set_option('display.max_columns', None)  # 显示所有列
    pandas.set_option('display.max_rows', None)  # 显示所有行


class Timer(ContextDecorator):
    """Elegant Timer via ContextDecorator"""
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        self.start = datetime.now()

    def __exit__(self, *args):
        self.end = datetime.now()
        self.elapse = (self.end - self.start).total_seconds()
        logging.info("[{}] Cost: {} seconds\n".format(self.name, self.elapse))


def str_date2num(date_str):
    if date_str == 'None--':
        return 0
    return int(date_str[0:4])*10000 + int(date_str[5:7])*100 + int(date_str[8:10])


def str2int(x):
    if x is None:
        return None
    return int(x)


def num2date(n):
    return date(int(n / 10000), int(n / 100 % 100), int(n % 100))


# remove all empty columns
def filter_all_nan_columns(df, specified_columns=None):
    na_cols = df.isna().all()
    cols = list()
    for col in na_cols.index.values.tolist():
        if specified_columns is not None:
            if col in specified_columns:
                continue

        if not na_cols[col]:
            cols.append(col)
    # print(df[cols])
    return df[cols]

