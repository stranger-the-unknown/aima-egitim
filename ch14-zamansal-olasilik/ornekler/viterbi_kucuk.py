#!/usr/bin/env python3
"""Aynı hava/şemsiye HMM üzerinde Viterbi — en olası durum yolu.

hmm_filtreleme.py ile aynı parametreler.
Dinamik programlama: her (t, durum) için max skor + geri işaret.
Resmi referans: https://aima.cs.berkeley.edu/ · https://github.com/aimacode
"""
from __future__ import annotations

from typing import List, Tuple

DURUMLAR = ("Gunes", "Yagmur")
P0_YAGMUR = 0.5
GECIS = [
    [0.7, 0.3],
    [0.3, 0.7],
]
P_SEMSIYE_VER_DURUM = [0.2, 0.9]


def p_gozlem(durum: int, semsiye: bool) -> float:
    pe = P_SEMSIYE_VER_DURUM[durum]
    return pe if semsiye else (1.0 - pe)


def viterbi(gozlemler: List[bool]) -> Tuple[List[int], float]:
    """En olası durum indeksi dizisi + birleşik skor (normalize edilmemiş)."""
    n = len(DURUMLAR)
    t_max = len(gozlemler)

    # delta[t][j] = max yol skoru, t=0..t_max-1 (gözlem indeksi)
    # psi[t][j] = geri işaret (önceki durum)
    delta: List[List[float]] = []
    psi: List[List[int]] = []

    # t = 0 (ilk gözlem)
    d0 = []
    for j in range(n):
        p0 = P0_YAGMUR if j == 1 else (1.0 - P0_YAGMUR)
        d0.append(p0 * p_gozlem(j, gozlemler[0]))
    delta.append(d0)
    psi.append([-1] * n)

    for t in range(1, t_max):
        dt = []
        pt = []
        for j in range(n):
            best_skor = -1.0
            best_i = 0
            for i in range(n):
                skor = delta[t - 1][i] * GECIS[i][j]
                if skor > best_skor:
                    best_skor = skor
                    best_i = i
            dt.append(best_skor * p_gozlem(j, gozlemler[t]))
            pt.append(best_i)
        delta.append(dt)
        psi.append(pt)

    # Sonda en iyi durum
    son = max(range(n), key=lambda j: delta[t_max - 1][j])
    yol = [0] * t_max
    yol[t_max - 1] = son
    for t in range(t_max - 1, 0, -1):
        yol[t - 1] = psi[t][yol[t]]

    return yol, delta[t_max - 1][son]


def filtre_argmax(gozlemler: List[bool]) -> List[int]:
    """Karşılaştırma: her adımda marjinal argmax (filtreleme)."""
    # Basit forward (hmm_filtreleme ile aynı mantık)
    inanc = [1.0 - P0_YAGMUR, P0_YAGMUR]
    yol = []
    for e in gozlemler:
        pred = [0.0, 0.0]
        for i in range(2):
            for j in range(2):
                pred[j] += GECIS[i][j] * inanc[i]
        upd = [p_gozlem(j, e) * pred[j] for j in range(2)]
        s = sum(upd)
        inanc = [x / s for x in upd]
        yol.append(1 if inanc[1] >= inanc[0] else 0)
    return yol


def fmt_bool(b: bool) -> str:
    return "T" if b else "F"


def main() -> None:
    print("Viterbi — en olası hava yolu (özgün eğitim)\n")
    gozlemler = [True, True, False, True, True]
    print("Gözlem (Şemsiye):", [fmt_bool(g) for g in gozlemler])
    print()

    yol, skor = viterbi(gozlemler)
    marj = filtre_argmax(gozlemler)

    print("t | Şemsiye | Viterbi yolu | Marjinal argmax")
    print("--+---------+--------------+----------------")
    for t, e in enumerate(gozlemler):
        print(
            f"{t+1} |    {fmt_bool(e)}    | {DURUMLAR[yol[t]]:12} | {DURUMLAR[marj[t]]}"
        )

    print()
    print(f"Viterbi birleşik skor (ham): {skor:.6e}")
    print("Not: Viterbi tüm diziyi birlikte optimize eder; marjinal argmax adım adım bakar.")
    if yol != marj:
        print("Bu örnekte iki yol farklı — marjinal ≠ global en iyi yol.")
    else:
        print("Bu örnekte iki yol aynı çıktı; başka gözlem dizilerinde ayrışabilir.")


if __name__ == "__main__":
    main()
