import os
import pandas
import numpy as np
import tushare
import time
from datetime import date
from datetime import timedelta
import logging
from util import *
from gold_db import *
import matplotlib.pyplot as plt


# ----------------------------------------------------------------------------------------
# 初始化pro接口
tushare_token = '8c5e0fe7597608f54d0789e9785a712b504fe74a0a37e608c27d45e4'
pro = tushare.pro_api(tushare_token)
DB: GoldDb = None


def set_db(db):
    global DB
    DB = db


# ----------------------------------------------------------------------------------------
def replace_ts_code(df):
    df['sid'] = df['ts_code'].copy()
    df.drop('ts_code', axis=1, inplace=True)


# ----------------------------------------------------------------------------------------
def standardize_tushare_price(df, asset_type=AssetType.stock):
    df['sid'] = df['ts_code']
    df['asset_type'] = [asset_type] * len(df)
    df['date'] = df['trade_date'].apply(tushare_date_to_int)
    df['time'] = [0] * len(df)
    df['volume'] = df['vol']
    df.drop(columns=['trade_date', 'ts_code', 'vol', 'pre_close', 'change', 'pct_chg'], axis=1, inplace=True)
    return df


# ----------------------------------------------------------------------------------------
def download_all_stock_list():
    '''
    # 查询当前所有正常上市交易的股票列表
    ts_code	str	TS代码
    name	str	股票名称
    area	str	所在地域
    industry	str	所属行业
    fullname	str	股票全称
    enname	str	英文全称
    market	str	市场类型 （主板/中小板/创业板/科创板）
    exchange	str	交易所代码
    curr_type	str	交易货币
    list_status	str	上市状态： L上市 D退市 P暂停上市
    list_date	str	上市日期
    delist_date	str	退市日期
    is_hs	str	是否沪深港通标的，N否 H沪股通 S深股通
    '''
    # data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    listed = pro.stock_basic(exchange='', list_status='L',
                             fields='ts_code,name,area,industry,fullname,enname,'
                                    'market,exchange,curr_type,list_status,list_date,delist_date,is_hs')
    d = pro.stock_basic(exchange='', list_status='D',
                        fields='ts_code,name,area,industry,fullname,enname,'
                               'market,exchange,curr_type,list_status,list_date,delist_date,is_hs')
    p = pro.stock_basic(exchange='', list_status='P',
                        fields='ts_code,name,area,industry,fullname,enname,'
                               'market,exchange,curr_type,list_status,list_date,delist_date,is_hs')
    full_list = listed
    full_list = full_list.append(d)
    full_list = full_list.append(p)
    replace_ts_code(full_list)
    full_list.set_index('sid', inplace=True, drop=True)
    print(full_list)
    full_list.to_sql(TBL_STOCK_LIST, DB.con, if_exists='replace', index=True)
    print(DB.select(TBL_STOCK_LIST).head())

    return full_list


# ----------------------------------------------------------------------------------------
# 更新时间：交易日每天15点～16点之间
# 下载每日所有股票价格
def update_stock_daily(date=None):
    try:
        df = pro.daily(trade_date=date, retry_count=5)
    except Exception as e:
        logging.info(e)
        return False

    # df.sort_values(by='ts_code', axis=0, inplace=True)
    if len(df) == 0:
        logging.info('No data on ' + date)
        return True

    df = standardize_tushare_price(df)
    print(df.head())
    print(df.shape)
    # print(df.dtypes)

    # insert into database
    # date, open, high, low, close, volume, amount
    return DB.insert_data_frame(TBL_PRICE, df)


# ----------------------------------------------------------------------------------------
# 获取单支股票日K
# 输出参数----------------------------
# 名称	类型	描述
# ts_code	str	股票代码
# date	str	交易日期
# open	float	开盘价
# high	float	最高价
# low	float	最低价
# close	float	收盘价
# pre_close	float	昨收价
# change	float	涨跌额
# pct_chg	float	涨跌幅 （未复权，如果是复权请用 通用行情接口 ）
# vol	float	成交量 （手）
# amount	float	成交额 （千元）

