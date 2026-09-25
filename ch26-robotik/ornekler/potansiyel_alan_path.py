#!/usr/bin/env python3
"""Çekim / itme potansiyel alanı ile ızgara yolu (toy).

Hedefe çekim + engellere itme; gradyan inişi ile hücre dizisi.
Yerel minimum riski kasıtlı olarak küçük örnekte görülebilir.
Özgün eğitim. Kitap metni yok. numpy OK.
https://aima.cs.berkeley.edu/ · https://github.com/aimacode
"""
from __future__ import annotations

from typing import List, Optional, Tuple

import numpy as np

# 0 boş, 1 engel
IZGARA = np.array(
    [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0, 1, 0],
        [0, 0, 0, 0, 1, 1, 0],
        [0, 0, 1, 0, 0, 0, 0],
        [0, 0, 1, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
    ],
    dtype=int,
)
BASLANGIC = (0, 0)
HEDEF = (5, 6)

K_ATTR = 1.0
K_REP = 8.0
D0 = 2.5          # itme etki yarıçapı (hücre)
ADIM_MAX = 80
EPS = 1e-6


def engeller() -> List[Tuple[int, int]]:
    ys, xs = np.where(IZGARA == 1)
    return list(zip(ys.tolist(), xs.tolist()))


def U_attr(y: int, x: int) -> float:
    gy, gx = HEDEF
    return 0.5 * K_ATTR * ((y - gy) ** 2 + (x - gx) ** 2)


def U_rep(y: int, x: int) -> float:
    u = 0.0
    for ey, ex in engeller():
        d = np.hypot(y - ey, x - ex)
        if d < EPS:
            return 1e6
        if d < D0:
            u += 0.5 * K_REP * (1.0 / d - 1.0 / D0) ** 2
    return u


def U(y: int, x: int) -> float:
    return U_attr(y, x) + U_rep(y, x)


def komsular(y: int, x: int) -> List[Tuple[int, int]]:
    aday = []
    for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)):
        yy, xx = y + dy, x + dx
        if 0 <= yy < IZGARA.shape[0] and 0 <= xx < IZGARA.shape[1] and IZGARA[yy, xx] == 0:
            aday.append((yy, xx))
    return aday


def gradyan_adim(y: int, x: int) -> Optional[Tuple[int, int]]:
    """En düşük potansiyelli komşuya git (eşitlikte hedefe daha yakın)."""
    eniyi = None
    en_u = U(y, x)
    gy, gx = HEDEF
    for yy, xx in komsular(y, x):
        u = U(yy, xx)
        daha_iyi = u < en_u - 1e-9
        esit_ama_yakin = abs(u - en_u) < 1e-9 and (
            eniyi is None
            or (yy - gy) ** 2 + (xx - gx) ** 2
            < (eniyi[0] - gy) ** 2 + (eniyi[1] - gx) ** 2
        )
        if daha_iyi or esit_ama_yakin:
            en_u = u
            eniyi = (yy, xx)
    return eniyi


def yol_bul() -> Tuple[List[Tuple[int, int]], str]:
    yol = [BASLANGIC]
    y, x = BASLANGIC
    for _ in range(ADIM_MAX):
        if (y, x) == HEDEF:
            return yol, "hedefe_ulasti"
        nxt = gradyan_adim(y, x)
        if nxt is None or nxt == (y, x):
            return yol, "yerel_minimum_veya_sikisma"
        if nxt in yol:
            return yol + [nxt], "dongu"
        yol.append(nxt)
        y, x = nxt
    return yol, "adim_limiti"


def yazdir_yol(yol: List[Tuple[int, int]]) -> None:
    g = np.array([["." if c == 0 else "#" for c in row] for row in IZGARA], dtype=object)
    for i, (y, x) in enumerate(yol):
        if g[y, x] == "#":
            continue
        g[y, x] = "*" if i not in (0, len(yol) - 1) else g[y, x]
    sy, sx = BASLANGIC
    gy, gx = HEDEF
    g[sy, sx] = "S"
    g[gy, gx] = "G"
    # yol üzerindeki ara noktalar
    for y, x in yol[1:-1]:
        if (y, x) != HEDEF:
            g[y, x] = "*"
    print("\n".join(" ".join(row) for row in g))


def potansiyel_ozet() -> None:
    print("Örnek potansiyel değerleri (köşe / engel yanı / hedef):")
    for nokta in [(0, 0), (1, 3), (2, 0), HEDEF]:
        print(f"  {nokta}: U={U(*nokta):.3f}  (attr={U_attr(*nokta):.3f}, rep={U_rep(*nokta):.3f})")


def main() -> None:
    print("Potansiyel alan yolu — çekim + itme (ızgara)")
    print(f"Başlangıç={BASLANGIC}, Hedef={HEDEF}, K_attr={K_ATTR}, K_rep={K_REP}, D0={D0}")
    potansiyel_ozet()
    yol, durum = yol_bul()
    print(f"\nDurum: {durum}, adım sayısı: {len(yol) - 1}")
    print("Yol:", " → ".join(str(p) for p in yol))
    print("\nHarita (S=start, G=goal, *=yol, #=engel):")
    yazdir_yol(yol)


if __name__ == "__main__":
    main()
