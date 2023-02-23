#! /usr/bin/env python
from zdt_simulator import Exchange, Trader
from argparse import ArgumentParser
from itertools import combinations_with_replacement
import numpy as np
import matplotlib.pyplot as plt


def simulate_simple_market():
    parser = ArgumentParser(
        description="""Simulate a market with customised partipants whose pAA,
        pAB are stored in csv files, each column corresponding to a different
        participant, with r optionally provided and stored in another file."""
        )
    parser.add_argument("pAA", type=str, nargs=1,
                        help="The filepath of the csv file containing pAA vals")
    
    parser.add_argument("pAB", type=str, nargs=1,
                        help="The filepath of the csv file containing pAB vals")
    
    parser.add_argument("r", type=str, nargs=1, required=False,
                        help="The filepath of the csv file containing r vals")

    args = parser.parse_args()
    player_count = args.player_count[0]

    round_type_count = 3*len([x for x in combinations_with_replacement(
        range(3),
        player_count - 1
    )])
    pAA = np.ones(round_type_count) / 3
    pAB = pAA
    p_initial = np.ones(3) / 3

    players = [Trader(p_initial, pAA, pAB, player_count)
               for _ in range(player_count)]
    r = np.ones(player_count) / player_count
    
    exchange = Exchange(players, r)

    pnl_history, position_history = exchange.run_simulation()

    for i, player in enumerate(players):
        plt.plot(pnl_history[:, i], label=player.name)
    plt.legend()
    plt.xlabel("Round")
    plt.ylabel("PnL")
    plt.show()

    for i, player in enumerate(players):
        plt.plot(position_history[:, i], label=player.name)
    plt.legend()
    plt.xlabel("Round")
    plt.ylabel("Position")
    plt.show()

    print("Final PnLs:", pnl_history[-1])
