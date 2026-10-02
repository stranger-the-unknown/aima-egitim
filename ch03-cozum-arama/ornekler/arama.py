#!/usr/bin/env python3
"""Bölüm 3'ün arama algoritmaları: tek bir çerçevede, okunaklı hâlde.

Kitabın 4. baskısı çoğu algoritmayı tek bir iskeletin çeşitleri olarak sunar:
**en iyi öncelikli arama** (best-first search). Sınırdan (frontier) her seferinde
f(n) değeri en küçük düğüm çıkarılır; f seçimine göre farklı algoritmalar çıkar:

    f(n) = g(n)            → tekdüze maliyet araması (UCS, Dijkstra)
    f(n) = h(n)            → açgözlü en iyi öncelikli arama
    f(n) = g(n) + h(n)     → A*
    f(n) = g(n) + W·h(n)   → ağırlıklı A* (W > 1: daha hızlı, optimal değil)

Genişlik öncelikli arama (BFS) ve yinelemeli derinleşme (IDS) ayrı yazılmıştır,
çünkü ikisi de öncelik kuyruğu yerine daha basit ve daha hızlı yapılar kullanır.

Bu dosya bir kütüphanedir. Çalıştırınca küçük bir kendi kendini sınama yapar:
    python arama.py
Asıl örnekler: romania_arama.py, sekiz_bulmaca.py
"""
from __future__ import annotations

import heapq
import itertools
import math
from collections import deque
from dataclasses import dataclass, field
from typing import Any, Callable, Hashable, Iterator, Optional

Durum = Hashable
Eylem = Any


# ---------------------------------------------------------------------------
# Problem ve düğüm
# ---------------------------------------------------------------------------

class Problem:
    """Arama problemi: başlangıç, eylemler, geçiş modeli, hedef testi, maliyet.

    Alt sınıflar `eylemler` ve `sonuc` fonksiyonlarını yazmak zorundadır.
    """

    def __init__(self, baslangic: Durum, hedef: Optional[Durum] = None) -> None:
        self.baslangic = baslangic
        self.hedef = hedef

    def eylemler(self, durum: Durum) -> Iterator[Eylem]:
        raise NotImplementedError

    def sonuc(self, durum: Durum, eylem: Eylem) -> Durum:
        raise NotImplementedError

    def hedef_mi(self, durum: Durum) -> bool:
        return durum == self.hedef

    def eylem_maliyeti(self, durum: Durum, eylem: Eylem, sonraki: Durum) -> float:
        return 1

    def h(self, dugum: "Dugum") -> float:
        """Sezgisel fonksiyon. Varsayılan: 0 (bilgisiz)."""
        return 0


@dataclass(eq=False)
class Dugum:
    """Arama ağacındaki bir düğüm. Durumla karıştırma: aynı duruma giden farklı
    yollar farklı düğümlerdir."""

    durum: Durum
    ebeveyn: Optional["Dugum"] = None
    eylem: Eylem = None
    g: float = 0.0  # yol maliyeti: başlangıçtan bu düğüme
    derinlik: int = field(default=0)

    def __repr__(self) -> str:
        return f"<Dugum {self.durum} g={self.g}>"


def genislet(problem: Problem, dugum: Dugum) -> Iterator[Dugum]:
    """Düğümün çocuklarını üret."""
    s = dugum.durum
    for eylem in problem.eylemler(s):
        s2 = problem.sonuc(s, eylem)
        maliyet = dugum.g + problem.eylem_maliyeti(s, eylem, s2)
        yield Dugum(s2, dugum, eylem, maliyet, dugum.derinlik + 1)


def yol_durumlari(dugum: Optional[Dugum]) -> list:
    yol = []
    while dugum is not None:
        yol.append(dugum.durum)
        dugum = dugum.ebeveyn
    return yol[::-1]


def yol_eylemleri(dugum: Optional[Dugum]) -> list:
    eylemler = []
    while dugum is not None and dugum.ebeveyn is not None:
        eylemler.append(dugum.eylem)
        dugum = dugum.ebeveyn
    return eylemler[::-1]


