import pandas as pd
import yaml
from yaml_utils import create_db_connection, parse_db_credentials_from_stdin

db_host, db_port, db_user, db_password, db_database = parse_db_credentials_from_stdin()
con = create_db_connection(db_host, db_port, db_user, db_password, db_database)
query = 'SELECT * FROM moneybook_data ORDER BY id'
result = pd.read_sql(query, con)

data = []
for i_row in range(len(result)):
    data.append({
        'model': 'moneybook.Data',
        'pk': i_row + 1,
        'fields': {
            'date': str(result.iat[i_row, 1]),
            'item': str(result.iat[i_row, 2]).replace('amp;', ''),
            'price': int(result.iat[i_row, 3]),
            'temp': bool(result.iat[i_row, 4]),
            'checked': bool(result.iat[i_row, 5]),
            'direction_id': int(result.iat[i_row, 6]),
            'category_id': int(result.iat[i_row, 7]),
            'method_id': int(result.iat[i_row, 8]),
        }
    })

print(yaml.dump(data, allow_unicode=True, sort_keys=False))
