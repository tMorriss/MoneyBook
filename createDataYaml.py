import pandas as pd
import mysql.connector

con = mysql.connector.connect(host='localhost', port=3306, user='moneybook', password='want2money', database='moneybook_django')
query = "SELECT * FROM moneybook_data ORDER BY id"
result = pd.read_sql(query, con)
resultStr = ""
for iRow in range(len(result)):
    
    resultStr += "- model: moneybook.Data\n"
    resultStr += "  pk: " + str(iRow + 1) + "\n"
    resultStr += "  fields: \n"
    resultStr += "    date: " + str(result.iat[iRow, 1]) + "\n"
    resultStr += "    item: " + str(result.iat[iRow, 2]).replace("amp;","") + "\n"
    resultStr += "    price: " + str(result.iat[iRow, 3]) + "\n"
    resultStr += "    temp: " + str(result.iat[iRow, 4]) + "\n"
    resultStr += "    checked: " + str(result.iat[iRow, 5]) + "\n"
    resultStr += "    direction_id: " + str(result.iat[iRow, 6]) + "\n"
    resultStr += "    genre_id: " + str(result.iat[iRow, 7]) + "\n"
    resultStr += "    method_id: " + str(result.iat[iRow, 8]) + "\n"
print(resultStr)
