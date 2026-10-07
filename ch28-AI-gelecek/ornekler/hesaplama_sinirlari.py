#!/usr/bin/env python3
"""Kaba kuvvetin sınırları, kaynak eğilimleri ve düşünmeyi denetlemek (kitaptaki 28.1 Resources, 28.2).

* Borges hesabı: Fizik kurallarının izin verdiği en hızlı 1 kg'lık bilgisayar (~10⁵¹ işlem/s) bir yılda
  İngilizce sözcük dizilerini sayarsa ancak 11 sözcüklük dizilere kadar gelir; 410 sayfalık kitaplar söz konusu bile değil.
* Kaynak eğilimleri: kitaptaki sayılardan katlanma/yarılanma süreleri.
* Her an kesilebilir (anytime) algoritma: Çıktının niteliği zamanla artar; kesildiği anda makul bir yanıt hazırdır.
* Karar kuramsal üst-akıl yürütme: Bir hesaplamanın değeri = karar niteliğindeki beklenen iyileşme − gecikmenin maliyeti.
  Değer maliyetin altına düşünce düşünmeyi bırak ve harekete geç.
* Sınırlı en iyilik: Mimari sabitken, olası programlar arasında en iyi performansı veren program. Burada oyuncak bir
  biçim: arama derinliği seçimi.

Çalıştırma:
    python hesaplama_sinirlari.py
"""
from __future__ import annotations

import math

import numpy as np

YIL = 365.25 * 24 * 3600


# --- Borges hesabı -------------------------------------------------------------------------------
def borges(islem_hizi: float = 1e51, sozluk: int = 100_000, sure: float = YIL) -> int:
    """Bir saniyede `islem_hizi` dizi sayılabildiğini varsay. Bir yılda bütünüyle sayılabilen en uzun dizi."""
    toplam = islem_hizi * sure
    return int(math.floor(math.log(toplam) / math.log(sozluk)))


# --- Eğilimler -------------------------------------------------------------------------------------
def katlanma_suresi(oran: float, yil: float) -> float:
    """`yil` içinde `oran` katına çıkan bir büyüklüğün katlanma süresi (yıl)."""
    return yil * math.log(2) / math.log(oran)


EGILIMLER = {          # ad: (oran, yıl, yön)
    "depolama fiyatı (1 MB: 1969'da $1 milyon → 2019'da $0.02)": (1e6 / 0.02, 50, "yarıya iniyor"),
    "süper bilgisayar hızı (1969–2019, 10¹⁰ kat)": (1e10, 50, "ikiye katlanıyor"),
    "ImageNet eğitim süresi (2014'te 1 gün → 2018'de 2 dakika)": (24 * 60 / 2, 4, "yarıya iniyor"),
    "arXiv'de makine öğrenmesi makaleleri (2009–2017, 16 kat)": (2 ** 4, 8, "ikiye katlanıyor"),
}


def sayi(v: float) -> str:
    return f"{v:,.0f}".replace(",", " ")


# --- Her an kesilebilir algoritma --------------------------------------------------------------------
def anytime_tahmin(adimlar=(10, 100, 1_000, 10_000, 100_000), tohum: int = 0) -> list[tuple[int, float]]:
    """Monte Carlo ile P(X + Y > 1.5), X, Y ~ U(0, 1) (gerçek değer 0.125). Her kesme anında (örnek sayısı, hata)."""
    rng = np.random.default_rng(tohum)
    X = rng.random((max(adimlar), 2))
    isabet = np.cumsum(X.sum(axis=1) > 1.5)
    return [(n, abs(isabet[n - 1] / n - 0.125)) for n in adimlar]


# --- Hesaplamanın değeri -------------------------------------------------------------------------------
def _phi(z: float) -> float:
    return math.exp(-z * z / 2) / math.sqrt(2 * math.pi)


def _Phi(z: float) -> float:
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def hesaplama_degeri(m: float, v: float, rakip: float, gurultu: float) -> float:
    """Seçeneğin değeri hakkındaki inanç N(m, v). Bir benzetim daha (gözlem gürültüsü σ²) yapılırsa sonsal ortalama
    N(m, s²) dağılımlı değişir, s² = v² / (v + σ²). Miyop değer: E[max(m', rakip)] − max(m, rakip)."""
    s = math.sqrt(v * v / (v + gurultu))
    if s == 0:
        return 0.0
    z = (m - rakip) / s
    beklenen = m * _Phi(z) + s * _phi(z) + rakip * (1 - _Phi(z))
    return beklenen - max(m, rakip)


