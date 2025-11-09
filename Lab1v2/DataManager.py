from dateutil.parser import parse

month_dict = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December"
}

def to_date(string):
    return parse(string, dayfirst=True)

def filter_by_period(data, date_from, date_to, ticker):
    date1 = to_date(date_from)
    date2 = to_date(date_to)
    print(date1.month, date1.year)
    arr = list(filter(lambda row: ticker == row[0] and date1 <= to_date(row[1]) <= date2, data))
    return arr

def prepare_prices_data(data):
    dic = {'x': [],
           'y': {
               'open': [],
               'max': [],
               'min': [],
               'close': []}
           }

    for row in data:
        dic['x'].append(row[1])
        dic['y']['open'].append(float(str(row[2]).replace(',', '')))
        dic['y']['max'].append(float(str(row[3]).replace(',', '')))
        dic['y']['min'].append(float(str(row[4]).replace(',', '')))
        dic['y']['close'].append(float(str(row[5]).replace(',', '')))

    return dic

def filter_by_year(data, ticker, year):
    arr = list(filter(lambda row: ticker == row[0] and to_date(row[1]).year == year, data))
    return arr

def prepare_avg_price_monthly(data):
    dic = {'x': [], 'y': []}

    grouped = {}
    for i in range(1, 13):
        grouped[i] = {'total': 0, 'count': 0}

    for row in data:
       grouped[to_date(row[1]).month]['total'] += sum([float(i) for i in row[2:6]])
       grouped[to_date(row[1]).month]['count'] += len(row[2:6])

    for k, v in grouped.items():
        dic['x'].append(month_dict.get(k))
        dic['y'].append(v['total'] / v['count'])

    return dic