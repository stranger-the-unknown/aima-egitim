#!/usr/bin/env python3
"""Sınıflandırmadan nesne tespitine (kitaptaki 25.4, 25.5).

* Konvolüsyon + ReLU = yerel desen dedektörü (Şekil 25.12'deki yatay/dikey çubuk dedektörleri gibi).
  İkinci katman birinci katmanın çıktılarına bakar: "desenlerin deseni" (burada: yatay ve dikey çizgilerin buluşması).
  Her katman daha geniş bir piksel penceresini görür (alıcı alan).
* Kayan pencere: n × n görüntüde O(n⁴) eksene hizalı dikdörtgen vardır; bu yüzden önce "nesnelik"
  puanı yüksek kutular seçilir. Faster RCNN: 16 piksel adımlı merkezlerin her birinde 9 çapa kutusu
  (3 boyut × 3 en-boy oranı).
* Maksimum olmayanı bastırma (NMS): Puana göre sırala; en iyisini kabul et, onunla çok örtüşenleri at; tekrarla.
* Değerlendirme: kesinlik (bulunanların ne kadarı gerçek) ve duyarlılık (gerçeklerin ne kadarı bulundu).
  Örtüşme ölçüsü olarak kesişim/birleşim (IoU) ve 0.5 eşiği kullanıyoruz (yaygın seçim; kitap belirli
  bir ölçü vermez, yalnızca birkaç piksellik kaymanın kabul edilmesi gerektiğini söyler).

Çalıştırma:
    python tespit.py
"""
from __future__ import annotations

import numpy as np

YATAY = np.array([[-1.0, -1.0, -1.0], [2.0, 2.0, 2.0], [-1.0, -1.0, -1.0]])   # yatay çubuk dedektörü
DIKEY = YATAY.T


# --- Konvolüsyon katmanları ---------------------------------------------------------------------
def konv2(I: np.ndarray, K: np.ndarray) -> np.ndarray:
    """'Geçerli' 2B ilinti (CNN'lerde konvolüsyon diye anılan işlem): çıktı (n−k+1) × (m−k+1)."""
    k = K.shape[0]
    n, m = I.shape[0] - k + 1, I.shape[1] - k + 1
    return np.array([[float((I[i:i + k, j:j + k] * K).sum()) for j in range(m)] for i in range(n)])


def relu(x):
    return np.maximum(0.0, x)


def birinci_katman(I: np.ndarray) -> dict[str, np.ndarray]:
    return {"yatay": relu(konv2(I, YATAY)), "dikey": relu(konv2(I, DIKEY))}


def bulusma_katmani(H: np.ndarray, V: np.ndarray, sapma: float = 24.0) -> np.ndarray:
    """İkinci katman (yine konvolüsyon + ReLU): 3 × 3 pencerede yatay ve dikey yanıtların toplamı eksi sapma.
    Sapma elle seçildi: Tek başına bir çubuk (en çok 18 + 3) eşiği aşamaz; yatay ve dikey çizgilerin
    buluştuğu yerde (köşe ya da kesişim) ikisi birlikte aşar."""
    bir = np.ones((3, 3))
    return relu(konv2(H, bir) + konv2(V, bir) - sapma)


def sekiller(n: int = 9) -> dict[str, np.ndarray]:
    c = n // 2
    bos = np.zeros((n, n))
    yatay, dikey = bos.copy(), bos.copy()
    yatay[c, 1:-1] = 1
    dikey[1:-1, c] = 1
    arti = np.maximum(yatay, dikey)
    L = bos.copy()                                   # köşesi merkezde: yukarı ve sağa giden iki kol
    L[1:c + 1, c] = 1
    L[c, c:-1] = 1
    return {"yatay çubuk": yatay, "dikey çubuk": dikey, "artı": arti, "L köşesi": L}


def alici_alan(katman: int, k: int = 3) -> int:
    """Adım 1'li, k × k çekirdekli `katman` katmanın bir çıktısının gördüğü pencere kenarı."""
    return 1 + katman * (k - 1)


