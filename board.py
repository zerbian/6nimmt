from card import Card

class Board():
    columns: list[list[Card]]

    def __init__(self):
        self.columns = [[], [], [], []]

    def init_columns(self, start_cards: list[Card]):
        for i in range(4):
            self.columns[i].append(start_cards[i])

    def check_next_spot(self, card: Card) -> int:
        """Check in which column the provided would go"""
        last_cards_in_cols = [(col[-1], i) for i, col in enumerate(self.columns)]
        last_cards_in_cols.sort(key=lambda x : x[0].number, reverse=True)
        for cmp_card, idx in last_cards_in_cols:
            if card > cmp_card:
                return idx
        
        return -1
    
    def take_column(self, card: Card, col_idx: int) -> list[Card]:
        """Return all cards from from a column and place the card in it"""
        penalty = self.columns[col_idx]
        self.columns[col_idx] = [card]
        return penalty

    def add_to_column(self, card: Card, col_idx: int) -> None | list[Card]:
        """Add a card to a column and collect possible penalty cards"""
        col = self.columns[col_idx]
        if len(col) <= 4:
            col.append(card)
            return None
        else:
            return self.take_column(card, col_idx)
        
    def __repr__(self):
        return f" 1 | {self.columns[0]}\n 2 | {self.columns[1]}\n 3 | {self.columns[2]}\n 4 | {self.columns[3]}\n"