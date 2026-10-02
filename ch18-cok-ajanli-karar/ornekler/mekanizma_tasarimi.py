#!/usr/bin/env python3
"""Toplu kararlar: açık artırmalar, VCG, ortak kaynaklar, oylama, pazarlık (kitaptaki 18.4).

Kitaptaki örnekler (testlerle doğrulanır):
  * İngiliz (artan teklif) açık artırması: en yüksek değerli kazanır, b_o + d öder.
  * Vickrey (ikinci fiyat, kapalı zarf): gerçek değeri teklif etmek baskın stratejidir.
  * Reklam yuvaları (n + 1 fiyat): v = 200, 180, 100; tıklanma 0.05 ve 0.02. Dürüst teklifle b1'in
    getirisi 1; 101–179 arası teklif verirse 2. Doğru (Aggarwal) mekanizmada 2.6.
  * VCG: 3 verici, teklifler 100, 50, 40, 20, 10 → kazananlar 100, 50, 40; her biri 20 vergi öder.
  * Ortak kaynakların trajedisi: 100 ülke; azaltmak −10, kirletmek −5 ve diğer her ülkeye −1.
    Herkes kirletirse her ülke −104, herkes azaltırsa −10.
  * Condorcet paradoksu (18.2): a ≻₁ b ≻₁ c; c ≻₂ a ≻₂ b; b ≻₃ c ≻₃ a → çoğunluk döngüsü.
  * Dönüşümlü teklif pazarlığı: tek tur → ilk teklif veren hepsini alır; iki tur → (1 − γ₂, γ₂);
    sınırsız tur (Rubinstein) → A1 (1 − γ₂)/(1 − γ₁γ₂) alır.

Çalıştırma:
    python mekanizma_tasarimi.py
"""
from __future__ import annotations

import itertools
import random
from collections import Counter


# --- Açık artırmalar --------------------------------------------------------------
def ingiliz(degerler: list[float], rezerv: float = 0.0, d: float = 1.0):
    """Artan teklif: Mevcut fiyat p ve lider L varken müzayedeci p + d ister; değeri buna yeten
    (lider olmayan) biri teklif verirse yeni lider o olur. Kimse vermezse L, p'yi öder.
    Sonuç (kitap): en yüksek değerli kazanır, b_o + d öder (b_o: diğerlerinin en yüksek değeri)."""
    adaylar = [i for i, v in enumerate(degerler) if v >= rezerv]
    if not adaylar:
        return None, None
    lider, fiyat = min(adaylar), rezerv
    while True:
        istekliler = [i for i, v in enumerate(degerler) if i != lider and v >= fiyat + d]
        if not istekliler:
            return lider, fiyat
        lider, fiyat = istekliler[0], fiyat + d


def ikinci_fiyat(teklifler: list[float]):
    sira = sorted(range(len(teklifler)), key=lambda i: -teklifler[i])
    return sira[0], teklifler[sira[1]]


def vickrey_fayda(v: float, b: float, bo: float) -> float:
    """Değer v, teklif b, diğerlerinin en iyi teklifi bo."""
    return v - bo if b > bo else 0.0


def dogruluk_baskin_mi(v: float, adaylar, rakipler) -> bool:
    """Vickrey'de b = v teklifi, her rakip teklifine karşı her başka tekliften en az iyi mi?"""
    return all(vickrey_fayda(v, v, bo) >= vickrey_fayda(v, b, bo) for bo in rakipler for b in adaylar)


def gelir_esitligi(n: int = 4, deneme: int = 100_000, tohum: int = 0) -> dict:
    """Değerler U(0, 1). Birinci fiyatta denge teklifi (n−1)/n · v; ikinci fiyatta dürüst teklif.
    İkisinin de beklenen geliri (n − 1)/(n + 1)."""
    rng = random.Random(tohum)
    birinci = ikinci = 0.0
    for _ in range(deneme):
        v = sorted((rng.random() for _ in range(n)), reverse=True)
        birinci += (n - 1) / n * v[0]
        ikinci += v[1]
    return {"birinci fiyat": birinci / deneme, "ikinci fiyat": ikinci / deneme, "kuram": (n - 1) / (n + 1)}


