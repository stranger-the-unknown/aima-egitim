#!/usr/bin/env python3
"""Dil modelleri (kitaptaki 23.1).

* Sözcük torbası (naif Bayes): P(Sınıf | w₁..w_N) = α P(Sınıf) Π P(wⱼ | Sınıf).
  Kitaptaki sayılar: 3000 metnin 300'ü ekonomi → P(ekonomi) = 0.1; ekonomideki 100 000 sözcükte
  "stocks" 700 kez → P(stocks | ekonomi) = 0.007.
* n-gram modelleri: P(wⱼ | w_{j−n+1:j−1}). Karakter ve sözcük düzeyinde.
* Düzeltme: Laplace (+1), doğrusal ara değerleme, bilinmeyen sözcük için <UNK>.
  Laplace'ın ardıllık kuralı: N gün boyunca güneş doğduysa yarın doğmama olasılığı 1/(N + 2).
* Şaşkınlık (perplexity) = P(w₁:N)^(−1/N): Modelleri karşılaştırmak için.
* Sözcük türü etiketleme: saklı Markov modeli + Viterbi (Bölüm 14).

Çalıştırma:
    python dil_modelleri.py
"""
from __future__ import annotations

import math
from collections import Counter, defaultdict

DERLEM = """ali okula gitti . ayşe okula gitti . ali kitap okudu . ayşe kitap okudu .
ali ayşe ile okula gitti . öğretmen kitap okudu . öğretmen okula gitti .
ayşe ali ile kitap okudu . ali okulda kitap okudu . ayşe okulda ders çalıştı .
öğretmen ders anlattı . ali ders çalıştı .""".split()


# --- Sözcük torbası ----------------------------------------------------------------
def naif_bayes_egit(belgeler: list[tuple[str, list[str]]]):
    sinif = Counter(c for c, _ in belgeler)
    sozcuk = defaultdict(Counter)
    for c, s in belgeler:
        sozcuk[c].update(s)
    sozluk = {w for _, s in belgeler for w in s}
    return sinif, sozcuk, sozluk


def naif_bayes_sinifla(model, sozcukler: list[str]) -> dict:
    sinif, sozcuk, sozluk = model
    N = sum(sinif.values())
    log = {}
    for c in sinif:
        toplam = sum(sozcuk[c].values())
        log[c] = math.log(sinif[c] / N) + sum(math.log((sozcuk[c][w] + 1) / (toplam + len(sozluk) + 1)) for w in sozcukler)
    m = max(log.values())
    z = sum(math.exp(v - m) for v in log.values())
    return {c: math.exp(v - m) / z for c, v in log.items()}


# --- n-gram modelleri -----------------------------------------------------------------
def cumlelere_bol(metin: list[str]) -> list[list[str]]:
    cumleler, simdiki = [], []
    for w in metin:
        simdiki.append(w)
        if w == ".":
            cumleler.append(simdiki)
            simdiki = []
    return cumleler + ([simdiki] if simdiki else [])


class NGram:
    """Her cümle başına n − 1 tane <s> eklenerek eğitilen n-gram modeli."""

    def __init__(self, n: int, metin: list[str], laplace: float = 0.0):
        self.n, self.laplace = n, laplace
        self.sozluk = set(metin) | {"<s>"}
        self.say, self.baglam = Counter(), Counter()
        for cumle in cumlelere_bol(metin):
            dolgu = ["<s>"] * (n - 1) + cumle
            for i in range(len(cumle)):
                self.say[tuple(dolgu[i:i + n])] += 1
                self.baglam[tuple(dolgu[i:i + n - 1])] += 1

    def P(self, w: str, baglam: tuple) -> float:
        baglam = tuple(baglam[-(self.n - 1):]) if self.n > 1 else ()
        pay = self.say[baglam + (w,)] + self.laplace
        payda = self.baglam[baglam] + self.laplace * len(self.sozluk)
        return pay / payda if payda else 0.0

    def log_olasilik(self, metin: list[str]) -> float:
        dolgu = ["<s>"] * (self.n - 1) + metin
        toplam = 0.0
        for i in range(len(metin)):
            p = self.P(dolgu[i + self.n - 1], tuple(dolgu[i:i + self.n - 1]))
            if p == 0:
                return -math.inf
            toplam += math.log(p)
        return toplam


def ara_degerleme(modeller: list[NGram], agirliklar: list[float]):
    def P(w, baglam):
        return sum(l * m.P(w, baglam) for l, m in zip(agirliklar, modeller))
    return P


def sasikinlik(P, metin: list[str], n: int = 3) -> float:
    dolgu = ["<s>"] * (n - 1) + metin
    log = sum(math.log(P(dolgu[i + n - 1], tuple(dolgu[i:i + n - 1]))) for i in range(len(metin)))
    return math.exp(-log / len(metin))


def ardillik_kurali(N: int) -> float:
    """Laplace: N kez gözlenen olayın bir sonraki denemede olmama olasılığı 1/(N + 2)."""
    return 1 / (N + 2)


