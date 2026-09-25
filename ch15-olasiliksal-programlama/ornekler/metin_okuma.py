#!/usr/bin/env python3
"""Programlar olasılık modeli olarak: bozulmuş metni okumak (kitaptaki 15.4'ün küçük bir sürümü).

Üretimsel program:
    n        ~ 3 + Poisson(2)                        (harf sayısı)
    harfler  ~ bağımsız (tekdüze) YA DA Markov (ikili harf) modeli
    görüntü  = harflerin 5×3 piksellik şekilleri yan yana
    gürültü  : her piksel p olasılıkla ters çevrilir
Çıkarım: Görüntüden harfleri bulmak. Kitap MCMC kullanır. Bizim modelimizde harf sınırları
bilindiği için kesin çıkarım mümkün: bağımsız modelde her harf ayrı ayrı, Markov modelinde
Viterbi (Bölüm 14) ile. Kitaptaki gözlem burada da görülür: Gürültü arttıkça ikili harf
modeli, olası harf dizileri hakkındaki önsel bilgisiyle daha iyi okur.

Çalıştırma:
    python metin_okuma.py
"""
from __future__ import annotations

import math
import random
from collections import Counter

SEKILLER = {
    "A": [".#.", "#.#", "###", "#.#", "#.#"], "B": ["##.", "#.#", "##.", "#.#", "##."],
    "D": ["##.", "#.#", "#.#", "#.#", "##."], "E": ["###", "#..", "##.", "#..", "###"],
    "I": ["###", ".#.", ".#.", ".#.", "###"], "K": ["#.#", "#.#", "##.", "#.#", "#.#"],
    "L": ["#..", "#..", "#..", "#..", "###"], "M": ["#.#", "###", "###", "#.#", "#.#"],
    "N": ["##.", "#.#", "#.#", "#.#", "#.#"], "O": ["###", "#.#", "#.#", "#.#", "###"],
    "P": ["##.", "#.#", "##.", "#..", "#.."], "R": ["##.", "#.#", "##.", "#.#", "#.#"],
    "S": ["###", "#..", "###", "..#", "###"], "T": ["###", ".#.", ".#.", ".#.", ".#."],
    "U": ["#.#", "#.#", "#.#", "#.#", "###"], "Y": ["#.#", "#.#", ".#.", ".#.", ".#."],
    "Z": ["###", "..#", ".#.", "#..", "###"],
}
HARFLER = sorted(SEKILLER)
BIT = {h: [c == "#" for satir in s for c in satir] for h, s in SEKILLER.items()}

# İkili harf modelini eğitmek için özgün küçük sözlük (yalnızca yukarıdaki harfler)
EGITIM = """KITAP KALEM OKUL MASA ARABA ELMA LIMON BALIK ORMAN TARIM YAZAR SEPET PARA KAPI DENIZ
YILDIZ BULUT TOPRAK RESIM SABUN KUMAS DOSYA KAYIK ODUN KAZAN LAMBA MASAL SOKAK PAZAR BAKIR
TUZ BORU DAMLA SELAM OYUN KORNA TABAK ANLAM NEDEN YASAK BARIS TAKIM DERS SINAV ZAMAN AYNA
KALP YUMUK TOPUZ DAMAR KIRAZ PAMUK UZAK YAKIN ONLAR BUNLAR KULAK SARAY KALE SAKAL""".split()
TEST = ["KAPAK", "BALON", "TABLO", "KARPUZ", "LOKMA", "SIMIT", "OYNAK", "BIDON", "DUMAN", "SAMAN"]


def ikili_model(sozluk=EGITIM, alfa: float = 0.1):
    """Başlangıç ve geçiş olasılıkları (Laplace yumuşatmalı)."""
    bas = Counter(k[0] for k in sozluk)
    gec = Counter((a, b) for k in sozluk for a, b in zip(k, k[1:]))
    baslangic = {h: (bas[h] + alfa) / (len(sozluk) + alfa * len(HARFLER)) for h in HARFLER}
    gecis = {}
    for a in HARFLER:
        toplam = sum(gec[(a, b)] for b in HARFLER)
        gecis[a] = {b: (gec[(a, b)] + alfa) / (toplam + alfa * len(HARFLER)) for b in HARFLER}
    return baslangic, gecis


def ciz(kelime: str, p: float, rng: random.Random) -> list[list[bool]]:
    """Her harf için 15 piksellik gürültülü gözlem."""
    return [[b if rng.random() > p else not b for b in BIT[h]] for h in kelime]


