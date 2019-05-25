import urllib.request
import json
import asyncio

import matplotlib.pyplot as plt

from datetime import datetime, timedelta


mlb_url = "http://gd2.mlb.com/components/game/mlb/year_2019/month_05/day_16/miniscoreboard.json"

base_url = "http://gd2.mlb.com/components/game/mlb"

def build_date_url(date_obj):

    year_str = date_obj.year
    month_str = "{:02}".format(date_obj.month)
    day_str = "{:02}".format(date_obj.day)

    url = f"{base_url}/year_{year_str}/month_{month_str}/day_{day_str}/miniscoreboard.json"

    return url


def create_date_range(start_date, end_date):

    # number of days between start_date and end_date
    start = datetime.strptime(start_date, '%d/%m/%Y')
    end = datetime.strptime(end_date, '%d/%m/%Y')
    delta = end - start

    date_list = [start + timedelta(days=x) for x in range(0, delta.days)]

    return date_list


def get_json_for_date(a_date):

    url = build_date_url(a_date)

    f = urllib.request.urlopen(url)
    data_file = json.loads(f.read())

    return data_file


def get_win_loss_data_for_team(team, data):
    """
    parses JSON to get data for the desired team
    """

    games = data["data"]["games"]["game"]

    for game in games:

        if game["home_code"] == team:
            # print("team is playing at home")
            return (game["home_win"], game["home_loss"])

        if game["away_code"] == team:
            # print("team is playing away")
            # get the data
            return (game["away_win"], game["away_loss"])

    return None


def build_plot_arrays(data):

    wins = []
    losses = []
    dates = []

    curr_wins = 0
    curr_losses = 0

    for each in data:
        if each[1] is not None:
            curr_wins = each[1][0]
            curr_losses = each[1][1]

        wins.append(curr_wins)
        losses.append(curr_losses)
        dates.append(each[0])

    fig = plt.figure()
    ax = plt.axes()

    x = dates

    ax.plot(x, wins)
    ax.plot(x, losses)

    plt.show()


def get_result(team, date):
    mlb_data = get_json_for_date(date)
    result = get_win_loss_data_for_team(team, mlb_data)

    return (date.strftime("%d-%m"), result)


def run(team, start_date, end_date):

    dates = create_date_range(start_date, end_date)

    results = []

    for date in dates:
        # print(f"checking on date: {date}")
        results.append(get_result(team, date))

    build_plot_arrays(results)




run("cin", "20/05/2019", "25/05/2019")



