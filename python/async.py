import asyncio
import aiohttp
import matplotlib.pyplot as plt
import logging
import json

from datetime import datetime, timedelta

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

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

    # logger.debug(f"getting data for: {a_date}")

    url = build_date_url(a_date)

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            # data_file = await resp.json(content_type=None)
            # data_tmp = await resp.text(encoding='utf-8')
            data_file = await resp.json(encoding='utf-8', content_type=None)
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

    # logger.debug(f"no. of games: {len(games)}")
    # if len(games) > 20:
    # logger.debug(f"{type(games)} : {games}")

    if not isinstance(games, list):
        # catch weird edge cases where returned data is corrupt and not in a list
        games = [games]

    for game in games:
        # logger.debug(game)

        # logger.debug(f"type: {type(game)}")

        # if isinstance(game, str):
        #     logger.debug(game)
        #     logger.debug(f"converting string to dict")
        #     game_tmp = json.dumps(game)
        #     game = game_tmp
        #
        #
        #
        #     logger.debug(f"game is now: {type(game)}")

        try:
            # logger.debug(game["home_code"])

            # logger.debug(f"keys: {len(game.keys())}")

            # logger.debug(f"type: {type(game)}")

            if game["home_code"] == team:
                # logger.debug(f"returning data for date: {game['time_date']}")
                return (game["home_win"], game["home_loss"])

            if game["away_code"] == team:
                # logger.debug(f"returning data for date: {game['time_date']}")
                return (game["away_win"], game["away_loss"])

        except TypeError as e:
            logger.debug(f"error parsing for date: {game['time_date']}")
            logger.debug(f"error code: {e}")

    # logger.debug(f"returning data for date: {game['time_date']}")

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


def build_over_under_plot(data):

    wins = []
    losses = []
    dates = []
    over_under = []

    curr_wins = 0
    curr_losses = 0

    for each in data:
        if each[1] is not None:
            curr_wins = int(each[1][0])
            curr_losses = int(each[1][1])

        wins.append(curr_wins)
        losses.append(curr_losses)
        ovr_und = (curr_wins - curr_losses)
        dates.append(each[0])
        # if curr_wins != 0:
        #     avg = curr_wins / float(games_played)
        # else:
        #     avg = 0
        over_under.append(ovr_und)

    fig = plt.figure()
    ax = plt.axes()

    plt.style.use('seaborn-darkgrid')
    plt.grid(True)

    x = dates

    plt.axhline(y=0, color="red")

    # ax.set_xticks(ax.get_xticks()[::5])

    ax.plot(x, over_under)

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
    build_over_under_plot(results)


# for testing
import time
start = time.time()
run("cin", "01/03/2017", "30/10/2017")
end = time.time()-start

print(f"time: {end:.2f}s")


