from typing import List
import numpy as np

from .trader import Trader
from .actions import Action


class Exchange:
    def __init__(self, participants: List(Trader), r: List(float),
                 tick_size: int = 1, maker_rebate: int = 2,
                 taker_fee: int = 4):
        self.participants = participants
        self.r = r
        self.T = tick_size
        self.K = maker_rebate
        self.F = taker_fee
        self.previous_round = None
        self.best_bid = self.best_ask = None

    def _run_round(self):
        order_sequence = np.random.choice(self.participants,
                                          size=len(self.participants),
                                          replace=False, p=self.r)
        for player in order_sequence:
            next_move = player.get_next_action(self.previous_round)
            


    def run_simulation(self, rounds: int = 100):
        history = [[participant.pnl for participant in self.participants]]
        for round in range(rounds):
            
