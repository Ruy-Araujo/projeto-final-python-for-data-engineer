from datetime import datetime


def from_unixtime(unixtime):
    """
    Converte um timestamp Unix em milissegundos em uma string de data e hora no formato 'YYYY-MM-DD HH:MM:SS'.

    Args:
        unixtime (int): O timestamp Unix em milissegundos a ser convertido.

    Returns:
        str or None: A string de data e hora formatada correspondente ao timestamp Unix fornecido,
                     ou None se o valor do timestamp estiver inválido.

    Examples:
        >>> from_unixtime(1609545600000)
        '2021-01-02 00:00:00'

        >>> from_unixtime(1672531200000)
        '2023-01-01 00:00:00'

        >>> from_unixtime("invalid_timestamp")
        None
    """
    try:
        unixtime_seconds = unixtime / 1000
        datetime_obj = datetime.fromtimestamp(unixtime_seconds)
        formatted_date = datetime_obj.strftime('%Y-%m-%d %H:%M:%S')
        return formatted_date
    except ValueError:
        return None


def to_unixtime(date):
    """
    Converte uma string de data no formato 'YYYY-MM-DD' em um timestamp Unix em milissegundos.

    Args:
        date (str): Uma string contendo a data no formato 'YYYY-MM-DD'.

    Returns:
        int or None: O timestamp Unix em milissegundos correspondente à data fornecida,
                    ou None se a string de data estiver em um formato inválido.

    Examples:
        >>> to_unixtime("2023-01-01")
        1672531200000

        >>> to_unixtime("2023-08-20")
        1679443200000

        >>> to_unixtime("invalid_date")
        None
    """
    try:
        datetime_obj = datetime.strptime(date, '%Y-%m-%d')
        unixtime_ms = int(datetime_obj.timestamp() * 1000)
        return unixtime_ms
    except ValueError:
        return None


if __name__ == '__main__':
    # Exemplos de uso
    start_date = '2021-01-01'
    end_date = '2021-01-31'
    start_unixtime = to_unixtime(start_date)
    end_unixtime = to_unixtime(end_date)
    print(f"start_unixtime: {start_unixtime}")
    print(f"end_unixtime: {end_unixtime}")

    start_date = from_unixtime(start_unixtime)
    print(f"start_date: {start_date}")
