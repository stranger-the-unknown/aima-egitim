#!/usr/bin/env python3
"""Olasılıksal bağlamdan bağımsız dilbilgisi (PCFG) ve CYK ayrıştırma (kitaptaki 23.2–23.3).

E₀ dilbilgisi ve sözlüğü kitaptaki Şekil 23.2 ve 23.3'ten (sözlük kısaltılmış; kitap da "..." ile bırakır).
CYK yalnızca X → sözcük ve X → Y Z biçimli kurallarla çalışır (Chomsky normal biçimi); burada tekli kurallar
(NP → Pronoun gibi) her hücrede kapanışla, üçlü kural (NP → Article Adjs Noun) bir ara simgeyle işlenir.
Karmaşıklık O(n³ m).

Kitaptaki örnek: "the wumpus is dead" → [S [NP [Article the] [Noun wumpus]] [VP [VP [Verb is]] [Adjective dead]]]
Olasılık: 0.90 × (0.25 × 0.40 × 0.15) × (0.05 × 0.40 × 0.10 × 0.05) = 1.35 × 10⁻⁶.

Çalıştırma:
    python ayristirma.py
"""
from __future__ import annotations

from collections import Counter, defaultdict

# (sol, sağ taraf, olasılık)
KURALLAR = [
    ("S", ("NP", "VP"), 0.90), ("S", ("S", "Conj_S"), 0.10), ("Conj_S", ("Conj", "S"), 1.0),
    ("NP", ("Pronoun",), 0.25), ("NP", ("Name",), 0.10), ("NP", ("Noun",), 0.10),
    ("NP", ("Article", "Noun"), 0.25), ("NP", ("Article", "Adjs_Noun"), 0.05), ("Adjs_Noun", ("Adjs", "Noun"), 1.0),
    ("NP", ("Digit", "Digit"), 0.05), ("NP", ("NP", "PP"), 0.10), ("NP", ("NP", "RelClause"), 0.05),
    ("NP", ("NP", "Conj_NP"), 0.05), ("Conj_NP", ("Conj", "NP"), 1.0),
    ("VP", ("Verb",), 0.40), ("VP", ("VP", "NP"), 0.35), ("VP", ("VP", "Adjective"), 0.05),
    ("VP", ("VP", "PP"), 0.10), ("VP", ("VP", "Adverb"), 0.10),
    ("Adjs", ("Adjective",), 0.80), ("Adjs", ("Adjective", "Adjs"), 0.20),
    ("PP", ("Prep", "NP"), 1.00), ("RelClause", ("RelPro", "VP"), 1.00),
]
SOZLUK = {
    "Noun": {"stench": 0.05, "breeze": 0.10, "wumpus": 0.15, "pits": 0.05},
    "Verb": {"is": 0.10, "feel": 0.10, "smells": 0.10, "stinks": 0.05, "go": 0.05},   # "go": bizim eklememiz
    "Adjective": {"right": 0.10, "dead": 0.05, "smelly": 0.02, "breezy": 0.02},
    "Adverb": {"here": 0.05, "ahead": 0.05, "nearby": 0.02},
    "Pronoun": {"me": 0.10, "you": 0.03, "i": 0.10, "it": 0.10},
    "RelPro": {"that": 0.40, "which": 0.15, "who": 0.20, "whom": 0.02},
    "Name": {"ali": 0.01, "bo": 0.01, "boston": 0.01},
    "Article": {"the": 0.40, "a": 0.30, "an": 0.10, "every": 0.05},
    "Prep": {"to": 0.20, "in": 0.10, "on": 0.05, "near": 0.10},
    "Conj": {"and": 0.50, "or": 0.10, "but": 0.20, "yet": 0.02},
    "Digit": {"0": 0.20, "1": 0.20, "2": 0.20, "3": 0.20, "4": 0.20},
}
TEKLI = [(a, sag[0], p) for a, sag, p in KURALLAR if len(sag) == 1]
IKILI = [(a, sag, p) for a, sag, p in KURALLAR if len(sag) == 2]


def _tekli_kapanis(hucre: dict):
    """Hücreye tekli kuralları (X → Y) iyileşme kalmayana kadar uygula."""
    degisti = True
    while degisti:
        degisti = False
        for a, b, p in TEKLI:
            if b in hucre:
                deger = p * hucre[b][0]
                if a not in hucre or deger > hucre[a][0]:
                    hucre[a] = (deger, ("tekli", b))
                    degisti = True


def cyk(sozcukler: list[str]):
    """En olası ayrıştırma (Viterbi CYK): P[(i, j)][X] = (olasılık, geri işaretçi)."""
    n = len(sozcukler)
    P = defaultdict(dict)
    for i, w in enumerate(sozcukler):
        for kat, kelimeler in SOZLUK.items():
            if w in kelimeler:
                P[(i, i + 1)][kat] = (kelimeler[w], ("sözcük", w))
        _tekli_kapanis(P[(i, i + 1)])
    for uzunluk in range(2, n + 1):
        for i in range(0, n - uzunluk + 1):
            j = i + uzunluk
            hucre = P[(i, j)]
            for k in range(i + 1, j):
                sol, sag = P[(i, k)], P[(k, j)]
                for a, (b, c), p in IKILI:
                    if b in sol and c in sag:
                        deger = p * sol[b][0] * sag[c][0]
                        if a not in hucre or deger > hucre[a][0]:
                            hucre[a] = (deger, ("ikili", b, c, k))
            _tekli_kapanis(hucre)
    return P


