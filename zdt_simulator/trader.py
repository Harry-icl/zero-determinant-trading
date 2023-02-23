import numpy as np

from .actions import Action


class Trader:
    PREVIOUS_ROUND_IDX_MAP = {
        (Action.AA, Action.AA): 0,
        (Action.AA, Action.AB): 1,
        (Action.AA, Action.N): 2,
        (Action.AB, Action.AA): 3,
        (Action.AB, Action.AB): 4,
        (Action.AB, Action.N): 5,
        (Action.N, Action.AA): 6,
        (Action.N, Action.AB): 7,
        (Action.N, Action.N): 8
    }

    def __init__(self, pAA, pAB, speed: float = 1):
        if np.max(pAA + pAB) > 1:
            raise ValueError("pAA + pAB must be less than or equal to 1.")
        elif np.min(np.min(pAA), np.min(pAB)) < 0:
            raise ValueError("pAA and pAB must be greater than or equal to 0.")

        self.pAA = pAA
        self.pAB = pAB
        self.pN = np.ones(9) - pAA - pAB
        self.speed = speed
        self.pnl = 0
        self.position = 0

    def get_next_action(self, prev_self_action: Action,
                        prev_opp_action: Action):
        idx = self.PREVIOUS_ROUND_IDX_MAP[(prev_self_action, prev_opp_action)]
        rand_num = np.random.rand()
        if rand_num < self.pAA[idx]:
            return Action.AA
        elif rand_num < self.pAA[idx] + self.pAB[idx]:
            return Action.AB
        else:
            return Action.N
    
    def update_pnl(self, change: float):
        self.pnl += change
