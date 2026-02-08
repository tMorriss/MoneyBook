import pandas as pd
from yaml_utils import create_db_connection, parse_db_credentials_from_stdin

db_host, db_port, db_user, db_password, db_database = parse_db_credentials_from_stdin()
con = create_db_connection(db_host, db_port, db_user, db_password, db_database)
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
