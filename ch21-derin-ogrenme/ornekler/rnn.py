#!/usr/bin/env python3
"""Yinelemeli sinir ağları (kitaptaki 21.6).

* Temel RNN: z_t = g_z(W_zz z_{t−1} + W_xz x_t),  ŷ_t = g_y(W_zy z_t). Aynı ağırlıklar her adımda kullanılır.
* Zamanda geri yayılım (BPTT): Ağ zamanda açılır; gradyan her adımda W_zz ve g' ile çarpılır.
  W_zz'nin en büyük özdeğeri 1'den küçükse gradyan geçmişe doğru üstel küçülür (kaybolan gradyan),
  büyükse patlar.
* LSTM: Bellek hücresi c_t = f_t ⊙ c_{t−1} + i_t ⊙ c̃_t. Unutma kapısı f ≈ 1 iken bilgi (ve gradyan)
  uzun süre korunur: ∂c_t/∂c_{t−k} = Π f.
Örnek görev: Dizinin başındaki işareti (±1) k adım sonra hatırlamak (temel RNN bu kolay görevi öğrenir).

Çalıştırma:
    python rnn.py
"""
from __future__ import annotations

import numpy as np


def rnn_ileri(Wzz, Wxz, Wzy, xs):
    z = np.zeros(Wzz.shape[0])
    zs, ys = [], []
    for x in xs:
        z = np.tanh(Wzz @ z + Wxz * x)
        zs.append(z)
        ys.append(float(Wzy @ z))
    return zs, ys


def gecmise_gradyan(Wzz, zs) -> list[float]:
    """Son gizli durumdan t adım önceki duruma ∂z_T/∂z_{T−t}'nin normu (BPTT'deki çarpımlar)."""
    J = np.eye(Wzz.shape[0])
    normlar = []
    for z in reversed(zs[1:]):
        J = J @ (np.diag(1 - z ** 2) @ Wzz)            # ∂z_t/∂z_{t−1} = diag(1 − z_t²) W_zz
        normlar.append(float(np.linalg.norm(J, 2)))
    return normlar


def rastgele_rnn(n: int = 8, olcek: float = 0.9, tohum: int = 0):
    rng = np.random.default_rng(tohum)
    W = rng.normal(size=(n, n))
    W *= olcek / max(abs(np.linalg.eigvals(W)))       # spektral yarıçapı ayarla
    return W, rng.normal(size=n), rng.normal(size=n)


def hatirlama_gorevi(k: int, n_ornek: int = 200, tohum: int = 0):
    """x_1 = ±1, sonraki k − 1 adım küçük gürültü; hedef: son adımda x_1'in işareti."""
    rng = np.random.default_rng(tohum)
    isaret = rng.choice([-1.0, 1.0], n_ornek)
    X = rng.normal(0, 0.1, (n_ornek, k))
    X[:, 0] = isaret
    return X, isaret


def rnn_egit(k: int, n: int = 8, tur: int = 300, alfa: float = 0.05, tohum: int = 0) -> float:
    """Tam BPTT ile kare kayıp; son adımın çıktısı x_1'in işaretini tahmin etmeli. Test doğruluğu döner."""
    rng = np.random.default_rng(tohum)
    Wzz, Wxz, Wzy = rastgele_rnn(n, 0.9, tohum)
    X, y = hatirlama_gorevi(k, 200, tohum)
    for _ in range(tur):
        for j in rng.permutation(len(X)):
            zs, ys = rnn_ileri(Wzz, Wxz, Wzy, X[j])
            hata = ys[-1] - y[j]
            gWzy = hata * zs[-1]
            dz = hata * Wzy
            gWzz, gWxz = np.zeros_like(Wzz), np.zeros_like(Wxz)
            for t in reversed(range(k)):
                da = dz * (1 - zs[t] ** 2)
                onceki = zs[t - 1] if t > 0 else np.zeros(n)
                gWzz += np.outer(da, onceki)
                gWxz += da * X[j, t]
                dz = Wzz.T @ da
            for W, g in ((Wzz, gWzz), (Wxz, gWxz), (Wzy, gWzy)):
                W -= alfa * np.clip(g, -1, 1)
    Xt, yt = hatirlama_gorevi(k, 300, tohum + 100)
    return float(np.mean([np.sign(rnn_ileri(Wzz, Wxz, Wzy, x)[1][-1]) == s for x, s in zip(Xt, yt)]))


def lstm_bellegi(f: float, k: int) -> float:
    """Unutma kapısı sabit f iken başlangıçtaki hücre değerinin k adım sonra kalan kısmı (= ∂c_k/∂c_0)."""
    return f ** k


def main() -> None:
    print("=== BPTT'de geçmişe doğru gradyan (8 birimli tanh RNN) ===")
    for olcek in (0.5, 0.9, 1.5):
        Wzz, Wxz, Wzy = rastgele_rnn(8, olcek)
        xs = np.random.default_rng(1).normal(0, 0.5, 41)
        zs, _ = rnn_ileri(Wzz, Wxz, Wzy, xs)
        g = gecmise_gradyan(Wzz, zs)
        print(f"  spektral yarıçap {olcek}: 1 adım {g[0]:.2e}, 10 adım {g[9]:.2e}, 40 adım {g[39]:.2e}")
    print("  (tanh'ın türevi ≤ 1 olduğundan büyük ağırlıklar da çoğu zaman doyumla küçülür.)")

    print("\n=== Hatırlama görevi: ilk girdinin işaretini k adım sonra söyle ===")
    for k in (2, 10, 20):
        print(f"  k = {k:>2}: test doğruluğu {rnn_egit(k, tur=10):.2f}")
    print("  Bu basit görevi temel RNN de öğrenir. Ama yukarıdaki gibi gradyan geçmişe doğru üstel küçüldüğü için")
    print("  daha uzun ve karmaşık bağımlılıklarda öğrenme yavaşlar ya da durur; LSTM bu yüzden geliştirildi.")

    print("\n=== LSTM'de bellek hücresi ===")
    for f in (0.5, 0.9, 0.99, 1.0):
        print(f"  unutma kapısı f = {f}: 30 adım sonra kalan bilgi (ve gradyan) çarpanı {lstm_bellegi(f, 30):.2e}")
    print("  f ≈ 1 iken bilgi hücrede neredeyse kayıpsız taşınır; kapılar ne zaman unutulacağını öğrenir.")


if __name__ == "__main__":
    main()
