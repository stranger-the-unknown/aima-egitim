#!/usr/bin/env python3
"""Aktif pekiştirmeli öğrenme: keşif, Q-öğrenme ve SARSA (kitaptaki 22.3).

* Açgözlü ADP ajanı: Öğrendiği modele göre en iyi eylemi seçer; çoğu zaman kötü bir politikaya takılır
  (kitapta 8 denemede, politika kaybı 0.235 olan alt-en iyi bir politikaya yakınsıyor).
* Keşifçi ADP: İyimser faydalarla U⁺(s) ← max_a f(Σ P̂(s′|s,a)[R + γU⁺(s′)], N(s, a)),
  f(u, n) = R⁺ eğer n < Nₑ, yoksa u. Kitap: R⁺ = 2, Nₑ = 5.
* Q-öğrenme (modelsiz, politika dışı): Q(s,a) ← Q(s,a) + α[R + γ max_a′ Q(s′,a′) − Q(s,a)]   (22.7)
* SARSA (politikaya bağlı): Q(s,a) ← Q(s,a) + α[R + γ Q(s′,a′) − Q(s,a)], a′ gerçekten seçilen eylem (22.8).
* GLIE: Her eylemi sonsuz kez dene ama zamanla açgözlüleş (ör. ε = 1/√t).

Çalıştırma:
    python aktif_ogrenme.py
"""
from __future__ import annotations

import math
import random
from collections import defaultdict

import pasif_ogrenme as po

mdp = po.mdp
DUNYA = po.DUNYA
GERCEK_U = po.GERCEK_U
EYLEMLER = list(mdp.YONLER)


def adim_at(s, a, rng: random.Random, dunya=DUNYA):
    sonuclar = dunya.gecis[(s, a)]
    s2 = rng.choices([x for _, x in sonuclar], weights=[p for p, _ in sonuclar])[0]
    return dunya.odul(s, a, s2), s2


def politika_kaybi(politika: dict, dunya=DUNYA) -> float:
    """U*(1,1) − U^π(1,1). Uç duruma hiç varmayan (uygun olmayan) politikada kayıp sonsuz."""
    try:
        U = mdp.politika_degerlendir(dunya, politika)
    except Exception:
        return math.inf
    if any(abs(v) > 1e6 for v in U.values()):
        return math.inf
    return GERCEK_U[(1, 1)] - U[(1, 1)]


class ADPAjani:
    def __init__(self, R_arti: float = 2.0, N_e: int = 5, kesif: bool = True, gama: float = 1.0):
        self.N = defaultdict(int)
        self.N_s2 = defaultdict(lambda: defaultdict(int))
        self.odul = {}
        self.R_arti, self.N_e, self.kesif, self.gama = R_arti, N_e, kesif, gama
        self.U = defaultdict(float)

    def f(self, u: float, n: int) -> float:
        return self.R_arti if self.kesif and n < self.N_e else u

    def q(self, s, a) -> float:
        n = self.N[(s, a)]
        if n == 0:
            return 0.0
        return sum(k / n * (self.odul[(s, a, s2)] + self.gama * self.U[s2]) for s2, k in self.N_s2[(s, a)].items())

    def planla(self, yineleme: int = 30):
        for _ in range(yineleme):
            for s in DUNYA.durumlar:
                if s not in DUNYA.uclar:
                    self.U[s] = max(self.f(self.q(s, a), self.N[(s, a)]) for a in EYLEMLER)

    def eylem(self, s):
        return max(EYLEMLER, key=lambda a: self.f(self.q(s, a), self.N[(s, a)]))

    def deneme(self, rng: random.Random, en_cok: int = 300):
        s = (1, 1)
        for _ in range(en_cok):
            if s in DUNYA.uclar:
                break
            a = self.eylem(s)
            r, s2 = adim_at(s, a, rng)
            self.N[(s, a)] += 1
            self.N_s2[(s, a)][s2] += 1
            self.odul[(s, a, s2)] = r
            self.planla(3)
            s = s2

    def politika(self) -> dict:
        """Öğrenilen modele göre açgözlü politika (denenmemiş eylemin değeri 0 sayılır)."""
        return {s: max(EYLEMLER, key=lambda a: self.q(s, a)) for s in DUNYA.durumlar if s not in DUNYA.uclar}


