from datetime import date


def is_valid_date(year, month):
    try:
        date(int(year), int(month), 1)
        return True
    except ValueError:
        return False
