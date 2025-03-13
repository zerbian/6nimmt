from card import Card
from board import Board
import random

import numpy as np

class Player():
    hand: list[Card]
    penalty: list[Card]

    def __repr__(self):
        "BasePlayer"

    def setHand(self, hand: list[Card]):
        self.hand = hand
        self.hand.sort()
        self.penalty = []

    def collect_penalty(self, penalty: list[Card]):
        self.penalty.extend(penalty)

    def get_penalty(self):
        return sum([card.value for card in self.penalty])
    
    def reset(self):
        self.hand.clear()
        self.penalty.clear()

    # strategy
    def card_selection(self, board: Board):
        # determine played card
        i = random.randint(0, len(self.hand) - 1)
        return self.hand.pop(i)
    
    def column_selection(self, board: Board, selected_cards: list[Card]) -> int:
        # determine taken column (return 0, 1, 3, 4)
        return random.randint(0, 3)

class DumbPlayer(Player):
    def column_selection(self, board: Board, selected_cards: list[Card]) -> int:
        idx = 0
        max_penalty = 0
        for i, col in enumerate(board.columns):
            val = sum([card.value for card in col])
            if val > max_penalty:
                idx = i
                max_penalty = val
        return idx

class BasicPlayer(Player):

    def __repr__(self):
        return "Basic Player"
    
    def column_selection(self, board: Board, selected_cards: list[Card]) -> int:
        idx = 0
        min_penalty = 1000
        for i, col in enumerate(board.columns):
            val = sum([card.value for card in col])
            if val < min_penalty:
                idx = i
                min_penalty = val
        return idx

    
class NoPenaltyPlayer(BasicPlayer):
    def card_selection(self, board: Board):
        cards_wo_penalty = []

        for card_idx, card in enumerate(self.hand):
            next_col = board.check_next_spot(card)
            if next_col == -1: continue

            if len(board.columns[next_col]) < 5:
                cards_wo_penalty.append(card_idx)

        if len(cards_wo_penalty) > 0:
            return self.hand.pop(random.choice(cards_wo_penalty))
        
        return super().card_selection(board)

class IncPlayer(NoPenaltyPlayer):
    def __repr__(self):
        return "Increment Player"

    def card_selection(self, board):
        card = self.hand.pop(0)
        return card
    
class DecPlayer(NoPenaltyPlayer):
    def __repr__(self):
        return "Decrement Player"

    def card_selection(self, board):
        return self.hand.pop(-1)

class BestFitPlayer(NoPenaltyPlayer):
    def card_selection(self, board):
        for card_id, card in enumerate(self.hand):
            col_idx = board.check_next_spot(card)
            # check if column is not full
            if len(board.columns[col_idx]) >= 5: continue

            diff = card - board.columns[col_idx][-1]
            if diff == 1:
                return self.hand.pop(card_id)

        return super().card_selection(board)
    
class NearlyFitPlayer(IncPlayer):
    def card_selection(self, board):
        for card_idx, card in enumerate(self.hand):
            col_idx = board.check_next_spot(card)
            # check if column is not full
            if len(board.columns[col_idx]) >= 5: continue

            diff = card - board.columns[col_idx][-1]
            if diff <= 3:
                return self.hand.pop(card_idx)

        return super().card_selection(board)
    

class AltPlayer(BasicPlayer):
    highest = True

    def card_selection(self, board):
        idx = -1 if self.highest else 0
        self.highest = not self.highest
        return self.hand.pop(idx)

class LowHighMidllePlayer(BasicPlayer):
    turn = 0

    def card_selection(self, board):
        if self.turn in range(0, 4):
            return self.hand.pop(0)
        
        if self.turn in range(4, 7):
            return super().card_selection(board)
        
        else:
            return self.hand.pop(-1)



ALL_PLAYER_TYPES = [Player, BasicPlayer, IncPlayer, DecPlayer, AltPlayer, LowHighMidllePlayer, NoPenaltyPlayer, BestFitPlayer, NearlyFitPlayer,]