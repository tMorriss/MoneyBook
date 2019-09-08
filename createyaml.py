import pandas as pd
import mysql.connector

con = mysql.connector.connect(host='localhost', port=3306, user='moneybook', password='want2money', database='moneybook')
query = "SELECT * FROM data WHERE date_format(date, '%Y-%m')='2019-08' ORDER BY date"
result = pd.read_sql(query, con)
resultStr = ""
for iRow in range(len(result)):
    resultStr += "- model: web.data\n"
    resultStr += "  pk: " + str(iRow + 1) + "\n"
    resultStr += "  fields: \n"
    resultStr += "    date: " + str(result.iat[iRow, 1]) + "\n"
    resultStr += "    item: " + str(result.iat[iRow, 2]) + "\n"
    resultStr += "    price: " + str(result.iat[iRow, 3]) + "\n"
    resultStr += "    method: " + str(result.iat[iRow, 4]) + "\n"
    resultStr += "    direction: " + str(result.iat[iRow, 5]) + "\n"
    resultStr += "    genre: " + str(result.iat[iRow, 6]) + "\n"
    resultStr += "    temp: " + str(result.iat[iRow, 7]) + "\n"
    resultStr += "    checked: " + str(result.iat[iRow, 8]) + "\n"
print(resultStr)
