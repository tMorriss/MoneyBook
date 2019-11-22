import pandas as pd
import mysql.connector

con = mysql.connector.connect(host='localhost', port=3306, user='moneybook', password='want2money', database='moneybook')
query = "SELECT * FROM data ORDER BY id"
result = pd.read_sql(query, con)
resultStr = ""
for iRow in range(len(result)):
    
    genre = result.iat[iRow, 6]
    if genre == 0:
        genre = 8
    elif genre == -1:
        genre = 9
    elif genre == -2:
        genre = 10
    elif genre == -3:
        genre = 11
    elif genre == -4:
        genre = 12

    resultStr += "- model: moneybook.data\n"
    resultStr += "  pk: " + str(iRow + 1) + "\n"
    resultStr += "  fields: \n"
    resultStr += "    date: " + str(result.iat[iRow, 1]) + "\n"
    resultStr += "    item: " + str(result.iat[iRow, 2]).replace("amp;","") + "\n"
    resultStr += "    price: " + str(result.iat[iRow, 3]) + "\n"
    resultStr += "    method: " + str(result.iat[iRow, 4]) + "\n"
    resultStr += "    direction: " + str(result.iat[iRow, 5] + 1) + "\n"
    resultStr += "    genre: " + str(genre) + "\n"
    resultStr += "    temp: " + str(result.iat[iRow, 7]) + "\n"
    resultStr += "    checked: " + str(result.iat[iRow, 8]) + "\n"
print(resultStr)
