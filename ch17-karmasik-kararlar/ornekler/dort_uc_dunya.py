#!/usr/bin/env python3
"""4 × 3 dünya: sıralı karar problemi (kitaptaki 17.1).

Kitaptaki değerler (testlerle doğrulanır):
  * [Yukarı, Yukarı, Sağ, Sağ, Sağ] dizisi hedefe 0.8^5 = 0.32768 olasılıkla, öbür yoldan
    0.1^4 × 0.8 olasılıkla ulaşır: toplam 0.32776.
  * 10 adımda +1'e varan geçmişin faydası 9 × (−0.04) + 1 = 0.64.
  * Şekil 17.3 (γ = 1, r = −0.04):
        0.8516 0.9078 0.9578   +1
        0.8016  ////  0.7003   −1
        0.7453 0.6953 0.6514 0.4279
  * En iyi politikanın değiştiği r değerleri: −1.6497, −0.7311, −0.4526, −0.0850, −0.0273; r < 0 için
    toplam 9 farklı en iyi politika.
  * İndirim çarpanı γ, (1/γ) − 1 faiz oranına denktir: γ = 0.9 → %11.1.
  * Şekillendirme teoremi: R′ = R + γΦ(s′) − Φ(s) en iyi politikayı değiştirmez.

Çalıştırma:
    python dort_uc_dunya.py
"""
from __future__ import annotations

import random

import numpy as np

import mdp

BASLANGIC = (1, 1)


def dizi_basari_olasiligi(m: mdp.MDP, eylemler: list[str], hedef=(4, 3)) -> float:
    """Sabit eylem dizisi uygulanınca dizinin sonunda hedefte olma olasılığı (uç durumlar emici)."""
    dagilim = {BASLANGIC: 1.0}
    for a in eylemler:
        yeni = {}
        for s, p in dagilim.items():
            sonraki = [(1.0, s)] if s in m.uclar else m.gecis[(s, a)]
            for q, s2 in sonraki:
                yeni[s2] = yeni.get(s2, 0.0) + p * q
        dagilim = yeni
    return dagilim.get(hedef, 0.0)


def en_iyi_eylemler(m: mdp.MDP, U: dict, tol: float = 1e-7) -> dict:
    """Her durumdaki bütün en iyi eylemler (eşitlikler dahil)."""
    sonuc = {}
    for s in m.durumlar:
        if m.eylemler[s]:
            q = {a: m.q(s, a, U) for a in m.eylemler[s]}
            en = max(q.values())
            sonuc[s] = tuple(a for a in m.eylemler[s] if q[a] > en - tol)
    return sonuc


def en_iyi_politika(r: float) -> dict:
    """r < 0 için politika yinelemesi, uygun (proper) bir politikadan başlayarak (γ = 1)."""
    m = mdp.dort_uc(r=r)
    baslangic = {s: ("Sağ" if s[1] == 3 else "Yukarı") for s in m.durumlar if m.eylemler[s]}
    baslangic[(4, 1)] = "Sol"
    _, U, _ = mdp.politika_yineleme(m, baslangic)
    return en_iyi_eylemler(m, U)


def kirilma_noktalari(alt: float = -2.0, ust: float = -0.002, adim: float = 0.004, tol: float = 1e-5) -> list:
    """En iyi politikanın değiştiği r değerlerini (ikili aramayla) bul."""
    noktalar = []
    r = alt
    onceki = en_iyi_politika(r)
    while r < ust:
        r2 = min(r + adim, ust)
        simdiki = en_iyi_politika(r2)
        if simdiki != onceki:
            a, b = r, r2
            while b - a > tol:
                orta = (a + b) / 2
                a, b = (orta, b) if en_iyi_politika(orta) == onceki else (a, orta)
            noktalar.append((round((a + b) / 2, 4), simdiki))
        onceki, r = simdiki, r2
    return noktalar


def sonlu_ufuk(m: mdp.MDP, N: int) -> list[dict]:
    """Sonlu ufuk: U_0 = 0, U_k = B U_{k−1}. Kalan k adım için en iyi eylemler (durağan olmayan politika)."""
    U, politikalar = {s: 0.0 for s in m.durumlar}, []
    for _ in range(N):
        politikalar.append(m.acgozlu(U))     # k adım kalmışken (k − 1 adımlık faydalarla)
        U = m.bellman(U)
    return politikalar


