#!/usr/bin/env python3
"""Dikkat, öz-dikkat ve transformer bileşenleri (kitaptaki 24.3.1, 24.4).

* Dizi-dizi dikkati: hedef durumu hᵢ₋₁ ile kaynak durumları sⱼ arasında puan rᵢⱼ = hᵢ₋₁ · sⱼ;
  aᵢⱼ = softmax(rᵢⱼ); bağlam vektörü cᵢ = Σⱼ aᵢⱼ sⱼ.
* Öz-dikkat: qᵢ = W_q xᵢ, kᵢ = W_k xᵢ, vᵢ = W_v xᵢ;  rᵢⱼ = (qᵢ · kⱼ)/√d;  aᵢⱼ = softmax;  cᵢ = Σ aᵢⱼ vⱼ.
  √d ile bölmek, d büyüdükçe iç çarpımların varyansının büyüyüp softmax'ı doyurmasını önler.
* Çok başlı dikkat: birkaç bağımsız (W_q, W_k, W_v) kümesi; çıktılar birleştirilir.
* Konum kodlaması: Öz-dikkat sırayı bilmez (girdinin yerini değiştirmek çıktıların yerini aynı biçimde
  değiştirir); sin/cos konum vektörleri eklenir.
* Nedensel maske: Dil modelinde i. konum yalnızca ≤ i konumlara bakabilir.

Çalıştırma:
    python dikkat.py
"""
from __future__ import annotations

import numpy as np


def softmax(z, eksen: int = -1):
    z = z - z.max(axis=eksen, keepdims=True)
    e = np.exp(z)
    return e / e.sum(axis=eksen, keepdims=True)


def diziden_diziye_dikkat(h_onceki, kaynak):
    """h_onceki: (d,), kaynak: (n, d). (dikkat olasılıkları, bağlam vektörü)."""
    r = kaynak @ h_onceki
    a = softmax(r)
    return a, a @ kaynak


def oz_dikkat(X, Wq, Wk, Wv, maske: bool = False):
    Q, K, V = X @ Wq, X @ Wk, X @ Wv
    d = Q.shape[1]
    R = Q @ K.T / np.sqrt(d)
    if maske:
        R = np.where(np.tril(np.ones_like(R)) > 0, R, -np.inf)
    A = softmax(R)
    return A, A @ V


def cok_basli(X, basliklar, Wo):
    return np.concatenate([oz_dikkat(X, *w)[1] for w in basliklar], axis=1) @ Wo


def konum_kodlamasi(n: int, d: int) -> np.ndarray:
    poz = np.arange(n)[:, None]
    i = np.arange(d)[None, :]
    aci = poz / np.power(10000, (2 * (i // 2)) / d)
    return np.where(i % 2 == 0, np.sin(aci), np.cos(aci))


def olcek_etkisi(d: int, deneme: int = 2000, tohum: int = 0) -> tuple[float, float]:
    """Rastgele q, k ~ N(0, I): q·k'nın standart sapması √d; √d'ye bölünce ~1."""
    rng = np.random.default_rng(tohum)
    q, k = rng.normal(size=(deneme, d)), rng.normal(size=(deneme, d))
    ic = (q * k).sum(axis=1)
    return float(ic.std()), float((ic / np.sqrt(d)).std())


def main() -> None:
    rng = np.random.default_rng(0)
    print("=== Dizi-dizi dikkati ===")
    kaynak = rng.normal(size=(4, 6))                 # 4 kaynak sözcüğün durum vektörleri
    h = kaynak[2] * 0.4 + rng.normal(0, 0.3, 6)      # hedef durum, 3. kaynak sözcüğe benziyor
    a, c = diziden_diziye_dikkat(h, kaynak)
    print(f"  dikkat olasılıkları {np.round(a, 3)} (toplam {a.sum():.1f}); en çok 3. sözcüğe bakıyor")

    print("\n=== Öz-dikkat ===")
    n, d = 5, 8
    X = rng.normal(size=(n, d))
    Wq, Wk, Wv = (rng.normal(0, 1 / np.sqrt(d), (d, d)) for _ in range(3))
    A, C = oz_dikkat(X, Wq, Wk, Wv)
    print(f"  dikkat matrisinin satır toplamları: {np.round(A.sum(axis=1), 6)}")
    p = rng.permutation(n)
    _, Cp = oz_dikkat(X[p], Wq, Wk, Wv)
    print(f"  Girdiyi karıştırınca çıktı da aynı biçimde karışıyor mu? {np.allclose(Cp, C[p])} (sırayı bilmiyor)")
    P = konum_kodlamasi(n, d)
    _, Cpk = oz_dikkat(X[p] + P, Wq, Wk, Wv)
    _, Ck = oz_dikkat(X + P, Wq, Wk, Wv)
    print(f"  Konum kodlaması eklenince hâlâ öyle mi? {np.allclose(Cpk, Ck[p])}")
    Am, _ = oz_dikkat(X, Wq, Wk, Wv, maske=True)
    print(f"  Nedensel maske: üst üçgen sıfır mı? {np.allclose(np.triu(Am, 1), 0)}")
    basliklar = [tuple(rng.normal(0, 1 / np.sqrt(d), (d, d // 2)) for _ in range(3)) for _ in range(2)]
    print(f"  2 başlı dikkat çıktısı boyutu: {cok_basli(X, basliklar, rng.normal(size=(d, d))).shape}")

    print("\n=== √d ile ölçekleme ===")
    for dd in (4, 64, 512):
        once, sonra = olcek_etkisi(dd)
        print(f"  d = {dd:>3}: q·k std {once:6.2f}, (q·k)/√d std {sonra:.2f}")


if __name__ == "__main__":
    main()