def ustakil_karar(maliyet: float, gercek=(1.0, 1.3), gurultu: float = 1.0, en_cok: int = 500, tohum: int = 0):
    """İki eylem; değerleri hakkında önsel N(0, 1). Her adımda değeri en yüksek benzetimi yap; hiçbir benzetimin değeri
    maliyeti aşmıyorsa dur. (yapılan hesaplama sayısı, seçilen eylem, toplam maliyet)."""
    rng = np.random.default_rng(tohum)
    m, v = [0.0, 0.0], [1.0, 1.0]
    for k in range(en_cok):
        degerler = [hesaplama_degeri(m[i], v[i], m[1 - i], gurultu) for i in (0, 1)]
        i = int(np.argmax(degerler))
        if degerler[i] < maliyet:
            return k, int(np.argmax(m)), k * maliyet
        x = gercek[i] + rng.normal(0, math.sqrt(gurultu))
        yeni_v = 1 / (1 / v[i] + 1 / gurultu)
        m[i] = yeni_v * (m[i] / v[i] + x / gurultu)
        v[i] = yeni_v
    return en_cok, int(np.argmax(m)), en_cok * maliyet


# --- Sınırlı en iyilik: arama derinliği ------------------------------------------------------------------
def en_iyi_derinlik(zaman_maliyeti: float, dallanma: int = 3, en_cok: int = 15) -> tuple[int, float]:
    """Oyuncak model: d derinlikli aramanın karar niteliği 1 − 0.6^d, süresi dallanma^d birim.
    Net değer = nitelik − zaman_maliyeti · süre. En iyi d ve net değeri."""
    net = [(1 - 0.6 ** d) - zaman_maliyeti * dallanma ** d for d in range(en_cok + 1)]
    d = int(np.argmax(net))
    return d, net[d]


def main() -> None:
    print("=== Borges hesabı: 10⁵¹ işlem/s, bir yıl ===")
    for V in (10_000, 100_000):
        print(f"  {sayi(V)} sözcüklük sözlükle bütünüyle sayılabilen en uzun dizi: {borges(sozluk=V)} sözcük")
    print("  (410 sayfalık bir kitap yaklaşık yüz binden fazla sözcüktür.)")

    print("\n=== Kaynak eğilimlerinden katlanma süreleri ===")
    for ad, (oran, yil, yon) in EGILIMLER.items():
        print(f"  {ad}: {katlanma_suresi(oran, yil):.2f} yılda bir {yon}")
    print(f"  En büyük modellerin eğitim hesabı (3.5 ayda bir 2 kat, 2012–2018 arası 6 yıl): ~{sayi(2 ** (72 / 3.5))} kat")
    print("  Otonom araç lidarı: $75 000 → $1 000 (75 kat); tek yongalı sürümü $10'a inebilir.")

    print("\n=== Her an kesilebilir algoritma (Monte Carlo) ===")
    for n, h in anytime_tahmin():
        print(f"  {n:>6} örnekte kesilirse hata {h:.4f}")

    print("\n=== Hesaplamanın değeri: iki eylem, gerçek değerler 1.0 ve 1.3 ===")
    for c in (0.1, 0.01, 0.001):
        sonuc = [ustakil_karar(c, tohum=t) for t in range(200)]
        net = np.mean([(1.0, 1.3)[s[1]] - s[2] for s in sonuc])
        print(f"  benzetim maliyeti {c:<5}: ort. {np.mean([s[0] for s in sonuc]):5.1f} benzetim, doğru eylem "
              f"%{100 * np.mean([s[1] == 1 for s in sonuc]):.0f}, net fayda {net:.3f}")
    print("  Miyop hesap 'tek bir benzetim kararı değiştirmez' deyip erken durabilir (kitaptaki miyopi sorunu).")

    print("\n=== Sınırlı en iyilik (oyuncak): arama derinliği ===")
    for c in (1e-2, 1e-4, 1e-6):
        d, net = en_iyi_derinlik(c)
        print(f"  birim zaman maliyeti {c:g}: en iyi derinlik {d}, net değer {net:.3f}")


if __name__ == "__main__":
    main()
