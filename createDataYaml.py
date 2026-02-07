import sys

import pandas as pd
from mysql.connector import connect

# 標準入力からデータベース認証情報を読み込む（1行ずつ）
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
query = "SELECT * FROM moneybook_data ORDER BY id"
result = pd.read_sql(query, con)
result_str = ""
for i_row in range(len(result)):

    result_str += "- model: moneybook.Data\n"
    result_str += "  pk: " + str(i_row + 1) + "\n"
    result_str += "  fields: \n"
    result_str += "    date: " + str(result.iat[i_row, 1]) + "\n"
    result_str += "    item: " + str(result.iat[i_row, 2]).replace("amp;", "") + "\n"
    result_str += "    price: " + str(result.iat[i_row, 3]) + "\n"
    result_str += "    temp: " + str(result.iat[i_row, 4]) + "\n"
    result_str += "    checked: " + str(result.iat[i_row, 5]) + "\n"
    result_str += "    direction_id: " + str(result.iat[i_row, 6]) + "\n"
    result_str += "    category_id: " + str(result.iat[i_row, 7]) + "\n"
    result_str += "    method_id: " + str(result.iat[i_row, 8]) + "\n"
print(result_str)
