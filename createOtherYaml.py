import pandas as pd
import mysql.connector

con = mysql.connector.connect(host='localhost', port=3306, user='moneybooker', password='want2money', database='moneybook_django')
resultStr = ""

# 現在銀行
query = "SELECT * FROM moneybook_bankbalance ORDER BY id"
result = pd.read_sql(query, con)
for iRow in range(len(result)):
    resultStr += "- model: moneybook.BankBalance\n"
    resultStr += "  pk: " + str(result.iat[iRow, 0]) + "\n"
    resultStr += "  fields: \n"
    resultStr += "    name: " + str(result.iat[iRow, 1]) + "\n"
    resultStr += "    price: " + str(result.iat[iRow, 2]) + "\n"
    resultStr += "    show_order: " + str(result.iat[iRow, 3]) + "\n"
resultStr += "\n"

# キャシュバックチェック
query = "SELECT * FROM moneybook_cachebackcheckeddate ORDER BY id"
result = pd.read_sql(query, con)
for iRow in range(len(result)):
    resultStr += "- model: moneybook.CachebackCheckedDate\n"
    resultStr += "  pk: " + str(result.iat[iRow, 0]) + "\n"
    resultStr += "  fields: \n"
    resultStr += "    show_order: " + str(result.iat[iRow, 1]) + "\n"
    resultStr += "    name: " + str(result.iat[iRow, 2]) + "\n"
    resultStr += "    date: " + str(result.iat[iRow, 3]) + "\n"
resultStr += "\n"

# チェック
query = "SELECT * FROM moneybook_checkeddate ORDER BY id"
result = pd.read_sql(query, con)
for iRow in range(len(result)):
    resultStr += "- model: moneybook.CheckedDate\n"
    resultStr += "  pk: " + str(result.iat[iRow, 0]) + "\n"
    resultStr += "  fields: \n"
    resultStr += "    date: " + str(result.iat[iRow, 1]) + "\n"
    resultStr += "    method_id: " + str(result.iat[iRow, 2]) + "\n"
resultStr += "\n"

# クレジットチェック
query = "SELECT * FROM moneybook_creditcheckeddate ORDER BY id"
result = pd.read_sql(query, con)
for iRow in range(len(result)):
    resultStr += "- model: moneybook.CreditCheckedDate\n"
    resultStr += "  pk: " + str(result.iat[iRow, 0]) + "\n"
    resultStr += "  fields: \n"
    resultStr += "    name: " + str(result.iat[iRow, 1]) + "\n"
    resultStr += "    date: " + str(result.iat[iRow, 2]) + "\n"
    resultStr += "    price: " + str(result.iat[iRow, 3]) + "\n"
    resultStr += "    show_order: " + str(result.iat[iRow, 3]) + "\n"
resultStr += "\n"

# クレジットチェック
query = "SELECT * FROM moneybook_direction ORDER BY id"
result = pd.read_sql(query, con)
for iRow in range(len(result)):
    resultStr += "- model: moneybook.Direction\n"
    resultStr += "  pk: " + str(result.iat[iRow, 0]) + "\n"
    resultStr += "  fields: \n"
    resultStr += "    name: " + str(result.iat[iRow, 1]) + "\n"
resultStr += "\n"

# ジャンル
query = "SELECT * FROM moneybook_genre ORDER BY id"
result = pd.read_sql(query, con)
for iRow in range(len(result)):
    resultStr += "- model: moneybook.Genre\n"
    resultStr += "  pk: " + str(result.iat[iRow, 0]) + "\n"
    resultStr += "  fields: \n"
    resultStr += "    name: " + str(result.iat[iRow, 1]) + "\n"
    resultStr += "    show_order: " + str(result.iat[iRow, 2]) + "\n"
resultStr += "\n"

# 支払い方法
query = "SELECT * FROM moneybook_method ORDER BY id"
result = pd.read_sql(query, con)
for iRow in range(len(result)):
    resultStr += "- model: moneybook.Method\n"
    resultStr += "  pk: " + str(result.iat[iRow, 0]) + "\n"
    resultStr += "  fields: \n"
    resultStr += "    show_order: " + str(result.iat[iRow, 1]) + "\n"
    resultStr += "    name: " + str(result.iat[iRow, 2]) + "\n"
    resultStr += "    chargeable: " + str(result.iat[iRow, 3]) + "\n"
resultStr += "\n"

# 諸々の価格
query = "SELECT * FROM moneybook_severalcosts ORDER BY id"
result = pd.read_sql(query, con)
for iRow in range(len(result)):
    resultStr += "- model: moneybook.SeveralCosts\n"
    resultStr += "  pk: " + str(result.iat[iRow, 0]) + "\n"
    resultStr += "  fields: \n"
    resultStr += "    name: " + str(result.iat[iRow, 1]) + "\n"
    resultStr += "    price: " + str(result.iat[iRow, 2]) + "\n"
resultStr += "\n"

print(resultStr)