import aiohttp
import logging

from utils import create_date_range
from config import base_url

logger = logging.getLogger(__name__)


def build_date_url(date_obj):

    year_str = date_obj.year
    month_str = "{:02}".format(date_obj.month)
    day_str = "{:02}".format(date_obj.day)
    url = f"{base_url}/year_{year_str}/month_{month_str}/day_{day_str}/miniscoreboard.json"

    return url


async def get_json_for_date(a_date):

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

        except TypeError as e:
            logger.debug(f"error parsing for date: {game['time_date']}")
            logger.debug(f"error code: {e}")

    return None


async def get_result(team, date):
    mlb_data = await get_json_for_date(date)
    result = await get_win_loss_data_for_team(team, mlb_data)

    return (date.strftime("%d-%m"), result)
