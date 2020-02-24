
class AssetType(enumerate):
    """资产类别"""
    stock = 1
    index = 2
    fund = 3
    coin = 4
    future = 5


class CompanyType(enumerate):
    """
    公司类别
    (1一般工商业2银行3保险4证券)
    """
    industry = 1
    bank = 2
    insurance = 3
    security = 4


class StatementType(enumerate):
    """
    报告类型
    1合并报表 2单季合并 3调整单季合并表 4调整合并报表 5调整前合并报表 6母公司报表 7母公司单季表 8 母公司调整单季表
    9母公司调整表 10母公司调整前报表 11调整前合并报表 12母公司调整前报表
    """
    merged = 1
    quarter = 2
    quarter_adjusted_merged = 3
    adjusted_merged = 4
    pass


# ----------------------------------------------------------------------------------------
"""
输入参数

名称	类型	必选	描述
ts_code	str	Y	股票代码
ann_date	str	N	公告日期
start_date	str	N	公告开始日期
end_date	str	N	公告结束日期
period	str	N	报告期(每个季度最后一天的日期，比如20171231表示年报)
report_type	str	N	报告类型： 参考下表说明
comp_type	str	N	公司类型：1一般工商业 2银行 3保险 4证券

主要报表类型说明

代码	类型	说明
1	合并报表	上市公司最新报表（默认）
2	单季合并	单一季度的合并报表
3	调整单季合并表	调整后的单季合并报表（如果有）
4	调整合并报表	本年度公布上年同期的财务报表数据，报告期为上年度
5	调整前合并报表	数据发生变更，将原数据进行保留，即调整前的原数据
6	母公司报表	该公司母公司的财务报表数据
7	母公司单季表	母公司的单季度表
8	母公司调整单季表	母公司调整后的单季表
9	母公司调整表	该公司母公司的本年度公布上年同期的财务报表数据
10	母公司调整前报表	母公司调整之前的原始财务报表数据
11	调整前合并报表	调整之前合并报表原数据
12	母公司调整前报表	母公司报表发生变更前保留的原数据

"""

# 输出参数
# 名称	类型	默认显示	描述
INCOME_STATEMENT_DESCRIPTION = """
ann_date	int	Y	公告日期
f_ann_date	int	Y	实际公告日期
end_date	int	Y	报告期
report_type	tinyint	Y	报告类型 1合并报表 2单季合并 3调整单季合并表 4调整合并报表 5调整前合并报表 6母公司报表 7母公司单季表 8 母公司调整单季表 9母公司调整表 10母公司调整前报表 11调整前合并报表 12母公司调整前报表
comp_type	tinyint	Y	公司类型(1一般工商业2银行3保险4证券)
basic_eps	float	Y	基本每股收益
diluted_eps	float	Y	稀释每股收益
total_revenue	float	Y	营业总收入
revenue	float	Y	营业收入
int_income	float	Y	利息收入
prem_earned	float	Y	已赚保费
comm_income	float	Y	手续费及佣金收入
n_commis_income	float	Y	手续费及佣金净收入
n_oth_income	float	Y	其他经营净收益
n_oth_b_income	float	Y	加:其他业务净收益
prem_income	float	Y	保险业务收入
out_prem	float	Y	减:分出保费
une_prem_reser	float	Y	提取未到期责任准备金
reins_income	float	Y	其中:分保费收入
n_sec_tb_income	float	Y	代理买卖证券业务净收入
n_sec_uw_income	float	Y	证券承销业务净收入
n_asset_mg_income	float	Y	受托客户资产管理业务净收入
oth_b_income	float	Y	其他业务收入
fv_value_chg_gain	float	Y	加:公允价值变动净收益
invest_income	float	Y	加:投资净收益
ass_invest_income	float	Y	其中:对联营企业和合营企业的投资收益
forex_gain	float	Y	加:汇兑净收益
total_cogs	float	Y	营业总成本
oper_cost	float	Y	减:营业成本
int_exp	float	Y	减:利息支出
comm_exp	float	Y	减:手续费及佣金支出
biz_tax_surchg	float	Y	减:营业税金及附加
sell_exp	float	Y	减:销售费用
admin_exp	float	Y	减:管理费用
fin_exp	float	Y	减:财务费用
assets_impair_loss	float	Y	减:资产减值损失
prem_refund	float	Y	退保金
compens_payout	float	Y	赔付总支出
reser_insur_liab	float	Y	提取保险责任准备金
div_payt	float	Y	保户红利支出
reins_exp	float	Y	分保费用
oper_exp	float	Y	营业支出
compens_payout_refu	float	Y	减:摊回赔付支出
insur_reser_refu	float	Y	减:摊回保险责任准备金
reins_cost_refund	float	Y	减:摊回分保费用
other_bus_cost	float	Y	其他业务成本
operate_profit	float	Y	营业利润
non_oper_income	float	Y	加:营业外收入
non_oper_exp	float	Y	减:营业外支出
nca_disploss	float	Y	其中:减:非流动资产处置净损失
total_profit	float	Y	利润总额
income_tax	float	Y	所得税费用
n_income	float	Y	净利润(含少数股东损益)
n_income_attr_p	float	Y	净利润(不含少数股东损益)
minority_gain	float	Y	少数股东损益
oth_compr_income	float	Y	其他综合收益
t_compr_income	float	Y	综合收益总额
compr_inc_attr_p	float	Y	归属于母公司(或股东)的综合收益总额
compr_inc_attr_m_s	float	Y	归属于少数股东的综合收益总额
ebit	float	Y	息税前利润
ebitda	float	Y	息税折旧摊销前利润
insurance_exp	float	Y	保险业务支出
undist_profit	float	Y	年初未分配利润
distable_profit	float	Y	可分配利润
"""


