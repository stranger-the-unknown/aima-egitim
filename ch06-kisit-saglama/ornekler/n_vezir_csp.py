#!/usr/bin/env python3
"""N-vezir problemi — CSP olarak backtracking (kısa eğitim örneği).

Değişken: sütun i'deki vezirin satırı. Kısıt: aynı satır / çapraz yok.
Bölüm 4'teki yerel aramadan fark: sistematik BT ile çözüm garantisi (varsa).
"""
from __future__ import annotations

import argparse
from typing import Dict, List, Optional


def guvenli(atama: Dict[int, int], sutun: int, satir: int) -> bool:
    for s, r in atama.items():
        if r == satir or abs(r - satir) == abs(s - sutun):
            return False
    return True


def bt(n: int, atama: Dict[int, int], sayac: Dict[str, int]) -> Optional[Dict[int, int]]:
    sayac["adim"] += 1
    if len(atama) == n:
        return dict(atama)
    sutun = len(atama)  # sütun sırası sabit; MRV isteğe bağlı genişletme
    for satir in range(n):
        if guvenli(atama, sutun, satir):
            atama[sutun] = satir
            sayac["deneme"] += 1
            sonuc = bt(n, atama, sayac)
            if sonuc is not None:
                return sonuc
            del atama[sutun]
    return None


def tahta_yazdir(atama: Dict[int, int], n: int) -> None:
    print(f"\n=== {n}-vezir çözümü (CSP backtracking) ===")
    for r in range(n):
        satir = []
        for c in range(n):
            satir.append("V" if atama.get(c) == r else ".")
        print(" ".join(satir))


def main() -> None:
    p = argparse.ArgumentParser(description="N-vezir CSP backtracking")
    p.add_argument("--n", type=int, default=8, help="Tahta boyutu (varsayılan 8)")
    args = p.parse_args()
    n = args.n
    if n < 1:
        raise SystemExit("n >= 1 olmalı")

    print(f"N-vezir CSP: {n} değişken (sütun), domain={{0..{n-1}}}, kısıt=satır/çapraz")
    sayac = {"adim": 0, "deneme": 0}
    sonuc = bt(n, {}, sayac)
    print(f"İstatistik: adım≈{sayac['adim']}, değer denemesi={sayac['deneme']}")
    if sonuc is None:
        print("Çözüm yok (n=2,3 gibi küçük bazı n'lerde).")
    else:
        tahta_yazdir(sonuc, n)
        print("Tüm vezirler birbirini saldırmıyor.")


if __name__ == "__main__":
    main()
