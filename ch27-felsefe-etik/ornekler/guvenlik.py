#!/usr/bin/env python3
"""Yapay zekâ güvenliği (kitaptaki 27.3.7).

* Hata ağacı analizi (FTA): olası arızaların VE/VEYA ağacı; kök nedenlere olasılık ver, toplam arıza
  olasılığını hesapla (burada nedenleri bağımsız varsayıyoruz).
* Düşük etki: "fayda eksi dünyadaki değişikliklerin ağırlıklı toplamı". Robot hangi nesnenin önemli olduğunu
  bilmeden de dünyayı gereksiz yere değiştirmekten kaçınır.
* Şartname oyunu (değer hizalama / Kral Midas sorunu): Ödül "temizlediğin her kir için +1" olursa en iyi
  politika kiri dökme ve yeniden temizlemedir; ödül "odanın temiz olması" olursa böyle bir boşluk yoktur.
* Yardım oyunlarından bir fikir: Tercihlerden emin olmayan robot sormanın beklenen faydasını hesaplar.
* Tekillik kestirimleri üzerine kitaptaki hesap: "24 yılda 2 yıl yaklaştı, bu hızla 336 yıl kaldı".

Çalıştırma:
    python guvenlik.py
"""
from __future__ import annotations

import heapq
import math

import numpy as np


# --- Hata ağacı ------------------------------------------------------------------------------------
def olasilik(dugum) -> float:
    """Yaprak: (ad, olasılık). İç düğüm: ("VE" | "VEYA", ad, [çocuklar]). Nedenler bağımsız varsayılır."""
    if len(dugum) == 2:
        return dugum[1]
    tur, _, cocuklar = dugum
    p = [olasilik(c) for c in cocuklar]
    return float(np.prod(p)) if tur == "VE" else 1 - float(np.prod([1 - q for q in p]))


def arac_agaci(yedek_bilgisayar: bool = True):
    guc = ("VE", "bilgisayar durur", [("ana güç kesilir", 1e-4), ("yedek güç kesilir", 1e-3)]) \
        if yedek_bilgisayar else ("ana güç kesilir", 1e-4)
    return ("VEYA", "araç denetimi kaybeder", [
        guc,
        ("VE", "lastik olayı", [("yüksek hızda lastik patlar", 1e-3), ("yazılım denetimi düzeltemez", 0.05)]),
        ("VE", "algı kaybı", [("ön kamera arızalanır", 1e-3), ("lidar da arızalanır", 1e-2)]),
    ])


# --- Düşük etki ------------------------------------------------------------------------------------
HARITA = ["..K....",
          "R..V..H",
          "......C"]          # R robot, H hedef (kahve), V vazo, K kedi mamasının kabı, C çiçek saksısı


def dusuk_etkili_yol(lam: float, harita=HARITA):
    """Durum (konum, bozulan nesneler). Maliyet = adım sayısı + λ · (bozulan nesne sayısı).
    Robot hangi nesnenin değerli olduğunu bilmez; her değişikliği aynı cezalandırır. (yol, adım, bozulanlar)."""
    n, m = len(harita), len(harita[0])
    bul = lambda c: next((i, j) for i in range(n) for j in range(m) if harita[i][j] == c)  # noqa: E731
    bas, hedef = bul("R"), bul("H")
    kuyruk = [(0.0, bas, frozenset(), [bas])]
    gorulen = {}
    while kuyruk:
        maliyet, (i, j), bozuk, yol = heapq.heappop(kuyruk)
        if (i, j) == hedef:
            return yol, len(yol) - 1, sorted(harita[a][b] for a, b in bozuk)
        if gorulen.get(((i, j), bozuk), math.inf) <= maliyet:
            continue
        gorulen[((i, j), bozuk)] = maliyet
        for di, dj in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            a, b = i + di, j + dj
            if 0 <= a < n and 0 <= b < m:
                yeni = bozuk | ({(a, b)} if harita[a][b] in "VKC" else set())
                heapq.heappush(kuyruk, (maliyet + 1 + lam * (len(yeni) - len(bozuk)), (a, b), yeni, yol + [(a, b)]))
    return None, math.inf, []


# --- Şartname oyunu -----------------------------------------------------------------------------------
EYLEMLER = ("bekle", "temizle", "dök")          # eşitlikte önce "bekle" seçilir


def gecis(kir: int, torba: int, eylem: str, en_cok: int = 3):
    """(yeni kir, yeni torba, temizlenen kir miktarı)."""
    if eylem == "temizle" and kir > 0 and torba < en_cok:
        return kir - 1, torba + 1, 1
    if eylem == "dök":
        return min(en_cok, kir + torba), 0, 0
    return kir, torba, 0


def odul(kir, torba, eylem, sonra, odul_turu: str) -> float:
    if odul_turu == "temizlenen kir başına +1":
        return float(sonra[2])
    return -float(sonra[0])                          # "oda temiz olsun": kalan kir başına −1