BALANCE_STATEMENT_DESCRIPTION = """
ann_date	int	Y	公告日期
f_ann_date	int	Y	实际公告日期
end_date	int	Y	报告期
report_type	tinyint	Y	报告类型 1合并报表 2单季合并 3调整单季合并表 4调整合并报表 5调整前合并报表 6母公司报表 7母公司单季表 8 母公司调整单季表 9母公司调整表 10母公司调整前报表 11调整前合并报表 12母公司调整前报表
comp_type	tinyint	Y	公司类型(1一般工商业2银行3保险4证券)
total_share	float	Y	期末总股本
cap_rese	float	Y	资本公积金
undistr_porfit	float	Y	未分配利润
surplus_rese	float	Y	盈余公积金
special_rese	float	Y	专项储备
money_cap	float	Y	货币资金
trad_asset	float	Y	交易性金融资产
notes_receiv	float	Y	应收票据
accounts_receiv	float	Y	应收账款
oth_receiv	float	Y	其他应收款
prepayment	float	Y	预付款项
div_receiv	float	Y	应收股利
int_receiv	float	Y	应收利息
inventories	float	Y	存货
amor_exp	float	Y	待摊费用
nca_within_1y	float	Y	一年内到期的非流动资产
sett_rsrv	float	Y	结算备付金
loanto_oth_bank_fi	float	Y	拆出资金
premium_receiv	float	Y	应收保费
reinsur_receiv	float	Y	应收分保账款
reinsur_res_receiv	float	Y	应收分保合同准备金
pur_resale_fa	float	Y	买入返售金融资产
oth_cur_assets	float	Y	其他流动资产
total_cur_assets	float	Y	流动资产合计
fa_avail_for_sale	float	Y	可供出售金融资产
htm_invest	float	Y	持有至到期投资
lt_eqt_invest	float	Y	长期股权投资
invest_real_estate	float	Y	投资性房地产
time_deposits	float	Y	定期存款
oth_assets	float	Y	其他资产
lt_rec	float	Y	长期应收款
fix_assets	float	Y	固定资产
cip	float	Y	在建工程
const_materials	float	Y	工程物资
fixed_assets_disp	float	Y	固定资产清理
produc_bio_assets	float	Y	生产性生物资产
oil_and_gas_assets	float	Y	油气资产
intan_assets	float	Y	无形资产
r_and_d	float	Y	研发支出
goodwill	float	Y	商誉
lt_amor_exp	float	Y	长期待摊费用
defer_tax_assets	float	Y	递延所得税资产
decr_in_disbur	float	Y	发放贷款及垫款
oth_nca	float	Y	其他非流动资产
total_nca	float	Y	非流动资产合计
cash_reser_cb	float	Y	现金及存放中央银行款项
depos_in_oth_bfi	float	Y	存放同业和其它金融机构款项
prec_metals	float	Y	贵金属
deriv_assets	float	Y	衍生金融资产
rr_reins_une_prem	float	Y	应收分保未到期责任准备金
rr_reins_outstd_cla	float	Y	应收分保未决赔款准备金
rr_reins_lins_liab	float	Y	应收分保寿险责任准备金
rr_reins_lthins_liab	float	Y	应收分保长期健康险责任准备金
refund_depos	float	Y	存出保证金
ph_pledge_loans	float	Y	保户质押贷款
refund_cap_depos	float	Y	存出资本保证金
indep_acct_assets	float	Y	独立账户资产
client_depos	float	Y	其中：客户资金存款
client_prov	float	Y	其中：客户备付金
transac_seat_fee	float	Y	其中:交易席位费
invest_as_receiv	float	Y	应收款项类投资
total_assets	float	Y	资产总计
lt_borr	float	Y	长期借款
st_borr	float	Y	短期借款
cb_borr	float	Y	向中央银行借款
depos_ib_deposits	float	Y	吸收存款及同业存放
loan_oth_bank	float	Y	拆入资金
trading_fl	float	Y	交易性金融负债
notes_payable	float	Y	应付票据
acct_payable	float	Y	应付账款
adv_receipts	float	Y	预收款项
sold_for_repur_fa	float	Y	卖出回购金融资产款
comm_payable	float	Y	应付手续费及佣金
payroll_payable	float	Y	应付职工薪酬
taxes_payable	float	Y	应交税费
int_payable	float	Y	应付利息
div_payable	float	Y	应付股利
oth_payable	float	Y	其他应付款
acc_exp	float	Y	预提费用
deferred_inc	float	Y	递延收益
st_bonds_payable	float	Y	应付短期债券
payable_to_reinsurer	float	Y	应付分保账款
rsrv_insur_cont	float	Y	保险合同准备金
acting_trading_sec	float	Y	代理买卖证券款
acting_uw_sec	float	Y	代理承销证券款
non_cur_liab_due_1y	float	Y	一年内到期的非流动负债
oth_cur_liab	float	Y	其他流动负债
total_cur_liab	float	Y	流动负债合计
bond_payable	float	Y	应付债券
lt_payable	float	Y	长期应付款
specific_payables	float	Y	专项应付款
estimated_liab	float	Y	预计负债
defer_tax_liab	float	Y	递延所得税负债
defer_inc_non_cur_liab	float	Y	递延收益-非流动负债
oth_ncl	float	Y	其他非流动负债
total_ncl	float	Y	非流动负债合计
depos_oth_bfi	float	Y	同业和其它金融机构存放款项
deriv_liab	float	Y	衍生金融负债
depos	float	Y	吸收存款
agency_bus_liab	float	Y	代理业务负债
oth_liab	float	Y	其他负债
prem_receiv_adva	float	Y	预收保费
depos_received	float	Y	存入保证金
ph_invest	float	Y	保户储金及投资款
reser_une_prem	float	Y	未到期责任准备金
reser_outstd_claims	float	Y	未决赔款准备金
reser_lins_liab	float	Y	寿险责任准备金
reser_lthins_liab	float	Y	长期健康险责任准备金
indept_acc_liab	float	Y	独立账户负债
pledge_borr	float	Y	其中:质押借款
indem_payable	float	Y	应付赔付款
policy_div_payable	float	Y	应付保单红利
total_liab	float	Y	负债合计
treasury_share	float	Y	减:库存股
ordin_risk_reser	float	Y	一般风险准备
forex_differ	float	Y	外币报表折算差额
invest_loss_unconf	float	Y	未确认的投资损失
minority_int	float	Y	少数股东权益
total_hldr_eqy_exc_min_int	float	Y	股东权益合计(不含少数股东权益)
total_hldr_eqy_inc_min_int	float	Y	股东权益合计(含少数股东权益)
total_liab_hldr_eqy	float	Y	负债及股东权益总计
lt_payroll_payable	float	Y	长期应付职工薪酬
oth_comp_income	float	Y	其他综合收益
oth_eqt_tools	float	Y	其他权益工具
oth_eqt_tools_p_shr	float	Y	其他权益工具(优先股)
lending_funds	float	Y	融出资金
acc_receivable	float	Y	应收款项
st_fin_payable	float	Y	应付短期融资款
payables	float	Y	应付款项
hfs_assets	float	Y	持有待售的资产
hfs_sales	float	Y	持有待售的负债
"""