def sekillendir(m: mdp.MDP, Phi: dict) -> mdp.MDP:
    """R′(s, a, s′) = R(s, a, s′) + γ Φ(s′) − Φ(s)   (17.9)."""
    eski = m.odul
    return mdp.MDP(m.durumlar, m.eylemler, m.gecis,
                   lambda s, a, s2: eski(s, a, s2) + m.gama * Phi[s2] - Phi[s], m.gama, m.uclar)


def main() -> None:
    m = mdp.dort_uc()
    print("=== Sabit eylem dizisi ===")
    p = dizi_basari_olasiligi(m, ["Yukarı", "Yukarı", "Sağ", "Sağ", "Sağ"])
    print(f"  [Yukarı, Yukarı, Sağ, Sağ, Sağ] hedefe ulaşma olasılığı: {p:.5f}  (0.8^5 = {0.8 ** 5:.5f})")
    print(f"  10 adımda +1'e varmanın faydası: 9 × (−0.04) + 1 = {9 * -0.04 + 1:.2f}")

    print("\n=== Durum faydaları, γ = 1, r = −0.04 (kitaptaki Şekil 17.3) ===")
    U, _ = mdp.deger_yineleme(m, eps=1e-10)
    print(mdp.ciz(U))
    print("\n  Bellman denklemi (1, 1)'de:")
    for a in m.eylemler[(1, 1)]:
        print(f"    Q((1,1), {a:<6}) = {m.q((1, 1), a, U):.4f}")
    print("  (3, 1)'de Sol mu, Yukarı mı?")
    for a in ("Sol", "Yukarı"):
        print(f"    Q((3,1), {a:<6}) = {m.q((3, 1), a, U):.4f}")
    print("  Kitap (3,1)'de iki eylemin eşit olduğunu söyler; bu yalnızca r ≈ −0.0448'de doğrudur.")

    print("\n=== r değişince en iyi politika (Şekil 17.2) ===")
    for r in (-2.0, -0.6, -0.04, -0.01):
        U_r, _ = mdp.deger_yineleme(mdp.dort_uc(r=r), eps=1e-10)
        print(f"  r = {r}:")
        print(mdp.ciz(pi=mdp.dort_uc(r=r).acgozlu(U_r), girinti="      "))
    noktalar = kirilma_noktalari()
    print(f"  Politikanın değiştiği r değerleri: {[n for n, _ in noktalar]}")
    print(f"  r < 0 için farklı en iyi politika sayısı: {len(noktalar) + 1}")

    print("\n=== Sonlu ufuk: durağan olmayan politika ===")
    pol = sonlu_ufuk(m, 100)
    for kalan in (1, 2, 3, 4, 5, 10, 100):
        print(f"  {kalan:>3} adım kaldı: (3,1)'de {pol[kalan - 1][(3, 1)]}")
    print("  Az zaman kalınca risk alıp Yukarı gider; zaman bolken güvenli yol Sol.")

    print("\n=== İndirim çarpanı ve faiz ===")
    for g in (0.9, 0.95, 0.99):
        print(f"  γ = {g}: faiz oranı (1/γ) − 1 = %{(1 / g - 1) * 100:.1f}")

    print("\n=== Şekillendirme teoremi ===")
    rng = random.Random(17)
    Phi = {s: (0.0 if s in m.uclar else rng.uniform(-5, 5)) for s in m.durumlar}
    m2 = sekillendir(m, Phi)
    U2, _ = mdp.deger_yineleme(m2, eps=1e-10)
    print(f"  Rastgele Φ ile politika aynı mı? {en_iyi_eylemler(m2, U2) == en_iyi_eylemler(m, U)}")
    print(f"  U′(s) = U(s) − Φ(s)? {max(abs(U2[s] - (U[s] - Phi[s])) for s in m.durumlar) < 1e-6}")
    m3 = sekillendir(m, U)
    acgozlu = {s: max(m.eylemler[s], key=lambda a: sum(p * m3.odul(s, a, s2) for p, s2 in m.gecis[(s, a)]))
               for s in m.durumlar if m.eylemler[s]}
    print(f"  Φ = U ile anlık ödüle göre açgözlü politika en iyi mi? {acgozlu == m.acgozlu(U)}")


if __name__ == "__main__":
    main()