# --- Pencereler ve çapa kutuları -----------------------------------------------------------------
def dikdortgen_sayisi(n: int) -> int:
    """n × n piksel görüntüde eksene hizalı dikdörtgen pencere sayısı: (n(n+1)/2)² = O(n⁴)."""
    return (n * (n + 1) // 2) ** 2


def capa_kutusu_sayisi(genislik: int, yukseklik: int, adim: int = 16, kutu: int = 9) -> int:
    return (genislik // adim) * (yukseklik // adim) * kutu


# --- IoU, NMS, değerlendirme ----------------------------------------------------------------------
def iou(a, b) -> float:
    """Kutular (x1, y1, x2, y2)."""
    ix = max(0.0, min(a[2], b[2]) - max(a[0], b[0]))
    iy = max(0.0, min(a[3], b[3]) - max(a[1], b[1]))
    kesisim = ix * iy
    alan = lambda k: (k[2] - k[0]) * (k[3] - k[1])  # noqa: E731
    return kesisim / (alan(a) + alan(b) - kesisim)


def nms(kutular: list, puanlar: list[float], esik: float = 0.5, en_az: float = 0.0) -> list[int]:
    """Açgözlü maksimum olmayanı bastırma; kabul edilen kutuların indeksleri."""
    liste = sorted((i for i, p in enumerate(puanlar) if p > en_az), key=lambda i: -puanlar[i])
    kabul = []
    while liste:
        en = liste.pop(0)
        kabul.append(en)
        liste = [i for i in liste if iou(kutular[en], kutular[i]) < esik]
    return kabul


def degerlendir(tahmin: list, gercek: list, esik: float = 0.5) -> tuple[float, float]:
    """Her gerçek kutu en fazla bir tahminle eşleşir. (kesinlik, duyarlılık)."""
    kullanildi = set()
    dogru = 0
    for t in tahmin:
        adaylar = [(iou(t, g), j) for j, g in enumerate(gercek) if j not in kullanildi]
        if adaylar and max(adaylar)[0] >= esik:
            kullanildi.add(max(adaylar)[1])
            dogru += 1
    return dogru / len(tahmin), dogru / len(gercek)


ORNEK_KUTULAR = [(10, 10, 60, 70), (14, 16, 56, 64), (12, 8, 64, 72), (100, 20, 140, 60), (30, 40, 90, 100)]
ORNEK_PUANLAR = [0.9, 0.7, 0.8, 0.6, 0.3]
ORNEK_GERCEK = [(11, 9, 61, 69), (102, 22, 141, 62), (150, 80, 190, 120)]


def main() -> None:
    print("=== Konvolüsyon + ReLU: desen dedektörleri ===")
    for ad, I in sekiller().items():
        k1 = birinci_katman(I)
        k2 = bulusma_katmani(k1["yatay"], k1["dikey"])
        print(f"  {ad:<12}: yatay en çok {k1['yatay'].max():4.1f}, dikey en çok {k1['dikey'].max():4.1f}, "
              f"buluşma en çok {k2.max():4.1f}")
    print("  1. katman çubukları bulur; 2. katman çizgilerin buluştuğu yerlerde (artı, köşe) yanıt verir.")
    print("  Artıyı köşeden ayırmak için desenlerin uzaysal düzenine bakan bir katman daha gerekir (A9).")
    print("  Alıcı alan (3 × 3, adım 1): " + ", ".join(f"{L}. katman {alici_alan(L)}×{alici_alan(L)}" for L in (1, 2, 3, 4)))

    print("\n=== Kaç pencere? ===")
    for n in (10, 100, 1000):
        print(f"  {n} × {n} görüntü: {dikdortgen_sayisi(n):,} dikdörtgen")
    print(f"  Faster RCNN çapaları, 640 × 480 görüntü, adım 16, 9 kutu: {capa_kutusu_sayisi(640, 480):,}")

    print("\n=== Maksimum olmayanı bastırma ===")
    for i in range(len(ORNEK_KUTULAR)):
        print(f"  kutu {i} {ORNEK_KUTULAR[i]} puan {ORNEK_PUANLAR[i]}, kutu 0 ile IoU {iou(ORNEK_KUTULAR[0], ORNEK_KUTULAR[i]):.2f}")
    kabul = nms(ORNEK_KUTULAR, ORNEK_PUANLAR)
    print(f"  NMS (IoU eşiği 0.5) kabul: {kabul}")
    tahmin = [ORNEK_KUTULAR[i] for i in kabul]
    k, d = degerlendir(tahmin, ORNEK_GERCEK)
    print(f"  Üç gerçek nesneye göre: kesinlik {k:.2f}, duyarlılık {d:.2f}")
    kabul5 = nms(ORNEK_KUTULAR, ORNEK_PUANLAR, en_az=0.5)
    k5, d5 = degerlendir([ORNEK_KUTULAR[i] for i in kabul5], ORNEK_GERCEK)
    print(f"  Puan eşiği 0.5 ile kabul {kabul5}: kesinlik {k5:.2f}, duyarlılık {d5:.2f}")
    k, d = degerlendir(ORNEK_KUTULAR, ORNEK_GERCEK)
    print(f"  NMS olmadan: kesinlik {k:.2f}, duyarlılık {d:.2f} (aynı nesne için fazladan kutular yanlış sayılır)")


if __name__ == "__main__":
    main()
