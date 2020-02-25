import data_source as ds
from gold_db import *
from util import *

# ----------------------------------------------------------------------------------------
if __name__ == '__main__':
    init_logging()
    db = GoldDb()
    ds.set_db(db)

    # db.test_database()
    # ds.update_all_stock_daily()
    # ds.delete_old_index_price()
    # ds.download_all_index_kline()
    # ds.download_all_fund_kline()
    # ds.test_index_id_unique()
    # ds.test_plot_index()
    # ds.download_all_dividend()


