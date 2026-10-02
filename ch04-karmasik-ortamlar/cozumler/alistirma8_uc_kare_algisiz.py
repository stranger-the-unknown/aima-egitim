#!/usr/bin/env python3
"""Alıştırma 8 çözümü: üç kareli algısız süpürge dünyası.

Durum: (konum ∈ {0, 1, 2}, kir₀, kir₁, kir₂) → 3 × 2³ = 24 fiziksel durum.
"""
from __future__ import annotations

from collections import deque
from itertools import product

KARE = 3
EYLEMLER = ["Sağ", "Sol", "Süpür"]
DURUMLAR = [(k, *kir) for k in range(KARE) for kir in product((True, False), repeat=KARE)]


def sonuc(s, eylem):
    k, *kir = s
    if eylem == "Sağ":
        return (min(k + 1, KARE - 1), *kir)
    if eylem == "Sol":
        return (max(k - 1, 0), *kir)
    kir[k] = False
    return (k, *kir)


def hedef_mi(s) -> bool:
    return not any(s[1:])


def algisiz_bfs(baslangic: frozenset):
    sinir = deque([(baslangic, [])])
    goruldu = {baslangic}
    while sinir:
        b, plan = sinir.popleft()
        if all(hedef_mi(s) for s in b):
            return plan, b
        for e in EYLEMLER:
            b2 = frozenset(sonuc(s, e) for s in b)
            if b2 not in goruldu:
                goruldu.add(b2)
                sinir.append((b2, plan + [e]))
    return None, None


def main() -> None:
    b0 = frozenset(DURUMLAR)
    print(f"Fiziksel durum sayısı: {len(DURUMLAR)}; başlangıç inancı: 24 durumun tamamı")
    plan, son = algisiz_bfs(b0)
    print(f"En kısa algısız plan ({len(plan)} adım): [{', '.join(plan)}]")
    print(f"Son inanç: {sorted(son)}")
    print("\nİki karede 4 adım yetiyordu; üç karede 7 adım gerekiyor. Ajan konumunu bilmediği"
          "\niçin önce bir uca 'yaslanmalı' (iki kez Sağ). Sonra her kareyi sırayla süpürmeli."
          "\nKonum bilgisi olsaydı daha kısa planlar mümkün olurdu.")


if __name__ == "__main__":
    main()
