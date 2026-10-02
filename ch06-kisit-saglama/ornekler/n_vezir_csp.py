#!/usr/bin/env python3
"""N-vezir bir CSP olarak: sezgiseller ve çıkarım ne kadar fark eder?

Değişken: her sütun (0..n−1). Alan: vezirin satırı (0..n−1).
Kısıt (her sütun çifti için): farklı satır ve farklı çapraz.

Bölüm 4'teki tepe tırmanmanın aksine geri izleme **sistematiktir**: çözüm varsa
bulur, yoksa (n = 2, 3) bunu kanıtlar. Maliyeti ise sezgisellere çok bağlıdır.

Çalıştırma:
    python n_vezir_csp.py            # n = 8 çözümü + karşılaştırma tablosu
    python n_vezir_csp.py --n 12
"""
from __future__ import annotations

import argparse

from kisit import CSP, geri_izleme


def vezir_kisiti(c1, r1, c2, r2) -> bool:
    return r1 != r2 and abs(r1 - r2) != abs(c1 - c2)


def n_vezir(n: int) -> CSP:
    sutunlar = list(range(n))
    return CSP(sutunlar, {c: list(range(n)) for c in sutunlar},
               {c: [d for d in sutunlar if d != c] for c in sutunlar}, vezir_kisiti)


AYARLAR = [
    ("sirali", "sirali", "yok"),
    ("sirali", "sirali", "ileri"),
    ("mrv", "sirali", "ileri"),
    ("mrv", "lcv", "mac"),
]


def tahta(cozum: dict, n: int) -> str:
    return "\n".join("  " + " ".join("♛" if cozum[c] == r else "·" for c in range(n)) for r in range(n))


def main() -> None:
    ap = argparse.ArgumentParser(description="N-vezir CSP")
    ap.add_argument("--n", type=int, default=8)
    args = ap.parse_args()

    c, ist = geri_izleme(n_vezir(args.n), "mrv", "sirali", "ileri")
    if not c:
        print(f"{args.n}-vezir için çözüm yok (geri izleme bunu kanıtladı).")
    else:
        print(f"{args.n}-vezir çözümü (MRV + ileri kontrol, {ist.atama} atama):")
        print(tahta(c[0], args.n))

    print("\nİlk çözüme kadar yapılan atama sayısı:")
    print(f"{'n':>4}" + "".join(f"{'/'.join(a):>24}" for a in AYARLAR))
    for n in (4, 8, 12, 16, 20):
        satir = f"{n:>4}"
        for ayar in AYARLAR:
            _, ist = geri_izleme(n_vezir(n), *ayar)
            satir += f"{ist.atama:>24,}"
        print(satir)
    print("\nİleri kontrol tek başına işi yaklaşık %25 azaltır. Asıl sıçrama MRV ile gelir: 'en az"
          "\nseçeneği kalan sütunu önce ele al' kuralı, n = 20'de iki yüz binden fazla atamayı"
          "\nyüzlere indirir. LCV + MAC çoğu zaman daha da iyidir ama her zaman değil (n = 16):"
          "\nsezgiseller ortalamada iyidir, her örnekte değil.")


if __name__ == "__main__":
    main()
