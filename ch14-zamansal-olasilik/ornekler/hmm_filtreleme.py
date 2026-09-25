#!/usr/bin/env python3
"""Küçük HMM: hava / şemsiye — forward filtreleme.

Gizli durum: Yağmur (T/F)
Gözlem:     Şemsiye (T/F) — komşunun şemsiye taşıması

Her adımda: predict (geçiş) → update (duyucu) → normalleştir.
Resmi referans: https://aima.cs.berkeley.edu/ · https://github.com/aimacode
"""
from __future__ import annotations

from typing import Dict, List, Tuple

# Durum indeksi: 0 = Yağmur=F (güneş), 1 = Yağmur=T
DURUMLAR = ("Gunes", "Yagmur")

# P(Yağmur_0=T)
P0_YAGMUR = 0.5

# Geçiş: P(X_t | X_{t-1})  satır = önceki, sütun = şimdi  [Gunes, Yagmur]
# Önceki Gunes → şimdi Gunes 0.7, Yagmur 0.3
# Önceki Yagmur → şimdi Gunes 0.3, Yagmur 0.7
GECIS = [
    [0.7, 0.3],  # önceki Gunes
    [0.3, 0.7],  # önceki Yagmur
]

# Duyucu: P(Şemsiye=T | X)
# Gunes iken şemsiye olasılığı düşük; yağmurda yüksek
P_SEMSIYE_VER_DURUM = [0.2, 0.9]  # [Gunes, Yagmur]


def normalestir(v: List[float]) -> List[float]:
    s = sum(v)
    if s == 0:
        raise ZeroDivisionError("sonsaldan sıfır kütle")
    return [x / s for x in v]


def baslangic() -> List[float]:
    """P(X_0) — yağmur önseli."""
    return normalestir([1.0 - P0_YAGMUR, P0_YAGMUR])


def predict(oncesel: List[float]) -> List[float]:
    """P(X_t | e_{1:t-1}) = Σ P(X_t | x) P(x | e)."""
    n = len(oncesel)
    sonuc = [0.0] * n
    for onceki in range(n):
        for simdi in range(n):
            sonuc[simdi] += GECIS[onceki][simdi] * oncesel[onceki]
    return sonuc


def update(inanc: List[float], semsiye: bool) -> List[float]:
    """P(X_t | e_{1:t}) ∝ P(e_t | X_t) P(X_t | e_{1:t-1})."""
    sonuc = []
    for i, p in enumerate(inanc):
        p_e = P_SEMSIYE_VER_DURUM[i] if semsiye else (1.0 - P_SEMSIYE_VER_DURUM[i])
        sonuc.append(p_e * p)
    return normalestir(sonuc)


def filtrele(gozlemler: List[bool]) -> List[List[float]]:
    """Her adım sonrası P(Yağmur=T | e_{1:t}) için sonsal vektörleri döndür."""
    bellek: List[List[float]] = []
    inanc = baslangic()
    # t=0 öncesi: yalnızca önsel (gözlemsiz)
    bellek.append(list(inanc))
    for e in gozlemler:
        inanc = predict(inanc)
        inanc = update(inanc, e)
        bellek.append(list(inanc))
    return bellek


def fmt_bool(b: bool) -> str:
    return "T" if b else "F"


def yazdir_model() -> None:
    print("HMM — hava / şemsiye (özgün eğitim)\n")
    print("Durumlar:", ", ".join(DURUMLAR))
    print(f"P0(Yagmur=T) = {P0_YAGMUR}")
    print("Geçiş P(şimdi | önceki):")
    print(f"  önceki Gunes → Gunes={GECIS[0][0]}, Yagmur={GECIS[0][1]}")
    print(f"  önceki Yagmur → Gunes={GECIS[1][0]}, Yagmur={GECIS[1][1]}")
    print(
        f"Duyucu P(Şemsiye=T | durum): Gunes={P_SEMSIYE_VER_DURUM[0]}, "
        f"Yagmur={P_SEMSIYE_VER_DURUM[1]}"
    )
    print()


def main() -> None:
    yazdir_model()

    # Gözlem dizisi: komşu şemsiye taşıdı mı? (T/F)
    gozlemler = [True, True, False, True, True]
    print("Gözlem dizisi (Şemsiye):", [fmt_bool(g) for g in gozlemler])
    print()

    sonsallar = filtrele(gozlemler)
    print("t | Şemsiye | P(Yagmur=T | e_1:t)")
    print("--+---------+---------------------")
    print(f"0 |    —    | {sonsallar[0][1]:.4f}  (önsel)")
    for t, e in enumerate(gozlemler, start=1):
        p_y = sonsallar[t][1]
        print(f"{t} |    {fmt_bool(e)}    | {p_y:.4f}")

    print()
    print("Sezgi: peş peşe şemsiye → yağmur inancı yükselir; şemsiyesiz gün düşürür.")
    print("Bu forward filtrelemedir (çevrimiçi). Yumuşatma için geleceğe de bakılır.")


if __name__ == "__main__":
    main()
