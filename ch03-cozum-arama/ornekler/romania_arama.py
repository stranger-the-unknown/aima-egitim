#!/usr/bin/env python3
"""Romanya haritasında arama: kitabın klasik örneği.

Arad'dan Bucharest'e en kısa yolu farklı algoritmalarla arıyoruz.
Harita ve kuş uçuşu mesafeleri (SLD) kitaptaki örnekle aynıdır; sonuçları
kitaptaki şekillerle karşılaştırabilirsin:

  * A* izi: Arad(366) → Sibiu(393) → Rimnicu Vilcea(413) → Fagaras(415)
            → Pitesti(417) → Bucharest(418)
  * A* ve UCS optimal yolu bulur: Arad–Sibiu–Rimnicu Vilcea–Pitesti–Bucharest = 418 km
  * Açgözlü arama Fagaras üzerinden gider: 450 km (optimal değil)

Çalıştırma:
    python romania_arama.py
    python romania_arama.py --baslangic Timisoara     # hedef yine Bucharest
    python romania_arama.py --baslangic Oradea --hedef Neamt  (SLD yok: h = 0)
"""
from __future__ import annotations

import argparse
import heapq
import math

from arama import (Problem, Sonuc, a_yildiz, acgozlu, agirlikli_a_yildiz,
                   derinlik_oncelikli, genislik_oncelikli, tekduze_maliyet,
                   yinelemeli_derinlesme)

# Yollar (km). Harita yönsüzdür; her yolu bir kez yazıp iki yöne ekliyoruz.
YOLLAR = [
    ("Arad", "Zerind", 75), ("Arad", "Sibiu", 140), ("Arad", "Timisoara", 118),
    ("Zerind", "Oradea", 71), ("Oradea", "Sibiu", 151), ("Timisoara", "Lugoj", 111),
    ("Lugoj", "Mehadia", 70), ("Mehadia", "Drobeta", 75), ("Drobeta", "Craiova", 120),
    ("Craiova", "Rimnicu Vilcea", 146), ("Craiova", "Pitesti", 138),
    ("Rimnicu Vilcea", "Sibiu", 80), ("Rimnicu Vilcea", "Pitesti", 97),
    ("Sibiu", "Fagaras", 99), ("Fagaras", "Bucharest", 211), ("Pitesti", "Bucharest", 101),
    ("Bucharest", "Giurgiu", 90), ("Bucharest", "Urziceni", 85), ("Urziceni", "Hirsova", 98),
    ("Hirsova", "Eforie", 86), ("Urziceni", "Vaslui", 142), ("Vaslui", "Iasi", 92),
    ("Iasi", "Neamt", 87),
]

HARITA: dict[str, dict[str, int]] = {}
for a, b, km in YOLLAR:
    HARITA.setdefault(a, {})[b] = km
    HARITA.setdefault(b, {})[a] = km

# Bucharest'e kuş uçuşu mesafe (km): kabul edilebilir bir sezgisel
SLD_BUCHAREST = {
    "Arad": 366, "Bucharest": 0, "Craiova": 160, "Drobeta": 242, "Eforie": 161,
    "Fagaras": 176, "Giurgiu": 77, "Hirsova": 151, "Iasi": 226, "Lugoj": 244,
    "Mehadia": 241, "Neamt": 234, "Oradea": 380, "Pitesti": 100, "Rimnicu Vilcea": 193,
    "Sibiu": 253, "Timisoara": 329, "Urziceni": 80, "Vaslui": 199, "Zerind": 374,
}


class RomanyaProblemi(Problem):
    """Durum: şehir adı (atomik temsil). Eylem: gidilecek komşu şehir."""

    def eylemler(self, sehir):
        return list(HARITA[sehir])

    def sonuc(self, sehir, eylem):
        return eylem

    def eylem_maliyeti(self, s, eylem, s2):
        return HARITA[s][s2]

    def h(self, dugum):
        if self.hedef == "Bucharest":
            return SLD_BUCHAREST[dugum.durum]
        return 0  # bu hedef için sezgisel tablomuz yok


def iki_yonlu_ucs(baslangic: str, hedef: str) -> Sonuc:
    """Çift yönlü tekdüze maliyet araması (yönsüz graf için).

    İki arama aynı anda ilerler: biri başlangıçtan, biri hedeften.
    Durma koşulu: iki sınırın en küçük g değerlerinin toplamı, bulunan en iyi
    yolun maliyetinden küçük değilse daha iyi bir yol bulunamaz.
    """
    sonuc = Sonuc("Çift yönlü UCS", None)
    if baslangic == hedef:
        return sonuc
    g = {"ileri": {baslangic: 0}, "geri": {hedef: 0}}
    ebeveyn = {"ileri": {baslangic: None}, "geri": {hedef: None}}
    sinir = {"ileri": [(0, baslangic)], "geri": [(0, hedef)]}
    en_iyi, bulusma = math.inf, None

    while sinir["ileri"] and sinir["geri"]:
        if sinir["ileri"][0][0] + sinir["geri"][0][0] >= en_iyi:
            break
        yon = "ileri" if sinir["ileri"][0][0] <= sinir["geri"][0][0] else "geri"
        diger = "geri" if yon == "ileri" else "ileri"
        maliyet, sehir = heapq.heappop(sinir[yon])
        if maliyet > g[yon][sehir]:
            continue
        sonuc.genisletilen += 1
        for komsu, km in HARITA[sehir].items():
            yeni = maliyet + km
            if yeni < g[yon].get(komsu, math.inf):
                g[yon][komsu] = yeni
                ebeveyn[yon][komsu] = sehir
                heapq.heappush(sinir[yon], (yeni, komsu))
            if komsu in g[diger] and g[yon][komsu] + g[diger][komsu] < en_iyi:
                en_iyi = g[yon][komsu] + g[diger][komsu]
                bulusma = komsu

    if bulusma is None:
        return sonuc
    # Yolu birleştir: başlangıç → buluşma ← hedef
    sol, s = [], bulusma
    while s is not None:
        sol.append(s)
        s = ebeveyn["ileri"][s]
    sag, s = [], ebeveyn["geri"][bulusma]
    while s is not None:
        sag.append(s)
        s = ebeveyn["geri"][s]
    sonuc.cift_yonlu_yol = sol[::-1] + sag
    sonuc.cift_yonlu_maliyet = en_iyi
    return sonuc


