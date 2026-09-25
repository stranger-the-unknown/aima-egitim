#!/usr/bin/env python3
"""Küçük gridworld üzerinde tablo Q-öğrenme.

3x2 ızgara; hedef ve tuzak. Eğitim sonrası Q tablosu ve açgözlü politika yazdırılır.

Özgün eğitim. Kitap metni yok. numpy OK.
https://aima.cs.berkeley.edu/ · https://github.com/aimacode
"""
from __future__ import annotations

from typing import Dict, List, Tuple

import numpy as np

# Durumlar: (satir, sutun) — 2 satır x 3 sütun
# (0,2) hedef +1; (1,2) tuzak -1; diğer geçişler -0.04 adım maliyeti
SATIR, SUTUN = 2, 3
HEDEF = (0, 2)
TUZAK = (1, 2)
ENGEL: set = set()  # bu demoda engel yok; genişletilebilir

EYLEMLER = ["U", "D", "L", "R"]
DELTA = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}


def gecerli(s: Tuple[int, int]) -> bool:
    r, c = s
    return 0 <= r < SATIR and 0 <= c < SUTUN and s not in ENGEL


def adim(s: Tuple[int, int], a: str) -> Tuple[Tuple[int, int], float, bool]:
    """Deterministik geçiş; terminalde biter."""
    if s in (HEDEF, TUZAK):
        return s, 0.0, True
    dr, dc = DELTA[a]
    ns = (s[0] + dr, s[1] + dc)
    if not gecerli(ns):
        ns = s
    if ns == HEDEF:
        return ns, 1.0, True
    if ns == TUZAK:
        return ns, -1.0, True
    return ns, -0.04, False


def q_ogren(
    epizot: int = 2000,
    alpha: float = 0.1,
    gamma: float = 0.9,
    epsilon: float = 0.2,
    seed: int = 0,
) -> Dict[Tuple[Tuple[int, int], str], float]:
    rng = np.random.default_rng(seed)
    durumlar = [(r, c) for r in range(SATIR) for c in range(SUTUN)]
    Q: Dict[Tuple[Tuple[int, int], str], float] = {
        (s, a): 0.0 for s in durumlar for a in EYLEMLER
    }

    for _ in range(epizot):
        s = (1, 0)  # sol alt başlangıç
        bitti = False
        adim_say = 0
        while not bitti and adim_say < 50:
            if rng.random() < epsilon:
                a = EYLEMLER[int(rng.integers(0, len(EYLEMLER)))]
            else:
                a = max(EYLEMLER, key=lambda x: Q[(s, x)])
            ns, r, bitti = adim(s, a)
            hedef = r + gamma * (0.0 if bitti else max(Q[(ns, x)] for x in EYLEMLER))
            Q[(s, a)] += alpha * (hedef - Q[(s, a)])
            s = ns
            adim_say += 1
    return Q


def yazdir_q(Q: Dict[Tuple[Tuple[int, int], str], float]) -> None:
    print("=== Q tablosu (yaklaşık) ===")
    for r in range(SATIR):
        for c in range(SUTUN):
            s = (r, c)
            etiket = "H" if s == HEDEF else ("T" if s == TUZAK else ".")
            vals = " ".join(f"{a}:{Q[(s, a)]:+.2f}" for a in EYLEMLER)
            print(f"  ({r},{c})[{etiket}]  {vals}")


def yazdir_politika(Q: Dict[Tuple[Tuple[int, int], str], float]) -> None:
    ok = {"U": "↑", "D": "↓", "L": "←", "R": "→"}
    print("=== Açgözlü politika ===")
    for r in range(SATIR):
        satir: List[str] = []
        for c in range(SUTUN):
            s = (r, c)
            if s == HEDEF:
                satir.append(" H")
            elif s == TUZAK:
                satir.append(" T")
            else:
                a = max(EYLEMLER, key=lambda x: Q[(s, x)])
                satir.append(f" {ok[a]}")
        print("".join(satir))


def main() -> None:
    Q = q_ogren()
    yazdir_q(Q)
    print()
    yazdir_politika(Q)


if __name__ == "__main__":
    main()
