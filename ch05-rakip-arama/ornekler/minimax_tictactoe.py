#!/usr/bin/env python3
"""XOX (tic-tac-toe) — minimax ve isteğe bağlı alpha-beta. Bölüm 5."""
from __future__ import annotations

import argparse
from typing import List, Optional, Tuple

# Tahta: 9 hücre, "." boş, "X" MAX, "O" MIN. İndeks 0..8 satır-major.
Boş = "."
X, O = "X", "O"
Tahta = List[str]

# Kazanan çizgiler
CIZGILER = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
)

# İstatistik (budama / düğüm sayacı)
_dugum = 0


def sayac_sifirla() -> None:
    global _dugum
    _dugum = 0


def dugum_sayisi() -> int:
    return _dugum


def yazdir(tahta: Tahta) -> None:
    for r in range(3):
        satir = " | ".join(tahta[r * 3 : r * 3 + 3])
        print(" " + satir)
        if r < 2:
            print("---+---+---")


def kazanan(tahta: Tahta) -> Optional[str]:
    for a, b, c in CIZGILER:
        if tahta[a] != Boş and tahta[a] == tahta[b] == tahta[c]:
            return tahta[a]
    return None


def dolu(tahta: Tahta) -> bool:
    return Boş not in tahta


def utility(tahta: Tahta) -> Optional[int]:
    """Bittiysa MAX açısından +1 / 0 / -1; değilse None."""
    k = kazanan(tahta)
    if k == X:
        return 1
    if k == O:
        return -1
    if dolu(tahta):
        return 0
    return None


def hamleler(tahta: Tahta) -> List[int]:
    return [i for i, h in enumerate(tahta) if h == Boş]


def uygula(tahta: Tahta, idx: int, oyuncu: str) -> Tahta:
    yeni = list(tahta)
    yeni[idx] = oyuncu
    return yeni


def minimax(tahta: Tahta, max_sira: bool) -> int:
    """Saf minimax; dönüş değeri MAX utility."""
    global _dugum
    _dugum += 1
    u = utility(tahta)
    if u is not None:
        return u
    if max_sira:
        en = -2
        for h in hamleler(tahta):
            en = max(en, minimax(uygula(tahta, h, X), False))
        return en
    en = 2
    for h in hamleler(tahta):
        en = min(en, minimax(uygula(tahta, h, O), True))
    return en


def alphabeta(
    tahta: Tahta, max_sira: bool, alpha: float = float("-inf"), beta: float = float("inf")
) -> int:
    global _dugum
    _dugum += 1
    u = utility(tahta)
    if u is not None:
        return u
    if max_sira:
        deger = float("-inf")
        for h in hamleler(tahta):
            deger = max(deger, alphabeta(uygula(tahta, h, X), False, alpha, beta))
            alpha = max(alpha, deger)
            if alpha >= beta:
                break
        return int(deger)
    deger = float("inf")
    for h in hamleler(tahta):
        deger = min(deger, alphabeta(uygula(tahta, h, O), True, alpha, beta))
        beta = min(beta, deger)
        if alpha >= beta:
            break
    return int(deger)


def en_iyi_hamle(tahta: Tahta, oyuncu: str, kullan_ab: bool) -> Tuple[int, int]:
    """(hamle_indeksi, beklenen_utility_MAX_açısından)."""
    sayac_sifirla()
    adaylar = hamleler(tahta)
    if not adaylar:
        raise ValueError("Hamle yok")

    def degerle(t: Tahta, max_sira: bool) -> int:
        return alphabeta(t, max_sira) if kullan_ab else minimax(t, max_sira)

    if oyuncu == X:
        en_h, en_v = adaylar[0], -2
        for h in adaylar:
            v = degerle(uygula(tahta, h, X), False)
            if v > en_v:
                en_v, en_h = v, h
        return en_h, en_v
    # O: MAX utility'sini küçült
    en_h, en_v = adaylar[0], 2
    for h in adaylar:
        v = degerle(uygula(tahta, h, O), True)
        if v < en_v:
            en_v, en_h = v, h
    return en_h, en_v


def parse_tahta(s: str) -> Tahta:
    s = s.strip().replace(" ", "")
    if len(s) != 9 or any(c not in "XO." for c in s):
        raise SystemExit("Tahta 9 karakter olmalı: X, O veya . — örn. X.O.X.O..")
    return list(s)


def siradaki(tahta: Tahta) -> str:
    return X if tahta.count(X) == tahta.count(O) else O


def ajan_ajan(kullan_ab: bool) -> None:
    tahta: Tahta = [Boş] * 9
    oyuncu = X
    tur = 0
    print("=== Ajan vs Ajan (ikisi de optimal) ===\n")
    yazdir(tahta)
    while utility(tahta) is None:
        tur += 1
        h, v = en_iyi_hamle(tahta, oyuncu, kullan_ab)
        dugum = dugum_sayisi()
        print(
            f"\nTur {tur}: {oyuncu} → hücre {h} "
            f"(beklenen utility={v}, incelenen düğüm≈{dugum})"
        )
        tahta = uygula(tahta, h, oyuncu)
        yazdir(tahta)
        oyuncu = O if oyuncu == X else X

    u = utility(tahta)
    print()
    if u == 1:
        print("Sonuç: X kazandı.")
    elif u == -1:
        print("Sonuç: O kazandı.")
    else:
        print("Sonuç: Beraberlik (optimal oyunda beklenen).")


def goster_en_iyi(tahta: Tahta, kullan_ab: bool) -> None:
    print("=== Pozisyondan en iyi hamle ===\n")
    yazdir(tahta)
    u = utility(tahta)
    if u is not None:
        print(f"\nOyun bitmiş (utility={u}).")
        return
    oyuncu = siradaki(tahta)
    h, v = en_iyi_hamle(tahta, oyuncu, kullan_ab)
    print(f"\nSıra: {oyuncu}")
    print(f"En iyi hücre: {h} (0–8, satır-major)")
    print(f"Beklenen utility (MAX/X açısından): {v}")
    print(f"İncelenen düğüm≈{dugum_sayisi()}")
    print("\nHamle sonrası:")
    yazdir(uygula(tahta, h, oyuncu))


def main() -> None:
    p = argparse.ArgumentParser(description="XOX minimax / alpha-beta")
    p.add_argument(
        "--mod",
        choices=("ajan-ajan", "en-iyi"),
        default="ajan-ajan",
        help="ajan-ajan: iki optimal ajan; en-iyi: verilen tahtada hamle",
    )
    p.add_argument(
        "--tahta",
        default=".........",
        help='9 karakter, örn. "X.O.X.O.." (en-iyi modu)',
    )
    p.add_argument(
        "--alpha-beta",
        action="store_true",
        help="Alpha-beta budama kullan",
    )
    args = p.parse_args()
    ab = args.alpha_beta
    etiket = "alpha-beta" if ab else "saf minimax"
    print(f"(Arama: {etiket})\n")

    if args.mod == "ajan-ajan":
        ajan_ajan(ab)
    else:
        goster_en_iyi(parse_tahta(args.tahta), ab)


if __name__ == "__main__":
    main()
