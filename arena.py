from game import GameRound
from player import Player, NoPenaltyPlayer, BasicPlayer, IncPlayer

def full_rounds(players: list[Player], n = 1000) -> list[int]:
    """Play n rounds of ten cards and collect total penalty scores for players"""
    N = len(players)
    total_scores = [0] * N

    for i in range(n):
        round_scores = GameRound.run_round(players)
        for pi in range(N):
            total_scores[pi] += round_scores[pi]

    return total_scores
    

def full_rounds_two_player(p1: Player, p2: Player, n = 1000, p = 4) -> float:
    """Play n rounds with specified two players p1 and p2 and return relative score differences"""
    players = [p1, p2] + [BasicPlayer() for _ in range(p - 2)]
    
    total_score = full_rounds(players, n)

    return (total_score[0] - total_score[1]) / n



if __name__ == "__main__":
    res = full_rounds_two_player(IncPlayer(), Player(), n = 1)
    print(res)