from player import Player
from card import Card
from board import Board
import random

class Game():
    players: list[Player]
    board: Board

    def __init__(self, players: list[Player]):
        self.players = players
        self.board = Board()

    def init_board(self):
        full_deck = Card.full_deck()

        random.shuffle(full_deck)

        # fill columns
        start_cards = [full_deck.pop() for _ in range(4)]
        self.board.init_columns(start_cards)

        # deal hand to players
        for player in self.players:
            hand = []
            for _ in range(10):
                hand.append(full_deck.pop())
            player.setHand(hand)

    def make_turn(self):
        # every player makes a choice
        card_choices = [(pl.card_selection(self.board), pl) for pl in self.players]
        card_choices.sort(key=lambda x : x[0].number) # sort them by card value

        for card, player in card_choices:
            penalty = None
            col_idx = self.board.check_next_spot(card)
            if col_idx == -1:
                col_idx = player.column_selection(self.board, [x[0] for x in card_choices])
                penalty = self.board.take_column(card, col_idx)

            else:
                penalty = self.board.add_to_column(card, col_idx)

            if penalty:
                player.collect_penalty(penalty)

class GameRound():
    @staticmethod
    def run_round(players: list[Player]) -> list[int]:
        game = Game(players)
        game.init_board()
        for _ in range(10):
            game.make_turn()
        
        score = [player.get_penalty() for player in players]
        for player in players:
            player.reset()
        
        return score