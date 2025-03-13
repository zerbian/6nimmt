class Card():
    number: int
    value: int

    def __init__(self, number, value):
        self.number = number
        self.value = value

    def __lt__(self, other):
        return self.number < other.number

    def __repr__(self):
        return f"{self.number} ({self.value})"
    
    def __sub__(self, other) -> int:
        return self.number - other.number
    @staticmethod
    def get_value(number: int):
        if number == 55:
            return 7
        if number in (11, 22, 33, 44, 66, 77, 88, 99):
            return 5
        if number in (10, 20, 30, 40, 50, 60, 70, 80, 90, 100):
            return 3
        if number in (5, 15, 25, 35, 45, 65, 75, 85, 95):
            return 2
        return 1
    
    def full_deck():
        return [Card(i, Card.get_value(i)) for i in range(1, 105)]