# --- Sözcük türü etiketleme: HMM + Viterbi -------------------------------------------------
ETIKETLI = [
    [("ali", "AD"), ("okula", "AD"), ("gitti", "FİİL")],
    [("ayşe", "AD"), ("kitap", "AD"), ("okudu", "FİİL")],
    [("öğretmen", "AD"), ("hızlı", "SIFAT"), ("okudu", "FİİL")],
    [("büyük", "SIFAT"), ("okul", "AD"), ("güzel", "SIFAT")],
    [("ali", "AD"), ("güzel", "SIFAT"), ("kitap", "AD"), ("okudu", "FİİL")],
    [("ayşe", "AD"), ("büyük", "SIFAT"), ("okula", "AD"), ("gitti", "FİİL")],
]


def hmm_egit(cumleler):
    gecis, yayilim, ilk = defaultdict(Counter), defaultdict(Counter), Counter()
    for c in cumleler:
        ilk[c[0][1]] += 1
        for (w, t), (_, t2) in zip(c, c[1:]):
            gecis[t][t2] += 1
        for w, t in c:
            yayilim[t][w] += 1
    etiketler = sorted(yayilim)
    return ilk, gecis, yayilim, etiketler


def viterbi(model, sozcukler: list[str]) -> list[str]:
    ilk, gecis, yayilim, etiketler = model

    def p_y(t, w):
        return (yayilim[t][w] + 0.1) / (sum(yayilim[t].values()) + 0.1 * 50)

    def p_g(t, t2):
        return (gecis[t][t2] + 0.1) / (sum(gecis[t].values()) + 0.1 * len(etiketler))

    m = {t: math.log((ilk[t] + 0.1) / (sum(ilk.values()) + 0.1 * len(etiketler))) + math.log(p_y(t, sozcukler[0])) for t in etiketler}
    geri = []
    for w in sozcukler[1:]:
        yeni, g = {}, {}
        for t2 in etiketler:
            en = max(etiketler, key=lambda t: m[t] + math.log(p_g(t, t2)))
            yeni[t2] = m[en] + math.log(p_g(en, t2)) + math.log(p_y(t2, w))
            g[t2] = en
        m = yeni
        geri.append(g)
    son = max(m, key=m.get)
    yol = [son]
    for g in reversed(geri):
        yol.append(g[yol[-1]])
    return list(reversed(yol))


def main() -> None:
    print("=== Sözcük torbası: kitaptaki sayılar ===")
    print(f"  P(ekonomi) ≈ 300/3000 = {300 / 3000};  P(stocks | ekonomi) ≈ 700/100000 = {700 / 100_000}")
    belgeler = [("ekonomi", "borsa yükseldi faiz düştü".split()), ("ekonomi", "dolar yükseldi borsa düştü".split()),
                ("hava", "yağmur yağdı rüzgar esti".split()), ("hava", "kar yağdı soğuk rüzgar".split())]
    model = naif_bayes_egit(belgeler)
    for cumle in ("borsa bugün yükseldi", "yarın kar yağacak", "rüzgar borsa"):
        p = naif_bayes_sinifla(model, cumle.split())
        print(f"  '{cumle}': " + ", ".join(f"{c} {v:.2f}" for c, v in p.items()))

    print("\n=== n-gram modelleri (küçük Türkçe derlem) ===")
    test = "ayşe okula gitti .".split()
    for n in (1, 2, 3):
        m = NGram(n, DERLEM)
        print(f"  {n}-gram: log P('{' '.join(test)}') = {m.log_olasilik(test):.3f}")
    gorulmemis = "öğretmen ders okudu .".split()
    print(f"  Görülmemiş üçlü içeren '{' '.join(gorulmemis)}': düzeltmesiz 3-gram {NGram(3, DERLEM).log_olasilik(gorulmemis)}, "
          f"Laplace {NGram(3, DERLEM, 1).log_olasilik(gorulmemis):.3f}")
    P = ara_degerleme([NGram(3, DERLEM), NGram(2, DERLEM), NGram(1, DERLEM, 1)], [0.6, 0.3, 0.1])
    print(f"  Ara değerleme (0.6, 0.3, 0.1) şaşkınlık: bilinen cümle {sasikinlik(P, test):.2f}, yeni cümle {sasikinlik(P, gorulmemis):.2f}")
    print(f"  Ardıllık kuralı: 2 milyon gün güneş doğduysa yarın doğmama olasılığı ≈ {ardillik_kurali(2_000_000):.1e}")

    print("\n=== Sözcük türü etiketleme (HMM + Viterbi) ===")
    hmm = hmm_egit(ETIKETLI)
    for cumle in ("ayşe güzel kitap okudu", "öğretmen büyük okula gitti", "ali hızlı okudu"):
        s = cumle.split()
        print(f"  {cumle}: {list(zip(s, viterbi(hmm, s)))}")


if __name__ == "__main__":
    main()
