#!/usr/bin/env python3
"""Bayes kuralı: nedenden sonuca bilinen olasılıklarla sonuçtan nedene akıl yürütmek.

    P(neden | sonuç) = P(sonuç | neden) P(neden) / P(sonuç)          (nedensel → tanısal)
    P(Y | x) = α P(x | Y) P(Y)                                        (normalizasyonla)

Kitaptaki örnekler (testlerle doğrulanır):
  * Menenjit: P(s|m) = 0.7, P(m) = 1/50000, P(s) = 0.01  →  P(m|s) = 0.0014
  * Kanıtları birleştirme (diş hekimi): Toothache ve Catch, Cavity verildiğinde koşullu
    bağımsız olduğundan P(Cavity | toothache, catch) = α P(t|Cav) P(c|Cav) P(Cav) ≈ ⟨0.871, 0.129⟩

Kendi örneklerimiz: nadir hastalık testi, olasılık oranı (odds) biçimi.

Çalıştırma:
    python bayes_kurali.py
"""
from __future__ import annotations


def bayes(p_sonuc_neden: float, p_neden: float, p_sonuc: float) -> float:
    """Doğrudan Bayes kuralı: P(neden | sonuç)."""
    return p_sonuc_neden * p_neden / p_sonuc


def bayes_normalize(oncel: float, p_e_h: float, p_e_degil_h: float) -> float:
    """P(sonuç)'u bilmeden: α⟨P(e|h)P(h), P(e|¬h)P(¬h)⟩'nin ilk bileşeni."""
    pay = p_e_h * oncel
    return pay / (pay + p_e_degil_h * (1 - oncel))


P_S_M, P_M, P_S = 0.7, 1 / 50000, 0.01
P_S_DEGIL_M = (P_S - P_S_M * P_M) / (1 - P_M)   # P(s) = 0.01 ile tutarlı P(s | ¬m) ≈ 0.009986


def menenjit() -> float:
    return bayes(P_S_M, P_M, P_S)


def menenjit_salgin(kat: float) -> float:
    """P(m) kat katına çıkınca P(m | s). P(s) sabit değildir (menenjitliler de boyun
    sertliği yaşar); nedensel P(s | m) ve P(s | ¬m) sabit kalır, normalizasyonla hesaplanır."""
    return bayes_normalize(kat * P_M, P_S_M, P_S_DEGIL_M)


def dis_naif_bayes() -> tuple[float, float]:
    """Kitaptaki tablodan okunan koşullu olasılıklarla iki kanıtı birleştir."""
    p_cav = 0.2
    p_t = {True: 0.6, False: 0.1}   # P(toothache | Cavity)
    p_c = {True: 0.9, False: 0.2}   # P(catch | Cavity)
    ham = {cav: p_t[cav] * p_c[cav] * (p_cav if cav else 1 - p_cav) for cav in (True, False)}
    z = sum(ham.values())
    return ham[True] / z, ham[False] / z


def main() -> None:
    print("=== Menenjit ve boyun sertliği (kitap) ===")
    print(f"  P(m | s) = 0.7 × (1/50000) / 0.01 = {menenjit():.4f}")
    print("  Boyun sertliği menenjitin güçlü bir belirtisi (0.7), ama menenjit çok nadir. Boyun")
    print("  sertliğinin başka nedenleri çok daha yaygın; sertliği olanların yalnızca %0.14'ü menenjit.")
    print(f"  Normalizasyonla (P(s | ¬m) ≈ {P_S_DEGIL_M:.6f}): P(m | s) = {menenjit_salgin(1):.4f}, aynı sonuç.")
    print(f"  Salgın: P(m) iki katına çıkarsa P(m | s) = {menenjit_salgin(2):.5f} (yaklaşık iki katı;")
    print("  P(s) de çok az arttığı için tam iki katı değil).")
    print("  Nedensel bilgi P(s | m) salgından etkilenmez; tanısal P(m | s) etkilenir. Bu yüzden")
    print("  nedensel bilgiyi saklayıp tanısal olasılığı Bayes ile hesaplamak daha sağlamdır.")

    print("\n=== Kanıtları birleştirme: diş hekimi (kitap) ===")
    print("  Tablodan: P(toothache|cavity)=0.6, P(toothache|¬cavity)=0.1,")
    print("            P(catch|cavity)=0.9,     P(catch|¬cavity)=0.2,  P(cavity)=0.2")
    evet, hayir = dis_naif_bayes()
    print(f"  α⟨0.6·0.9·0.2, 0.1·0.2·0.8⟩ = α⟨0.108, 0.016⟩ = ⟨{evet:.3f}, {hayir:.3f}⟩")
    print("  Tam ortak tablodan okunan değerle aynı: tablo koşullu bağımsızlığı sağlıyor.")

    print("\n=== Kendi örneğimiz: nadir hastalık testi ===")
    oncel, duyarlilik, yanlis_poz = 0.001, 0.99, 0.05
    sonsal = bayes_normalize(oncel, duyarlilik, yanlis_poz)
    print(f"  P(Hasta) = {oncel}, P(+ | Hasta) = {duyarlilik}, P(+ | Sağlam) = {yanlis_poz}")
    print(f"  P(Hasta | +) = {sonsal:.4f}  (yaklaşık %{100 * sonsal:.1f})")
    print("  1000 kişiden ~1 hasta pozitif çıkar; 999 sağlamdan ~50'si de pozitif çıkar.")
    ikinci = bayes_normalize(sonsal, duyarlilik, yanlis_poz)
    print(f"  İkinci bağımsız test de pozitifse: P(Hasta | +, +) = {ikinci:.4f}")
    print("  (İlk testin sonsalı, ikinci test için önsel olur.)")

    print("\n=== Olasılık oranı (odds) biçimi ===")
    oran_once = oncel / (1 - oncel)
    lr = duyarlilik / yanlis_poz
    oran_sonra = lr * oran_once
    print(f"  önsel oran {oran_once:.5f} × olabilirlik oranı {lr:.1f} = sonsal oran {oran_sonra:.5f}")
    print(f"  → olasılık {oran_sonra / (1 + oran_sonra):.4f} (yukarıdakiyle aynı)")


if __name__ == "__main__":
    main()
