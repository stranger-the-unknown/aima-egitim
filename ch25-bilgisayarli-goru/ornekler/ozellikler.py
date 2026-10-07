#!/usr/bin/env python3
"""Basit görüntü özellikleri: kenar, doku, optik akış, bölütleme (kitaptaki 25.3).

* Kenar: Gürültülü bir basamağın türevinde sahte tepeler çıkar; önce Gauss ile düzeltmek bunları
  bastırır. (f ∗ g)′ = f ∗ g′ olduğu için görüntü doğrudan Gauss'un türeviyle evrişilebilir.
  2B'de gradyan büyüklüğü kenar gücünü, yönü kenarın yönelimini verir; yön ışıktan bağımsızdır.
  Kenar noktası: gradyan yönünde yerel en büyük + eşik üstü.
* Doku: Bir yamadaki gradyan yönlerinin histogramı. Dikey çizgilerde iki tepe (çizginin sol ve sağ
  kenarı), benekli desende daha düzgün dağılım; ışık değişince histogram değişmez.
* Optik akış: Bir pikselin çevresindeki bloğu sonraki karede kaydırarak arar, kare farkları toplamını
  (SSD) en aza indiren kaydırmayı seçer. Dokusuz bir duvarda bütün adaylar eşittir.
* Bölütleme: Shi ve Malik (2000) normalleştirilmiş kesme — pikseller düğüm, benzerlikler ağırlık;
  gruplar arası bağlantıyı küçültüp grup içini büyüten bölme. Burada ikinci en küçük özvektörle yaklaşık çözülür.

Çalıştırma:
    python ozellikler.py
"""
from __future__ import annotations

import numpy as np


# --- Gauss süzgeci ve evrişim -------------------------------------------------------------
def gauss(sigma: float) -> np.ndarray:
    """Toplamı 1 olan 1B Gauss çekirdeği; ±3σ'da kesilir (kitaptaki öneri)."""
    r = max(1, int(np.ceil(3 * sigma)))
    x = np.arange(-r, r + 1)
    g = np.exp(-x ** 2 / (2 * sigma ** 2))
    return g / g.sum()


def turev() -> np.ndarray:
    """Merkezî fark: (I(x+1) − I(x−1)) / 2 (np.convolve çekirdeği ters çevirdiği için bu sırada)."""
    return np.array([0.5, 0.0, -0.5])


def evris2(I: np.ndarray, satir: np.ndarray, sutun: np.ndarray) -> np.ndarray:
    """Ayrılabilir 2B evrişim: önce satırlar boyunca, sonra sütunlar boyunca (kenarlar yansıtılır)."""
    r1, r2 = len(satir) // 2, len(sutun) // 2
    J = np.pad(I, ((0, 0), (r1, r1)), mode="reflect")
    J = np.array([np.convolve(s, satir, mode="valid") for s in J])
    J = np.pad(J, ((r2, r2), (0, 0)), mode="reflect")
    return np.array([np.convolve(s, sutun, mode="valid") for s in J.T]).T


# --- 1B kenar ------------------------------------------------------------------------------
def basamak(n: int = 100, kenar: int = 50, gurultu: float = 0.15, tohum: int = 0) -> np.ndarray:
    """x < kenar'da 0, x > kenar'da 1 (kenar pikselinde 0.5) + Gauss gürültüsü."""
    rng = np.random.default_rng(tohum)
    x = np.arange(n)
    return np.clip(x - kenar + 0.5, 0, 1) + rng.normal(0, gurultu, n)


def tepeler(y: np.ndarray, esik: float) -> list[int]:
    """Eşiği aşan yerel en büyükler (mutlak değer)."""
    a = np.abs(y)
    return [i for i in range(1, len(a) - 1) if a[i] > esik and a[i] >= a[i - 1] and a[i] >= a[i + 1]]


def kenar_1b(I: np.ndarray, sigma: float | None, oran: float = 0.4) -> list[int]:
    """Yanıtı en büyük yanıtın `oran` katını aşan tepeler (G′'nin yanıtı σ büyüdükçe küçüldüğü için göreli eşik)."""
    if sigma is None:
        cevap = np.convolve(I, turev(), mode="same")
    else:
        cevap = np.convolve(I, np.convolve(gauss(sigma), turev()), mode="same")   # I ∗ G′
    r = len(gauss(sigma)) // 2 + 1 if sigma else 1
    cevap[:r], cevap[-r:] = 0, 0                     # dizinin uçlarındaki dolgu etkisini at
    return tepeler(cevap, oran * np.abs(cevap).max())


# --- 2B gradyan ve kenar noktaları -----------------------------------------------------------
def gradyan(I: np.ndarray, sigma: float = 1.0) -> tuple[np.ndarray, np.ndarray]:
    """∇(I ∗ G_σ): Gauss'un kısmi türevleriyle evrişim. (büyüklük, yön θ radyan)."""
    G, d = gauss(sigma), np.convolve(gauss(sigma), turev())
    Ix = evris2(I, d, G)                             # x boyunca türev, y boyunca düzeltme
    Iy = evris2(I, G, d)
    return np.hypot(Ix, Iy), np.arctan2(Iy, Ix)


