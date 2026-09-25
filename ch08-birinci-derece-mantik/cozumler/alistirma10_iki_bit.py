#!/usr/bin/env python3
"""Alıştırma 10 çözümü: iki tam toplayıcıdan iki bitlik dalgalı elde toplayıcı.

Adım 3 (sözcük dağarcığı): C1 ile aynı; yeni devre sabitleri FA0, FA1 ve C2.
Adım 5 (problem örneği):
    Devre(FA0) ∧ Devre(FA1): ikisi de C1 ile aynı iç yapıda (tam toplayıcı)
    Bağlı(Giriş(1,C2), Giriş(1,FA0))   a0
    Bağlı(Giriş(2,C2), Giriş(2,FA0))   b0
    Bağlı(Giriş(3,C2), Giriş(3,FA0))   elde0
    Bağlı(Giriş(4,C2), Giriş(1,FA1))   a1
    Bağlı(Giriş(5,C2), Giriş(2,FA1))   b1
    Bağlı(Çıkış(2,FA0), Giriş(3,FA1))  ← dalgalı elde
    Bağlı(Çıkış(1,FA0), Çıkış(1,C2))   s0
    Bağlı(Çıkış(1,FA1), Çıkış(2,C2))   s1
    Bağlı(Çıkış(2,FA1), Çıkış(3,C2))   elde2
"""
from __future__ import annotations

import sys
from itertools import product
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ornekler"))

from tam_toplayici import cikislar  # noqa: E402  — C1'in çıkarım tabanlı simülatörü


def iki_bit_topla(a1, a0, b1, b0, elde0, bozuk: bool = False) -> tuple[int, int, int]:
    """Döner: (elde2, s1, s0). bozuk=True: FA1'in eldesine yanlışlıkla FA0'ın toplamı bağlı."""
    s0, elde1 = cikislar((a0, b0, elde0))       # FA0
    ucuncu = s0 if bozuk else elde1              # Bağlı(Çıkış(2,FA0), Giriş(3,FA1))
    s1, elde2 = cikislar((a1, b1, ucuncu))       # FA1
    return elde2, s1, s0


def dogrula(bozuk: bool = False) -> list:
    hatalar = []
    for a1, a0, b1, b0, c0 in product((0, 1), repeat=5):
        e2, s1, s0 = iki_bit_topla(a1, a0, b1, b0, c0, bozuk)
        sonuc = 4 * e2 + 2 * s1 + s0
        beklenen = (2 * a1 + a0) + (2 * b1 + b0) + c0
        if sonuc != beklenen:
            hatalar.append(((a1, a0, b1, b0, c0), sonuc, beklenen))
    return hatalar


def main() -> None:
    print(f"Doğru bağlantılarla 32 girişte hata sayısı: {len(dogrula())}")
    e2, s1, s0 = iki_bit_topla(1, 1, 1, 0, 1)
    print(f"Örnek: 11₂ + 10₂ + 1 = {4 * e2 + 2 * s1 + s0}  (elde2, s1, s0 = {e2}, {s1}, {s0})")
    hatalar = dogrula(bozuk=True)
    print(f"\nBozuk bağlantı (FA1'in eldesine FA0'ın TOPLAM biti bağlı): {len(hatalar)} hatalı satır")
    for g, gercek, beklenen in hatalar[:5]:
        print(f"  a1a0={g[0]}{g[1]} b1b0={g[2]}{g[3]} elde0={g[4]}: {gercek}, olması gereken {beklenen}")
    print("  …\nHatalar yalnızca FA0'ın toplam biti ile elde bitinin farklı olduğu girişlerde ortaya çıkar."
          "\nBu desen, hatanın FA0 → FA1 bağlantısında olduğunu gösterir.")


if __name__ == "__main__":
    main()
