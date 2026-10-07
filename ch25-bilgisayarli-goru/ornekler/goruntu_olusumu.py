#!/usr/bin/env python3
"""Görüntü oluşumu ve 3B ipuçlarının geometrisi (kitaptaki 25.2, 25.6).

* İğne deliği kamera: x = −fX/Z, y = −fY/Z (görüntü ters döner; Z büyüdükçe görüntü küçülür).
* Kaybolma noktası: (U, V, W) yönlü paralel doğrular P∞ = (fU/W, fV/W) noktasında buluşur
  (kitap bu formülü işaretsiz, yani görüntü düzlemini deliğin önüne koyarak yazar).
* Ölçekli ortografik izdüşüm: Derinlik Z₀ ± ΔZ aralığında ve ΔZ ≪ Z₀ ise x = sX, y = sY, s = f/Z₀.
* Lambert'in kosinüs yasası: I = ρ I₀ cos θ.
* Stereo: Paralel eksenli iki kamerada yatay eşitsizlik H = b/Z (f = 1). İnsanın sabitlediği noktada
  açısal eşitsizlik δθ ≈ b δZ / Z².
* Optik akış (f = 1): vx = (−Tx + x Tz)/Z, vy = (−Ty + y Tz)/Z; genişleme odağı (Tx/Tz, Ty/Tz);
  çarpışma zamanı Z/Tz.

Çalıştırma:
    python goruntu_olusumu.py
"""
from __future__ import annotations

import math


def perspektif(P, f: float = 1.0, ters: bool = True) -> tuple[float, float]:
    """Sahne noktası P = (X, Y, Z) → görüntü noktası. ters=False: deliğin önündeki (sanal) düzlem."""
    X, Y, Z = P
    k = -f / Z if ters else f / Z
    return k * X, k * Y


def kaybolma_noktasi(yon, f: float = 1.0) -> tuple[float, float]:
    U, V, W = yon
    if W == 0:
        raise ValueError("W = 0: doğrular görüntü düzlemine paralel, kaybolma noktası sonsuzda")
    return f * U / W, f * V / W


def dogru_uzerinde(P0, yon, lam: float):
    return tuple(p + lam * d for p, d in zip(P0, yon))


def ortografik_hatasi(Z0: float, dZ: float) -> float:
    """Perspektif ölçek f/Z ile sabit s = f/Z₀ arasındaki en büyük göreli fark."""
    return max(abs(Z0 / (Z0 + d) - 1) for d in (-dZ, dZ))


def lambert(rho: float, I0: float, theta_derece: float) -> float:
    return rho * I0 * max(0.0, math.cos(math.radians(theta_derece)))


def stereo_derinlik(H: float, b: float, f: float = 1.0) -> float:
    """Yatay eşitsizlikten derinlik: H = f b / Z  →  Z = f b / H."""
    return f * b / H


def ayirt_edilebilir_derinlik(Z: float, b: float, dtheta: float) -> float:
    """δθ = b δZ / Z²  →  δZ = δθ Z² / b."""
    return dtheta * Z ** 2 / b


def optik_akis(x: float, y: float, Z: float, T) -> tuple[float, float]:
    Tx, Ty, Tz = T
    return (-Tx + x * Tz) / Z, (-Ty + y * Tz) / Z


def genisleme_odagi(T) -> tuple[float, float]:
    Tx, Ty, Tz = T
    return Tx / Tz, Ty / Tz


def main() -> None:
    print("=== Perspektif izdüşüm (f = 1) ===")
    for Z in (2, 4, 8):
        print(f"  P = (1, 0.5, {Z}) → {tuple(round(v, 3) for v in perspektif((1, 0.5, Z)))}")
    print("  Z iki katına çıkınca görüntü yarıya iner; eksi işaretler görüntünün ters döndüğünü gösterir.")

    print("\n=== Kaybolma noktası: iki ray (aralık 1.5 m, kamera 1.5 m yüksekte) ===")
    for lam in (1, 10, 100, 1000):
        a = perspektif(dogru_uzerinde((-0.75, -1.5, 2), (0, 0, 1), lam), ters=False)
        b = perspektif(dogru_uzerinde((0.75, -1.5, 2), (0, 0, 1), lam), ters=False)
        print(f"  λ = {lam:>4}: sol ray {tuple(round(v, 4) for v in a)}, sağ ray {tuple(round(v, 4) for v in b)}")
    print(f"  Yön (0, 0, 1) → kaybolma noktası {kaybolma_noktasi((0, 0, 1))}; "
          f"yön (1, 0, 2) → {kaybolma_noktasi((1, 0, 2))}")

    print("\n=== Ölçekli ortografik izdüşüm ===")
    for Z0, dZ in ((100, 1), (100, 10), (10, 5)):
        print(f"  Z₀ = {Z0}, ΔZ = {dZ}: en büyük göreli hata %{100 * ortografik_hatasi(Z0, dZ):.1f}")

    print("\n=== Lambert'in kosinüs yasası ===")
    for th in (0, 30, 60, 89):
        print(f"  θ = {th:>2}°: I = {lambert(0.8, 100, th):6.2f}  (ρ = 0.8, I₀ = 100)")
    siyah, beyaz = lambert(0.05, 1900, 0), lambert(0.95, 100, 0)
    print(f"  Güçlü ışıkta siyah yüzey (ρ = 0.05, I₀ = 1900): {siyah:.0f};  "
          f"loş ışıkta beyaz yüzey (ρ = 0.95, I₀ = 100): {beyaz:.0f} → aynı parlaklık, belirsizlik")

    print("\n=== Stereo görme ===")
    dtheta = math.radians(5 / 3600)                         # 5 açı saniyesi
    for Z in (100, 30):
        print(f"  b = 6 cm, Z = {Z} cm: ayırt edilebilen derinlik farkı "
              f"δZ = {10 * ayirt_edilebilir_derinlik(Z, 6, dtheta):.3f} mm")
    print(f"  Kamera çifti b = 0.12 m, f = 700 piksel, eşitsizlik 7 piksel → Z = "
          f"{stereo_derinlik(7, 0.12, 700):.1f} m")

    print("\n=== Hareketli kameradan optik akış (f = 1) ===")
    T = (0.0, 0.0, 2.0)                                     # ileri doğru 2 m/s
    print(f"  Genişleme odağı: {genisleme_odagi(T)}")
    for x, Z in ((0.1, 10), (0.2, 10), (0.2, 20)):
        print(f"  x = {x}, Z = {Z}: vx = {optik_akis(x, 0, Z, T)[0]:.3f}")
    v1 = optik_akis(0.2, 0, 10, T)
    v3 = optik_akis(0.2, 0, 20, (0, 0, 4))
    print(f"  Ölçek belirsizliği: (Tz = 2, Z = 10) → {v1[0]:.3f};  (Tz = 4, Z = 20) → {v3[0]:.3f}")
    print(f"  Çarpışma zamanı Z/Tz = {10 / 2:.1f} s; ölçek iki katına çıksa da aynı ({20 / 4:.1f} s)")
    yan = (1.0, 0.0, 0.0)                                   # yan pencereden bakış: yanal hareket
    a, b = optik_akis(0, 0, 5, yan)[0], optik_akis(0, 0, 50, yan)[0]
    print(f"  Hareket paralaksı: Z = 5 m'deki ağaç {abs(a):.2f}, Z = 50 m'deki tepe {abs(b):.2f} birim/s; "
          f"akış oranı {abs(a) / abs(b):.0f} → derinlik oranı Z₂/Z₁ = 10")


if __name__ == "__main__":
    main()
