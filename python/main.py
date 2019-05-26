import asyncio
import logging

from plots import build_over_under_plot, build_wl_plot, build_worm_plot
from utils import create_date_range
from mlb_data import get_result


from flask import Flask, flash, redirect, render_template, request, url_for
import mlb_data

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

app = Flask(__name__)

@app.route('/')

def index():
    logger.debug("index called")
    return render_template(
        'test.html',
        data=[{'name':'Cincinnati',
               'id': 'cin'},
              {'name':'St. Louis',
               'id': 'sln'}
              ]
    )


@app.route('/result', methods=['GET', 'POST'])
def result():
    logger.debug("result called")
    data = []
    error = None
    select = request.form.get('comp_select')
    logger.debug(f"select is: {select}")
    resp = mlb_data.query(select, "28/03/2019", "25/05/2019")
    # resp = mlb_data.test_api(select)
    logger.debug(f"resp is: {resp}")
    if resp:
        data.append(resp)

    # do stuff

    return render_template(
        'result.html',
        data = data,
        error = error
    )


# def test_api(team):
#     logger.debug('test api called')
#
#     return f"selected {team}"
#


if __name__ == '__main__':
    logger.debug('running app')
    app.run(debug=True)


