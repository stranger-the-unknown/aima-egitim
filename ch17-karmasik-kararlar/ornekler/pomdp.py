#!/usr/bin/env python3
"""Kısmen gözlemlenebilir MDP'ler (kitaptaki 17.4–17.5).

İki durumlu dünya (kitap): durumlar A ve B. Kal (Stay) 0.9 olasılıkla yerinde kalır, Git (Go)
0.9 olasılıkla diğer duruma geçer. B'ye giren her geçişin ödülü 1, A'ya girenin 0. Algılayıcı
doğru durumu 0.6 olasılıkla söyler. γ = 1.

* İnanç güncellemesi: b′(s′) = α P(e | s′) Σ_s P(s′ | s, a) b(s)       (17.16)
* Koşullu plan p'nin fayda vektörü:
      α_p(s) = Σ_s′ P(s′ | s, a) [R(s, a, s′) + γ Σ_e P(e | s′) α_{p.e}(s′)]     (17.18)
* U(b) = max_p b · α_p: parçalı doğrusal ve dışbükey.
Kitaptaki değerler: α[Kal] = (0.1, 0.9), α[Git] = (0.9, 0.1); 1 adımlık en iyi politika
b(B) > 0.5 ise Kal. Derinlik 2'de 8 plan, 4'ü baskın değil; derinlik 8'de 144 baskın olmayan plan.

Çalıştırma:
    python pomdp.py
"""
from __future__ import annotations

import itertools

import numpy as np

DURUMLAR = ("A", "B")
EYLEMLER = ("Kal", "Git")
GOZLEMLER = ("A", "B")
DOGRULUK = 0.6          # algılayıcının doğru durumu söyleme olasılığı


def gecis(s: str, a: str) -> dict:
    diger = "B" if s == "A" else "A"
    return {s: 0.9, diger: 0.1} if a == "Kal" else {diger: 0.9, s: 0.1}


def odul(s: str, a: str, s2: str) -> float:
    return 1.0 if s2 == "B" else 0.0


def algilayici(e: str, s: str) -> float:
    return DOGRULUK if e == s else 1 - DOGRULUK


def inanc_guncelle(b: dict, a: str, e: str) -> dict:
    """b′ = α FORWARD(b, a, e)."""
    ham = {s2: algilayici(e, s2) * sum(gecis(s, a).get(s2, 0.0) * b[s] for s in DURUMLAR) for s2 in DURUMLAR}
    z = sum(ham.values())
    return {s: v / z for s, v in ham.items()}


def gozlem_olasiligi(b: dict, a: str, e: str) -> float:
    """P(e | a, b) = Σ_s′ P(e | s′) Σ_s P(s′ | s, a) b(s)."""
    return sum(algilayici(e, s2) * sum(gecis(s, a).get(s2, 0.0) * b[s] for s in DURUMLAR) for s2 in DURUMLAR)


# --- Koşullu planlarla değer yinelemesi -------------------------------------------
class Plan:
    """Bir eylem ve her gözlem için bir alt plan; alfa = (α(A), α(B))."""

    def __init__(self, eylem: str | None, alt: dict | None, alfa: np.ndarray):
        self.eylem, self.alt, self.alfa = eylem, alt, alfa

    def __repr__(self) -> str:
        if self.eylem is None:
            return "[]"
        if all(p.eylem is None for p in self.alt.values()):
            return f"[{self.eylem}]"
        return f"[{self.eylem}; " + ", ".join(f"{e}→{p!r}" for e, p in self.alt.items()) + "]"


def alfa_hesapla(eylem: str, alt: dict, gama: float = 1.0) -> np.ndarray:
    alfa = []
    for s in DURUMLAR:
        toplam = 0.0
        for s2, p in gecis(s, eylem).items():
            devam = sum(algilayici(e, s2) * alt[e].alfa[DURUMLAR.index(s2)] for e in GOZLEMLER)
            toplam += p * (odul(s, eylem, s2) + gama * devam)
        alfa.append(toplam)
    return np.array(alfa)


