#!/usr/bin/env python3
"""Uzun (genişletilmiş) biçimli oyunlar ve yardım oyunları (kitaptaki 18.2.4–18.2.5).

1. Şekil 18.4: Oyuncu 1 aşağı (0, 0) ya da yukarı; yukarıda oyuncu 2 yukarı (1, 1) ya da aşağı (0, 0).
   Geriye tümevarım (yukarı, yukarı)'yı bulur: alt oyun yetkin Nash dengesi. (aşağı, aşağı) da bir Nash
   dengesidir ama oyuncu 2'nin "aşağı" tehdidi inandırıcı değildir.
2. Basitleştirilmiş poker (Şekil 18.5): 2 as, 2 papaz; her oyuncuya bir kart. Oyuncu 1 artırır (r) ya da
   bekler (k). Beklerse oyun 1 puanla biter. Artırırsa oyuncu 2 görür (c, oyun 2 puan) ya da çekilir
   (f, 1 puan kaybeder). Kartlar aynıysa 0; değilse papazlı olan asa ödeme yapar.
   Kitaptaki normal biçim matrisi (oyuncu 1'in faydası) koddan türetilir ve doğrulanır; oyunun değeri 0.
3. Ataş oyunu (Şekil 18.6): Harriet 2 ataş, 1+1 ya da 2 zımba yapar; Robbie 90 ataş, 50+50 ya da 90 zımba.
   Harriet'in faydası pθ + s(1 − θ); Robbie'nin önseli θ ~ U(0, 1). Miyop en iyi tepkiyle denge:
   Harriet θ ∈ [0.446, 0.554] ise 1+1 yapar (kitap).

Çalıştırma:
    python uzun_bicim.py
"""
from __future__ import annotations

import itertools
from fractions import Fraction

import numpy as np

import oyun_kurami as ok


# --- 1. Geriye tümevarım -------------------------------------------------------------
# Düğüm: ("uç", (u1, u2)) ya da (oyuncu, {eylem: alt düğüm})
SEKIL_18_4 = (0, {"aşağı": ("uç", (0, 0)),
                  "yukarı": (1, {"yukarı": ("uç", (1, 1)), "aşağı": ("uç", (0, 0))})})


def geriye_tumevarim(dugum, yol=""):
    """(fayda profili, {düğüm yolu: seçilen eylem}). Eşitlikte ilk eylem."""
    if dugum[0] == "uç":
        return dugum[1], {}
    oyuncu, cocuklar = dugum
    en, strateji = None, {}
    for eylem, cocuk in cocuklar.items():
        u, alt = geriye_tumevarim(cocuk, yol + "/" + eylem)
        strateji.update(alt)
        if en is None or u[oyuncu] > en[1][oyuncu]:
            en = (eylem, u)
    strateji[yol or "/"] = en[0]
    return en[1], strateji


def sekil_18_4_normal_bicim() -> ok.Oyun:
    tablo = {}
    for a1, a2 in itertools.product(("yukarı", "aşağı"), repeat=2):
        tablo[(a1, a2)] = (0, 0) if a1 == "aşağı" else ((1, 1) if a2 == "yukarı" else (0, 0))
    return ok.iki_oyunculu(("1", "2"), ("yukarı", "aşağı"), ("yukarı", "aşağı"), tablo)


# --- 2. Basitleştirilmiş poker ---------------------------------------------------------
DAGITIMLAR = {("A", "A"): Fraction(1, 6), ("A", "K"): Fraction(1, 3),
              ("K", "A"): Fraction(1, 3), ("K", "K"): Fraction(1, 6)}
P1_STRATEJILER = ["rr", "kr", "rk", "kk"]     # (as varken, papaz varken)
P2_STRATEJILER = ["cc", "cf", "ff", "fc"]     # (as varken, papaz varken), artırmaya karşı


def hesaplasma(k1: str, k2: str, pay: int) -> int:
    return 0 if k1 == k2 else (pay if k1 == "A" else -pay)


def poker_fayda(s1: str, s2: str) -> Fraction:
    """Oyuncu 1'in beklenen faydası (sıfır toplamlı)."""
    toplam = Fraction(0)
    for (k1, k2), p in DAGITIMLAR.items():
        eylem1 = s1[0] if k1 == "A" else s1[1]
        if eylem1 == "k":
            u = hesaplasma(k1, k2, 1)
        else:
            eylem2 = s2[0] if k2 == "A" else s2[1]
            u = 1 if eylem2 == "f" else hesaplasma(k1, k2, 2)
        toplam += p * u
    return toplam


