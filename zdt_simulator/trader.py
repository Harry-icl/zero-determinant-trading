import numpy as np
from math import comb
from itertools import product, combinations_with_replacement, count
from typing import List

from .actions import Action


AA, AB, N = Action.AA, Action.AB, Action.N


class Trader:
    _ids = count(1)

    def __init__(self, p_initial, pAA, pAB, player_count, speed: float = 1,
                 name=None):
        if np.max(pAA + pAB) > 1 + 1e-6:
            raise ValueError("pAA + pAB must be less than or equal to 1.")
        if np.min((np.min(pAA), np.min(pAB))) < 0:
            raise ValueError("pAA and pAB must be greater than or equal to 0.")
        if sum(p_initial) > 1 + 1e-6 or sum(p_initial) < 1 - 1e-6:
            raise ValueError("p_initial must sum to 1.")
        if len(p_initial) != 3:
            raise ValueError("p_initial must be length 3.")
        if len(pAA) != len(pAB):
            raise ValueError("Lengths of pAA and pAB must be the same.")

        if name is None:
            name = f"Player {next(self._ids)}"
        
        self.name = name
        self.p_initial = p_initial
        self.pAA = pAA
        self.pAB = pAB
        self.pN = np.ones(len(pAA)) - pAA - pAB
        self.speed = speed
        self.pnl = 0
        self.position = 0
        self.previous_action = None

        # Possible previous rounds
        prev_round_list = [
            (my_action, tuple(sorted(other_actions)))
            for my_action, other_actions in product(
                [AA, AB, N],
                combinations_with_replacement([AA, AB, N],
                                              player_count - 1)
            )
        ]
        self.prev_round_idx_map = {
            prev_round: i
            for i, prev_round in enumerate(sorted(prev_round_list))
        }
        if len(pAA) != len(self.prev_round_idx_map):
            raise ValueError(f"Length of pAA and pAB was {len(pAA)}, expected "
                             f"{len(self.prev_round_idx_map)} given "
                             f"player_count")

    def get_next_action(self, previous_round: List[Action]):
        if previous_round is None:
            p=self.p_initial
        else:
            previous_round.remove(self.previous_action)
            idx = self.prev_round_idx_map[(self.previous_action,
                                           tuple(sorted(previous_round)))]
            p = [self.pAA[idx], self.pAB[idx], self.pN[idx]]
        self.previous_action = np.random.choice([AA, AB, N], p=p)
        return self.previous_action