def reklam_yuvalari(degerler=(200, 180, 100), tik=(0.05, 0.02)):
    """n + 1 fiyat mekanizmasında b1'in getirisi: dürüst ve 101–179 arası teklif; doğru mekanizmada."""
    v1, v2, v3 = degerler
    durust = (v1 - v2) * tik[0]
    dusuk = (v1 - v3) * tik[1]
    dogru = (v1 - v2) * (tik[0] - tik[1]) + (v1 - v3) * tik[1]
    return {"dürüst (n+1 fiyat)": durust, "düşük teklif (n+1 fiyat)": dusuk, "doğru mekanizma": dogru}


def vcg(teklifler: list[float], k: int):
    """k özdeş mal, her ajan en çok bir tane ister. Kazananlar toplam değeri en büyükler; her kazanan,
    varlığının diğerlerine verdiği kaybı vergi olarak öder."""
    def en_iyi_toplam(ajanlar):
        return sum(sorted((teklifler[i] for i in ajanlar), reverse=True)[:k])

    herkes = list(range(len(teklifler)))
    kazananlar = sorted(herkes, key=lambda i: -teklifler[i])[:k]
    vergi = {}
    for i in kazananlar:
        digerleri = [j for j in herkes if j != i]
        varken = en_iyi_toplam(herkes) - teklifler[i]        # i varken diğerlerinin aldığı
        yokken = en_iyi_toplam(digerleri)                    # i yokken diğerlerinin alacağı
        vergi[i] = yokken - varken
    return kazananlar, vergi


def ortak_kaynak(n: int = 100) -> dict:
    """Her ülke: azalt (−10) ya da kirlet (−5 ve diğer her ülkeye −1)."""
    def fayda(benim: str, kirleten_diger: int) -> int:
        return (-10 if benim == "azalt" else -5) - kirleten_diger

    return {"herkes kirletir": fayda("kirlet", n - 1), "herkes azaltır": fayda("azalt", 0),
            "kirletmek baskın mı": all(fayda("kirlet", k) > fayda("azalt", k) for k in range(n))}


# --- Oylama ------------------------------------------------------------------------
CONDORCET = [["a", "b", "c"], ["c", "a", "b"], ["b", "c", "a"]]


def ikili(oylar, x, y) -> int:
    """x'i y'ye tercih eden seçmen sayısı − tersi."""
    return sum(1 if o.index(x) < o.index(y) else -1 for o in oylar)


def condorcet_kazanani(oylar):
    adaylar = oylar[0]
    for x in adaylar:
        if all(ikili(oylar, x, y) > 0 for y in adaylar if y != x):
            return x
    return None


def cogunluk(oylar) -> list:
    sayim = Counter(o[0] for o in oylar)
    en = max(sayim.values())
    return sorted(a for a, s in sayim.items() if s == en)


def borda(oylar) -> dict:
    k = len(oylar[0])
    puan = Counter()
    for o in oylar:
        for sira, a in enumerate(o):
            puan[a] += k - sira
    return dict(puan)


def aninda_ikinci_tur(oylar):
    kalan = list(oylar[0])
    while True:
        sayim = Counter(next(a for a in o if a in kalan) for o in oylar)
        lider, oy = sayim.most_common(1)[0]
        if oy * 2 > len(oylar):
            return lider
        en_az = min(kalan, key=lambda a: (sayim.get(a, 0), a))
        kalan.remove(en_az)


