"""Shared utilities for creating YAML fixture files from MySQL database."""
import sys

from mysql.connector import connect


def parse_db_credentials_from_stdin():
    """標準入力からデータベース認証情報を読み込む（1行ずつ）

    Returns:
        tuple: (db_host, db_port, db_user, db_password, db_database)

    Raises:
        SystemExit: If required credentials are missing or invalid.
    """
    lines = sys.stdin.read().strip().split('\n')
    if len(lines) < 5:
        print('Error: Missing required credentials from stdin', file=sys.stderr)
        print('Expected 5 lines: hostname, port, username, password, database', file=sys.stderr)
        sys.exit(1)

    db_host = lines[0].strip()
    try:
        db_port = int(lines[1].strip())
    except ValueError:
        print('Error: Port must be a valid integer', file=sys.stderr)
        sys.exit(1)
    db_user = lines[2].strip()
    db_password = lines[3].strip()
    db_database = lines[4].strip()

    return db_host, db_port, db_user, db_password, db_database


def create_db_connection(db_host, db_port, db_user, db_password, db_database):
    """Create a connection to MySQL database.

    Args:
        db_host: Database hostname
        db_port: Database port number
        db_user: Database username
        db_password: Database password
        db_database: Database name

    Returns:
        mysql.connector.connection.MySQLConnection: MySQL database connection object

    Raises:
        mysql.connector.Error: If the connection fails
    """
    try:
        return connect(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_password,
            database=db_database
        )
    except Exception as e:
        print(f'Error: Failed to connect to database: {e}', file=sys.stderr)
        sys.exit(1)
