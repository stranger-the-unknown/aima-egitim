#!/usr/bin/env python3
"""Türkiye bölgeleri harita boyama — CSP backtracking (+ isteğe bağlı MRV).

Komşu bölgeler farklı renk almalı. Eğitim amaçlı; kitap metni kopyası değildir.
Resmi referans: https://aima.cs.berkeley.edu/ · https://github.com/aimacode
"""
from __future__ import annotations

import argparse
from typing import Dict, List, Optional, Tuple

# Basitleştirilmiş Türkiye coğrafi bölgeleri (7 bölge) ve komşuluklar.
BOLGELER = [
    "Marmara",
    "Ege",
    "Akdeniz",
    "IcAnadolu",
    "Karadeniz",
    "Doguanadolu",
    "Guneydogu",
]

KOMŞULUK: Dict[str, List[str]] = {
    "Marmara": ["Ege", "IcAnadolu", "Karadeniz"],
    "Ege": ["Marmara", "Akdeniz", "IcAnadolu"],
    "Akdeniz": ["Ege", "IcAnadolu", "Guneydogu"],
    "IcAnadolu": ["Marmara", "Ege", "Akdeniz", "Karadeniz", "Doguanadolu", "Guneydogu"],
    "Karadeniz": ["Marmara", "IcAnadolu", "Doguanadolu"],
    "Doguanadolu": ["Karadeniz", "IcAnadolu", "Guneydogu"],
    "Guneydogu": ["Akdeniz", "IcAnadolu", "Doguanadolu"],
}

RENKLER_VARSAYILAN = ["Kirmizi", "Yesil", "Mavi"]


def komşular_farkli(atama: Dict[str, str], degisken: str, deger: str) -> bool:
    """degisken=deger ataması mevcut atamayla komşuluk kısıtını bozar mı?"""
    for komsu in KOMŞULUK[degisken]:
        if komsu in atama and atama[komsu] == deger:
            return False
    return True


def sec_degisken(
    atanmamis: List[str],
    domainler: Dict[str, List[str]],
    atama: Dict[str, str],
    mrv: bool,
) -> str:
    """MRV: kalan domaini en küçük olan; beraberlikte derece (komşu sayısı)."""
    if not mrv:
        return atanmamis[0]

    def anahtar(v: str) -> Tuple[int, int]:
        kalan = len(domainler[v])
        # Atanmamış komşu sayısı = derece sezgiseli (tie-break)
        derece = sum(1 for k in KOMŞULUK[v] if k not in atama)
        return (kalan, -derece)

    return min(atanmamis, key=anahtar)


def ileri_kontrol(
    degisken: str,
    deger: str,
    atama: Dict[str, str],
    domainler: Dict[str, List[str]],
) -> Optional[Dict[str, List[str]]]:
    """Atama sonrası komşu domainlerinden deger'i sil. Boş domain → None."""
    yeni = {v: list(domainler[v]) for v in domainler}
    for komsu in KOMŞULUK[degisken]:
        if komsu in atama:
            continue
        if deger in yeni[komsu]:
            yeni[komsu] = [d for d in yeni[komsu] if d != deger]
            if not yeni[komsu]:
                return None
    return yeni


def backtrack(
    atama: Dict[str, str],
    domainler: Dict[str, List[str]],
    *,
    mrv: bool,
    forward: bool,
    sayac: Dict[str, int],
) -> Optional[Dict[str, str]]:
    sayac["adim"] += 1
    if len(atama) == len(BOLGELER):
        return dict(atama)

    atanmamis = [v for v in BOLGELER if v not in atama]
    var = sec_degisken(atanmamis, domainler, atama, mrv)

    for deger in list(domainler[var]):
        if not komşular_farkli(atama, var, deger):
            continue
        atama[var] = deger
        sayac["deneme"] += 1
        if forward:
            yeni_dom = ileri_kontrol(var, deger, atama, domainler)
            if yeni_dom is None:
                del atama[var]
                continue
            sonuc = backtrack(atama, yeni_dom, mrv=mrv, forward=forward, sayac=sayac)
        else:
            sonuc = backtrack(atama, domainler, mrv=mrv, forward=forward, sayac=sayac)
        if sonuc is not None:
            return sonuc
        del atama[var]
    return None


def coz(renkler: List[str], mrv: bool, forward: bool) -> Tuple[Optional[Dict[str, str]], Dict[str, int]]:
    domainler = {b: list(renkler) for b in BOLGELER}
    sayac = {"adim": 0, "deneme": 0}
    sonuc = backtrack({}, domainler, mrv=mrv, forward=forward, sayac=sayac)
    return sonuc, sayac


def yazdir_cozum(atama: Dict[str, str]) -> None:
    print("\n=== Harita boyama çözümü ===")
    genislik = max(len(b) for b in BOLGELER)
    for b in BOLGELER:
        print(f"  {b:<{genislik}} → {atama[b]}")
    # Kısıt doğrulama
    for b in BOLGELER:
        for k in KOMŞULUK[b]:
            if atama[b] == atama[k]:
                print(f"HATA: {b} ve {k} aynı renk!")
                return
    print("Tüm komşuluk kısıtları sağlandı.")


def main() -> None:
    p = argparse.ArgumentParser(description="Türkiye bölgeleri CSP harita boyama")
    p.add_argument("--mrv", action="store_true", help="MRV + derece tie-break kullan")
    p.add_argument(
        "--forward",
        action="store_true",
        help="İleriye kontrol (forward checking) aç",
    )
    p.add_argument(
        "--renkler",
        default=",".join(RENKLER_VARSAYILAN),
        help="Virgülle ayrılmış renk listesi (varsayılan 3 renk)",
    )
    p.add_argument(
        "--karsilastir",
        action="store_true",
        help="Düz BT vs MRV+FC deneme sayılarını karşılaştır",
    )
    args = p.parse_args()
    renkler = [r.strip() for r in args.renkler.split(",") if r.strip()]

    print("Türkiye coğrafi bölgeleri — harita boyama CSP")
    print(f"Değişkenler: {', '.join(BOLGELER)}")
    print(f"Domain: {renkler}")
    print(f"Kısıt: komşu bölgeler farklı renk\n")

    if args.karsilastir:
        for etiket, mrv, fwd in [
            ("Düz backtracking", False, False),
            ("MRV", True, False),
            ("MRV + ileriye kontrol", True, True),
        ]:
            sol, say = coz(renkler, mrv, fwd)
            durum = "çözüldü" if sol else "çözüm yok"
            print(f"  [{etiket}] {durum} — adım≈{say['adim']}, değer denemesi={say['deneme']}")
        print()
        # Son olarak en iyi ayarla göster
        args.mrv, args.forward = True, True

    sonuc, sayac = coz(renkler, args.mrv, args.forward)
    mod = []
    if args.mrv:
        mod.append("MRV")
    if args.forward:
        mod.append("ileriye-kontrol")
    print(f"Mod: {', '.join(mod) if mod else 'düz backtracking'}")
    print(f"İstatistik: adım≈{sayac['adim']}, değer denemesi={sayac['deneme']}")

    if sonuc is None:
        print("Çözüm bulunamadı (renk sayısı yetersiz olabilir).")
    else:
        yazdir_cozum(sonuc)


if __name__ == "__main__":
    main()
