#!/usr/bin/env python3
"""Politika yinelemesi, değiştirilmiş politika yinelemesi, doğrusal programlama ve
çevrimiçi beklenti-maks araması (kitaptaki 17.2.2–17.2.4).

* Politika değerlendirme: Politika sabitken Bellman denklemleri doğrusaldır (17.14); n bilinmeyenli
  n denklem O(n³)'te tam çözülür.
* Politika iyileştirme: Her durumda tek adım ileri bakan MEU eylemi.
* Değiştirilmiş politika yinelemesi: Tam çözüm yerine k basit Bellman güncellemesi.
* DP'nin LP biçimi: Σ U(s)'yi en küçükle, öyle ki her s, a için U(s) ≥ Σ P(s′|s,a)[R + γU(s′)].
  Gerçek faydalar bu kısıtları sağlar ve her durumda en az bir kısıt eşitlikle sağlanır.
* ε-ufku: H = ⌈log_γ(ε(1 − γ)/R_max)⌉. Kitap: γ = 0.5, ε = 0.1, R_max = 1 → H = 5; γ = 0.9 → H = 44.

Çalıştırma:
    python politika_yineleme.py
"""
from __future__ import annotations

import math
import random

import mdp


def lp_kisitlari_saglanir_mi(m: mdp.MDP, U: dict, tol: float = 1e-6) -> tuple[bool, bool]:
    """(bütün kısıtlar sağlanıyor mu, her durumda bir kısıt eşitlikle mi sağlanıyor)."""
    hepsi, siki = True, True
    for s in m.durumlar:
        if not m.eylemler[s]:
            continue
        q = [m.q(s, a, U) for a in m.eylemler[s]]
        hepsi &= all(U[s] >= x - tol for x in q)
        siki &= any(abs(U[s] - x) < tol for x in q)
    return hepsi, siki


def epsilon_ufku(gama: float, eps: float, rmax: float = 1.0) -> int:
    return math.ceil(math.log(eps * (1 - gama) / rmax) / math.log(gama))


def beklenti_maks(m: mdp.MDP, s, derinlik: int, yaprak=lambda s: 0.0) -> tuple[float, str | None]:
    """Derinlik sınırlı beklenti-maks ağacı (Şekil 17.10). Yapraklarda 'yaprak' değerlendirmesi."""
    if not m.eylemler[s]:
        return 0.0, None
    if derinlik == 0:
        return yaprak(s), None
    en, en_a = -math.inf, None
    for a in m.eylemler[s]:
        deger = sum(p * (m.odul(s, a, s2) + m.gama * beklenti_maks(m, s2, derinlik - 1, yaprak)[0])
                    for p, s2 in m.gecis[(s, a)])
        if deger > en:
            en, en_a = deger, a
    return en, en_a


def main() -> None:
    m = mdp.dort_uc()
    rng = random.Random(0)
    print("=== Politika yinelemesi (γ = 1) ===")
    baslangic = {s: "Sağ" if s[1] == 3 else "Yukarı" for s in m.durumlar if m.eylemler[s]}
    baslangic[(4, 1)] = "Sol"
    pi, U, i = mdp.politika_yineleme(m, baslangic)
    print(f"  {i} yinelemede durdu.")
    print(mdp.ciz(pi=pi))
    print(mdp.ciz(U))

    m9 = mdp.dort_uc(gama=0.9)
    print("\n=== γ = 0.9: rastgele başlangıç politikalarından yineleme sayıları ===")
    for _ in range(3):
        pi0 = {s: rng.choice(m9.eylemler[s]) for s in m9.durumlar if m9.eylemler[s]}
        _, _, i_tam = mdp.politika_yineleme(m9, pi0)
        _, _, i_k = mdp.politika_yineleme(m9, pi0, k=3)
        print(f"  tam değerlendirme: {i_tam} yineleme;  değiştirilmiş (k = 3): {i_k} yineleme")
    U9, _ = mdp.deger_yineleme(m9, eps=1e-10)
    pi_k, _, _ = mdp.politika_yineleme(m9, k=3)
    print(f"  Değiştirilmiş PI'nin politikası değer yinelemesininkiyle aynı mı? {pi_k == m9.acgozlu(U9)}")

    print("\n=== Doğrusal programlama biçimi ===")
    hepsi, siki = lp_kisitlari_saglanir_mi(m9, U9)
    print(f"  U*: bütün kısıtlar sağlanıyor mu? {hepsi};  her durumda biri sıkı mı? {siki}")
    yukari = {s: v + 0.1 for s, v in U9.items()}
    print(f"  U* + 0.1 kısıtları sağlıyor mu? {lp_kisitlari_saglanir_mi(m9, yukari)[0]} "
          "(sağlar ama toplamı daha büyük; LP en küçüğü seçer)")

    print("\n=== Çevrimiçi: derinlik sınırlı beklenti-maks, γ = 0.9, (3, 2)'den ===")
    for d in (1, 2, 3, 4, 6):
        deger, a = beklenti_maks(m9, (3, 2), d)
        print(f"  derinlik {d}: değer {deger:+.4f}, eylem {a}")
    print(f"  gerçek U(3,2) = {U9[(3, 2)]:+.4f}, en iyi eylem {m9.acgozlu(U9)[(3, 2)]}")
    for g in (0.5, 0.9):
        print(f"  ε-ufku (ε = 0.1, R_max = 1), γ = {g}: H = {epsilon_ufku(g, 0.1)}")


if __name__ == "__main__":
    main()
