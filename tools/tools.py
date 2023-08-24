from datetime import datetime, timedelta
from datetime import datetime


def from_unixtime_sec(unixtime):
    """
    Converte um timestamp Unix em segundos em uma string de data e hora no formato 'YYYY-MM-DD HH:MM:SS'.

    Args:
        unixtime (int): O timestamp Unix em segundos a ser convertido.

    Returns:
        str or None: A string de data e hora formatada correspondente ao timestamp Unix fornecido,
                     ou None se o valor do timestamp estiver inválido.

    Examples:
        >>> from_unixtime_sec(1609545600)
        '2021-01-02 00:00:00'

        >>> from_unixtime_sec(1672531200)
        '2023-01-01 00:00:00'

        >>> from_unixtime_sec("invalid_timestamp")
        None
    """
    try:
        datetime_obj = datetime.fromtimestamp(unixtime)
        formatted_date = datetime_obj.strftime('%Y-%m-%d %H:%M:%S')
        return formatted_date
    except ValueError:
        return None


async def to_unixtime_sec(date):
    """
    Converte uma string de data no formato 'YYYY-MM-DD' em um timestamp Unix em Segundos.

    Args:
        date (str): Uma string contendo a data no formato 'YYYY-MM-DD'.

    Returns:
        int or None: O timestamp Unix em Segundos correspondente à data fornecida,
                    ou None se a string de data estiver em um formato inválido.

    Examples:
        >>> to_unixtime_sec("2023-01-01")
        1672531200

        >>> to_unixtime_sec("2023-08-20")
        1679443200

        >>> to_unixtime_sec("invalid_date")
        None
    """
    try:
        datetime_obj = datetime.strptime(date, '%Y-%m-%d')
        unixtime_sec = int(datetime_obj.timestamp())
        return unixtime_sec
    except ValueError:
        return None


def generate_date_ranges(start_date, end_date, size):
    date_format = "%Y-%m-%d"
    date_ranges = []

    current_date = datetime.strptime(start_date, date_format)
    end_date_obj = datetime.strptime(end_date, date_format)

    while current_date <= end_date_obj:
        date_ranges.append((current_date.strftime(date_format), (current_date + timedelta(days=size-1)).strftime(date_format)))
        current_date += timedelta(days=size)

    return date_ranges


if __name__ == '__main__':
    # Exemplos de uso
    start_date = '2021-01-01'
    end_date = '2021-01-31'
    start_unixtime = to_unixtime_sec(start_date)
    end_unixtime = to_unixtime_sec(end_date)
    print(f"start_unixtime: {start_unixtime}")
    print(f"end_unixtime: {end_unixtime}")

    start_date = from_unixtime_sec(start_unixtime)
    print(f"start_date: {start_date}")
