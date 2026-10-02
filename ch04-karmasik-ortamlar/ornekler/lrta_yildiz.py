#!/usr/bin/env python3
"""Çevrimiçi arama: LRTA* (öğrenen gerçek zamanlı A*).

Çevrimiçi ajan önce planlayıp sonra uygulamaz; **hareket ederek** öğrenir.
LRTA* her durum için bir maliyet tahmini H(s) tutar (başta H = h) ve her adımda:

    1. Komşulara bakar: maliyet(s, a, s') + H(s') en küçük olan eylemi seçer.
    2. Ayrıldığı durumun tahminini günceller: H(s) ← min_a [maliyet + H(s')]
       Böylece yerel minimumlar zamanla "doldurulur" ve ajan oradan kurtulur.
    3. Hiç denenmemiş bir eylemin sonucunu bilmiyorsa **iyimser** davranır:
       o eylemin doğrudan hedefe h(s) maliyetle götürdüğünü varsayar.

Bölüm 1: Kitaptaki tek boyutlu örnek. H = 8 9 2 2 4 3 ile başlar; ajan
         yerel minimumda ileri geri gidip tahminleri 3, 4, 5, 5'e yükseltir.
Bölüm 2: Haritası bilinmeyen bir labirentte tekrarlanan denemeler. Ajan her
         denemede H'yi daha iyi öğrenir ve yol uzunluğu optimale yaklaşır.

Çalıştırma:
    python lrta_yildiz.py
"""
from __future__ import annotations


# ---------------------------------------------------------------------------
# Bölüm 1: kitaptaki tek boyutlu örnek (komşuluk bilinir, H öğrenilir)
# ---------------------------------------------------------------------------

def tek_boyut_ornegi(adim: int = 4) -> list[tuple[list[int], int]]:
    """Durumlar: 0..5 (tahminler 8 9 2 2 4 3), 6 = hedef (H = 0). Kenar maliyeti 1.

    Döner: her adımdan önceki (H listesi, ajanın konumu).
    """
    H = [8, 9, 2, 2, 4, 3, 0]
    s = 2  # ajan, düz bir yerel minimumda
    iz = [(H[:6], s)]
    for _ in range(adim):
        komsular = [k for k in (s - 1, s + 1) if 0 <= k <= 6]
        maliyet = {k: 1 + H[k] for k in komsular}
        H[s] = min(maliyet.values())          # ayrılmadan önce tahmini güncelle
        s = min(komsular, key=maliyet.get)    # görünüşte en iyi komşuya git
        iz.append((H[:6], s))
    return iz


# ---------------------------------------------------------------------------
# Bölüm 2: bilinmeyen labirentte gerçek LRTA*-AJANI
# ---------------------------------------------------------------------------

LABIRENT = [
    "S....#....",
    ".###.#.##.",
    ".#...#..#.",
    ".#.###..#.",
    ".#......#G",
]
YONLER = {"K": (-1, 0), "G": (1, 0), "B": (0, -1), "D": (0, 1)}


def bul(harf: str) -> tuple[int, int]:
    for r, satir in enumerate(LABIRENT):
        if harf in satir:
            return r, satir.index(harf)
    raise ValueError(harf)


BASLANGIC, HEDEF = bul("S"), bul("G")


def gercek_sonuc(s, eylem):
    """Ortamın fiziği: duvara çarpan eylem yerinde bırakır. Ajan bunu BİLMEZ,
    ancak eylemi deneyince öğrenir."""
    r, c = s
    dr, dc = YONLER[eylem]
    r2, c2 = r + dr, c + dc
    if 0 <= r2 < len(LABIRENT) and 0 <= c2 < len(LABIRENT[0]) and LABIRENT[r2][c2] != "#":
        return r2, c2
    return s


def h(s) -> int:
    """Manhattan uzaklığı: duvarları bilmediği için iyimser (kabul edilebilir)."""
    return abs(s[0] - HEDEF[0]) + abs(s[1] - HEDEF[1])


class LRTAAjani:
    """Kitaptaki LRTA*-AGENT'ın doğrudan karşılığı. `sonuc` ve `H` denemeler arasında korunur."""

    def __init__(self, sezgisel=None) -> None:
        self.h = sezgisel or h                # varsayılan: Manhattan uzaklığı
        self.sonuc: dict[tuple, tuple] = {}   # öğrenilen harita: (s, a) → s'
        self.H: dict[tuple, float] = {}
        self.onceki = None                    # (s, a)

    def maliyet(self, s, a) -> float:
        s2 = self.sonuc.get((s, a))
        if s2 is None:
            return self.h(s)     # denenmemiş eylem: iyimser varsayım
        return 1 + self.H[s2]

    def __call__(self, s):
        if s == HEDEF:
            self.onceki = None
            return None
        self.H.setdefault(s, self.h(s))
        if self.onceki is not None:
            s0, a0 = self.onceki
            self.sonuc[(s0, a0)] = s
            self.H[s0] = min(self.maliyet(s0, b) for b in YONLER)
        a = min(YONLER, key=lambda b: self.maliyet(s, b))
        self.onceki = (s, a)
        return a


def deneme(ajan: LRTAAjani, sinir: int = 1000) -> int:
    s, adim = BASLANGIC, 0
    while adim < sinir:
        a = ajan(s)
        if a is None:
            return adim
        s = gercek_sonuc(s, a)
        adim += 1
    return adim


def optimal_uzunluk() -> int:
    """Karşılaştırma için: haritayı bilen BFS."""
    from collections import deque
    sinir, gor = deque([(BASLANGIC, 0)]), {BASLANGIC}
    while sinir:
        s, d = sinir.popleft()
        if s == HEDEF:
            return d
        for a in YONLER:
            s2 = gercek_sonuc(s, a)
            if s2 not in gor:
                gor.add(s2)
                sinir.append((s2, d + 1))
    return -1


def main() -> None:
    print("=== Bölüm 1: kitaptaki tek boyutlu örnek ===")
    print("(her durumda H tahmini; [ ] ajanın konumu; en sağdaki komşu hedef)\n")
    for i, (H, s) in enumerate(tek_boyut_ornegi()):
        hucreler = [f"[{v}]" if j == s else f" {v} " for j, v in enumerate(H)]
        print(f"  ({'abcde'[i]})  " + " ".join(hucreler))
    print("\nAjan yerel minimumda ileri geri gidip H'yi 2 → 3 → 5 ve 2 → 4 → 5 yaptı,"
          "\nböylece minimumu 'düzleştirip' sağa kaçtı (kitaptaki şekille aynı).")

    print("\n=== Bölüm 2: haritası bilinmeyen labirent ===")
    for satir in LABIRENT:
        print("  " + " ".join(satir))
    ajan = LRTAAjani()
    print(f"\nOptimal yol uzunluğu (haritayı bilen BFS): {optimal_uzunluk()}")
    for i in range(1, 13):
        print(f"  {i}. deneme: {deneme(ajan):3d} adım")
    print("\nİlk denemede ajan duvarlara çarparak öğrenir ve uzun yollara sapar. Harita ve H"
          "\ndenemeler arasında korunur. Denenmemiş eylemlere iyimser davrandığı için arada"
          "\nuzun 'keşif' denemeleri de olur. Birkaç denemeden sonra her seferinde optimal"
          "\nyolu izler: H artık gerçek maliyeti öğrenmiştir.")


if __name__ == "__main__":
    main()
