#!/usr/bin/env python3
"""Ayrık Bayes filtresi: küçük 2D koridor lokalizasyonu + landmark.

Durum = ızgara hücresi. Hareket: sağa/sola/yukarı/aşağı (gürültülü).
Gözlem: hücredeki landmark kimliği (veya "yok"); duyucu gürültülü.
Özgün eğitim. Kitap metni yok. numpy OK.
https://aima.cs.berkeley.edu/ · https://github.com/aimacode
"""
from __future__ import annotations

from typing import Dict, List, Optional, Tuple

import numpy as np

# 1×5 koridor + yan hücrelerle minik 3×5 ızgara
# '#' duvar (geçilmez), '.' boş, harf = landmark
HARITA = [
    "#####",
    "#.A.#",
    "#...#",
    "#.B.#",
    "#####",
]
H = len(HARITA)
W = len(HARITA[0])

# Hareket: (dy, dx) — satır, sütun
HAREKETLER = {
    "sag": (0, 1),
    "sol": (0, -1),
    "asagi": (1, 0),
    "yukari": (-1, 0),
}

P_BASARILI_HAREKET = 0.80  # istenen yöne
P_KAL = 0.10               # yerinde kal
P_YANLIS = 0.10            # rastgele diğer yön (eşit bölünür)

P_DOGRu_GOZLEM = 0.85      # doğru landmark / boş okuma
# kalan kütle yanlış etiketlere dağılır


def serbest_mi(y: int, x: int) -> bool:
    return 0 <= y < H and 0 <= x < W and HARITA[y][x] != "#"


def landmark(y: int, x: int) -> Optional[str]:
    c = HARITA[y][x]
    if c.isalpha():
        return c
    return None


def tum_serbest() -> List[Tuple[int, int]]:
    return [(y, x) for y in range(H) for x in range(W) if serbest_mi(y, x)]


def uniform_inanc() -> np.ndarray:
    bel = np.zeros((H, W), dtype=float)
    hucreler = tum_serbest()
    p = 1.0 / len(hucreler)
    for y, x in hucreler:
        bel[y, x] = p
    return bel


def predict(bel: np.ndarray, komut: str) -> np.ndarray:
    """Hareket modeli: istenen yön / kal / diğer."""
    yeni = np.zeros_like(bel)
    dy0, dx0 = HAREKETLER[komut]
    diger = [k for k in HAREKETLER if k != komut]
    p_diger = P_YANLIS / len(diger)

    for y, x in tum_serbest():
        if bel[y, x] == 0:
            continue
        # başarılı
        yy, xx = y + dy0, x + dx0
        if serbest_mi(yy, xx):
            yeni[yy, xx] += P_BASARILI_HAREKET * bel[y, x]
        else:
            yeni[y, x] += P_BASARILI_HAREKET * bel[y, x]  # duvara çarp → kal
        # kal
        yeni[y, x] += P_KAL * bel[y, x]
        # yanlış yönler
        for k in diger:
            dy, dx = HAREKETLER[k]
            yy, xx = y + dy, x + dx
            if serbest_mi(yy, xx):
                yeni[yy, xx] += p_diger * bel[y, x]
            else:
                yeni[y, x] += p_diger * bel[y, x]
    s = yeni.sum()
    return yeni / s if s > 0 else yeni


def olasi_gozlemler() -> List[str]:
    etiketler = sorted({landmark(y, x) for y, x in tum_serbest() if landmark(y, x)})
    return etiketler + ["yok"]


def sensor_olasiligi(y: int, x: int, gozlem: str) -> float:
    gercek = landmark(y, x)
    gercek_etiket = gercek if gercek else "yok"
    tum = olasi_gozlemler()
    if gozlem == gercek_etiket:
        return P_DOGRu_GOZLEM
    yanlislar = [g for g in tum if g != gercek_etiket]
    return (1.0 - P_DOGRu_GOZLEM) / len(yanlislar)


def update(bel: np.ndarray, gozlem: str) -> np.ndarray:
    yeni = np.zeros_like(bel)
    for y, x in tum_serbest():
        yeni[y, x] = bel[y, x] * sensor_olasiligi(y, x, gozlem)
    s = yeni.sum()
    return yeni / s if s > 0 else yeni


def yazdir_bel(bel: np.ndarray, baslik: str) -> None:
    print(f"\n=== {baslik} ===")
    for y in range(H):
        satir = []
        for x in range(W):
            if not serbest_mi(y, x):
                satir.append(" ## ")
            else:
                satir.append(f"{bel[y, x]:4.2f}")
        print(" ".join(satir))
    yx = np.unravel_index(int(np.argmax(bel)), bel.shape)
    print(f"MAP hücre: ({yx[0]}, {yx[1]})  P={bel[yx]:.3f}  harita='{HARITA[yx[0]][yx[1]]}'")


def simulasyon() -> None:
    # Gerçek yol: (1,1) → sağ → (1,2)=A → aşağı → (2,2) → aşağı → (3,2)=B
    gercek = (1, 1)
    adimlar = [
        ("sag", "A"),    # (1,2) A
        ("asagi", "yok"),  # (2,2)
        ("asagi", "B"),  # (3,2) B
    ]
    bel = uniform_inanc()
    yazdir_bel(bel, "Başlangıç (uniform)")
    print(f"Gerçek başlangıç: {gercek}")

    for i, (komut, gozlem) in enumerate(adimlar, 1):
        dy, dx = HAREKETLER[komut]
        gy, gx = gercek[0] + dy, gercek[1] + dx
        if serbest_mi(gy, gx):
            gercek = (gy, gx)
        bel = predict(bel, komut)
        bel = update(bel, gozlem)
        yazdir_bel(bel, f"Adım {i}: komut={komut}, gözlem={gozlem}, gerçek={gercek}")


def main() -> None:
    print("2D koridor lokalizasyonu — ayrık Bayes filtresi")
    print("Harita:")
    for satir in HARITA:
        print(" ", satir)
    simulasyon()


if __name__ == "__main__":
    main()
