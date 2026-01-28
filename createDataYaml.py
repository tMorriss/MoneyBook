import sys

import pandas as pd
from mysql.connector import connect

if len(sys.argv) < 6:
    print("Error: Missing required arguments", file=sys.stderr)
    print("Usage: python3 createDataYaml.py <hostname> <port> <user> <password> <database>", file=sys.stderr)
    sys.exit(1)

db_host = sys.argv[1]
db_port = int(sys.argv[2])
db_user = sys.argv[3]
db_password = sys.argv[4]
db_database = sys.argv[5]

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
