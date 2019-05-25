import asyncio
import aiohttp
import matplotlib.pyplot as plt
import logging

from datetime import datetime, timedelta

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

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


async def get_json_for_date(a_date):

    logger.debug(f"getting data for: {a_date}")

    url = build_date_url(a_date)

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data_file = await resp.json()

    return data_file


async def get_win_loss_data_for_team(team, data):
    """
    parses JSON to get data for the desired team
    """

    try:
        games = data["data"]["games"]["game"]

    except KeyError:
        # likely no games at all this day
        return None

    logger.debug(f"returning data for date: {game['time_date']}")

    for game in games:

        if game["home_code"] == team:
            print(f"returning data for date: {game['time_date']}")
            return (game["home_win"], game["home_loss"])

        if game["away_code"] == team:
            print(f"returning data for date: {game['time_date']}")
            return (game["away_win"], game["away_loss"])

    logger.debug(f"returning data for date: {game['time_date']}")

    return None


def build_wl_plot(data):

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

    plt.style.use('seaborn-darkgrid')
    plt.grid(True)

    x = dates

    ax.plot(x, wins)
    ax.plot(x, losses)

    plt.show()

def build_worm_plot(data):

    wins = []
    losses = []
    dates = []
    avgs = []

    curr_wins = 0
    curr_losses = 0

    for each in data:
        if each[1] is not None:
            curr_wins = int(each[1][0])
            curr_losses = int(each[1][1])

        wins.append(curr_wins)
        losses.append(curr_losses)
        games_played = curr_wins + curr_losses
        dates.append(each[0])
        if curr_wins != 0:
            avg = curr_wins / float(games_played)
        else:
            avg = 0
        avgs.append(avg)

    fig = plt.figure()
    ax = plt.axes()

    plt.style.use('seaborn-darkgrid')
    plt.grid(True)

    x = dates

    plt.axhline(y=0.5, color="red")

    ax.plot(x, avgs)

    plt.show()


async def get_result(team, date):
    mlb_data = await get_json_for_date(date)
    result = await get_win_loss_data_for_team(team, mlb_data)

    return (date.strftime("%d-%m"), result)


def run(team, start_date, end_date):

    dates = create_date_range(start_date, end_date)

    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(
        asyncio.gather(
            *(get_result(team, date) for date in dates)
        )
    )
    loop.close()

    build_worm_plot(results)
    build_wl_plot(results)


# for testing
import time
start = time.time()
run("cin", "27/03/2019", "25/05/2019")
end = time.time()-start

print(f"time: {end:.2f}s")