def kenar_noktalari(I: np.ndarray, sigma: float = 1.0, esik: float = 0.1) -> np.ndarray:
    """Gradyan yönünde yerel en büyük olan ve eşiği aşan pikseller."""
    M, T = gradyan(I, sigma)
    K = np.zeros_like(M, dtype=bool)
    for y in range(1, M.shape[0] - 1):
        for x in range(1, M.shape[1] - 1):
            dx, dy = int(round(np.cos(T[y, x]))), int(round(np.sin(T[y, x])))
            if M[y, x] > esik and M[y, x] >= M[y + dy, x + dx] and M[y, x] >= M[y - dy, x - dx]:
                K[y, x] = True
    return K


def kare_goruntu(n: int = 32, gurultu: float = 0.05, tohum: int = 0, parlaklik: float = 1.0) -> np.ndarray:
    rng = np.random.default_rng(tohum)
    I = np.zeros((n, n))
    I[n // 4:3 * n // 4, n // 4:3 * n // 4] = 1.0
    return parlaklik * I + rng.normal(0, gurultu, (n, n))


# --- Doku: yön histogramı ---------------------------------------------------------------------
def yon_histogrami(I: np.ndarray, kutu: int = 8, sigma: float = 1.0) -> np.ndarray:
    """Gradyan yönlerinin büyüklükle ağırlıklı, normalleştirilmiş histogramı; kutu 0 = 0° (sağa)."""
    M, T = gradyan(I, sigma)
    k = np.round((T % (2 * np.pi)) / (2 * np.pi / kutu)).astype(int) % kutu
    h = np.bincount(k.ravel(), weights=M.ravel(), minlength=kutu)
    return h / h.sum()


def cizgiler(n: int = 36, periyot: int = 8, dikey: bool = True) -> np.ndarray:
    x = np.arange(n)
    satir = ((x // (periyot // 2)) % 2).astype(float)
    I = np.tile(satir, (n, 1))
    return I if dikey else I.T


def benekler(n: int = 32, periyot: int = 8, yaricap: float = 2.0) -> np.ndarray:
    y, x = np.mgrid[0:n, 0:n]
    cy = (y % periyot) - periyot / 2 + 0.5
    cx = (x % periyot) - periyot / 2 + 0.5
    return (cx ** 2 + cy ** 2 <= yaricap ** 2).astype(float)


# --- Optik akış: SSD blok eşleme ---------------------------------------------------------------
def ssd_akis(I1: np.ndarray, I2: np.ndarray, p: tuple[int, int], blok: int = 3, arama: int = 5):
    """p = (x0, y0) çevresindeki (2·blok+1)² bloğu I2'de ±arama içinde arar. (en iyi (Dx, Dy), SSD tablosu)."""
    x0, y0 = p
    A = I1[y0 - blok:y0 + blok + 1, x0 - blok:x0 + blok + 1]
    tablo = {}
    for Dy in range(-arama, arama + 1):
        for Dx in range(-arama, arama + 1):
            B = I2[y0 + Dy - blok:y0 + Dy + blok + 1, x0 + Dx - blok:x0 + Dx + blok + 1]
            tablo[(Dx, Dy)] = float(((A - B) ** 2).sum())
    return min(tablo, key=tablo.get), tablo


def kaydir(I: np.ndarray, Dx: int, Dy: int) -> np.ndarray:
    """Görüntü içeriğini Dx sağa, Dy aşağı kaydır (dairesel)."""
    return np.roll(np.roll(I, Dy, axis=0), Dx, axis=1)


# --- Bölütleme: normalleştirilmiş kesme -----------------------------------------------------------
def benzerlik_matrisi(I: np.ndarray, sigma_I: float = 0.2, sigma_X: float = 4.0, r: float = 3.0) -> np.ndarray:
    n, m = I.shape
    y, x = np.mgrid[0:n, 0:m]
    konum = np.stack([y.ravel(), x.ravel()], axis=1).astype(float)
    deger = I.ravel()
    d2 = ((konum[:, None, :] - konum[None, :, :]) ** 2).sum(axis=2)
    W = np.exp(-(deger[:, None] - deger[None, :]) ** 2 / sigma_I ** 2) * np.exp(-d2 / sigma_X ** 2)
    W[d2 > r ** 2] = 0.0
    return W


def ncut_degeri(W: np.ndarray, etiket: np.ndarray) -> float:
    A, B = etiket, ~etiket
    kesik = W[np.ix_(A, B)].sum()
    return float(kesik / W[A].sum() + kesik / W[B].sum())


def normallestirilmis_kesme(I: np.ndarray, **kw) -> np.ndarray:
    """(D − W) y = λ D y'nin ikinci en küçük çözümü; en iyi Ncut veren eşikle ikiye böl."""
    W = benzerlik_matrisi(I, **kw)
    d = W.sum(axis=1)
    Dm = 1 / np.sqrt(d)
    L = np.eye(len(d)) - Dm[:, None] * W * Dm[None, :]
    _, V = np.linalg.eigh(L)
    y = Dm * V[:, 1]
    en_iyi = None
    for t in np.quantile(y, np.linspace(0.05, 0.95, 37)):
        e = y > t
        c = ncut_degeri(W, e)
        if en_iyi is None or c < en_iyi[0]:
            en_iyi = (c, e)
    return en_iyi[1].reshape(I.shape)


def iki_bolgeli(n: int = 12, gurultu: float = 0.1, egim: float = 0.0, tohum: int = 0):
    """Koyu zemin (0.2) üzerinde parlak daire (0.8); `egim`: soldan sağa artan aydınlatma. (görüntü, gerçek)."""
    rng = np.random.default_rng(tohum)
    y, x = np.mgrid[0:n, 0:n]
    gercek = (y - n / 2 + 0.5) ** 2 + (x - n / 2 + 0.5) ** 2 <= (n / 3) ** 2
    I = 0.2 + 0.6 * gercek + egim * (x / (n - 1) - 0.5) + rng.normal(0, gurultu, (n, n))
    return I, gercek


def en_iyi_esik(I: np.ndarray, gercek: np.ndarray) -> float:
    """Tek bir genel parlaklık eşiğiyle (gerçeği bilerek seçilmiş en iyi eşik) ulaşılabilen doğruluk."""
    return max(dogruluk(I > t, gercek) for t in np.linspace(I.min(), I.max(), 101))


def dogruluk(tahmin: np.ndarray, gercek: np.ndarray) -> float:
    """Bölge adları önemsiz: iki eşleşmeden iyisini al."""
    a = float((tahmin == gercek).mean())
    return max(a, 1 - a)


def main() -> None:
    print("=== 1B kenar: x = 50'de gürültülü basamak ===")
    I = basamak()
    print(f"  düzeltmeden türev → tepeler: {kenar_1b(I, None)}")
    for s in (1, 2, 4):
        print(f"  I ∗ G′ (σ = {s})    → tepeler: {kenar_1b(I, s)}")
    print("  (eşik: en büyük yanıtın 0.4 katı)")
    G = gauss(2)
    sol = np.convolve(np.convolve(I, G), turev())
    sag = np.convolve(I, np.convolve(G, turev()))
    print(f"  (I ∗ G)′ ile I ∗ G′ aynı mı? {np.allclose(sol, sag)}")

    print("\n=== 2B gradyan ve kenar noktaları ===")
    I = kare_goruntu()
    M, T = gradyan(I)
    M2, T2 = gradyan(0.3 * I)
    secim = M > 0.2
    print(f"  Görüntüyü 0.3 ile karartınca: büyüklük oranı {np.median(M2[secim] / M[secim]):.2f}, "
          f"yönler aynı mı? {np.allclose(T[secim], T2[secim])}")
    K = kenar_noktalari(I, esik=0.2)
    yy, xx = np.nonzero(K)
    sinira = np.minimum(np.minimum(abs(yy - 7.5), abs(yy - 23.5)), np.minimum(abs(xx - 7.5), abs(xx - 23.5)))
    print(f"  {K.sum()} kenar pikseli; gerçek sınıra (≤ 1 piksel) yakın olanların oranı {np.mean(sinira <= 1):.2f}")

    print("\n=== Doku: yön histogramları (8 kutu: 0°, 45°, …, 315°) ===")
    for ad, D in (("dikey çizgiler", cizgiler()), ("yatay çizgiler", cizgiler(dikey=False)),
                  ("benekler", benekler()), ("dikey, karanlık", 0.2 * cizgiler() + 0.1)):
        print(f"  {ad:<16}: {np.round(yon_histogrami(D), 2)}")
    print("  Dikey çizgiler: 0° ve 180°'de iki tepe; yatay: 90° ve 270°; benekler: dağılmış; ışık değişince aynı.")

    print("\n=== Optik akış: SSD blok eşleme ===")
    rng = np.random.default_rng(1)
    I1 = rng.random((40, 40))
    I2 = kaydir(I1, 3, -2)
    (Dx, Dy), _ = ssd_akis(I1, I2, (20, 20))
    print(f"  Dokulu görüntü 3 sağa, 2 yukarı kaydırıldı → bulunan (Dx, Dy) = ({Dx}, {Dy})")
    duvar = np.ones((40, 40))
    _, tablo = ssd_akis(duvar, duvar, (20, 20))
    print(f"  Beyaz duvar: {sum(v == 0 for v in tablo.values())}/{len(tablo)} aday SSD = 0 → kör tahmin")

    print("\n=== Normalleştirilmiş kesme ===")
    for egim in (0.0, 0.8):
        I, gercek = iki_bolgeli(egim=egim)
        S = normallestirilmis_kesme(I)
        print(f"  12×12 daire + zemin, aydınlatma eğimi {egim}: Ncut doğruluğu {dogruluk(S, gercek):.2f}, "
              f"en iyi tek eşik {en_iyi_esik(I, gercek):.2f}")
    print("  Ncut yerel benzerliklere baktığı için düzgün olmayan aydınlatmadan daha az etkilenir.")


if __name__ == "__main__":
    main()