@dataclass
class Sonuc:
    """Bir aramanın sonucu ve maliyet istatistikleri."""

    algoritma: str
    dugum: Optional[Dugum]
    genisletilen: int = 0   # çocukları üretilen düğüm sayısı
    uretilen: int = 0       # oluşturulan toplam düğüm sayısı
    en_buyuk_sinir: int = 0  # bellek göstergesi: sınırın ulaştığı en büyük boyut

    @property
    def basarili(self) -> bool:
        return self.dugum is not None

    @property
    def maliyet(self) -> float:
        return self.dugum.g if self.dugum else math.inf

    @property
    def yol(self) -> list:
        return yol_durumlari(self.dugum)

    @property
    def eylemler(self) -> list:
        return yol_eylemleri(self.dugum)


# ---------------------------------------------------------------------------
# En iyi öncelikli arama ailesi
# ---------------------------------------------------------------------------

def en_iyi_oncelikli(problem: Problem, f: Callable[[Dugum], float], ad: str = "en iyi öncelikli",
                     izle: Optional[Callable[[Dugum, float], None]] = None) -> Sonuc:
    """Kitaptaki BEST-FIRST-SEARCH'ün doğrudan karşılığı.

    * `sinir`: f değerine göre sıralı öncelik kuyruğu
    * `ulasilan`: her durum için bilinen en iyi düğüm (graf araması: tekrarlanan
      durumları eleriz, ama daha ucuz bir yol bulursak güncelleriz)
    * Hedef testi, düğüm kuyruktan **çıkarken** yapılır. Bu, UCS ve A*'ın
      optimalliği için gereklidir.
    * `izle(dugum, f)`: verilirse kuyruktan çıkan her düğüm için çağrılır
      (algoritmanın hangi sırayla ilerlediğini görmek için).
    """
    sayac = itertools.count()  # eşit f değerlerinde FIFO sırası için
    kok = Dugum(problem.baslangic)
    sinir = [(f(kok), next(sayac), kok)]
    ulasilan = {problem.baslangic: kok}
    sonuc = Sonuc(ad, None, uretilen=1)
    while sinir:
        sonuc.en_buyuk_sinir = max(sonuc.en_buyuk_sinir, len(sinir))
        f_deger, _, dugum = heapq.heappop(sinir)
        if dugum is not ulasilan.get(dugum.durum):
            continue  # bu durum için sonradan daha iyi bir yol bulunmuştu: eski kayıt
        if izle:
            izle(dugum, f_deger)
        if problem.hedef_mi(dugum.durum):
            sonuc.dugum = dugum
            return sonuc
        sonuc.genisletilen += 1
        for cocuk in genislet(problem, dugum):
            sonuc.uretilen += 1
            s = cocuk.durum
            if s not in ulasilan or cocuk.g < ulasilan[s].g:
                ulasilan[s] = cocuk
                heapq.heappush(sinir, (f(cocuk), next(sayac), cocuk))
    return sonuc


def tekduze_maliyet(problem: Problem, izle=None) -> Sonuc:
    return en_iyi_oncelikli(problem, lambda n: n.g, "UCS", izle)


def acgozlu(problem: Problem, h: Optional[Callable[[Dugum], float]] = None, izle=None) -> Sonuc:
    h = h or problem.h
    return en_iyi_oncelikli(problem, h, "Açgözlü", izle)


def a_yildiz(problem: Problem, h: Optional[Callable[[Dugum], float]] = None, izle=None) -> Sonuc:
    h = h or problem.h
    return en_iyi_oncelikli(problem, lambda n: n.g + h(n), "A*", izle)


def agirlikli_a_yildiz(problem: Problem, W: float = 1.5,
                       h: Optional[Callable[[Dugum], float]] = None) -> Sonuc:
    h = h or problem.h
    return en_iyi_oncelikli(problem, lambda n: n.g + W * h(n), f"A* (W={W})")