# --- Pazarlık -----------------------------------------------------------------------
def donusumlu_teklif(tur: int, g1: float, g2: float) -> float:
    """Sabit tur sayısında geriye tümevarım: A1'in payı (A1 ilk teklifi verir)."""
    # Son turda teklif veren her şeyi alır. Teklif veren, karşısına onun bir sonraki turdaki
    # (indirimli) payını verir.
    pay_teklif_veren = 1.0
    for t in range(tur - 1, 0, -1):
        # t. turdaki teklif veren; karşıdaki (t+1'de teklif verecek) γ_karşı × pay_sonraki ister
        teklif_veren_A1 = (t % 2 == 1)          # tur 1, 3, ...: A1 (1'den sayıyoruz)
        karsi_gama = g2 if teklif_veren_A1 else g1
        pay_teklif_veren = 1 - karsi_gama * pay_teklif_veren
    return pay_teklif_veren


def rubinstein(g1: float, g2: float) -> float:
    return (1 - g2) / (1 - g1 * g2)


def main() -> None:
    print("=== Açık artırmalar ===")
    degerler = [120, 95, 180, 150]
    print(f"  Değerler {degerler}: İngiliz → {ingiliz(degerler, rezerv=50, d=1)} (kazanan, fiyat); "
          f"Vickrey (dürüst teklif) → {ikinci_fiyat(degerler)}")
    print(f"  Vickrey'de dürüst teklif baskın mı? "
          f"{dogruluk_baskin_mi(100, range(0, 201, 5), range(0, 201, 7))}")
    g = gelir_esitligi()
    print(f"  Gelir eşitliği (4 teklifçi, U(0,1)): birinci fiyat {g['birinci fiyat']:.4f}, "
          f"ikinci fiyat {g['ikinci fiyat']:.4f}, kuram {g['kuram']:.4f}")
    for k, v in reklam_yuvalari().items():
        print(f"  Reklam yuvaları, b1'in getirisi — {k}: {v:.2f}")

    print("\n=== VCG: 3 verici, teklifler 100, 50, 40, 20, 10 ===")
    kazananlar, vergi = vcg([100, 50, 40, 20, 10], 3)
    print(f"  Kazananlar: {[ [100, 50, 40, 20, 10][i] for i in kazananlar]}, vergiler: {list(vergi.values())}")

    print("\n=== Ortak kaynakların trajedisi (100 ülke) ===")
    for k, v in ortak_kaynak().items():
        print(f"  {k}: {v}")

    print("\n=== Oylama ===")
    print(f"  Condorcet: a–b {ikili(CONDORCET, 'a', 'b'):+d}, b–c {ikili(CONDORCET, 'b', 'c'):+d}, "
          f"c–a {ikili(CONDORCET, 'c', 'a'):+d} → döngü; Condorcet kazananı: {condorcet_kazanani(CONDORCET)}")
    secim = [["A", "C", "B"]] * 4 + [["B", "C", "A"]] * 3 + [["C", "B", "A"]] * 2
    print(f"  9 seçmen (4: A≻C≻B, 3: B≻C≻A, 2: C≻B≻A):")
    print(f"    çoğunluk (en çok birinci): {cogunluk(secim)}, Borda: {borda(secim)}, "
          f"anında ikinci tur: {aninda_ikinci_tur(secim)}, Condorcet: {condorcet_kazanani(secim)}")
    print("    Aynı oylar, farklı kurallar, farklı kazananlar (Arrow: kusursuz kural yok).")

    print("\n=== Dönüşümlü teklif pazarlığı (pastanın değeri 1) ===")
    g1, g2 = 0.9, 0.8
    for tur in (1, 2, 3, 10, 50):
        print(f"  {tur:>2} tur, γ1 = {g1}, γ2 = {g2}: A1'in payı {donusumlu_teklif(tur, g1, g2):.4f}")
    print(f"  Sınırsız tur (Rubinstein): {rubinstein(g1, g2):.4f}. Sabırlı olan daha çok alır.")


if __name__ == "__main__":
    main()