# 输入参数----------------------------
# 名称	类型	必选	描述
# ts_code	str	Y	证券代码
# pro_api	str	N	pro版api对象
# start_date	str	N	开始日期 (格式：YYYYMMDD)
# end_date	str	N	结束日期 (格式：YYYYMMDD)
# asset	str	Y	资产类别：E股票 I沪深指数 C数字货币 FT期货 FD基金 O期权，默认E
# adj	str	N	复权类型(只针对股票)：None未复权 qfq前复权 hfq后复权 , 默认None
# freq	str	Y	数据频度 ：1MIN表示1分钟（1/5/15/30/60分钟） D日线 ，默认D，包括指数在内的分钟数据已经定向开放，有需求的用户请在QQ群私信群主。
# ma	list	N	均线，支持任意合理int数值
# factors	list	N	股票因子（asset='E'有效）支持 tor换手率 vr量比
def download_kline(ts_code, asset_type=AssetType.stock):
    try:
        df = None
        if asset_type == AssetType.stock:      # 获取前复权数据
            df = tushare.pro_bar(api=pro, ts_code=ts_code, adj='qfq', retry_count=5)
        elif asset_type == AssetType.index:
            df = pro.index_daily(ts_code=ts_code)
        elif asset_type == AssetType.fund:     # 每次只能取800条
            start_date = 20010101
            end_date = start_date + 30000
            while start_date < 20500101:
                sub_df = pro.fund_daily(ts_code=ts_code, retry_count=5, asset='FD',
                                        start_date=str(start_date), end_date=str(end_date))
                start_date = end_date
                end_date = end_date + 30000

                if sub_df is None or (len(sub_df) == 0):
                    continue
                if df is None:
                    df = sub_df
                else:
                    df = pandas.concat([sub_df, df])

        if df is None or len(df) == 0:
            return False
    except Exception as e:
        logging.info(e)
        return False

    df = standardize_tushare_price(df, asset_type)

    # sort by date
    df.sort_values(by='date', ascending=True, inplace=True)

    logging.info(df.head())
    logging.info(df.shape)
    DB.insert_data_frame(TBL_PRICE, df)
    return True


def download_dividend(sid):
    fields = list()
    lines = DIVIDEND_DESCRIPTION.split('\n')
    for line in lines:
        if line == "":
            continue
        fields.append(line.split('\t')[0])

    # print(fields)
    # print(', '.join(fields))
    try:
        df = pro.dividend(ts_code=sid, fields=', '.join(fields))
    except Exception as e:
        logging.info(e)
        return False

    # sort by date
    df.sort_values(by='ex_date', ascending=True, inplace=True)
    for d in ['end_date', 'ann_date', 'record_date', 'ex_date',
              'pay_date', 'div_listdate', 'imp_ann_date', 'base_date']:
        df[d] = df[d].apply(tushare_date_to_int)
        pass

    # logging.info(df.head())
    # logging.info(df.shape)
    df['sid'] = [sid] * len(df)
    DB.insert_data_frame(TBL_DIVIDEND, df)

    sel = DB.select(TBL_DIVIDEND, condition="sid='%s'" % sid)
    print(sel)
    return True


def download_all_dividend():
    all_stock = query_all_stock_list()
    for sid in all_stock['sid'].values.tolist():
        while True:
            logging.info('downloading %s ...' % (sid))
            success = download_dividend(sid)
            if success is True:
                break
            else:
                logging.info('Timeout occurred, rest a second...')
                time.sleep(1)
                continue
    logging.info("done")


def delete_old_index_price():
    sql = 'delete from price where sid="%s"'
    for ts_code in INTERESTED_INDEX.values():
        print(sql % ts_code)
        res = DB.execute(sql % ts_code)
        print(res)
    pass


# ----------------------------------------------------------------------------------------
# 获取指数行情
def download_all_index_kline():
    global INTERESTED_INDEX
    finished_count = 0
    for ts_code in INTERESTED_INDEX.values():
        while True:
            logging.info('downloading No.' + str(finished_count) + '--' + ts_code + ' ...')
            success = download_kline(ts_code, AssetType.index)
            if success is True:
                break
            else:
                logging.info('Timeout occurred, rest a second...')
                time.sleep(1)
                continue
        finished_count = finished_count + 1
        # time.sleep(60/20)

    logging.info('Done!')


# ----------------------------------------------------------------------------------------
# 下载所有基金K线
def download_all_fund_kline():
    global INTERESTED_FUND
    finished_count = 0
    for ts_code in INTERESTED_FUND.values():
        while True:
            logging.info('downloading No.' + str(finished_count) + '--' + ts_code + ' ...')
            success = download_kline(ts_code, AssetType.fund)
            if success is True:
                break
            else:
                logging.info('Timeout occurred, rest a second...')
                time.sleep(1)
                continue
        finished_count = finished_count + 1
        # time.sleep(60/20)

    logging.info('Done!')


# 测试指数ID是否唯一
def test_index_id_unique():
    sql = 'select count(distinct asset_type) from price where sid="%s"'
    for sid in INTERESTED_INDEX.values():
        print(sql % sid)
        df = DB.query(sql % sid)
        print(df)

    for sid in INTERESTED_FUND.values():
        print(sql % sid)
        df = DB.query(sql % sid)
        print(df)


def test_plot_index():
    sci = query_sci()
    sci['close'].plot()
    # sh001 = query_price('600000.SH')
    # sh001['close'].plot()
    plt.show()