class QAjani:
    """kesif: "f" (keşif fonksiyonu, R⁺ ve Nₑ), "glie" (ε = 1/√deneme ile ε-açgözlü), "sabit" (sabit ε)."""

    def __init__(self, sarsa: bool = False, kesif: str = "glie", R_arti: float = 2.0, N_e: int = 5,
                 gama: float = 1.0, epsilon: float = 0.1):
        self.Q, self.N = defaultdict(float), defaultdict(int)
        self.sarsa, self.kesif, self.R_arti, self.N_e, self.gama, self.epsilon = sarsa, kesif, R_arti, N_e, gama, epsilon
        self.t = 0

    def alfa(self, n: int) -> float:
        return 60 / (59 + n)

    def sec(self, s, rng):
        if self.kesif == "f":
            return max(EYLEMLER, key=lambda a: self.R_arti if self.N[(s, a)] < self.N_e else self.Q[(s, a)])
        eps = self.epsilon if self.kesif == "sabit" else 1 / math.sqrt(self.t)
        if rng.random() < eps:
            return rng.choice(EYLEMLER)
        return max(EYLEMLER, key=lambda a: self.Q[(s, a)])

    def deneme(self, rng: random.Random, en_cok: int = 300):
        self.t += 1
        s = (1, 1)
        a = self.sec(s, rng)
        for _ in range(en_cok):
            r, s2 = adim_at(s, a, rng)
            self.N[(s, a)] += 1
            if s2 in DUNYA.uclar:
                hedef, a2 = r, None
            else:
                a2 = self.sec(s2, rng)
                hedef = r + self.gama * (self.Q[(s2, a2)] if self.sarsa else max(self.Q[(s2, b)] for b in EYLEMLER))
            self.Q[(s, a)] += self.alfa(self.N[(s, a)]) * (hedef - self.Q[(s, a)])
            if a2 is None:
                break
            s, a = s2, a2

    def politika(self) -> dict:
        return {s: max(EYLEMLER, key=lambda a: self.Q[(s, a)]) for s in DUNYA.durumlar if s not in DUNYA.uclar}


def egit(ajan, deneme_sayisi: int, tohum: int = 0, kontrol=(10, 50, 200, 500)) -> dict:
    rng = random.Random(tohum)
    kayip = {}
    for i in range(1, deneme_sayisi + 1):
        ajan.deneme(rng)
        if i in kontrol:
            kayip[i] = politika_kaybi(ajan.politika())
    return kayip


AJANLAR = {
    "açgözlü ADP": lambda: ADPAjani(kesif=False),
    "keşifçi ADP (R⁺=2, Nₑ=5)": lambda: ADPAjani(),
    "Q-öğrenme, keşif fonksiyonu Nₑ=5": lambda: QAjani(kesif="f"),
    "Q-öğrenme, GLIE ε = 1/√t": lambda: QAjani(kesif="glie"),
    "SARSA, GLIE ε = 1/√t": lambda: QAjani(sarsa=True, kesif="glie"),
}


def karsilastir(deneme: int = 500, tohumlar=(0, 1, 2)) -> dict:
    import statistics
    sonuc = {}
    for ad, kurucu in AJANLAR.items():
        kayiplar = [egit(kurucu(), deneme, tohum=t) for t in tohumlar]
        sonuc[ad] = {n: statistics.median(k[n] for k in kayiplar) for n in kayiplar[0]}
    return sonuc


def main() -> None:
    print("=== Politika kaybı U*(1,1) − U^π(1,1) (4 × 3 dünya), 3 tohumun ortancası ===")
    for ad, k in karsilastir().items():
        print(f"  {ad:<34} " + ", ".join(f"{n}: {v:.3f}" for n, v in k.items()))
    print("  Açgözlü ADP keşfetmediği için kötü bir politikaya takılır; keşifçi ADP hızla en iyiye yaklaşır.")
    print("  Modelsiz Q-öğrenmede her eylemi yalnızca Nₑ = 5 kez denemek yetmez: Erken ve gürültülü Q tahminleri,")
    print("  bir daha denenmeyen eylemleri haksız yere düşük bırakır. Azalan ε (GLIE) ile yakınsar.")

    ajan = ADPAjani()
    egit(ajan, 200)
    print("\n  Keşifçi ADP'nin 200 denemeden sonraki politikası:")
    print(mdp.ciz(pi=ajan.politika(), girinti="    "))
    print("  Gerçek en iyi politika:")
    print(mdp.ciz(pi=DUNYA.acgozlu(GERCEK_U), girinti="    "))


if __name__ == "__main__":
    main()
