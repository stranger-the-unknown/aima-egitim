#!/usr/bin/env python3
"""Sudoku bir CSP olarak: kısıt yayılımı ne kadarını tek başına çözer?

81 değişken (kareler), alan {1..9}. Her satır, sütun ve 3×3 kutu bir Alldiff kısıtıdır;
burada her Alldiff, ikili "≠" kısıtlarına açılır (her karenin 20 "akranı" var).

Kitaptaki gözlem: "Kolay" Sudokular yalnızca AC-3 ile çözülür, arama gerekmez.
Zor olanlarda AC-3 alanları daraltır ama bitiremez; geri izleme (MRV + MAC) devreye girer.

Çalıştırma:
    python sudoku_csp.py
    python sudoku_csp.py --bulmaca "53..7....6..195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79"
"""
from __future__ import annotations

import argparse
import time

from kisit import CSP, ac3, geri_izleme

KOLAY = "..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3.."
ZOR = "8..........36......7..9.2...5...7.......457.....1...3...1....68..85...1..9....4.."

KARELER = [(r, c) for r in range(9) for c in range(9)]


def akranlar(kare) -> list:
    r, c = kare
    kutu = {(r // 3 * 3 + i, c // 3 * 3 + j) for i in range(3) for j in range(3)}
    ayni = {(r, k) for k in range(9)} | {(k, c) for k in range(9)} | kutu
    return sorted(ayni - {kare})


def sudoku(bulmaca: str) -> CSP:
    bulmaca = bulmaca.replace("0", ".")
    assert len(bulmaca) == 81, "bulmaca 81 karakter olmalı"
    alanlar = {k: [int(ch)] if ch != "." else list(range(1, 10)) for k, ch in zip(KARELER, bulmaca)}
    return CSP(KARELER, alanlar, {k: akranlar(k) for k in KARELER})


def tahta(atama: dict) -> str:
    satirlar = []
    for r in range(9):
        if r in (3, 6):
            satirlar.append("  ------+-------+------")
        parca = []
        for c in range(9):
            if c in (3, 6):
                parca.append("|")
            v = atama.get((r, c))
            parca.append(str(v) if v else ".")
        satirlar.append("  " + " ".join(parca))
    return "\n".join(satirlar)


def coz(bulmaca: str) -> dict:
    """AC-3'ün kendi başına ne yaptığını ve gerekirse aramayı raporla."""
    csp = sudoku(bulmaca)
    bos = sum(len(d) > 1 for d in csp.alanlar.values())
    t0 = time.perf_counter()
    tutarli, alanlar = ac3(csp)
    kalan = sum(len(d) > 1 for d in alanlar.values())
    sonuc = {"bos": bos, "ac3_sonrasi_bos": kalan, "tutarli": tutarli,
             "aday_once": sum(len(d) for d in csp.alanlar.values()),
             "aday_sonra": sum(len(d) for d in alanlar.values())}
    if tutarli and kalan == 0:
        sonuc["cozum"] = {k: d[0] for k, d in alanlar.items()}
        sonuc["atama"] = 0
    elif tutarli:
        csp.alanlar = alanlar  # AC-3'ün daralttığı alanlarla aramaya başla
        c, ist = geri_izleme(csp, "mrv", "sirali", "mac")
        sonuc["cozum"] = c[0] if c else None
        sonuc["atama"] = ist.atama
        sonuc["geri_donus"] = ist.geri_donus
    sonuc["sure"] = time.perf_counter() - t0
    return sonuc


def main() -> None:
    ap = argparse.ArgumentParser(description="Sudoku CSP")
    ap.add_argument("--bulmaca", default=None, help="81 karakter; boş kare için . ya da 0")
    args = ap.parse_args()
    bulmacalar = [("özel", args.bulmaca)] if args.bulmaca else [("kolay", KOLAY), ("zor", ZOR)]
    for ad, b in bulmacalar:
        s = coz(b)
        print(f"=== {ad} bulmaca ===")
        print(tahta({k: int(ch) for k, ch in zip(KARELER, b.replace('0', '.')) if ch != '.'}))
        print(f"\n  Boş kare: {s['bos']} → yalnızca AC-3 sonrası belirsiz kalan: {s['ac3_sonrasi_bos']}")
        print(f"  Toplam aday değer: {s['aday_once']} → AC-3 sonrası {s['aday_sonra']}")
        if s["atama"] == 0:
            print("  AC-3 bulmacayı TEK BAŞINA çözdü; hiç arama gerekmedi.")
        else:
            print(f"  Arama gerekti (MRV + MAC): {s['atama']} atama, {s['geri_donus']} geri dönüş.")
        print(f"  Süre: {s['sure']:.2f} sn\n")
        print(tahta(s["cozum"]))
        print()


if __name__ == "__main__":
    main()
