from typing import List
from collections import deque
import numpy as np

from .trader import Trader
from .actions import Action


AA, AB, N = Action.AA, Action.AB, Action.N


class Exchange:
    def __init__(self, participants: List[Trader], r: List[float],
                 tick_size: int = 1, maker_rebate: int = 2,
                 taker_fee: int = 4):
        self.participants = participants
        self.r = r
        self.T = tick_size
        self.K = maker_rebate
        self.F = taker_fee
        self.previous_round = None

    def _run_round(self):
        bids = (deque(), deque())
        asks = (deque(), deque())
        # best_bid, best_ask will store a tuple of lists, both have the first
        # list containing the players who bid/ask the midpoint price S, and the
        # second list containing the players who bid/ask S+/-T, this is to allow
        # the simulator to implement price-time priority
        order_sequence = np.random.choice(self.participants,
                                          size=len(self.participants),
                                          replace=False, p=self.r)

        for player in order_sequence:
            next_move = player.get_next_action(self.previous_round)
            # Player knows what their previous round was, so they can remove
            # that from the play list themselves
            if next_move == AA:
                bids[1].append(player)
                if len(best_bid[0]) > 0:
                    best_bidder = bids[0].popleft()
                    best_bidder.pnl += self.K
                    best_bidder.position += 1
                    player.pnl -= self.F
                    player.position -= 1
                else:
                    asks[0].append(player)
            
            elif next_move == AB:
                asks[1].append(player)
                if len(asks[0]) > 0:
                    best_asker = asks[0].popleft()
                    best_asker.pnl += self.K
                    best_asker.position -= 1
                    player.pnl -= self.F
                    player.position += 1
                else:
                    bids[0].append(player)
            
            elif next_move == N:
                bids[1].append(player)
                asks[1].append(player)

        if len(bids[0]) > 0:
            bids[0][0].pnl += self.K
            bids[0][0].position += 1
        elif len(bids[1]) > 0:
            bids[1][0].pnl += self.T + self.K
            bids[1][0].position += 1
        
        if len(asks[0]) > 0:
            asks[0][0].pnl += self.K
            asks[0][0].position -= 1
        elif len(asks[1]) > 0:
            asks[1][0].pnl += self.T + self.K
            asks[1][0].position -= 1

    def run_simulation(self, rounds: int = 100):
        history = [[participant.pnl for participant in self.participants]]
        for round in range(rounds):
            pass