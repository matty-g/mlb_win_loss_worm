from datetime import datetime, timedelta


def create_date_range(start_date, end_date):

    # number of days between start_date and end_date
    start = datetime.strptime(start_date, '%d/%m/%Y')
    end = datetime.strptime(end_date, '%d/%m/%Y')
    delta = end - start
    date_list = [start + timedelta(days=x) for x in range(0, delta.days)]

    return date_list