def agac(P, i: int, j: int, X: str) -> str:
    _, geri = P[(i, j)][X]
    if geri[0] == "sözcük":
        return f"[{X} {geri[1]}]"
    if geri[0] == "tekli":
        return f"[{X} {agac(P, i, j, geri[1])}]"
    _, b, c, k = geri
    ic = f"{agac(P, i, k, b)} {agac(P, k, j, c)}"
    if X in ("Adjs_Noun", "Conj_S", "Conj_NP"):                  # ara simgeleri ağaçta gösterme
        return ic
    return f"[{X} {ic}]"


def ayristir(cumle: str):
    s = cumle.lower().split()
    P = cyk(s)
    if "S" not in P[(0, len(s))]:
        return None, 0.0
    return agac(P, 0, len(s), "S"), P[(0, len(s))]["S"][0]


def ayristirma_sayisi(sozcukler: list[str], X: str = "S") -> int:
    """Kaç farklı ayrıştırma ağacı var? (sayım için aynı CYK, olasılık yerine 1)."""
    n = len(sozcukler)
    say = defaultdict(Counter)
    for i, w in enumerate(sozcukler):
        for kat, kel in SOZLUK.items():
            if w in kel:
                say[(i, i + 1)][kat] += 1
        for _ in range(3):
            for a, b, _p in TEKLI:
                if say[(i, i + 1)][b] and not say[(i, i + 1)][a]:
                    say[(i, i + 1)][a] = say[(i, i + 1)][b]
    for uzunluk in range(2, n + 1):
        for i in range(0, n - uzunluk + 1):
            j = i + uzunluk
            for k in range(i + 1, j):
                for a, (b, c), _p in IKILI:
                    say[(i, j)][a] += say[(i, k)][b] * say[(k, j)][c]
            for a, b, _p in TEKLI:
                say[(i, j)][a] += say[(i, j)][b]
    return say[(0, n)][X]


def agac_bankasindan_pcfg(agaclar: list) -> dict:
    """Ağaç bankasındaki her iç düğümün kuralını say: P(X → α) = sayı(X → α) / sayı(X)."""
    kural, sol = Counter(), Counter()

    def gez(d):
        if isinstance(d, str):
            return
        X, *cocuklar = d
        sag = tuple(c if isinstance(c, str) else c[0] for c in cocuklar)
        kural[(X, sag)] += 1
        sol[X] += 1
        for c in cocuklar:
            gez(c)

    for a in agaclar:
        gez(a)
    return {k: v / sol[k[0]] for k, v in kural.items()}


AGAC_BANKASI = [
    ("S", ("NP", ("Pronoun", "i")), ("VP", ("Verb", "feel"))),
    ("S", ("NP", ("Article", "the"), ("Noun", "wumpus")), ("VP", ("Verb", "stinks"))),
    ("S", ("NP", ("Article", "a"), ("Noun", "breeze")), ("VP", ("VP", ("Verb", "is")), ("Adverb", "here"))),
    ("S", ("NP", ("Name", "ali")), ("VP", ("VP", ("Verb", "smells")), ("NP", ("Article", "the"), ("Noun", "stench")))),
    ("S", ("S", ("NP", ("Pronoun", "it")), ("VP", ("Verb", "stinks"))), ("Conj", "and"), ("S", ("NP", ("Pronoun", "i")), ("VP", ("Verb", "feel")))),
]


def main() -> None:
    print("=== E₀ ile CYK: kitaptaki örnek ===")
    a, p = ayristir("the wumpus is dead")
    print(f"  the wumpus is dead\n    {a}\n    P = {p:.3e}   (elle: 0.9 × 0.015 × 0.0001 = {0.9 * 0.015 * 0.0001:.3e})")

    print("\n=== Başka cümleler ===")
    for c in ("I feel a breeze", "the smelly dead wumpus stinks", "I feel a breeze and it stinks", "Me go I", "I think the wumpus is smelly"):
        a, p = ayristir(c)
        print(f"  {c!r}: {'ayrıştırılamadı' if a is None else f'P = {p:.2e}'}")
    print("  E₀ fazla üretir ('Me go I' dilbilgisine uygun sayılır) ve eksik üretir ('I think ...' reddedilir) (kitap).")

    print("\n=== Belirsizlik: edat öbeği nereye bağlanıyor? ===")
    c = "i feel the wumpus near 1 3"
    s = c.split()
    a, p = ayristir(c)
    print(f"  {c}: {ayristirma_sayisi(s)} farklı ağaç; en olası:\n    {a}")

    print("\n=== Ağaç bankasından PCFG ===")
    pcfg = agac_bankasindan_pcfg(AGAC_BANKASI)
    for (X, sag), p in sorted(pcfg.items()):
        if X in ("S", "NP", "VP"):
            print(f"  {X} → {' '.join(sag):<20} [{p:.2f}]")


if __name__ == "__main__":
    main()
