#! /usr/bin/env python
from zdt_simulator import Exchange, Trader
from argparse import ArgumentParser
import numpy as np
import matplotlib.pyplot as plt


def find_estimated_payoffs():
    parser = ArgumentParser(
        description="""Simulate a market to find estimated payoff values for
        the first player, with customised partipants whose pAA, pAB are stored
        in csv files, each column corresponding to a different participant,
        with r optionally provided and stored in another file."""
        )
    parser.add_argument("strategies", type=str, nargs="+",
                        help=("the filepaths of the csv file containing each p"
                              "layer's strategy"))

    parser.add_argument("-r", type=str, nargs=1, required=False,
                        help="the filepath of the csv file containing r vals")

    parser.add_argument("-n", "--names", type=str, nargs="+", required=False,
                        help=("the names of the participants, given in the sam"
                              "e order as the pAA/pAB/r values"))

    parser.add_argument("--rounds", type=int, required=False)

    args = parser.parse_args()
    filepaths = args.strategies
    rounds = args.rounds if args.rounds is not None else 10000

    probabilities = [np.genfromtxt(filepath, delimiter=',')
                     for filepath in filepaths]

    player_count = len(probabilities)

    if args.r is not None:
        r_filepath = args.r[0]
        r = np.genfromtxt(r_filepath, delimiter=',')
    else:
        r = np.ones(player_count) / player_count

    if args.names is not None:
        names = args.names
    else:
        names = [f'player_{i}' for i in range(1, player_count + 1)]

    if len(names) != player_count:
        raise ValueError(f"Number of player names was {len(names)} but size of"
                         f" size of pAA suggests {player_count} players.")

    p_initial = np.ones(3) / 3

    players = [Trader(p_initial, p[:, 0], p[:, 1], player_count, name=name)
               for p, name in zip(probabilities, names)]

    exchange = Exchange(players, r)

    pnl_history, position_history = exchange.run_simulation(rounds=rounds)

    print(f"Estimated Si: {players[0].estimated_Si}")