def a_yildiz_izi(baslangic: str = "Arad", hedef: str = "Bucharest") -> list[tuple[str, float, float, float]]:
    """A*'ın kuyruktan çıkardığı düğümler: (şehir, g, h, f)."""
    p = RomanyaProblemi(baslangic, hedef)
    iz: list[tuple[str, float, float, float]] = []
    a_yildiz(p, izle=lambda n, f: iz.append((n.durum, n.g, p.h(n), f)))
    return iz


def karsilastir(baslangic: str, hedef: str) -> list[Sonuc]:
    p = RomanyaProblemi(baslangic, hedef)
    return [
        genislik_oncelikli(p),
        derinlik_oncelikli(p),
        yinelemeli_derinlesme(p),
        tekduze_maliyet(p),
        acgozlu(p),
        a_yildiz(p),
        agirlikli_a_yildiz(p, W=2.0),
    ]


def main() -> None:
    ap = argparse.ArgumentParser(description="Romanya haritasında arama")
    ap.add_argument("--baslangic", default="Arad")
    ap.add_argument("--hedef", default="Bucharest")
    a = ap.parse_args()
    if a.baslangic not in HARITA or a.hedef not in HARITA:
        raise SystemExit(f"Bilinmeyen şehir. Seçenekler: {', '.join(sorted(HARITA))}")

    print("=" * 78)
    print(f"ROMANYA: {a.baslangic} → {a.hedef}")
    print("Sezgisel: kuş uçuşu mesafe (SLD)" if a.hedef == "Bucharest"
          else "Sezgisel: h = 0 (SLD tablosu yalnızca Bucharest için var)")
    print("=" * 78)

    sonuclar = karsilastir(a.baslangic, a.hedef)
    print(f"{'Algoritma':<16}{'km':>6}{'kenar':>7}{'genişl.':>9}{'üretilen':>10}{'en büyük sınır':>16}")
    print("-" * 78)
    for s in sonuclar:
        km = f"{s.maliyet:.0f}" if s.basarili else "—"
        kenar = len(s.yol) - 1 if s.basarili else "—"
        print(f"{s.algoritma:<16}{km:>6}{kenar:>7}{s.genisletilen:>9}{s.uretilen:>10}{s.en_buyuk_sinir:>16}")
    cy = iki_yonlu_ucs(a.baslangic, a.hedef)
    print(f"{cy.algoritma:<16}{getattr(cy, 'cift_yonlu_maliyet', math.inf):>6.0f}"
          f"{len(getattr(cy, 'cift_yonlu_yol', [])) - 1:>7}{cy.genisletilen:>9}")
    print("-" * 78)

    print("\nBulunan yollar:")
    for s in sonuclar:
        print(f"  {s.algoritma:<14} {' → '.join(s.yol)}")
    print(f"  {'Çift yönlü':<14} {' → '.join(getattr(cy, 'cift_yonlu_yol', []))}")

    if a.hedef == "Bucharest":
        print("\nA* izi (kuyruktan çıkış sırası, f = g + h):")
        print(f"  {'şehir':<16}{'g':>6}{'h':>6}{'f':>6}")
        for sehir, g, h, f in a_yildiz_izi(a.baslangic, a.hedef):
            print(f"  {sehir:<16}{g:>6.0f}{h:>6.0f}{f:>6.0f}")
        print("  Dikkat: Bucharest ilk kez Fagaras üzerinden f=450 ile sınıra girer, ama"
              "\n  A* onu çıkarmadan önce f=417 olan Pitesti'yi genişletir ve 418'lik yolu bulur.")

    print("\nOkuma notları:")
    print("  • BFS ve IDS en az *kenarlı* yolu bulur; km açısından optimal değildir.")
    print("  • DFS'in bulduğu yol komşu sırasına bağlıdır; burada şans eseri iyi olabilir."
          "\n    --baslangic Oradea --hedef Neamt ile dene: DFS 13 kenarlı, 1285 km'lik bir yol bulur.")
    print("  • UCS ve A* optimaldir. A* sezgisel sayesinde çok daha az düğüm genişletir.")
    print("  • Açgözlü arama hızlıdır ama optimal değildir.")
    print("  • Ağırlıklı A* (W=2) h'ye fazla güvenir: daha az iş yapar, optimal olmayabilir.")


if __name__ == "__main__":
    main()
