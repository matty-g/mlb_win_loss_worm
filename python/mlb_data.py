import aiohttp
import asyncio
import logging

from utils import create_date_range
from config import base_url, teams

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def build_date_url(date_obj):

    year_str = date_obj.year
    month_str = "{:02}".format(date_obj.month)
    day_str = "{:02}".format(date_obj.day)
    url = f"{base_url}/year_{year_str}/month_{month_str}/day_{day_str}/miniscoreboard.json"

    return url


async def get_json_for_date(a_date):
    logger.debug(f"getting json for {a_date}")
    url = build_date_url(a_date)

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
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

    if not isinstance(games, list):
        # catch weird edge cases where returned data is corrupt and not in a list
        games = [games]

    for game in games:

        try:
            if game["home_code"] == team:
                logger.debug(f"returning data for date: {game['time_date']}")
                return (game["home_win"], game["home_loss"])

            if game["away_code"] == team:
                logger.debug(f"returning data for date: {game['time_date']}")
                return (game["away_win"], game["away_loss"])

        except TypeError or KeyError as e:
            logger.debug(f"error parsing for date: {game['time_date']}")
            logger.debug(f"error code: {e}")

    return None


async def get_result(team, date):
    logger.debug(f"get_result called for {team} on {date}")
    mlb_data = await get_json_for_date(date)
    result = await get_win_loss_data_for_team(team, mlb_data)

    return (date.strftime("%d-%m"), result)


def query(team, start_date, end_date):
    logger.debug("query called")
    dates = create_date_range(start_date, end_date)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    results = loop.run_until_complete(
        asyncio.gather(
            *(get_result(team, date) for date in dates)
        )
    )
    loop.close()

    return results


def test_api(team):
    logger.debug('test api called from mlb data')

    return f"you selected {team}"


def extract_labels(data):

    labels = []
    for each in data:
        labels.append(each[0])

    logger.debug(f"labels: {labels}")
    return labels


def extract_wins(data):
    wins = []

    # logger.debug(f"data: {data}")

    curr_wins = 0

    for each in data:
        if each[1] is not None:
            curr_wins = each[1][0]

        wins.append(curr_wins)

    logger.debug(f"wins: {wins}")
    return wins


def extract_losses(data):
    losses = []

    curr_losses = 0

    for each in data:
        if each[1] is not None:
            curr_losses = each[1][1]

        losses.append(curr_losses)

    logger.debug(f"losses: {losses}")
    return losses


def get_team(team):
    # perform team lookup
    for obj in teams:
        if obj['id'] == team:
            return obj['name']