# ---------------------------------------------------------------------------
# Bilgisiz aramanın diğer üyeleri
# ---------------------------------------------------------------------------

def genislik_oncelikli(problem: Problem) -> Sonuc:
    """BFS: FIFO kuyruğu ve **erken hedef testi** (çocuk üretilirken).

    Erken test güvenlidir, çünkü BFS en sığ hedefi zaten ilk bulur.
    Birim maliyetli problemlerde optimaldir, genel maliyetlerde değildir.
    """
    sonuc = Sonuc("BFS", None, uretilen=1)
    kok = Dugum(problem.baslangic)
    if problem.hedef_mi(kok.durum):
        sonuc.dugum = kok
        return sonuc
    sinir = deque([kok])
    ulasilan = {problem.baslangic}
    while sinir:
        sonuc.en_buyuk_sinir = max(sonuc.en_buyuk_sinir, len(sinir))
        dugum = sinir.popleft()
        sonuc.genisletilen += 1
        for cocuk in genislet(problem, dugum):
            sonuc.uretilen += 1
            if problem.hedef_mi(cocuk.durum):
                sonuc.dugum = cocuk
                return sonuc
            if cocuk.durum not in ulasilan:
                ulasilan.add(cocuk.durum)
                sinir.append(cocuk)
    return sonuc


KESILDI = "kesildi"  # derinlik sınırına takıldı (daha derinde çözüm olabilir)


def _dongu_mu(dugum: Dugum) -> bool:
    """Düğümün durumu, kendi yolunda daha önce geçti mi? (yalnızca yolu kontrol eder)"""
    s, ata = dugum.durum, dugum.ebeveyn
    while ata is not None:
        if ata.durum == s:
            return True
        ata = ata.ebeveyn
    return False


def derinlik_sinirli(problem: Problem, sinir_derinlik: int, _sonuc: Optional[Sonuc] = None):
    """DLS: derinlik öncelikli arama, `sinir_derinlik` üstüne inmez.

    Ağaç benzeri arama: `ulasilan` tablosu tutmaz, yalnızca mevcut yoldaki
    döngüleri keser. Bu sayede bellek O(b·ℓ) kalır.
    Döndürür: hedef düğümü, `KESILDI` ya da None (bu sınır içinde çözüm yok).
    """
    sonuc = _sonuc or Sonuc(f"DLS(ℓ={sinir_derinlik})", None)
    yigin = [Dugum(problem.baslangic)]
    cevap: Any = None
    while yigin:
        sonuc.en_buyuk_sinir = max(sonuc.en_buyuk_sinir, len(yigin))
        dugum = yigin.pop()
        if problem.hedef_mi(dugum.durum):
            return dugum
        if dugum.derinlik >= sinir_derinlik:
            cevap = KESILDI
            continue
        if _dongu_mu(dugum):
            continue
        sonuc.genisletilen += 1
        cocuklar = list(genislet(problem, dugum))
        sonuc.uretilen += len(cocuklar)
        yigin.extend(reversed(cocuklar))  # ilk eylem önce denensin
    return cevap


def yinelemeli_derinlesme(problem: Problem, en_fazla: int = 100) -> Sonuc:
    """IDS: ℓ = 0, 1, 2, … için DLS. BFS'in optimalliği + DFS'in az belleği."""
    sonuc = Sonuc("IDS", None)
    for limit in range(en_fazla + 1):
        cevap = derinlik_sinirli(problem, limit, sonuc)
        if cevap is not KESILDI:
            sonuc.dugum = cevap if isinstance(cevap, Dugum) else None
            return sonuc
    return sonuc