def baskin_olmayanlar(planlar: list[Plan], eps: float = 1e-9) -> list[Plan]:
    """1 boyutlu inanç uzayında (x = b(B) ∈ [0, 1]) üst zarfı oluşturan planlar.
    Her plan bir doğru: değer(x) = α(A) + x (α(B) − α(A)). [0, 1] içinde pozitif uzunlukta bir
    aralıkta en iyi olan planlar tutulur (kitaptaki REMOVE-DOMINATED-PLANS; genelde LP ile yapılır)."""
    egim = lambda p: p.alfa[1] - p.alfa[0]
    # Eğime göre sırala; aynı eğimdekilerden yalnızca en yükseği kalır.
    tekil = []
    for p in sorted(planlar, key=egim):
        if tekil and abs(egim(tekil[-1]) - egim(p)) < eps:
            if p.alfa[0] > tekil[-1].alfa[0]:
                tekil[-1] = p
        else:
            tekil.append(p)

    def kesisim(p, q):  # p'nin eğimi q'nunkinden küçük
        return (p.alfa[0] - q.alfa[0]) / (egim(q) - egim(p))

    zarf = []
    for p in tekil:
        while len(zarf) >= 2 and kesisim(zarf[-2], p) <= kesisim(zarf[-2], zarf[-1]) + 1e-12:
            zarf.pop()
        zarf.append(p)
    sonuc = []
    for i, p in enumerate(zarf):
        bas = -np.inf if i == 0 else kesisim(zarf[i - 1], p)
        son = np.inf if i == len(zarf) - 1 else kesisim(p, zarf[i + 1])
        if min(son, 1.0) - max(bas, 0.0) > eps:
            sonuc.append(p)
    return sonuc


def deger_yineleme(derinlik: int, gama: float = 1.0) -> list[list[Plan]]:
    """POMDP-VALUE-ITERATION'ın sabit derinlikli hâli: her derinlik için baskın olmayan planlar."""
    bos = Plan(None, None, np.zeros(2))
    katmanlar, U = [], [bos]
    for _ in range(derinlik):
        yeni = [Plan(a, dict(zip(GOZLEMLER, secim)), alfa_hesapla(a, dict(zip(GOZLEMLER, secim)), gama))
                for a in EYLEMLER for secim in itertools.product(U, repeat=len(GOZLEMLER))]
        U = baskin_olmayanlar(yeni)
        katmanlar.append(U)
    return katmanlar


def fayda(planlar: list[Plan], bB: float) -> tuple[float, Plan]:
    b = np.array([1 - bB, bB])
    p = max(planlar, key=lambda p: float(b @ p.alfa))
    return float(b @ p.alfa), p


def main() -> None:
    print("=== İnanç güncellemesi ===")
    b = {"A": 0.5, "B": 0.5}
    for a, e in (("Kal", "B"), ("Kal", "B"), ("Git", "A")):
        print(f"  {a}, gözlem {e}: P(e) = {gozlem_olasiligi(b, a, e):.3f}", end="")
        b = inanc_guncelle(b, a, e)
        print(f"  → b(B) = {b['B']:.4f}")

    print("\n=== Bir adımlık planlar (kitap) ===")
    katmanlar = deger_yineleme(8)
    for p in katmanlar[0]:
        print(f"  {p!r:<8} α = ({p.alfa[0]:.1f}, {p.alfa[1]:.1f})")

    print("\n=== Derinlik arttıkça baskın olmayan planlar ===")
    for d, U in enumerate(katmanlar, 1):
        tum = len(EYLEMLER) * (len(katmanlar[d - 2]) if d > 1 else 1) ** len(GOZLEMLER)
        print(f"  derinlik {d}: üretilen {tum:>6}, baskın olmayan {len(U):>4}")
    print("  (Budamasız plan sayısı |A|^O(|E|^(d−1)): derinlik 8'de 2^255.)")
    print("  Derinlik 2'nin baskın olmayan planları:")
    for p in katmanlar[1]:
        print(f"    {p!r}  α = ({p.alfa[0]:.3f}, {p.alfa[1]:.3f})")

    print("\n=== Derinlik 8 fayda fonksiyonu ve politika ===")
    for bB in (0.0, 0.2, 0.4, 0.5, 0.6, 0.8, 1.0):
        u, p = fayda(katmanlar[-1], bB)
        print(f"  b(B) = {bB:.1f}: U = {u:.3f}, ilk eylem {p.eylem}")
    print("  Ara inançlarda fayda düşük: ajan iyi eylemi seçecek bilgiye sahip değil (bilginin değeri).")


if __name__ == "__main__":
    main()
