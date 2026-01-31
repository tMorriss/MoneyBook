import sys

import pandas as pd
from mysql.connector import connect

# Read database credentials from stdin (one per line)
lines = sys.stdin.read().strip().split('\n')
if len(lines) < 5:
    print("Error: Missing required credentials from stdin", file=sys.stderr)
    print("Expected 5 lines: hostname, port, username, password, database", file=sys.stderr)
    sys.exit(1)

db_host = lines[0].strip()
try:
    db_port = int(lines[1].strip())
except ValueError:
    print("Error: Port must be a valid integer", file=sys.stderr)
    sys.exit(1)
db_user = lines[2].strip()
db_password = lines[3].strip()
db_database = lines[4].strip()

con = connect(host=db_host, port=db_port, user=db_user,
              password=db_password,
              database=db_database)
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
