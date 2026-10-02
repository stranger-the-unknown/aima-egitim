#!/usr/bin/env python3
"""Zihinsel nesneler ve modal mantık: olası dünyalarla "bilmek".

K_A P ("A, P'yi bilir"), ancak ve ancak P, A'nın o dünyadan ERİŞEBİLDİĞİ (A'nın
bildikleriyle tutarlı) her dünyada doğruysa doğrudur.

Kitaptaki örnekler:
  1. Göndergesel geçirimsizlik: Süpermen = Clark olsa bile Lois, "Clark uçabilir"i bilmez.
     Çünkü Lois'in erişebildiği bir dünyada Süpermen ile Clark farklı kişilerdir.
  2. İç içe bilgi: Lois, Clark'ın kimliğini bildiğini bilir:
       K_Lois[K_Clark Kimlik ∨ K_Clark ¬Kimlik]
  3. "Bond birinin casus olduğunu biliyor" iki anlama gelir:
       ∃x K_Bond Casus(x)   (belirli birini biliyor; de re)
       K_Bond ∃x Casus(x)   (casus olduğunu biliyor, kim olduğunu değil; de dicto)
  4. Bilmek doğruluğu gerektirir (K_A P ⇒ P) ancak erişim yansımalıysa. İnanmak (B) için
     bu geçerli değildir: yanlış bir şeye inanılabilir.

Çalıştırma:
    python modal_bilgi.py
"""
from __future__ import annotations

from typing import Callable

# ---------------------------------------------------------------------------
# Süpermen / Clark
# ---------------------------------------------------------------------------

# Her dünya: Süpermen ve Clark hangi kişiye gönderme yapıyor, kim uçabiliyor?
DUNYALAR = {
    "w0 (gerçek)": {"Süpermen": "Kal-El", "Clark": "Kal-El", "uçar": {"Kal-El"}},
    "w1": {"Süpermen": "Kal-El", "Clark": "SıradanAdam", "uçar": {"Kal-El"}},
}
# Erişim: A'nın w'deki bilgisiyle tutarlı dünyalar
ERISIM = {
    "Lois": {"w0 (gerçek)": {"w0 (gerçek)", "w1"}, "w1": {"w0 (gerçek)", "w1"}},
    "Clark": {"w0 (gerçek)": {"w0 (gerçek)"}, "w1": {"w1"}},  # Clark kendi kimliğini bilir
}

Cumle = Callable[[str], bool]


def K(ajan: str, p: Cumle) -> Cumle:
    """K_ajan p: p, erişilebilir her dünyada doğru."""
    return lambda w: all(p(v) for v in ERISIM[ajan][w])


def ucar(ad: str) -> Cumle:
    return lambda w: DUNYALAR[w][ad] in DUNYALAR[w]["uçar"]


def ayni_kisi(a: str, b: str) -> Cumle:
    return lambda w: DUNYALAR[w][a] == DUNYALAR[w][b]


def degil(p: Cumle) -> Cumle:
    return lambda w: not p(w)


def veya(p: Cumle, q: Cumle) -> Cumle:
    return lambda w: p(w) or q(w)


# ---------------------------------------------------------------------------
# Bond ve casus
# ---------------------------------------------------------------------------

KISILER = ["Ahmet", "Burak", "Cem"]
BOND_DUNYALARI = {"wa": {"Ahmet"}, "wb": {"Burak"}}  # her dünyada farklı biri casus
BOND_ERISIM = {"wa": {"wa", "wb"}, "wb": {"wa", "wb"}}


def de_re(w: str) -> bool:  # ∃x K_Bond Casus(x)
    return any(all(x in BOND_DUNYALARI[v] for v in BOND_ERISIM[w]) for x in KISILER)


def de_dicto(w: str) -> bool:  # K_Bond ∃x Casus(x)
    return all(any(x in BOND_DUNYALARI[v] for x in KISILER) for v in BOND_ERISIM[w])


# ---------------------------------------------------------------------------
# Bilmek ve inanmak
# ---------------------------------------------------------------------------

INANC_DUNYALARI = {"g (gerçek)": {"yağmur": False}, "h": {"yağmur": True}}
INANC_ERISIM = {"g (gerçek)": {"h"}, "h": {"h"}}  # yansımalı değil: ajan gerçek dünyayı dışlıyor


def main() -> None:
    w0 = "w0 (gerçek)"
    print("=== Süpermen ve Clark (gerçek dünyada Süpermen = Clark) ===")
    satirlar = [
        ("Süpermen = Clark", ayni_kisi("Süpermen", "Clark")),
        ("K_Lois Uçar(Süpermen)", K("Lois", ucar("Süpermen"))),
        ("K_Lois Uçar(Clark)", K("Lois", ucar("Clark"))),
        ("K_Lois (Süpermen = Clark)", K("Lois", ayni_kisi("Süpermen", "Clark"))),
        ("K_Clark (Süpermen = Clark)", K("Clark", ayni_kisi("Süpermen", "Clark"))),
        ("K_Lois[K_Clark Kimlik ∨ K_Clark ¬Kimlik]",
         K("Lois", veya(K("Clark", ayni_kisi("Süpermen", "Clark")),
                        K("Clark", degil(ayni_kisi("Süpermen", "Clark")))))),
    ]
    for metin, c in satirlar:
        print(f"  {metin:<44} → {c(w0)}")
    print("  Birinci derece mantıkta Süpermen = Clark ve Bilir(Lois, Uçar(Süpermen)) birlikte"
          "\n  Bilir(Lois, Uçar(Clark))'ı gerektirirdi (göndergesel saydamlık). Modal mantık"
          "\n  bunu engeller: Lois, Clark'ın başka biri olduğu w1 dünyasını da olası sayıyor.")

    print("\n=== 'Bond birinin casus olduğunu biliyor' ===")
    print(f"  ∃x K_Bond Casus(x)   (de re: belirli birini biliyor) → {de_re('wa')}")
    print(f"  K_Bond ∃x Casus(x)   (de dicto: bir casus olduğunu biliyor) → {de_dicto('wa')}")

    print("\n=== Bilmek ve inanmak ===")
    inanir = all(INANC_DUNYALARI[v]["yağmur"] for v in INANC_ERISIM["g (gerçek)"])
    gercek = INANC_DUNYALARI["g (gerçek)"]["yağmur"]
    print(f"  B_Ajan Yağmur = {inanir}, ama gerçekte Yağmur = {gercek}")
    print("  Erişim yansımalı olmadığı için (ajan gerçek dünyayı olası saymıyor) yanlış bir inanç"
          "\n  mümkün. 'Bilmek' için erişim yansımalı kabul edilir; böylece K_A P ⇒ P geçerli olur.")


if __name__ == "__main__":
    main()
