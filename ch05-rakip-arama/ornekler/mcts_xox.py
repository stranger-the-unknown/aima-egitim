#!/usr/bin/env python3
"""Monte Carlo ağaç araması (MCTS, UCT seçimi) ile XOX.

MCTS değerlendirme fonksiyonu kullanmaz. Durumun değerini, oradan rastgele
oynanan oyunların (playout) sonuçlarının ortalamasıyla tahmin eder. Her yinelemede:

    1. Seçim      : Kökten başlayıp UCB1'i en büyük çocuğa inerek bir yaprağa ulaş.
    2. Genişletme : Yaprağa henüz denenmemiş bir çocuk ekle.
    3. Benzetim   : O çocuktan rastgele hamlelerle oyunu sonuna kadar oyna.
    4. Geri yayma : Sonucu yol boyunca tüm düğümlerin sayaçlarına ekle.

    UCB1(n) = U(n)/N(n) + C · √( ln N(ebeveyn) / N(n) )
              └ sömürü ┘   └──────── keşif ────────┘

Kitaptaki örnek (ebeveynde 100 oyun; çocuklar 60/79, 1/10, 2/11):
    C = 1,4 ise UCB1'i en büyük çocuk 60/79, C = 1,5 ise 2/11 olur.

Çalıştırma:
    python mcts_xox.py
    python mcts_xox.py --iterasyon 500
"""
from __future__ import annotations

import argparse
import math
import random
from dataclasses import dataclass, field

from minimax_tictactoe import Boş, O, X, en_iyi_hamle, hamleler, kazanan, uygula, utility


def ucb1(U: float, N: int, N_ebeveyn: int, C: float = math.sqrt(2)) -> float:
    if N == 0:
        return math.inf
    return U / N + C * math.sqrt(math.log(N_ebeveyn) / N)


def rakip(oyuncu: str) -> str:
    return O if oyuncu == X else X


@dataclass(eq=False)
class Dugum:
    tahta: list
    sira: str                      # bu durumda hamle sırası kimde
    ebeveyn: "Dugum | None" = None
    hamle: int | None = None       # ebeveynden buraya getiren hamle
    cocuklar: list = field(default_factory=list)
    denenmemis: list = field(default_factory=list)
    U: float = 0.0                 # bu düğüme hamle yapan oyuncunun toplam kazancı
    N: int = 0

    def __post_init__(self) -> None:
        if utility(self.tahta) is None:
            self.denenmemis = hamleler(self.tahta)


def playout(tahta: list, sira: str, rng: random.Random) -> str | None:
    """Rastgele oyna; kazananı (X/O) ya da beraberlik için None döndür."""
    t = list(tahta)
    while utility(t) is None:
        t[rng.choice(hamleler(t))] = sira
        sira = rakip(sira)
    return kazanan(t)


def mcts(tahta: list, sira: str, iterasyon: int = 2000, C: float = math.sqrt(2),
         rng: random.Random | None = None) -> tuple[int, Dugum]:
    rng = rng or random.Random(0)
    kok = Dugum(list(tahta), sira)
    for _ in range(iterasyon):
        # 1. Seçim
        n = kok
        while not n.denenmemis and n.cocuklar:
            n = max(n.cocuklar, key=lambda c: ucb1(c.U, c.N, n.N, C))
        # 2. Genişletme
        if n.denenmemis:
            h = n.denenmemis.pop(rng.randrange(len(n.denenmemis)))
            cocuk = Dugum(uygula(n.tahta, h, n.sira), rakip(n.sira), n, h)
            n.cocuklar.append(cocuk)
            n = cocuk
        # 3. Benzetim
        kazanan_oyuncu = playout(n.tahta, n.sira, rng)
        # 4. Geri yayma: her düğümün U'su, o düğüme hamle yapan oyuncunun bakış açısından
        while n is not None:
            n.N += 1
            hamle_yapan = rakip(n.sira)
            if kazanan_oyuncu is None:
                n.U += 0.5
            elif kazanan_oyuncu == hamle_yapan:
                n.U += 1
            n = n.ebeveyn
    # En çok oynanan hamleyi seç (kitaptaki gibi: ortalaması yüksek ama az denenmiş olanı değil)
    en_iyi = max(kok.cocuklar, key=lambda c: c.N)
    return en_iyi.hamle, kok


def tahta_metni(t: list) -> str:
    return "\n".join("    " + " ".join(t[r * 3:r * 3 + 3]) for r in range(3))


def oyun(x_oyuncusu, o_oyuncusu) -> int:
    """Oyunu oynat; X açısından sonucu döndür (+1, 0, −1)."""
    t, sira = [Boş] * 9, X
    while utility(t) is None:
        h = (x_oyuncusu if sira == X else o_oyuncusu)(t, sira)
        t = uygula(t, h, sira)
        sira = rakip(sira)
    return utility(t)


def main() -> None:
    ap = argparse.ArgumentParser(description="MCTS ile XOX")
    ap.add_argument("--iterasyon", type=int, default=2000)
    args = ap.parse_args()

    print("=== Kitaptaki UCB1 örneği (ebeveyn N = 100) ===")
    cocuklar = {"60/79": (60, 79), "1/10": (1, 10), "2/11": (2, 11)}
    for C in (1.4, 1.5):
        puan = {ad: ucb1(u, n, 100, C) for ad, (u, n) in cocuklar.items()}
        secilen = max(puan, key=puan.get)
        print(f"  C = {C}: " + ", ".join(f"{ad} → {p:.3f}" for ad, p in puan.items()) + f"   seçilen: {secilen}")

    print(f"\n=== Pozisyonlarda MCTS ({args.iterasyon} yineleme) ===")
    pozisyonlar = [
        ("X kazanabilir (8. hücre)", list("XO.OX...."), X),
        ("O, X'in kazanmasını engellemeli (2. hücre)", list("XX..O...."), O),
    ]
    for ad, t, sira in pozisyonlar:
        h, kok = mcts(t, sira, args.iterasyon)
        ziyaret = ", ".join(f"{c.hamle}:{c.N}" for c in sorted(kok.cocuklar, key=lambda c: -c.N)[:4])
        print(f"\n  {ad}; sıra {sira}\n{tahta_metni(t)}")
        print(f"  MCTS seçimi: {h}   (en çok ziyaret edilenler hücre:N → {ziyaret})")

    print("\n=== MCTS (X) — minimax (O), 10 oyun ===")
    rng = random.Random(1)
    sonuclar = [oyun(lambda t, s: mcts(t, s, args.iterasyon, rng=rng)[0],
                     lambda t, s: en_iyi_hamle(t, s, True)[0]) for _ in range(10)]
    print(f"  X kazandı: {sonuclar.count(1)}, beraberlik: {sonuclar.count(0)}, O kazandı: {sonuclar.count(-1)}")
    print("\nMCTS hiçbir değerlendirme fonksiyonu ya da oyun bilgisi kullanmadan, yalnızca"
          "\nrastgele oyunlarla, kusursuz oynayan minimax'a karşı berabere kalabiliyor.")


if __name__ == "__main__":
    main()