CASH_FLOW_STATEMENT_DESCRIPTION = """
ann_date	int	Y	公告日期
f_ann_date	int	Y	实际公告日期
end_date	int	Y	报告期
report_type	tinyint	Y	报告类型 1合并报表 2单季合并 3调整单季合并表 4调整合并报表 5调整前合并报表 6母公司报表 7母公司单季表 8 母公司调整单季表 9母公司调整表 10母公司调整前报表 11调整前合并报表 12母公司调整前报表
comp_type	tinyint	Y	公司类型(1一般工商业2银行3保险4证券)
net_profit	float	Y	净利润
finan_exp	float	Y	财务费用
c_fr_sale_sg	float	Y	销售商品、提供劳务收到的现金
recp_tax_rends	float	Y	收到的税费返还
n_depos_incr_fi	float	Y	客户存款和同业存放款项净增加额
n_incr_loans_cb	float	Y	向中央银行借款净增加额
n_inc_borr_oth_fi	float	Y	向其他金融机构拆入资金净增加额
prem_fr_orig_contr	float	Y	收到原保险合同保费取得的现金
n_incr_insured_dep	float	Y	保户储金净增加额
n_reinsur_prem	float	Y	收到再保业务现金净额
n_incr_disp_tfa	float	Y	处置交易性金融资产净增加额
ifc_cash_incr	float	Y	收取利息和手续费净增加额
n_incr_disp_faas	float	Y	处置可供出售金融资产净增加额
n_incr_loans_oth_bank	float	Y	拆入资金净增加额
n_cap_incr_repur	float	Y	回购业务资金净增加额
c_fr_oth_operate_a	float	Y	收到其他与经营活动有关的现金
c_inf_fr_operate_a	float	Y	经营活动现金流入小计
c_paid_goods_s	float	Y	购买商品、接受劳务支付的现金
c_paid_to_for_empl	float	Y	支付给职工以及为职工支付的现金
c_paid_for_taxes	float	Y	支付的各项税费
n_incr_clt_loan_adv	float	Y	客户贷款及垫款净增加额
n_incr_dep_cbob	float	Y	存放央行和同业款项净增加额
c_pay_claims_orig_inco	float	Y	支付原保险合同赔付款项的现金
pay_handling_chrg	float	Y	支付手续费的现金
pay_comm_insur_plcy	float	Y	支付保单红利的现金
oth_cash_pay_oper_act	float	Y	支付其他与经营活动有关的现金
st_cash_out_act	float	Y	经营活动现金流出小计
n_cashflow_act	float	Y	经营活动产生的现金流量净额
oth_recp_ral_inv_act	float	Y	收到其他与投资活动有关的现金
c_disp_withdrwl_invest	float	Y	收回投资收到的现金
c_recp_return_invest	float	Y	取得投资收益收到的现金
n_recp_disp_fiolta	float	Y	处置固定资产、无形资产和其他长期资产收回的现金净额
n_recp_disp_sobu	float	Y	处置子公司及其他营业单位收到的现金净额
stot_inflows_inv_act	float	Y	投资活动现金流入小计
c_pay_acq_const_fiolta	float	Y	购建固定资产、无形资产和其他长期资产支付的现金
c_paid_invest	float	Y	投资支付的现金
n_disp_subs_oth_biz	float	Y	取得子公司及其他营业单位支付的现金净额
oth_pay_ral_inv_act	float	Y	支付其他与投资活动有关的现金
n_incr_pledge_loan	float	Y	质押贷款净增加额
stot_out_inv_act	float	Y	投资活动现金流出小计
n_cashflow_inv_act	float	Y	投资活动产生的现金流量净额
c_recp_borrow	float	Y	取得借款收到的现金
proc_issue_bonds	float	Y	发行债券收到的现金
oth_cash_recp_ral_fnc_act	float	Y	收到其他与筹资活动有关的现金
stot_cash_in_fnc_act	float	Y	筹资活动现金流入小计
free_cashflow	float	Y	企业自由现金流量
c_prepay_amt_borr	float	Y	偿还债务支付的现金
c_pay_dist_dpcp_int_exp	float	Y	分配股利、利润或偿付利息支付的现金
incl_dvd_profit_paid_sc_ms	float	Y	其中:子公司支付给少数股东的股利、利润
oth_cashpay_ral_fnc_act	float	Y	支付其他与筹资活动有关的现金
stot_cashout_fnc_act	float	Y	筹资活动现金流出小计
n_cash_flows_fnc_act	float	Y	筹资活动产生的现金流量净额
eff_fx_flu_cash	float	Y	汇率变动对现金的影响
n_incr_cash_cash_equ	float	Y	现金及现金等价物净增加额
c_cash_equ_beg_period	float	Y	期初现金及现金等价物余额
c_cash_equ_end_period	float	Y	期末现金及现金等价物余额
c_recp_cap_contrib	float	Y	吸收投资收到的现金
incl_cash_rec_saims	float	Y	其中:子公司吸收少数股东投资收到的现金
uncon_invest_loss	float	Y	未确认投资损失
prov_depr_assets	float	Y	加:资产减值准备
depr_fa_coga_dpba	float	Y	固定资产折旧、油气资产折耗、生产性生物资产折旧
amort_intang_assets	float	Y	无形资产摊销
lt_amort_deferred_exp	float	Y	长期待摊费用摊销
decr_deferred_exp	float	Y	待摊费用减少
incr_acc_exp	float	Y	预提费用增加
loss_disp_fiolta	float	Y	处置固定、无形资产和其他长期资产的损失
loss_scr_fa	float	Y	固定资产报废损失
loss_fv_chg	float	Y	公允价值变动损失
invest_loss	float	Y	投资损失
decr_def_inc_tax_assets	float	Y	递延所得税资产减少
incr_def_inc_tax_liab	float	Y	递延所得税负债增加
decr_inventories	float	Y	存货的减少
decr_oper_payable	float	Y	经营性应收项目的减少
incr_oper_payable	float	Y	经营性应付项目的增加
others	float	Y	其他
im_net_cashflow_oper_act	float	Y	经营活动产生的现金流量净额(间接法)
conv_debt_into_cap	float	Y	债务转为资本
conv_copbonds_due_within_1y	float	Y	一年内到期的可转换公司债券
fa_fnc_leases	float	Y	融资租入固定资产
end_bal_cash	float	Y	现金的期末余额
beg_bal_cash	float	Y	减:现金的期初余额
end_bal_cash_equ	float	Y	加:现金等价物的期末余额
beg_bal_cash_equ	float	Y	减:现金等价物的期初余额
im_n_incr_cash_equ	float	Y	现金及现金等价物净增加额(间接法)
"""

