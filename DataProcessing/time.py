from datetime import datetime


def days_apart(d1, d2):
    return abs(to_datetime(d1) - to_datetime(d2)).days


def to_datetime(date: str):
    d, m, y = date.split(".")
    return datetime(int(y), int(m), int(d))
