#!/usr/bin/env python3
"""Zamansal olasılık modelleri için araçlar (Bölüm 14): gizli Markov modeli (HMM).

Model:
    durumlar : ["Yağmur", "Kuru"] gibi
    T[i][j]  : P(X_{t+1} = j | X_t = i)          (geçiş modeli)
    sensor(e): [P(e | X_t = i) for i]             (algılayıcı modeli)
    onsel    : P(X_0)

Matris biçimi (kitaptaki 14.3.1):
    ileri   f_{1:t+1} = α O_{t+1} Tᵀ f_{1:t}
    geri    b_{k+1:t} = T O_{k+1} b_{k+2:t}
    Viterbi m_{1:t+1} = O_{t+1} max_{x_t} (T(x_t, ·) m_{1:t}(x_t))

Çalıştırınca şemsiye dünyası için kısa bir özet yazdırır:
    python zamansal.py
"""
from __future__ import annotations

from typing import Callable, Sequence

Vektor = list[float]


def normalize(v: Sequence[float]) -> Vektor:
    s = sum(v)
    if s == 0:
        raise ZeroDivisionError("Gözlem dizisi modelde imkânsız")
    return [x / s for x in v]


class HMM:
    def __init__(self, durumlar: list, T: list[list[float]], sensor: Callable[[object], Vektor], onsel: Vektor):
        self.durumlar = list(durumlar)
        self.T = T
        self.sensor = sensor
        self.onsel = list(onsel)
        self.n = len(durumlar)

    # -- tahmin ve filtreleme ------------------------------------------------
    def tahmin_adimi(self, f: Vektor) -> Vektor:
        """P(X_{t+1} | e_{1:t}) = Σ_x P(X_{t+1} | x) P(x | e_{1:t})."""
        return [sum(self.T[i][j] * f[i] for i in range(self.n)) for j in range(self.n)]

    def ileri(self, f: Vektor, e, normalize_et: bool = True) -> Vektor:
        """Tek filtreleme adımı: önce tahmin, sonra gözlemle güncelle."""
        tahmin = self.tahmin_adimi(f)
        o = self.sensor(e)
        ham = [o[j] * tahmin[j] for j in range(self.n)]
        return normalize(ham) if normalize_et else ham

    def filtrele(self, kanitlar: Sequence) -> list[Vektor]:
        """[P(X_1 | e_1), P(X_2 | e_{1:2}), ...]"""
        f, sonuc = self.onsel, []
        for e in kanitlar:
            f = self.ileri(f, e)
            sonuc.append(f)
        return sonuc

    def olabilirlik(self, kanitlar: Sequence) -> float:
        """P(e_{1:t}): normalize edilmemiş ileri mesajın toplamı (adım adım ölçekleyerek)."""
        f, p = self.onsel, 1.0
        for e in kanitlar:
            ham = self.ileri(f, e, normalize_et=False)
            s = sum(ham)
            p *= s
            f = [x / s for x in ham]
        return p

    def ileriye_tahmin(self, f: Vektor, k: int) -> list[Vektor]:
        sonuc = []
        for _ in range(k):
            f = self.tahmin_adimi(f)
            sonuc.append(f)
        return sonuc

    def duragan_dagilim(self, adim: int = 10_000, tol: float = 1e-12) -> Vektor:
        f = self.onsel
        for _ in range(adim):
            yeni = self.tahmin_adimi(f)
            if max(abs(a - b) for a, b in zip(yeni, f)) < tol:
                return yeni
            f = yeni
        return f

    # -- yumuşatma -----------------------------------------------------------
    def geri(self, b: Vektor, e) -> Vektor:
        """b_{k+1:t}(i) = Σ_j P(e_{k+1} | j) b_{k+2:t}(j) P(j | i)."""
        o = self.sensor(e)
        return [sum(o[j] * b[j] * self.T[i][j] for j in range(self.n)) for i in range(self.n)]

    def ileri_geri(self, kanitlar: Sequence) -> list[Vektor]:
        """Yumuşatılmış dağılımlar P(X_k | e_{1:t}), k = 1..t (FORWARD-BACKWARD)."""
        ileriler = self.filtrele(kanitlar)
        b = [1.0] * self.n
        sonuc = [None] * len(kanitlar)
        for k in range(len(kanitlar) - 1, -1, -1):
            sonuc[k] = normalize([ileriler[k][i] * b[i] for i in range(self.n)])
            b = self.geri(b, kanitlar[k])
        return sonuc

    def geri_mesajlari(self, kanitlar: Sequence) -> list[Vektor]:
        """[b_{2:t}, b_{3:t}, ..., b_{t+1:t} = 1]: k. gün için yumuşatmada kullanılan b_{k+1:t}
        mesajları (normalize edilmemiş). Liste indeksi k − 1."""
        b = [1.0] * self.n
        sonuc = [b]
        for e in reversed(kanitlar[1:]):
            b = self.geri(b, e)
            sonuc.append(b)
        return list(reversed(sonuc))

    # -- en olası dizi -------------------------------------------------------
    def viterbi(self, kanitlar: Sequence) -> tuple[list, list[Vektor]]:
        """Döner: (en olası durum dizisi, m_{1:t} mesajları).
        Kitaptaki şekildeki gibi ilk mesaj m_{1:1} = P(X_1 | e_1) normalize edilir; bu yalnızca
        bütün mesajları aynı sabitle ölçekler, yolu değiştirmez."""
        m = self.filtrele(kanitlar[:1])[0]
        mesajlar, geri_isaret = [m], []
        for e in kanitlar[1:]:
            o = self.sensor(e)
            yeni, isaret = [], []
            for j in range(self.n):
                en_iyi = max(range(self.n), key=lambda i: self.T[i][j] * m[i])
                isaret.append(en_iyi)
                yeni.append(o[j] * self.T[en_iyi][j] * m[en_iyi])
            m = yeni
            mesajlar.append(m)
            geri_isaret.append(isaret)
        son = max(range(self.n), key=lambda j: m[j])
        yol = [son]
        for isaret in reversed(geri_isaret):
            yol.append(isaret[yol[-1]])
        return [self.durumlar[i] for i in reversed(yol)], mesajlar


def semsiye_hmm() -> HMM:
    """Kitabın şemsiye dünyası: P(R_t | R_{t-1}) = 0.7 / 0.3, P(U_t | R_t) = 0.9 / 0.2."""
    return HMM(["Yağmur", "Kuru"],
               [[0.7, 0.3], [0.3, 0.7]],
               lambda semsiye: [0.9, 0.2] if semsiye else [0.1, 0.8],
               [0.5, 0.5])


if __name__ == "__main__":
    h = semsiye_hmm()
    print("Şemsiye dünyası, iki gün şemsiye görüldü:")
    print("  Filtreleme:", [round(f[0], 3) for f in h.filtrele([True, True])], "(kitap: 0.818, 0.883)")
    print("  Yumuşatma :", [round(s[0], 3) for s in h.ileri_geri([True, True])], "(kitap: 1. gün 0.883)")
    print("  Viterbi   :", h.viterbi([True, True, False, True, True])[0])
