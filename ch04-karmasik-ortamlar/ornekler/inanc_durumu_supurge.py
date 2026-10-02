#!/usr/bin/env python3
"""Kısmi gözlem: inanç durumu uzayında arama (süpürge dünyası).

İnanç durumu = ajanın "şu an içinde olabileceğim fiziksel durumlar" kümesi.
Durum numaraları kitaptakiyle aynı (bkz. and_or_supurge.py): 7 ve 8 hedef.

Bölüm 1 — Algısız (sensorless) süpürge
    Ajan ne konumunu ne de kiri görür. Başlangıç inancı {1, …, 8}.
    Kitaptaki sonuç: [Sağ, Süpür, Sol, Süpür] her başlangıçta hedefe (7) götürür.
    İnanç durumları uzayında BFS bu planı bulur.

Bölüm 2 — Yerel algılı süpürge
    Ajan konumunu ve bulunduğu karenin kirli olup olmadığını görür.
    İnanç güncellemesi iki adımdır:
      TAHMİN   : b' = ∪_{s ∈ b} SONUÇ(s, a)
      GÜNCELLE : b'' = {s ∈ b' : ALGI(s) = gözlenen algı}
    Kitaptaki örnek: ilk algı [Sol, Kirli] → inanç {1, 3}.

Çalıştırma:
    python inanc_durumu_supurge.py
"""
from __future__ import annotations

from collections import deque

NUMARA = {
    ("L", True, True): 1, ("R", True, True): 2,
    ("L", True, False): 3, ("R", True, False): 4,
    ("L", False, True): 5, ("R", False, True): 6,
    ("L", False, False): 7, ("R", False, False): 8,
}
DURUM = {n: d for d, n in NUMARA.items()}
HEDEFLER = frozenset({7, 8})
EYLEMLER = ["Sağ", "Sol", "Süpür"]


def sonuc(s: int, eylem: str) -> int:
    """Deterministik süpürge dünyası."""
    konum, sol, sag = DURUM[s]
    if eylem == "Sağ":
        return NUMARA[("R", sol, sag)]
    if eylem == "Sol":
        return NUMARA[("L", sol, sag)]
    return NUMARA[(konum, False, sag) if konum == "L" else (konum, sol, False)]


def tahmin(inanc: frozenset[int], eylem: str) -> frozenset[int]:
    return frozenset(sonuc(s, eylem) for s in inanc)


def algi(s: int) -> tuple[str, str]:
    """Yerel algı: (konum, bulunduğun kare kirli mi)."""
    konum, sol, sag = DURUM[s]
    kirli = sol if konum == "L" else sag
    return ("Sol" if konum == "L" else "Sağ", "Kirli" if kirli else "Temiz")


def guncelle(inanc: frozenset[int], gozlem: tuple[str, str]) -> frozenset[int]:
    return frozenset(s for s in inanc if algi(s) == gozlem)


def algisiz_plan(baslangic: frozenset[int]) -> list[tuple[str, frozenset[int]]]:
    """İnanç durumu uzayında BFS. Hedef: inancın tamamı hedef durumlardan oluşsun."""
    sinir = deque([(baslangic, [])])
    goruldu = {baslangic}
    while sinir:
        b, yol = sinir.popleft()
        if b <= HEDEFLER:
            return yol
        for eylem in EYLEMLER:
            b2 = tahmin(b, eylem)
            if b2 not in goruldu:
                goruldu.add(b2)
                sinir.append((b2, yol + [(eylem, b2)]))
    return []


def goster(b: frozenset[int]) -> str:
    return "{" + ", ".join(map(str, sorted(b))) + "}"


def main() -> None:
    print("=== Bölüm 1: Algısız süpürge ===")
    b0 = frozenset(range(1, 9))
    print(f"Başlangıç inancı: {goster(b0)}  ({2 ** 8 - 1} olası boş olmayan inanç durumu var)")
    plan = algisiz_plan(b0)
    for eylem, b in plan:
        print(f"  {eylem:<6} → {goster(b)}")
    print(f"Plan: [{', '.join(e for e, _ in plan)}]  (kitap: [Sağ, Süpür, Sol, Süpür])")
    print("Ajan hiçbir şey görmeden dünyayı durum 7'ye 'zorladı'. Sağ'a gitmek bile bilgi verdi:"
          "\n{1..8} → {2, 4, 6, 8} (artık sağda olduğunu biliyor).")

    print("\n=== Bölüm 2: Yerel algılı süpürge — inanç güncelleme ===")
    b = guncelle(b0, ("Sol", "Kirli"))
    print(f"İlk algı [Sol, Kirli]           → {goster(b)}   (kitap: {{1, 3}})")
    b_tahmin = tahmin(b, "Sağ")
    print(f"TAHMİN: Sağ                     → {goster(b_tahmin)}")
    for gozlem in [("Sağ", "Kirli"), ("Sağ", "Temiz")]:
        print(f"GÜNCELLE: algı [{gozlem[0]}, {gozlem[1]}]{' ' * (10 - len(gozlem[1]))}→ {goster(guncelle(b_tahmin, gozlem))}")
    print("\nHer algı inancı ya daraltır ya da aynı bırakır; asla genişletmez (deterministik algı)."
          "\nDeterministik olmayan ortamlarda ise TAHMİN adımı inancı genişletebilir.")


if __name__ == "__main__":
    main()
