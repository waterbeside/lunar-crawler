import types

def get_year_list(start: int, end: int) -> list:

    """
    Returns a list of years from start to end.
    """
    years = []
    for year in range(start, end + 1):
        years.append(year)
    return years

def save_to_file(data: str, fileName: str) -> None:
    """
    Saves data to file.
    """
    with open(fileName, 'wb') as f:
        if type(data) is bytes:
            f.write(data)
        elif type(data) is str:
            f.write(data.encode('utf-8'))
        elif type(data) is list:
            for line in data:
                f.write(line.encode('utf-8'))
        f.close()


if __name__ == '__main__':
    print(get_year_list(1901, 2100))