def en_iyi_politika(odul_turu: str, gamma: float = 0.95, en_cok: int = 3) -> dict:
    durumlar = [(k, t) for k in range(en_cok + 1) for t in range(en_cok + 1)]
    V = {d: 0.0 for d in durumlar}
    for _ in range(500):
        V = {d: max(odul(*d, e, gecis(*d, e), odul_turu) + gamma * V[gecis(*d, e)[:2]] for e in EYLEMLER)
             for d in durumlar}
    return {d: max(EYLEMLER, key=lambda e: odul(*d, e, gecis(*d, e), odul_turu) + gamma * V[gecis(*d, e)[:2]])
            for d in durumlar}


def calistir(politika: dict, kir: int = 3, adim: int = 12) -> list[str]:
    torba, iz = 0, []
    for _ in range(adim):
        e = politika[(kir, torba)]
        kir, torba, _ = gecis(kir, torba, e)
        iz.append(e)
    return iz


# --- Sormanın değeri ---------------------------------------------------------------------------------
def sor_ya_da_uygula(p: float, iyi: float = 10.0, felaket: float = -100.0, soru_maliyeti: float = 1.0,
                     insan_dogrulugu: float = 1.0) -> dict:
    """Plan p olasılıkla insanın istediği şeydir. İnsan sorulunca (insan_dogrulugu olasılıkla) doğru yanıt verir;
    yanlışlıkla felaket bir plana izin verebilir ya da iyi bir planı reddedebilir."""
    q = insan_dogrulugu
    uygula = p * iyi + (1 - p) * felaket
    sor = -soru_maliyeti + p * q * iyi + (1 - p) * (1 - q) * felaket
    return {"uygula": uygula, "sor": sor, "hiçbir şey yapma": 0.0}


# --- Tekillik hesabı ------------------------------------------------------------------------------------
def tekillik_hizi(yil1: int = 1993, kalan1: int = 30, yil2: int = 2017, hedef2: int = 2045) -> float:
    """Vinge 1993'te "30 yıl içinde"; Kurzweil 2017'de "2045". Bu yaklaşma hızıyla kalan süre."""
    kalan2 = hedef2 - yil2
    yaklasma = kalan1 - kalan2                      # 24 yılda kaç yıl yaklaştı
    return kalan2 / (yaklasma / (yil2 - yil1))


def s_egrisi_ve_ustel(t_gozlem: float = 10.0, t_tahmin: float = 30.0) -> tuple[float, float]:
    """Lojistik büyüme L/(1 + e^(−k(t − t0))) ilk dönemde üstel görünür. İlk 10 yıla üstel uydur, 30. yılı tahmin et."""
    L, k, t0 = 1000.0, 0.5, 15.0
    f = lambda t: L / (1 + np.exp(-k * (t - t0)))  # noqa: E731
    t = np.linspace(0, t_gozlem, 50)
    a, b = np.polyfit(t, np.log(f(t)), 1)
    return float(np.exp(b + a * t_tahmin)), float(f(t_tahmin))


def main() -> None:
    print("=== Hata ağacı analizi ===")
    for yedek in (True, False):
        print(f"  Yedek bilgisayar {'var ' if yedek else 'yok '}: P(araç denetimi kaybeder) = {olasilik(arac_agaci(yedek)):.2e}")

    print("\n=== Düşük etki: kahveyi getir (V vazo, K mama kabı, C saksı) ===")
    for lam in (0, 1, 5):
        yol, adim, bozuk = dusuk_etkili_yol(lam)
        print(f"  λ = {lam}: {adim} adım, değiştirilen nesneler {bozuk or 'yok'}")
    print("  Robot vazonun kırılacağını bilmez; yalnızca 'dünyayı gereksiz değiştirme' cezası onu dolaştırır.")

    print("\n=== Şartname oyunu: temizlik robotu (3 birim kirli oda, 3 birimlik torba) ===")
    for tur in ("temizlenen kir başına +1", "kalan kir başına −1"):
        iz = calistir(en_iyi_politika(tur))
        print(f"  Ödül '{tur}': {' '.join(iz)}")
    print("  Birinci ödülle en iyi politika kiri döküp yeniden temizlemek: istediğimizi değil, istediğimiz şeyi ölçen")
    print("  sayıyı en büyütür (Kral Midas sorunu).")

    print("\n=== Sor mu, uygula mı? (iyi plan +10, felaket −100, soru maliyeti 1) ===")
    for p in (0.5, 0.9, 0.98, 0.999):
        r = sor_ya_da_uygula(p)
        r2 = sor_ya_da_uygula(p, insan_dogrulugu=0.95)
        print(f"  P(plan doğru) = {p:<5}: uygula {r['uygula']:7.2f}, sor {r['sor']:6.2f} → {max(r, key=r.get):<16}"
              f"| insan %95 doğru: sor {r2['sor']:6.2f} → {max(r2, key=r2.get)}")

    print("\n=== Tekillik kestirimleri ===")
    print(f"  1993'te 30 yıl, 2017'de 28 yıl kaldı denmiş: Bu hızla kalan süre {tekillik_hizi():.0f} yıl")
    ust, ger = s_egrisi_ve_ustel()
    sayi = lambda v: f"{v:,.0f}".replace(",", " ")  # noqa: E731
    print(f"  S eğrisinin ilk 10 yılına uydurulan üstel, 30. yıl için {sayi(ust)} tahmin ediyor; gerçek değer {sayi(ger)}")


if __name__ == "__main__":
    main()
