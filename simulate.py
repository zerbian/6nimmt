import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm

import itertools
from tqdm import tqdm

import argparse

import arena
from player import ALL_PLAYER_TYPES


def two_players_relative_scores(n, p):
    N = len(ALL_PLAYER_TYPES)
    m = np.zeros((N, N))

    for a,b in tqdm(list(itertools.combinations(range(N),2))):
        p1 = ALL_PLAYER_TYPES[a]
        p2 = ALL_PLAYER_TYPES[b]
        res = arena.full_rounds_two_player(p1(), p2(), n, p)
        m[b,a] = -res
        m[a,b] = res

    return m

def visualize_two_players_relative_scores(n: int, p: int):
    res = two_players_relative_scores(n, p)
    N = len(ALL_PLAYER_TYPES)
    
    fig, ax = plt.subplots()
    norm = TwoSlopeNorm(vmin=res.min(), vcenter=0, vmax=res.max())
    ax.imshow(res, cmap="PiYG", norm=norm)

    ax.tick_params(top=True, labeltop=True, bottom=False, labelbottom=False)
    ax.set_xticks(range(N), labels=[pl.__name__ for pl in ALL_PLAYER_TYPES], rotation=45, ha="left", rotation_mode="anchor")

    ax.set_yticks(range(N), labels=[pl.__name__ for pl in ALL_PLAYER_TYPES], ha="right", rotation_mode="anchor")

    for i in range(N):
        for j in range(N):
            if i == j: continue
            text = ax.text(j, i, res[i, j],ha="center", va="center", color="black")

    plt.tight_layout()
    plt.show()

def realistic_game_placing(n=100, p=4):
    N = len(ALL_PLAYER_TYPES)

    scores = np.zeros(N)
    for indecies in tqdm(list(itertools.combinations(range(N),p))):
        players = [ALL_PLAYER_TYPES[idx]() for idx in indecies]
        res = arena.full_rounds(players, n)

        sort_idxs = np.argsort(res)
        for sco, ply in zip(sort_idxs, indecies):
            scores[ply] += sco + 1

    return scores / n

def visualize_realistic_game_placing(n: int, p: int):
    scores = realistic_game_placing(n, p)
    
    fig, ax = plt.subplots()
    labels = [pl.__name__ for pl in ALL_PLAYER_TYPES]
    ax.bar([pl.__name__ for pl in ALL_PLAYER_TYPES], scores)
    ax.set_xticklabels(labels, rotation=45, ha='right')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("type", choices=["2p_rel", "g_pos"])
    parser.add_argument("-n", type=int, help="Rounds played", default=100)
    parser.add_argument("-p", type=int, help="Number of players", default=4)
    args = parser.parse_args()

    match args.type:
        case "2p_rel":
            visualize_two_players_relative_scores(n=args.n, p=args.p)
        case "g_pos":
            visualize_realistic_game_placing(n=args.n, p=args.p)

    