#!/usr/bin/env python3
"""Markov karar süreçleri için küçük, okunaklı bir kütüphane (kitaptaki 17.1–17.2).

Kitabın 4. baskısındaki gösterim: ödül geçişe aittir, R(s, a, s′).
    Q(s, a) = Σ_s′ P(s′ | s, a) [R(s, a, s′) + γ U(s′)]          (Q-VALUE)
    U(s)    = max_a Q(s, a)                                       (Bellman denklemi, 17.5)

Uç durumlar emicidir: Eylem yoktur, faydaları 0'dır. Uç duruma girişin ödülü (4 × 3 dünyada +1 / −1)
geçişin ödülüdür; bu yüzden bir uç durumun ödülü yalnızca bir kez sayılır.

4 × 3 dünya (kitaptaki Şekil 17.1): koordinatlar (sütun, satır), (1, 1) sol alt köşe, (2, 2) duvar,
(4, 3) = +1, (4, 2) = −1. Eylem 0.8 olasılıkla istenen yöne, 0.1'er olasılıkla dik yönlere gider;
duvara çarpan yerinde kalır. Uç olmayan durumlar arasındaki her geçişin ödülü r (kitapta −0.04).

Çalıştırma:
    python mdp.py
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

YONLER = {"Yukarı": (0, 1), "Aşağı": (0, -1), "Sol": (-1, 0), "Sağ": (1, 0)}
DIK = {"Yukarı": ("Sol", "Sağ"), "Aşağı": ("Sol", "Sağ"), "Sol": ("Yukarı", "Aşağı"), "Sağ": ("Yukarı", "Aşağı")}
OK = {"Yukarı": "↑", "Aşağı": "↓", "Sol": "←", "Sağ": "→"}


@dataclass
class MDP:
    durumlar: list
    eylemler: dict                    # durum → eylem listesi (uç durumda boş)
    gecis: dict                       # (s, a) → [(olasılık, s′), ...]
    odul: callable                    # odul(s, a, s′)
    gama: float = 1.0
    uclar: set = field(default_factory=set)

    def q(self, s, a, U) -> float:
        return sum(p * (self.odul(s, a, s2) + self.gama * U[s2]) for p, s2 in self.gecis[(s, a)])

    def bellman(self, U) -> dict:
        """Bellman güncellemesi B: bütün durumlar aynı anda."""
        return {s: max((self.q(s, a, U) for a in self.eylemler[s]), default=0.0) for s in self.durumlar}

    def acgozlu(self, U) -> dict:
        """π(s) = argmax_a Q(s, a)  (17.4). Eşitlikte eylem listesindeki ilk eylem."""
        return {s: max(self.eylemler[s], key=lambda a: self.q(s, a, U))
                for s in self.durumlar if self.eylemler[s]}


# --- Algoritmalar ----------------------------------------------------------------
def deger_yineleme(mdp: MDP, eps: float = 1e-6, en_cok: int = 100_000):
    """Kitaptaki VALUE-ITERATION (Şekil 17.6). (U, yineleme sayısı) döndürür.
    γ < 1 iken durma koşulu δ ≤ ε(1 − γ)/γ (17.12); γ = 1 iken (uygun politikalarla) δ ≤ ε."""
    U = {s: 0.0 for s in mdp.durumlar}
    esik = eps * (1 - mdp.gama) / mdp.gama if mdp.gama < 1 else eps
    for i in range(1, en_cok + 1):
        U2 = mdp.bellman(U)
        delta = max(abs(U2[s] - U[s]) for s in mdp.durumlar)
        U = U2
        if delta <= esik:
            return U, i
    return U, en_cok


def politika_degerlendir(mdp: MDP, pi: dict) -> dict:
    """Doğrusal denklemleri tam çöz: U = R_π + γ P_π U  (17.14), O(n³)."""
    indeks = {s: i for i, s in enumerate(mdp.durumlar)}
    n = len(mdp.durumlar)
    A, b = np.eye(n), np.zeros(n)
    for s in mdp.durumlar:
        if s not in pi:
            continue            # uç durum: U = 0
        i = indeks[s]
        for p, s2 in mdp.gecis[(s, pi[s])]:
            b[i] += p * mdp.odul(s, pi[s], s2)
            A[i, indeks[s2]] -= mdp.gama * p
    x = np.linalg.solve(A, b)
    return {s: float(x[indeks[s]]) for s in mdp.durumlar}


def politika_degerlendir_yaklasik(mdp: MDP, pi: dict, U: dict, k: int) -> dict:
    """Değiştirilmiş politika yinelemesi için: sabit politikayla k basit Bellman güncellemesi."""
    for _ in range(k):
        U = {s: (mdp.q(s, pi[s], U) if s in pi else 0.0) for s in mdp.durumlar}
    return U


def politika_yineleme(mdp: MDP, pi: dict | None = None, k: int | None = None):
    """Kitaptaki POLICY-ITERATION (Şekil 17.9). k verilirse değiştirilmiş politika yinelemesi.
    (π, U, yineleme sayısı) döndürür."""
    pi = dict(pi) if pi else {s: mdp.eylemler[s][0] for s in mdp.durumlar if mdp.eylemler[s]}
    U = {s: 0.0 for s in mdp.durumlar}
    for i in range(1, 10_000):
        U = politika_degerlendir(mdp, pi) if k is None else politika_degerlendir_yaklasik(mdp, pi, U, k)
        degisti = False
        for s in pi:
            en_iyi = max(mdp.eylemler[s], key=lambda a: mdp.q(s, a, U))
            if mdp.q(s, en_iyi, U) > mdp.q(s, pi[s], U) + 1e-12:
                pi[s], degisti = en_iyi, True
        if not degisti:
            return pi, U, i
    raise RuntimeError("politika yinelemesi yakınsamadı")


def en_cok_hata(U: dict, V: dict) -> float:
    return max(abs(U[s] - V[s]) for s in U)


# --- 4 × 3 dünya --------------------------------------------------------------------
DUVARLAR = {(2, 2)}
UC_ODUL = {(4, 3): +1.0, (4, 2): -1.0}


def hareket(s, yon, genislik=4, yukseklik=3, duvarlar=DUVARLAR):
    dx, dy = YONLER[yon]
    x, y = s[0] + dx, s[1] + dy
    if not (1 <= x <= genislik and 1 <= y <= yukseklik) or (x, y) in duvarlar:
        return s
    return (x, y)


def dort_uc(r: float = -0.04, gama: float = 1.0, olasiliklar=(0.8, 0.1, 0.1)) -> MDP:
    durumlar = [(x, y) for y in (1, 2, 3) for x in (1, 2, 3, 4) if (x, y) not in DUVARLAR]
    eylemler, gecis = {}, {}
    for s in durumlar:
        eylemler[s] = [] if s in UC_ODUL else list(YONLER)
        for a in eylemler[s]:
            dagilim = {}
            for p, yon in zip(olasiliklar, (a, *DIK[a])):
                s2 = hareket(s, yon)
                dagilim[s2] = dagilim.get(s2, 0.0) + p
            gecis[(s, a)] = [(p, s2) for s2, p in dagilim.items()]

    def odul(s, a, s2):
        return UC_ODUL.get(s2, r)

    return MDP(durumlar, eylemler, gecis, odul, gama, set(UC_ODUL))


def ciz(U: dict | None = None, pi: dict | None = None, girinti: str = "  ") -> str:
    satirlar = []
    for y in (3, 2, 1):
        hucre = []
        for x in (1, 2, 3, 4):
            s = (x, y)
            if s in DUVARLAR:
                hucre.append(" ████ " if U else "█")
            elif s in UC_ODUL:
                hucre.append(f"{UC_ODUL[s]:+5.0f} " if U else ("+" if UC_ODUL[s] > 0 else "−"))
            elif U is not None:
                hucre.append(f"{U[s]:6.4f}")
            else:
                hucre.append(OK[pi[s]])
        satirlar.append(girinti + " ".join(hucre))
    return "\n".join(satirlar)


def main() -> None:
    mdp = dort_uc()
    U, i = deger_yineleme(mdp, eps=1e-9)
    print(f"4 × 3 dünya, r = −0.04, γ = 1: değer yinelemesi {i} adımda yakınsadı.")
    print(ciz(U))
    print("\nEn iyi politika:")
    print(ciz(pi=mdp.acgozlu(U)))


if __name__ == "__main__":
    main()