def log_olabilirlik(goruntu: list[bool], harf: str, p: float) -> float:
    uyusmayan = sum(a != b for a, b in zip(goruntu, BIT[harf]))
    return uyusmayan * math.log(p) + (15 - uyusmayan) * math.log(1 - p)


def bagimsiz_oku(goruntuler, p: float) -> str:
    return "".join(max(HARFLER, key=lambda h: log_olabilirlik(g, h, p)) for g in goruntuler)


def markov_oku(goruntuler, p: float, model=None) -> str:
    baslangic, gecis = model or ikili_model()
    m = {h: math.log(baslangic[h]) + log_olabilirlik(goruntuler[0], h, p) for h in HARFLER}
    geri = []
    for g in goruntuler[1:]:
        yeni, isaret = {}, {}
        for b in HARFLER:
            en_iyi = max(HARFLER, key=lambda a: m[a] + math.log(gecis[a][b]))
            isaret[b] = en_iyi
            yeni[b] = m[en_iyi] + math.log(gecis[en_iyi][b]) + log_olabilirlik(g, b, p)
        m = yeni
        geri.append(isaret)
    son = max(HARFLER, key=m.get)
    yol = [son]
    for isaret in reversed(geri):
        yol.append(isaret[yol[-1]])
    return "".join(reversed(yol))


def uret(rng: random.Random, markov: bool = True, lam: float = 2.0) -> str:
    """Üretimsel programın harf üretme kısmı: n ~ 3 + Poisson(λ)."""
    n, esik, k = 3, math.exp(-lam), 1.0
    while True:  # Knuth'un Poisson örneklemesi
        k *= rng.random()
        if k < esik:
            break
        n += 1
    if not markov:
        return "".join(rng.choice(HARFLER) for _ in range(n))
    baslangic, gecis = ikili_model()
    h = rng.choices(HARFLER, weights=[baslangic[x] for x in HARFLER])[0]
    kelime = h
    for _ in range(n - 1):
        h = rng.choices(HARFLER, weights=[gecis[h][x] for x in HARFLER])[0]
        kelime += h
    return kelime


def dogruluk(p: float, deneme: int = 20, tohum: int = 0) -> tuple[float, float]:
    rng = random.Random(tohum)
    model = ikili_model()
    dogru_b = dogru_m = toplam = 0
    for _ in range(deneme):
        for k in TEST:
            g = ciz(k, p, rng)
            dogru_b += sum(a == b for a, b in zip(bagimsiz_oku(g, p), k))
            dogru_m += sum(a == b for a, b in zip(markov_oku(g, p, model), k))
            toplam += len(k)
    return dogru_b / toplam, dogru_m / toplam


def goster(kelime: str, goruntuler) -> str:
    satirlar = []
    for r in range(5):
        satirlar.append("   " + "  ".join("".join("#" if g[r * 3 + c] else "." for c in range(3)) for g in goruntuler))
    return "\n".join(satirlar)


def main() -> None:
    rng = random.Random(3)
    print("=== Üretimsel programdan örnekler ===")
    print("  bağımsız harfler:", ", ".join(uret(rng, markov=False) for _ in range(5)))
    print("  ikili harf modeli:", ", ".join(uret(rng, markov=True) for _ in range(5)))
    print("  Markov modeli sözlükteki harf geçişlerini taklit eder (küçük sözlükle eğitildiği için kusurlu).")

    for tohum in (4, 5):
        print(f"\n=== Gözlem: 'KARPUZ', gürültü p = 0.2 (tohum {tohum}) ===")
        g = ciz("KARPUZ", 0.2, random.Random(tohum))
        print(goster("KARPUZ", g))
        print(f"  bağımsız model okur: {bagimsiz_oku(g, 0.2)}")
        print(f"  ikili harf modeli  : {markov_oku(g, 0.2)}")
    print("  İlkinde önsel bilgi hataları düzeltiyor. İkincisinde ise okumayı sözlükte sık görülen harf")
    print("  geçişlerine doğru çekip yeni bir hata yaratıyor: Önsel ortalamada yardım eder, her zaman değil.")

    print("\n=== Harf doğruluğu (eğitim sözlüğünde olmayan 10 kelime, 20 deneme) ===")
    print("   p      bağımsız   ikili harf")
    for p in (0.05, 0.15, 0.25, 0.35):
        b, m = dogruluk(p)
        print(f"  {p:<5}   {b:6.1%}     {m:6.1%}")
    print("  Az gürültüde ikisi de iyi. Gürültü arttıkça harf dizisi hakkındaki önsel bilgi fark yaratır.")


if __name__ == "__main__":
    main()
