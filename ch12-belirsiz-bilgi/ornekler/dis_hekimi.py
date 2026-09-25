#!/usr/bin/env python3
"""Kitabın diş hekimi örneği: Toothache (ağrı), Catch (sonda takılıyor), Cavity (çürük).

Tam ortak dağılım (kitaptaki tablo, 8 dünya):
                    toothache            ¬toothache
                  catch   ¬catch       catch   ¬catch
    cavity        0.108   0.012        0.072   0.008
    ¬cavity       0.016   0.064        0.144   0.576

Kitaptaki sonuçlar (testlerle doğrulanır):
    P(cavity) = 0.2                     P(cavity ∨ toothache) = 0.28
    P(Cavity | toothache) = ⟨0.6, 0.4⟩   P(Cavity | toothache, catch) ≈ ⟨0.871, 0.129⟩
    Toothache ve Catch, Cavity verildiğinde koşullu bağımsızdır; 7 bağımsız sayı yerine 5 yeter.
    Weather eklenince 32 satır, ama bağımsızlıkla 8 + 4 satıra ayrışır.

Çalıştırma:
    python dis_hekimi.py
"""
from __future__ import annotations

from olasilik import OrtakDagilim

DEGISKENLER = ["Toothache", "Catch", "Cavity"]
TABLO = {
    (True, True, True): 0.108, (True, False, True): 0.012,
    (False, True, True): 0.072, (False, False, True): 0.008,
    (True, True, False): 0.016, (True, False, False): 0.064,
    (False, True, False): 0.144, (False, False, False): 0.576,
}
HAVA = OrtakDagilim(["Weather"], {("güneşli",): 0.6, ("yağmurlu",): 0.1, ("bulutlu",): 0.29, ("karlı",): 0.01})


def dis_dagilimi() -> OrtakDagilim:
    return OrtakDagilim(DEGISKENLER, TABLO)


def ayristirilmis(d: OrtakDagilim) -> OrtakDagilim:
    """P(Toothache, Catch, Cavity) = P(Toothache | Cavity) P(Catch | Cavity) P(Cavity) ile yeniden kur."""
    tablo = {}
    for (t, c, cav) in TABLO:
        tablo[(t, c, cav)] = (d.P({"Toothache": t}, {"Cavity": cav}) * d.P({"Catch": c}, {"Cavity": cav})
                              * d.P({"Cavity": cav}))
    return OrtakDagilim(DEGISKENLER, tablo)


def _yuvarla(dagilim: dict, n: int = 3) -> dict:
    return {k: round(v, n) for k, v in dagilim.items()}


def main() -> None:
    d = dis_dagilimi()
    print("=== Tam ortak dağılımdan çıkarım ===")
    print(f"  Toplam olasılık                     = {sum(TABLO.values()):.3f}")
    print(f"  P(cavity)             (marjinal)    = {d.P({'Cavity': True}):.3f}")
    print(f"  P(cavity ∨ toothache)               = {d.P(lambda w: w['Cavity'] or w['Toothache']):.3f}")
    print(f"  P(toothache)                        = {d.P({'Toothache': True}):.3f}")
    print(f"  P(cavity | toothache)               = {d.P({'Cavity': True}, {'Toothache': True}):.3f}")
    print(f"  P(Cavity | toothache)   (α ile)     = {_yuvarla(d.kosullu('Cavity', {'Toothache': True}))}")
    print(f"  P(Cavity | toothache, catch)        = {_yuvarla(d.kosullu('Cavity', {'Toothache': True, 'Catch': True}))}")
    print("  Normalizasyon: α⟨0.108 + 0.012, 0.016 + 0.064⟩ = α⟨0.12, 0.08⟩ = ⟨0.6, 0.4⟩."
          "\n  P(toothache)'ı hiç hesaplamadan sonuca ulaştık.")

    print("\n=== Bağımsızlık ===")
    print(f"  Toothache ⊥ Catch (mutlak)?            {d.bagimsiz_mi('Toothache', 'Catch')}")
    print(f"  Toothache ⊥ Catch | Cavity (koşullu)?  {d.bagimsiz_mi('Toothache', 'Catch', 'Cavity')}")
    print("  Sonda takılırsa çürük olasılığı artar, o da ağrıyı olası kılar: ağrı ve sonda ilişkili."
          "\n  Ama çürüğün var olup olmadığını bilirsek biri diğeri hakkında bir şey söylemez.")
    a = ayristirilmis(d)
    en_buyuk_fark = max(abs(a.tablo[k] - TABLO[k]) for k in TABLO)
    print(f"  P(T|Cav)·P(C|Cav)·P(Cav) tabloyu yeniden üretiyor mu? en büyük fark = {en_buyuk_fark:.1e}")
    print("  Bağımsız sayı: tam tablo 2³ − 1 = 7; ayrışmış hâl 2 + 2 + 1 = 5.")
    print("  n belirti için: tam tablo 2^(n+1) − 1, naif Bayes 2n + 1.")
    for n in (3, 10, 30):
        print(f"    n = {n:>2}: {2 ** (n + 1) - 1:>13,} yerine {2 * n + 1}")

    print("\n=== Mutlak bağımsızlık: hava durumu ===")
    dh = d.carp(HAVA)
    print(f"  P(Toothache, Catch, Cavity, Weather): {len(dh.tablo)} satır = 8 × 4")
    print(f"  Ama saklamak için 8 + 4 = 12 sayı yeter. Weather ⊥ Cavity? {dh.bagimsiz_mi('Weather', 'Cavity')}")
    print(f"  P(toothache, catch, cavity, bulutlu) = 0.108 × 0.29 = "
          f"{dh.P({'Toothache': True, 'Catch': True, 'Cavity': True, 'Weather': 'bulutlu'}):.5f}")


if __name__ == "__main__":
    main()
