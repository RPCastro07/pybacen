from datetime import datetime

def date_validator(date: str, format: str, format_converter: str) -> str:
    try:
        date = datetime.strptime(date, format)

        return date.strftime(format_converter)

    except ValueError:
        raise ValueError(f"'{date}' is not date or does not match format '{format}'")

def compare_dates(start: str, end: str, format: str) -> str:
    try:

        start = datetime.strptime(start, '%Y-%m-%d')
        end = datetime.strptime(end, '%Y-%m-%d')

    except ValueError:
        raise ValueError(f"Is not date or does not match format '{format}'")

    if start <= end:
        return True
    else:
        raise AttributeError('end date less than start date')

def to_date(date: str, format: str, format_converter: str) -> str:
    try:
        date = datetime.strptime(date, format)

        return date

    except ValueError:
        raise ValueError(f"'{date}' is not date or does not match format '{format}'")


def to_timestamp(date: str, format: str) -> str:
    try:
        date = datetime.strptime(date, format)

        return datetime.timestamp(date)

    except ValueError:
        raise ValueError(f"'{date}' is not date or does not match format '{format}'")

def sysdate(format: str) -> str:
    return datetime.now().strftime(format)