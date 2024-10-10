def _is_date_valid_today(date):
    try:
        return date <= date.today()
    except ValueError:
        return False
    except TypeError:
        return False
