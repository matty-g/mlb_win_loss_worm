import matplotlib.pyplot as plt


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
        over_under.append(ovr_und)

    fig = plt.figure()
    ax = plt.axes()

    plt.style.use('seaborn-darkgrid')
    plt.grid(True)

    x = dates

    plt.axhline(y=0, color="red")
    ax.plot(x, over_under)

    plt.show()
