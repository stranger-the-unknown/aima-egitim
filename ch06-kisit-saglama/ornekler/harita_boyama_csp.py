#!/usr/bin/env python3
"""Türkiye'nin 7 coğrafi bölgesini boyamak: 3 renk yeter mi?

Komşuluklar il sınırlarına göredir. İki bölge, en az bir ilinin sınırı ortaksa komşudur:
    Marmara     – Ege, İç Anadolu, Karadeniz
    Ege         – Marmara, İç Anadolu, Akdeniz
    Akdeniz     – Ege, İç Anadolu, Güneydoğu, Doğu Anadolu (Kahramanmaraş–Malatya)
    İç Anadolu  – Marmara, Ege, Akdeniz, Karadeniz, Doğu Anadolu
    Karadeniz   – Marmara, İç Anadolu, Doğu Anadolu
    Doğu Anadolu– İç Anadolu, Karadeniz, Akdeniz, Güneydoğu
    Güneydoğu   – Akdeniz, Doğu Anadolu   (İç Anadolu ile ortak sınırı YOKTUR)

Sonuç: Bu harita **3 renkle boyanamaz**, 4 renk gerekir. Geri izleme araması bunu
tüm olasılıkları dolaşarak kanıtlar. (Dört renk teoremi: düzlemdeki her harita 4 renkle
boyanabilir; bu harita o sınırın tam üstünde.)

Çalıştırma:
    python harita_boyama_csp.py                  # 3 renk (başarısız) ve 4 renk
    python harita_boyama_csp.py --renk 4 --mrv --forward
    python harita_boyama_csp.py --karsilastir    # sezgisellerin maliyeti
"""
from __future__ import annotations

import argparse

from kisit import CSP, geri_izleme

BOLGELER = ["Marmara", "Ege", "Akdeniz", "IcAnadolu", "Karadeniz", "Doguanadolu", "Guneydogu"]
KOMSULUK = {
    "Marmara": ["Ege", "IcAnadolu", "Karadeniz"],
    "Ege": ["Marmara", "IcAnadolu", "Akdeniz"],
    "Akdeniz": ["Ege", "IcAnadolu", "Guneydogu", "Doguanadolu"],
    "IcAnadolu": ["Marmara", "Ege", "Akdeniz", "Karadeniz", "Doguanadolu"],
    "Karadeniz": ["Marmara", "IcAnadolu", "Doguanadolu"],
    "Doguanadolu": ["IcAnadolu", "Karadeniz", "Akdeniz", "Guneydogu"],
    "Guneydogu": ["Akdeniz", "Doguanadolu"],
}
RENKLER = ["Kirmizi", "Yesil", "Mavi", "Sari"]


def turkiye(renk_sayisi: int) -> CSP:
    return CSP(BOLGELER, {b: RENKLER[:renk_sayisi] for b in BOLGELER}, KOMSULUK)


def coz(renk_sayisi: int, mrv: bool = False, ileri: bool = False):
    return geri_izleme(turkiye(renk_sayisi), "mrv" if mrv else "sirali", "sirali",
                       "ileri" if ileri else "yok")


def main() -> None:
    ap = argparse.ArgumentParser(description="Türkiye bölgeleri harita boyama CSP")
    ap.add_argument("--renk", type=int, choices=[3, 4], default=None)
    ap.add_argument("--mrv", action="store_true", help="MRV (+ derece ile eşitlik bozma)")
    ap.add_argument("--forward", action="store_true", help="ileri kontrol")
    ap.add_argument("--karsilastir", action="store_true")
    args = ap.parse_args()

    if args.karsilastir:
        print(f"{'renk':>5}{'ayar':>22}{'atama':>8}{'geri dönüş':>12}   sonuç")
        for k in (3, 4):
            for mrv, ileri in ((False, False), (True, False), (False, True), (True, True)):
                c, ist = coz(k, mrv, ileri)
                ayar = ("MRV" if mrv else "sıralı") + (" + ileri" if ileri else "")
                print(f"{k:>5}{ayar:>22}{ist.atama:>8}{ist.geri_donus:>12}   {'çözüm' if c else 'yok'}")
        return

    for k in ([args.renk] if args.renk else [3, 4]):
        c, ist = coz(k, args.mrv, args.forward)
        print(f"=== {k} renk ===")
        if not c:
            print(f"  Çözüm YOK. Arama {ist.atama} atama deneyip {ist.geri_donus} kez geri döndü ve"
                  "\n  bütün olasılıkları tükenmiş buldu: 3 renk bu harita için yetersiz.")
        else:
            for b in BOLGELER:
                print(f"  {b:<12} → {c[0][b]}")
            print(f"  ({ist.atama} atama, {ist.geri_donus} geri dönüş)")
        print()
    print("Neden 3 renk yetmez? İç Anadolu, Akdeniz ve Doğu Anadolu karşılıklı komşudur: 1, 2, 3 renklerini"
          "\nalırlar. Güneydoğu (Akdeniz + D. Anadolu komşusu) 1'e, Karadeniz (İç Anadolu + D. Anadolu"
          "\nkomşusu) 2'ye, Marmara (İç Anadolu + Karadeniz komşusu) 3'e zorlanır. Ege ise Marmara (3),"
          "\nİç Anadolu (1) ve Akdeniz'e (2) komşudur: renk kalmaz.")


if __name__ == "__main__":
    main()