def derinlik_oncelikli(problem: Problem) -> Sonuc:
    """DFS (graf araması sürümü): LIFO yığını ve `ulasilan` kümesi.

    Sonlu durum uzaylarında tamdır ama optimal değildir. Bulduğu ilk yolu döndürür.
    """
    sonuc = Sonuc("DFS", None, uretilen=1)
    yigin = [Dugum(problem.baslangic)]
    ulasilan = {problem.baslangic}
    while yigin:
        sonuc.en_buyuk_sinir = max(sonuc.en_buyuk_sinir, len(yigin))
        dugum = yigin.pop()
        if problem.hedef_mi(dugum.durum):
            sonuc.dugum = dugum
            return sonuc
        sonuc.genisletilen += 1
        cocuklar = [c for c in genislet(problem, dugum) if c.durum not in ulasilan]
        sonuc.uretilen += len(cocuklar)
        for c in cocuklar:
            ulasilan.add(c.durum)
        yigin.extend(reversed(cocuklar))
    return sonuc


# ---------------------------------------------------------------------------
# Bellek sınırlı bilgili arama: IDA*
# ---------------------------------------------------------------------------

def ida_yildiz(problem: Problem, h: Optional[Callable[[Dugum], float]] = None) -> Sonuc:
    """IDA*: IDS'teki derinlik sınırı yerine f = g + h sınırı kullanır.

    Her turda, sınırı aşan düğümler arasındaki en küçük f değeri bir sonraki
    turun sınırı olur. Bellek kullanımı yalnızca mevcut yol kadardır.
    """
    h = h or problem.h
    sonuc = Sonuc("IDA*", None)
    kok = Dugum(problem.baslangic)
    esik = h(kok)

    def ara(dugum: Dugum, yol: set) -> tuple[Optional[Dugum], float]:
        f = dugum.g + h(dugum)
        if f > esik:
            return None, f
        if problem.hedef_mi(dugum.durum):
            return dugum, f
        sonuc.genisletilen += 1
        en_kucuk = math.inf
        for cocuk in genislet(problem, dugum):
            sonuc.uretilen += 1
            if cocuk.durum in yol:
                continue
            yol.add(cocuk.durum)
            bulunan, yeni_esik = ara(cocuk, yol)
            yol.remove(cocuk.durum)
            if bulunan:
                return bulunan, yeni_esik
            en_kucuk = min(en_kucuk, yeni_esik)
        return None, en_kucuk

    while True:
        bulunan, yeni_esik = ara(kok, {kok.durum})
        if bulunan:
            sonuc.dugum = bulunan
            return sonuc
        if yeni_esik == math.inf:
            return sonuc
        esik = yeni_esik


# ---------------------------------------------------------------------------
# Yardımcılar
# ---------------------------------------------------------------------------

def etkin_dallanma(N: int, d: int, tolerans: float = 1e-6) -> float:
    """N + 1 = 1 + b* + b*² + … + b*^d denklemini b* için çöz (ikiye bölme)."""
    if d == 0:
        return float("nan")

    def toplam(b: float) -> float:
        return d + 1 if abs(b - 1) < 1e-12 else (b ** (d + 1) - 1) / (b - 1)

    alt, ust = 1.0, max(2.0, float(N))
    while ust - alt > tolerans:
        orta = (alt + ust) / 2
        if toplam(orta) < N + 1:
            alt = orta
        else:
            ust = orta
    return (alt + ust) / 2


if __name__ == "__main__":
    class Sayi(Problem):
        """Oyuncak problem: 1'den başla, +1 veya ×2 ile hedefe ulaş."""

        def eylemler(self, s):
            return ["+1", "×2"]

        def sonuc(self, s, a):
            return s + 1 if a == "+1" else s * 2

        def h(self, n):
            return 0

    p = Sayi(1, 10)
    for algoritma in (genislik_oncelikli, tekduze_maliyet, yinelemeli_derinlesme):
        s = algoritma(p)
        print(f"{s.algoritma:5s}: {s.yol}  eylemler={s.eylemler}  genişletilen={s.genisletilen}")
    print(f"b*(N=52, d=5) = {etkin_dallanma(52, 5):.2f}  (kitaptaki klasik örnek: 1.92)")