# ----------------------------------------------------------------------------------------
# 指数成分和权重
# index_code	str	指数代码
# con_code	str	成分代码
# date	str	交易日期
# weight	float	权重
def download_index_weight():
    global INTERESTED_INDEX
    finished_count = 0
    index_weight = None

    for ts_code in INTERESTED_INDEX.values():
        if ts_code == '000001.SH':  # 上证综指不下载
            continue
        today = date.today()
        last_day = date(2009, 1, 1)
        finished_count = finished_count + 1
        while last_day < today:
            start_date = '%04d%02d%02d' % (last_day.year, last_day.month, 1)
            end_date = '%04d%02d%02d' % (last_day.year, last_day.month, 31)
            print('downloading No.' + str(finished_count) + '--' + ts_code + ' ...')
            print('start_date: ' + start_date + 'end_date' + end_date)

            while True:
                try:
                    df = pro.index_weight(index_code=ts_code, start_date=start_date, end_date=end_date)
                    break
                except Exception as e:
                    logging.info(e)
                    time.sleep(1)

            if last_day.month == 12:
                last_day = last_day.replace(year=last_day.year+1, month=1)
            else:
                last_day = last_day.replace(month=last_day.month+1)

            time.sleep(60 / 70)     # 您每分钟最多访问该接口70次
            if len(df) == 0:
                continue

            df = standardize_tushare_date(df)
            df['sid'] = df['con_code']
            df.drop('con_code', axis=1, inplace=True)
            print(df)
            if index_weight is None:
                index_weight = df.copy()
            else:
                index_weight = index_weight.append(df)

    index_weight.to_sql(TBL_INDEX_WEIGHT, DB.con, if_exists='replace', index=False)
    print(DB.select(TBL_INDEX_WEIGHT))
    print('Done!')


# ----------------------------------------------------------------------------------------
def download_statement(sid, table):
    try:
        if table == TBL_INCOME:
            df = pro.income(ts_code=sid)
        elif table == TBL_BALANCE:
            df = pro.balancesheet(ts_code=sid)
        elif table == TBL_CASH_FLOW:
            df = pro.cashflow(ts_code=sid)
        else:
            raise Exception("Unknown table")
    except Exception as e:
        logging.warning(e)
        return False

    standardize_statement_date(df)
    print(df.head())

    return DB.insert_data_frame(table, df)


# ----------------------------------------------------------------------------------------
# 获取三个表
def download_statements():
    all_stock = query_all_stock_list()
    for sid in all_stock['sid'].values:
        for table in [TBL_BALANCE, TBL_CASH_FLOW, TBL_INCOME]:
            while True:
                logging.info('downloading %s, %s ...' % (str(sid), table))
                success = download_statement(sid, table)
                if success is True:
                    break
                else:
                    logging.info('Timeout occurred, rest a second...')
                    time.sleep(1)
                    continue
            time.sleep(1 / (200 / 60) / 2)  # 每分钟内最多调取200次，单次传输时间比较长，实际上不用睡那么久


# ----------------------------------------------------------------------------------------
# 标准化日期
def standardize_tushare_date(df: pandas.DataFrame):
    if 'trade_date' in df.columns:
        print('standardise trade date')
        df['date'] = df['trade_date']
        df.drop('trade_date', axis=1, inplace=True)

    df['date'] = df['date'].apply(tushare_date_to_int)
    return df


def standardize_statement_date(df):
    replace_ts_code(df)
    df['ann_date'] = df['ann_date'].apply(tushare_date_to_int)
    df['f_ann_date'] = df['f_ann_date'].apply(tushare_date_to_int)
    df['end_date'] = df['end_date'].apply(tushare_date_to_int)


# ----------------------------------------------------------------------------------------
# tushare 日期转INT
def tushare_date_to_int(tushare_date):
    if tushare_date is None:
        return np.NAN
    return int(tushare_date)


# ----------------------------------------------------------------------------------------
def update_all_stock_daily():
    """
    # 更新每日股票、指数、基金数据
    ts_code	str	股票代码
    trade_date	str	交易日期
    open	float	开盘价
    high	float	最高价
    low	float	最低价
    close	float	收盘价
    pre_close	float	昨收价
    change	float	涨跌额
    pct_chg	float	涨跌幅 （未复权，如果是复权请用 通用行情接口 ）
    vol	float	成交量 （手）
    amount	float	成交额 （千元）
    """
    
    # 读取上次的最新日期
    last_day = DB.select(TBL_PRICE, field='max(date)', condition='asset_type=1')
    last_day = last_day.iloc[0, 0]
    if last_day is None:
        last_day = 19901201

    last_day = num2date(last_day)
    last_day += timedelta(days=1)

    today = date.today()
    while last_day < today:
        if last_day.weekday() > 4:  # weekend
            last_day += timedelta(days=1)
            continue

        the_date = '%04d%02d%02d' % (last_day.year, last_day.month, last_day.day)
        while True:
            logging.info('downloading %s, %s ...' % (str(last_day), last_day.weekday()))
            success = update_stock_daily(the_date)
            if success is True:
                break
            else:
                logging.info('Timeout occurred, rest a second...')
                time.sleep(1)
                continue
        time.sleep(1 / (200 / 60) / 2)  # 每分钟内最多调取200次，单次传输时间比较长，实际上不用睡那么久
        last_day += timedelta(days=1)

    # download_all_index_kline()
    # download_all_fund_kline()
    pass

