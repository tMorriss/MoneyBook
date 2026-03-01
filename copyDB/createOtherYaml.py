import pandas as pd
import yaml
from yaml_utils import create_db_connection, parse_db_credentials_from_stdin

db_host, db_port, db_user, db_password, db_database = parse_db_credentials_from_stdin()
con = create_db_connection(db_host, db_port, db_user, db_password, db_database)
data = []

# 現在銀行
query = 'SELECT * FROM moneybook_bankbalance ORDER BY id'
result = pd.read_sql(query, con)
for i_row in range(len(result)):
    data.append({
        'model': 'moneybook.BankBalance',
        'pk': int(result.iat[i_row, 0]),
        'fields': {
            'name': str(result.iat[i_row, 1]),
            'price': int(result.iat[i_row, 2]),
            'show_order': int(result.iat[i_row, 3]),
        }
    })

# チェック
query = 'SELECT * FROM moneybook_checkeddate ORDER BY id'
result = pd.read_sql(query, con)
for i_row in range(len(result)):
    data.append({
        'model': 'moneybook.CheckedDate',
        'pk': int(result.iat[i_row, 0]),
        'fields': {
            'date': str(result.iat[i_row, 1]),
            'method_id': int(result.iat[i_row, 2]),
        }
    })

# クレジットチェック
query = 'SELECT * FROM moneybook_creditcheckeddate ORDER BY id'
result = pd.read_sql(query, con)
for i_row in range(len(result)):
    data.append({
        'model': 'moneybook.CreditCheckedDate',
        'pk': int(result.iat[i_row, 0]),
        'fields': {
            'name': str(result.iat[i_row, 1]),
            'date': str(result.iat[i_row, 2]),
            'price': int(result.iat[i_row, 3]),
            'show_order': int(result.iat[i_row, 4]),
        }
    })

# 方向（Direction）
query = 'SELECT * FROM moneybook_direction ORDER BY id'
result = pd.read_sql(query, con)
for i_row in range(len(result)):
    data.append({
        'model': 'moneybook.Direction',
        'pk': int(result.iat[i_row, 0]),
        'fields': {
            'name': str(result.iat[i_row, 1]),
        }
    })

# ジャンル
query = 'SELECT * FROM moneybook_category ORDER BY id'
result = pd.read_sql(query, con)
for i_row in range(len(result)):
    data.append({
        'model': 'moneybook.Category',
        'pk': int(result.iat[i_row, 0]),
        'fields': {
            'name': str(result.iat[i_row, 1]),
            'show_order': int(result.iat[i_row, 2]),
            'is_living_cost': bool(result.iat[i_row, 3]),
            'is_variable_cost': bool(result.iat[i_row, 4]),
        }
    })

# 支払い方法
query = 'SELECT * FROM moneybook_method ORDER BY id'
result = pd.read_sql(query, con)
for i_row in range(len(result)):
    data.append({
        'model': 'moneybook.Method',
        'pk': int(result.iat[i_row, 0]),
        'fields': {
            'show_order': int(result.iat[i_row, 1]),
            'name': str(result.iat[i_row, 2]),
            'chargeable': bool(result.iat[i_row, 3]),
        }
    })

# 諸々の価格
query = 'SELECT * FROM moneybook_severalcosts ORDER BY id'
result = pd.read_sql(query, con)
for i_row in range(len(result)):
    data.append({
        'model': 'moneybook.SeveralCosts',
        'pk': int(result.iat[i_row, 0]),
        'fields': {
            'name': str(result.iat[i_row, 1]),
            'price': int(result.iat[i_row, 2]),
        }
    })

print(yaml.dump(data, allow_unicode=True, sort_keys=False))
