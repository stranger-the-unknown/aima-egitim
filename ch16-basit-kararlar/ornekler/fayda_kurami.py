#!/usr/bin/env python3
"""Fayda kuramı: paranın faydası, risk tutumu, insan yargısındaki paradokslar (kitaptaki 16.2–16.3).

Kitaptaki örnekler (testlerle doğrulanır):
  * Yarışma: 1 000 000 $ kesin ya da yazı-tura ile 0 / 2 500 000 $. EMV = 1 250 000 $.
    U(S_k) = 5, U(S_{k+2.5M}) = 9, U(S_{k+1M}) = 8 → EU(kabul) = 7 < EU(ret) = 8.
  * Bay Beard'ın faydası: U(S_{k+n}) = −263.31 + 22.09 log(n + 150 000),  −150 000 ≤ n ≤ 800 000.
  * İnsanların çoğu, yarı yarıya 1000 $ / 0 $ piyango yerine ~400 $ kabul eder:
    kesinlik eşdeğeri 400 $, EMV 500 $, sigorta primi 100 $.
  * Allais paradoksu: A 0.8 × 4000 $, B kesin 3000 $; C 0.2 × 4000 $, D 0.25 × 3000 $.
    B ≻ A ve C ≻ D tercihlerini birlikte açıklayan bir fayda fonksiyonu yoktur.
  * Ellsberg paradoksu: 1/3 kırmızı, 2/3 siyah ya da sarı. A ≻ B ve D ≻ C hiçbir dünyada rasyonel değil.

Çalıştırma:
    python fayda_kurami.py
"""
from __future__ import annotations

import math


def beklenen(piyango: list[tuple[float, float]], U=lambda x: x) -> float:
    """piyango: [(olasılık, sonuç), ...]"""
    return sum(p * U(x) for p, x in piyango)


def beard(n: float) -> float:
    """Bay Beard'ın servet artışı n için faydası (doğal logaritma; U(0) ≈ 0)."""
    return -263.31 + 22.09 * math.log(n + 150_000)


def beard_ters(u: float) -> float:
    return math.exp((u + 263.31) / 22.09) - 150_000


def kesinlik_esdegeri(piyango, U, U_ters) -> float:
    return U_ters(beklenen(piyango, U))


def allais_tutarli_mi(adim: float = 0.01) -> bool:
    """U($0) = 0, U($4000) = 1 alınır (ölçek serbest). B ≻ A ve C ≻ D aynı anda sağlanabilir mi?"""
    u = 0.0
    while u <= 1.0:  # u = U($3000)
        b_a = u > 0.8 * 1.0
        c_d = 0.2 * 1.0 > 0.25 * u
        if b_a and c_d:
            return True
        u += adim
    return False


def ellsberg_tutarli_mi(adim: float = 0.001) -> bool:
    """Siyah top oranı b ∈ [0, 2/3]. A ≻ B ⇔ 1/3 > b;  D ≻ C ⇔ 2/3 > 1/3 + (2/3 − b)."""
    b = 0.0
    while b <= 2 / 3:
        if 1 / 3 > b and 2 / 3 > 1 / 3 + (2 / 3 - b):
            return True
        b += adim
    return False


def para_pompasi(tercih: dict, baslangic: str, tur: int = 3, ucret: float = 0.01) -> tuple[list[str], float]:
    """Döngüsel tercihleri olan ajan (A ≻ B ≻ C ≻ A): her takas için küçük bir ücret öder."""
    elde, odenen, yol = baslangic, 0.0, [baslangic]
    for _ in range(3 * tur):
        elde = tercih[elde]  # elindekinden daha çok sevdiği seçenek
        odenen += ucret
        yol.append(elde)
    return yol, odenen


def main() -> None:
    print("=== Yarışma: 1 milyon kesin mi, yazı-tura mı? ===")
    kumar = [(0.5, 0), (0.5, 2_500_000)]
    print(f"  EMV(kumar) = {beklenen(kumar):,.0f} $  >  1,000,000 $")
    U = {0: 5, 2_500_000: 9, 1_000_000: 8}
    print(f"  EU(kabul) = 0.5 × 5 + 0.5 × 9 = {beklenen(kumar, U.get)},  EU(ret) = {U[1_000_000]}  → reddet")
    print("  Paranın faydası doğrusal değil: ilk milyonun faydası, ikincisininkinden çok daha büyük.")

    print("\n=== Bay Beard'ın fayda fonksiyonu ===")
    for n in (-150_000 + 1, 0, 100_000, 400_000, 800_000):
        print(f"  n = {n:>9,} $  →  U = {beard(n):7.2f}")
    for piyango in ([(0.5, 0), (0.5, 1000)], [(0.5, 0), (0.5, 800_000)]):
        emv = beklenen(piyango)
        ke = kesinlik_esdegeri(piyango, beard, beard_ters)
        print(f"  Piyango {piyango}: EMV {emv:,.0f} $, kesinlik eşdeğeri {ke:,.0f} $, sigorta primi {emv - ke:,.0f} $")
    print("  Küçük tutarlarda neredeyse risk-nötr; büyük tutarlarda belirgin biçimde riskten kaçınan.")
    print("  (İnsanların çoğu yarı yarıya 1000 $ / 0 $ piyango için ~400 $ kabul eder: prim 100 $.)")

    print("\n=== Allais ve Ellsberg paradoksları ===")
    print(f"  Allais: B ≻ A ve C ≻ D ile tutarlı bir U var mı? {allais_tutarli_mi()}")
    print("    B ≻ A ⇒ U(3000) > 0.8 U(4000);  C ≻ D ⇒ 0.2 U(4000) > 0.25 U(3000) ⇒ U(3000) < 0.8 U(4000)")
    print(f"  Ellsberg: A ≻ B ve D ≻ C ile tutarlı bir siyah top oranı var mı? {ellsberg_tutarli_mi()}")
    print("    A ≻ B ⇒ siyah < 1/3;  D ≻ C ⇒ siyah > 1/3. İnsanlar bilinmeyen olasılıklardan kaçınır.")

    print("\n=== Para pompası: geçişli olmayan tercihler ===")
    yol, odenen = para_pompasi({"C": "B", "B": "A", "A": "C"}, "C")
    print(f"  Takaslar: {' → '.join(yol)}")
    print(f"  Ajan başladığı yere döndü ve {odenen:.2f} $ ödedi. Geçişlilik aksiyomu bu yüzden gereklidir.")


if __name__ == "__main__":
    main()
