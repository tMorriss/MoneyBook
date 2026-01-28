import pandas as pd
from yaml_utils import create_db_connection, parse_db_arguments

db_host, db_port, db_user, db_password, db_database = parse_db_arguments()
con = create_db_connection(db_host, db_port, db_user, db_password, db_database)
result_str = ""

# 現在銀行
query = "SELECT * FROM moneybook_bankbalance ORDER BY id"
result = pd.read_sql(query, con)
for i_row in range(len(result)):
    result_str += "- model: moneybook.BankBalance\n"
    result_str += "  pk: " + str(result.iat[i_row, 0]) + "\n"
    result_str += "  fields:\n"
    result_str += "    name: " + str(result.iat[i_row, 1]) + "\n"
    result_str += "    price: " + str(result.iat[i_row, 2]) + "\n"
    result_str += "    show_order: " + str(result.iat[i_row, 3]) + "\n"
result_str += "\n"

# チェック
query = "SELECT * FROM moneybook_checkeddate ORDER BY id"
result = pd.read_sql(query, con)
for i_row in range(len(result)):
    result_str += "- model: moneybook.CheckedDate\n"
    result_str += "  pk: " + str(result.iat[i_row, 0]) + "\n"
    result_str += "  fields:\n"
    result_str += "    date: " + str(result.iat[i_row, 1]) + "\n"
    result_str += "    method_id: " + str(result.iat[i_row, 2]) + "\n"
result_str += "\n"

# クレジットチェック
query = "SELECT * FROM moneybook_creditcheckeddate ORDER BY id"
result = pd.read_sql(query, con)
for i_row in range(len(result)):
    result_str += "- model: moneybook.CreditCheckedDate\n"
    result_str += "  pk: " + str(result.iat[i_row, 0]) + "\n"
    result_str += "  fields:\n"
    result_str += "    name: " + str(result.iat[i_row, 1]) + "\n"
    result_str += "    date: " + str(result.iat[i_row, 2]) + "\n"
    result_str += "    price: " + str(result.iat[i_row, 3]) + "\n"
    result_str += "    show_order: " + str(result.iat[i_row, 3]) + "\n"
result_str += "\n"

# クレジットチェック
query = "SELECT * FROM moneybook_direction ORDER BY id"
result = pd.read_sql(query, con)
for i_row in range(len(result)):
    result_str += "- model: moneybook.Direction\n"
    result_str += "  pk: " + str(result.iat[i_row, 0]) + "\n"
    result_str += "  fields:\n"
    result_str += "    name: " + str(result.iat[i_row, 1]) + "\n"
result_str += "\n"

# ジャンル
query = "SELECT * FROM moneybook_category ORDER BY id"
result = pd.read_sql(query, con)
for i_row in range(len(result)):
    result_str += "- model: moneybook.Category\n"
    result_str += "  pk: " + str(result.iat[i_row, 0]) + "\n"
    result_str += "  fields:\n"
    result_str += "    name: " + str(result.iat[i_row, 1]) + "\n"
    result_str += "    show_order: " + str(result.iat[i_row, 2]) + "\n"
    result_str += "    is_living_cost: " + str(result.iat[i_row, 3]) + "\n"
    result_str += "    is_variable_cost: " + str(result.iat[i_row, 4]) + "\n"
result_str += "\n"

# 支払い方法
query = "SELECT * FROM moneybook_method ORDER BY id"
result = pd.read_sql(query, con)
for i_row in range(len(result)):
    result_str += "- model: moneybook.Method\n"
    result_str += "  pk: " + str(result.iat[i_row, 0]) + "\n"
    result_str += "  fields:\n"
    result_str += "    show_order: " + str(result.iat[i_row, 1]) + "\n"
    result_str += "    name: " + str(result.iat[i_row, 2]) + "\n"
    result_str += "    chargeable: " + str(result.iat[i_row, 3]) + "\n"
result_str += "\n"

# 諸々の価格
query = "SELECT * FROM moneybook_severalcosts ORDER BY id"
result = pd.read_sql(query, con)
for i_row in range(len(result)):
    result_str += "- model: moneybook.SeveralCosts\n"
    result_str += "  pk: " + str(result.iat[i_row, 0]) + "\n"
    result_str += "  fields:\n"
    result_str += "    name: " + str(result.iat[i_row, 1]) + "\n"
    result_str += "    price: " + str(result.iat[i_row, 2]) + "\n"
result_str += "\n"

print(result_str)
