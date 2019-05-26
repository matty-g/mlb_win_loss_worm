import asyncio
import logging

from plots import build_over_under_plot, build_wl_plot, build_worm_plot
from utils import create_date_range
from mlb_data import get_result


logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def run(team, start_date, end_date):

    dates = create_date_range(start_date, end_date)

    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(
        asyncio.gather(
            *(get_result(team, date) for date in dates)
        )
    )
    loop.close()

    # build_worm_plot(results)
    build_wl_plot(results)
    # build_over_under_plot(results)


# for testing
import time
start = time.time()
run("cin", "27/03/2019", "24/05/2019")
end = time.time()-start

print(f"time: {end:.2f}s")


