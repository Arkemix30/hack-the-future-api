from datetime import datetime as dt


def next_month():
    return dt(year=dt.now().year, month=dt.now().month + 1, day=1)