def poker_matrisi() -> list[list[Fraction]]:
    return [[poker_fayda(s1, s2) for s2 in P2_STRATEJILER] for s1 in P1_STRATEJILER]


def saf_eyer_noktalari(A) -> list:
    """Satırında en küçük, sütununda en büyük olan hücreler (sıfır toplamlı saf dengeler)."""
    return [(i, j) for i, satir in enumerate(A) for j, x in enumerate(satir)
            if x == min(satir) and x == max(A[k][j] for k in range(len(A)))]


# --- 3. Ataş oyunu ------------------------------------------------------------------------
HARRIET = {"2 ataş": (2, 0), "1 + 1": (1, 1), "2 zımba": (0, 2)}
ROBBIE = {"90 ataş": (90, 0), "50 + 50": (50, 50), "90 zımba": (0, 90)}


def harriet_fayda(urun, theta):
    p, s = urun
    return p * theta + s * (1 - theta)


def atas_dengesi(izgara: int = 20001, en_cok: int = 20):
    """Miyop en iyi tepki. θ ızgarası üzerinde Harriet'in stratejisi: θ → eylem.
    Robbie her gözlem için, o eylemi seçen θ'ların ortalamasına göre en iyi ürünü seçer."""
    thetalar = np.linspace(0, 1, izgara)
    # 1. adım: açgözlü Harriet
    harriet = np.array([max(HARRIET, key=lambda h: (harriet_fayda(HARRIET[h], t), h == "1 + 1")) for t in thetalar])
    robbie = {}
    for _ in range(en_cok):
        yeni_robbie = {}
        for h in HARRIET:
            secenler = thetalar[harriet == h]
            ort = secenler.mean() if len(secenler) else 0.5
            yeni_robbie[h] = max(ROBBIE, key=lambda r: harriet_fayda(ROBBIE[r], ort))
        yeni_harriet = np.array([max(HARRIET, key=lambda h: harriet_fayda(HARRIET[h], t)
                                     + harriet_fayda(ROBBIE[yeni_robbie[h]], t)) for t in thetalar])
        if yeni_robbie == robbie and np.array_equal(yeni_harriet, harriet):
            break
        robbie, harriet = yeni_robbie, yeni_harriet
    araligi = thetalar[harriet == "1 + 1"]
    return robbie, ((float(araligi.min()), float(araligi.max())) if len(araligi) else None)


def main() -> None:
    print("=== Şekil 18.4: geriye tümevarım ve inandırıcı olmayan tehdit ===")
    u, strateji = geriye_tumevarim(SEKIL_18_4)
    print(f"  Geriye tümevarım: {strateji}, faydalar {u}")
    print(f"  Normal biçimdeki saf Nash dengeleri: {ok.saf_nash(sekil_18_4_normal_bicim())}")
    print("  (aşağı, aşağı) bir Nash dengesi ama alt oyun yetkin değil: Oyuncu 2 o düğüme gelirse yukarı seçer.")

    print("\n=== Basitleştirilmiş poker: normal biçim (oyuncu 1'in faydası) ===")
    A = poker_matrisi()
    print("        " + "".join(f"{s:>7}" for s in P2_STRATEJILER))
    for s1, satir in zip(P1_STRATEJILER, A):
        print(f"  1:{s1}  " + "".join(f"{str(x):>7}" for x in satir))
    print(f"  Saf dengeler: {[(P1_STRATEJILER[i], P2_STRATEJILER[j]) for i, j in saf_eyer_noktalari(A)]}")
    v, p, q = ok.maksimin([[float(x) for x in satir] for satir in A])
    print(f"  LP: oyunun değeri {v:+.4f}; oyuncu 1 {dict(zip(P1_STRATEJILER, np.round(p, 3).tolist()))}, "
          f"oyuncu 2 {dict(zip(P2_STRATEJILER, np.round(q, 3).tolist()))}")
    print(f"  Bilgi kümesi başına a eylem, I bilgi kümesi → a^I saf strateji (burada 2² = 4).")

    print("\n=== Ataş oyunu (yardım oyunu) ===")
    robbie, (alt, ust) = atas_dengesi()
    print(f"  Robbie'nin dengedeki tepkisi: {robbie}")
    print(f"  Harriet 1 + 1 yapar ⇔ θ ∈ [{alt:.3f}, {ust:.3f}]   (kitap: 0.446 – 0.554; tam değer 41/92 – 51/92)")
    print("  Harriet tercihlerini Robbie'ye basit bir 'kodla' öğretir; Robbie θ'yı tam bilmez ama doğru davranır.")


if __name__ == "__main__":
    main()
