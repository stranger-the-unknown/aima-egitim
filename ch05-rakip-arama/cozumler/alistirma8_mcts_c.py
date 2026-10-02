#!/usr/bin/env python3
"""Alıştırma 8 çözümü: MCTS'te keşif sabiti C ve yineleme sayısının etkisi."""
from __future__ import annotations

import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ornekler"))

from mcts_xox import mcts, oyun  # noqa: E402
from minimax_tictactoe import en_iyi_hamle  # noqa: E402

C_DEGERLERI = (0.0, 0.5, 1.4, 5.0)
YINELEMELER = (50, 200, 1000)


def kayiplar(C: float, yineleme: int, oyun_sayisi: int = 10) -> int:
    rng = random.Random(0)
    mcts_x = lambda t, s: mcts(t, s, yineleme, C, rng)[0]  # noqa: E731
    minimax_o = lambda t, s: en_iyi_hamle(t, s, True)[0]  # noqa: E731
    return sum(oyun(mcts_x, minimax_o) == -1 for _ in range(oyun_sayisi))


def main() -> None:
    print("MCTS (X) — tam minimax (O), 10 oyun; tablodaki sayı MCTS'in kayıplarıdır\n")
    print(f"{'C':>6}" + "".join(f"{y:>8}" for y in YINELEMELER))
    for C in C_DEGERLERI:
        print(f"{C:>6}" + "".join(f"{kayiplar(C, y):>8}" for y in YINELEMELER))


if __name__ == "__main__":
    main()
