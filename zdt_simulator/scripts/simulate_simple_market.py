#! /usr/bin/env python
from zdt_simulator import Exchange, Trader
from argparse import ArgumentParser
from itertools import combinations_with_replacement
import numpy as np
import matplotlib.pyplot as plt


def simulate_simple_market():
    parser = ArgumentParser(
        description="""Simulate a market with equal speed participants who have
        equal chance of choosing each action in all situations."""
        )
    parser.add_argument("player_count", type=int, nargs=1,
                        help="Number of market makers in the market.")

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
