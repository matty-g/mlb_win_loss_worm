import asyncio
import logging
import mlb_data

from flask import Flask, flash, redirect, render_template, request, url_for

from config import teams

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

app = Flask(__name__)

@app.route('/')

def index():
    logger.debug("index called")
    return render_template(
        'test.html',
        data=teams
    )


@app.route('/result', methods=['GET', 'POST'])
def result():
    logger.debug("result called")
    data = []
    wins = []
    losses = []
    chart_labels = []
    team = None
    error = None
    select = request.form.get('comp_select')
    logger.debug(f"select is: {select}")
    resp = mlb_data.query(select, "27/03/2019", "26/05/2019")
    # resp = mlb_data.test_api(select)
    logger.debug(f"resp is: {resp}")
    if resp:
        chart_labels = mlb_data.extract_labels(resp)
        wins = mlb_data.extract_wins(resp)
        losses = mlb_data.extract_losses(resp)
        team = mlb_data.get_team(select)
        # data.append(resp)

    # do stuff

    return render_template(
        'result.html',
        team = team,
        data = data,
        error = error,
        chart_labels = chart_labels,
        wins = wins,
        losses = losses
    )


if __name__ == '__main__':
    logger.debug('running app')
    app.run(debug=True)


