#!/usr/bin/env python3
"""Alıştırma 7, 8, 9, 10 çözümleri."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ornekler"))

import prolog_yol as py  # noqa: E402
import suclu_bati as sb  # noqa: E402
from fol_cikarim import (birlestir, cozumleme, degiskenler, geri_zincirleme,  # noqa: E402
                         ileri_zincirleme, tamamla, terim, tumce, tumce_yaz, yaz,
                         yerine_koy, yerine_yaz, _kural_ayir, _eslestir)

A7 = [
    ("P(x, f(x))", "P(f(y), y)"),
    ("Q(x, y, z)", "Q(y, z, A)"),
    ("R(g(x), x)", "R(y, h(y))"),
    ("Knows(x, Mother(x))", "Knows(John, y)"),
]


def a8():
    kurallar = sb.KURALLAR + [
        sb.k(["Rocket(x)"], "Weapon(x)"),
        sb.k(["Rocket(x)", "Owns(Nopo, x)"], "Sells(Smith, x, Nopo)"),
    ]
    olgular = sb.OLGULAR + [terim(f) for f in
                            ["Enemy(Nopo, America)", "Owns(Nopo, R1)", "Rocket(R1)", "American(Smith)"]]
    _, turlar = ileri_zincirleme(kurallar, olgular)
    sucular_fc = sorted(yaz(f[1]) for tur in turlar for f in tur if f[0] == "Criminal")
    sucular_bc = [yaz(tamamla(t)["x"]) for t in geri_zincirleme(kurallar, olgular, terim("Criminal(x)"))]
    return len(turlar), sucular_fc, sucular_bc


# A9: Marcus örneği (CNF)
MARCUS = [
    "Insan(Marcus)",
    "Pompeili(Marcus)",
    "~Pompeili(x) | Romali(x)",
    "Hukumdar(Sezar)",
    "~Romali(x) | Sadik(x, Sezar) | Nefret(x, Sezar)",
    "~Insan(x) | ~Hukumdar(y) | ~Suikast(x, y) | ~Sadik(x, y)",
    "Suikast(Marcus, Sezar)",
]


def a9():
    return cozumleme([tumce(t) for t in MARCUS], [tumce("~Nefret(Marcus, Sezar)")])


# A10: tablolama
def _kanonik(atom) -> str:
    """Değişken adlarından bağımsız biçim: yol(A, x_3) → yol(A, _0)."""
    ad = {}
    for v in sorted(degiskenler(atom), key=lambda v: yaz(atom).index(v)):
        ad[v] = f"_{len(ad)}"
    return yaz(yerine_koy(ad, atom))


def tablolu_sor(kurallar, olgular, sorgu):
    """Basit tablolama: tablo[alt hedef] = yanıt kümesi; sabit noktaya kadar yinele."""
    tablo = {_kanonik(sorgu): (sorgu, set())}
    degisti = True
    while degisti:
        degisti = False
        for anahtar, (hedef, yanitlar) in list(tablo.items()):
            yeni = set()
            for f in olgular:
                if birlestir(hedef, f) is not None:
                    yeni.add(yaz(f))
            for oncul, sonuc in kurallar:
                oncul, sonuc = _kural_ayir(oncul, sonuc)
                teta = birlestir(sonuc, hedef)
                if teta is None:
                    continue
                # Her öncül için: olgulardan ya da (tablodaki) alt hedef yanıtlarından eşleş
                cozulen = [terim(y) for _, (_, ys) in tablo.items() for y in ys]
                for alt in oncul:
                    k = _kanonik(yerine_koy(teta, alt))
                    if k not in tablo and alt[0] == hedef[0]:
                        tablo[k] = (yerine_koy(teta, alt), set())
                        degisti = True
                for t2 in _eslestir([yerine_koy(teta, o) for o in oncul], olgular + cozulen, dict(teta)):
                    yeni.add(yaz(yerine_koy(t2, sonuc)))
            yeni = {y for y in yeni if birlestir(hedef, terim(y)) is not None}
            if not yeni <= yanitlar:
                yanitlar |= yeni
                degisti = True
    return tablo


def main() -> None:
    print("=== A7: zor birleştirmeler ===")
    for a, b in A7:
        print(f"  UNIFY({a}, {b}) = {yerine_yaz(birlestir(terim(a), terim(b)))}")

    turlar, fc, bc = a8()
    print(f"\n=== A8: genişletilmiş suç KB'si ===\n  İleri zincirleme {turlar} turda bitti; suçlular: {fc}")
    print(f"  Geri zincirleme yanıt sırası: {bc}")

    bulundu, adimlar = a9()
    print(f"\n=== A9: Marcus, Sezar'dan nefret ediyordu ===\n  Kanıtlandı mı? {bulundu} ({len(adimlar)} adım)")
    for a, b, r, _ in adimlar:
        print(f"    ({tumce_yaz(a)}) + ({tumce_yaz(b)}) → {tumce_yaz(r)}")

    print("\n=== A10: tablolama ile (b) programı ===")
    tablo = tablolu_sor([py.OZYINELI, py.TABAN], py.OLGULAR, terim("yol(A, q)"))
    for anahtar, (_, yanitlar) in tablo.items():
        print(f"  tablo[{anahtar}] = {sorted(yanitlar)}")


if __name__ == "__main__":
    main()