DIVIDEND_DESCRIPTION = """
end_date	int	Y	分红年度
ann_date	int	Y	预案公告日
record_date	int	Y	股权登记日
ex_date	int	Y	除权除息日
pay_date	int	Y	派息日
div_listdate	int	Y	红股上市日
imp_ann_date	int	Y	实施公告日
base_date	int	N	基准日
base_share	float	N	基准股本（万）
div_proc	str	Y	实施进度
stk_div	float	Y	每股送转
stk_bo_rate	float	Y	每股送股比例
stk_co_rate	float	Y	每股转增比例
cash_div	float	Y	每股分红（税后）
cash_div_tax	float	Y	每股分红（税前）"""


def init_statement_field_map(statement_description):
    lines = statement_description.split('\n')
    fields_map = dict()
    for line in lines:
        if line == '':
            continue
        # print(line)
        structs = line.split('\t')
        key = structs[0]
        fields_map[key] = dict()
        fields_map[key]['type'] = structs[1]
        fields_map[key]['description'] = structs[3]

    return fields_map


# 字段映射
BALANCE_FIELD_MAP = init_statement_field_map(INCOME_STATEMENT_DESCRIPTION)
BALANCE_FIELD_MAP = init_statement_field_map(BALANCE_STATEMENT_DESCRIPTION)
CASH_FLOW_FIELD_MAP = init_statement_field_map(CASH_FLOW_STATEMENT_DESCRIPTION)

