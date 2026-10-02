#!/usr/bin/env python3
"""Alıştırma 7 çözümü: XOX için değerlendirme fonksiyonu ve derinlik sınırlı minimax.

EVAL = (3·X₂ + X₁) − (3·O₂ + O₁)
X₂: içinde tam 2 X olan ve O olmayan hat sayısı; X₁: tam 1 X olan ve O olmayan hat sayısı.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ornekler"))

from minimax_tictactoe import (CIZGILER, Boş, O, X, en_iyi_hamle, hamleler,  # noqa: E402
                               uygula, utility)

KAZANC = 100  # terminal değerler EVAL'ın ulaşabileceği her değerden büyük olmalı


def degerlendir(t: list) -> int:
    puan = 0
    for hat in CIZGILER:
        degerler = [t[i] for i in hat]
        x, o = degerler.count(X), degerler.count(O)
        if o == 0:
            puan += {1: 1, 2: 3}.get(x, 0)
        if x == 0:
            puan -= {1: 1, 2: 3}.get(o, 0)
    return puan


def sinirli_minimax(t: list, max_sirasi: bool, derinlik: int) -> int:
    u = utility(t)
    if u is not None:
        return u * KAZANC
    if derinlik == 0:
        return degerlendir(t)
    oyuncu = X if max_sirasi else O
    degerler = [sinirli_minimax(uygula(t, h, oyuncu), not max_sirasi, derinlik - 1) for h in hamleler(t)]
    return max(degerler) if max_sirasi else min(degerler)


def sinirli_hamle(t: list, oyuncu: str, derinlik: int) -> int:
    max_sirasi = oyuncu == X
    puanlar = {h: sinirli_minimax(uygula(t, h, oyuncu), not max_sirasi, derinlik - 1) for h in hamleler(t)}
    return (max if max_sirasi else min)(puanlar, key=puanlar.get)


def oyun(x_hamle, o_hamle) -> int:
    t, sira = [Boş] * 9, X
    while utility(t) is None:
        t = uygula(t, (x_hamle if sira == X else o_hamle)(t, sira), sira)
        sira = O if sira == X else X
    return utility(t)


def kaybedebilir_mi(derinlik: int, ajan: str) -> bool:
    """Rakibin olası TÜM hamle dizilerini dene: ajan herhangi birinde kaybediyor mu?"""
    def gez(t: list, sira: str) -> bool:
        u = utility(t)
        if u is not None:
            return (u == -1) if ajan == X else (u == 1)
        if sira == ajan:
            return gez(uygula(t, sinirli_hamle(t, sira, derinlik), sira), O if sira == X else X)
        return any(gez(uygula(t, h, sira), O if sira == X else X) for h in hamleler(t))
    return gez([Boş] * 9, X)


def main() -> None:
    bos = [Boş] * 9
    print(f"X ortaya oynadıktan sonra EVAL = {degerlendir(uygula(bos, 4, X))}")
    print(f"X köşeye oynadıktan sonra EVAL = {degerlendir(uygula(bos, 0, X))}")
    print(f"X kenara oynadıktan sonra EVAL = {degerlendir(uygula(bos, 1, X))}\n")

    tam = lambda t, s: en_iyi_hamle(t, s, True)[0]  # noqa: E731
    print(f"{'derinlik':>9}  {'X olarak':>10}  {'O olarak':>10}   (tam minimax'a karşı sonuç)")
    for d in (1, 2, 3, 4):
        ajan = lambda t, s, d=d: sinirli_hamle(t, s, d)  # noqa: E731
        x_sonuc = oyun(ajan, tam)
        o_sonuc = oyun(tam, ajan)
        metin = {1: "kazandı", 0: "berabere", -1: "kaybetti"}
        print(f"{d:>9}  {metin[x_sonuc]:>10}  {metin[-o_sonuc]:>10}")

    print("\nDaha güçlü sınav: rakibin olası TÜM hamle dizilerine karşı kaybedebilir mi?")
    print(f"{'derinlik':>9}  {'X olarak':>10}  {'O olarak':>10}")
    for d in (1, 2, 3, 4):
        x_k = "kaybedebilir" if kaybedebilir_mi(d, X) else "asla"
        o_k = "kaybedebilir" if kaybedebilir_mi(d, O) else "asla"
        print(f"{d:>9}  {x_k:>10}  {o_k:>10}")


if __name__ == "__main__":
    main()
