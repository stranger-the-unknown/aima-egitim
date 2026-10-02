#!/usr/bin/env python3
"""Wumpus dünyasına olasılıkla dönüş (kitaptaki 12.7).

4×4 ızgara, kareler [x, y] (x sütun, y satır; [1,1] sol alt). [1,1] dışındaki her karede
bağımsız olarak 0.2 olasılıkla çukur var. Çukur, komşu karelerde esinti yaratır.
Ajan [1,1]'de esinti yok, [1,2]'de ve [2,1]'de esinti algıladı. Mantık ajanı sıkışır:
[1,3], [2,2], [3,1] güvenli mi bilinmiyor. Olasılık ajanı ise hangisinin daha riskli olduğunu hesaplar.

Kitaptaki sonuçlar (testlerle doğrulanır):
    P(P[1,3] | known, b) ≈ ⟨0.31, 0.69⟩     (simetriyle [3,1] de 0.31)
    P(P[2,2] | known, b) ≈ 0.86

İki yol:
  * tam_toplam   : Bilinmeyen 12 karenin 2^12 = 4096 ataması üzerinden toplam (12.23)
  * sinir_toplami: Yalnızca sınır kareleri (burada 2 kare, 4 terim); diğerleri koşullu
                   bağımsızlıkla hesaptan tamamen çıkar.

Çalıştırma:
    python wumpus_olasilik.py
"""
from __future__ import annotations

import itertools

BOYUT = 4
CUKUR = 0.2
KITAP_GOZLEM = {(1, 1): False, (1, 2): True, (2, 1): True}   # ziyaret edilen kare → esinti var mı?


def komsular(k: tuple[int, int], boyut: int = BOYUT) -> list[tuple[int, int]]:
    x, y = k
    return [(a, b) for a, b in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))
            if 1 <= a <= boyut and 1 <= b <= boyut]


def tutarli(cukurlar: set, gozlem: dict, boyut: int = BOYUT) -> bool:
    """P(b | çukurlar): 1 ya da 0. Her ziyaret edilen karede esinti ⇔ komşularda çukur."""
    return all(esinti == any(n in cukurlar for n in komsular(k, boyut)) for k, esinti in gozlem.items())


def tam_toplam(sorgu, gozlem=KITAP_GOZLEM, p=CUKUR, boyut=BOYUT) -> tuple[float, int]:
    """P(sorgu'da çukur | known, b): bütün bilinmeyen kareler üzerinden toplam.
    Döner: (olasılık, toplamdaki terim sayısı / sorgu değeri)."""
    tum = [(x, y) for x in range(1, boyut + 1) for y in range(1, boyut + 1)]
    bilinmeyen = [k for k in tum if k not in gozlem and k != sorgu]
    ham = {}
    for q in (True, False):
        toplam = 0.0
        for atama in itertools.product((True, False), repeat=len(bilinmeyen)):
            cukurlar = {k for k, v in zip(bilinmeyen, atama) if v} | ({sorgu} if q else set())
            if tutarli(cukurlar, gozlem, boyut):
                n = len(cukurlar)
                toplam += p ** n * (1 - p) ** (len(bilinmeyen) + 1 - n)
        ham[q] = toplam
    return ham[True] / (ham[True] + ham[False]), 2 ** len(bilinmeyen)


def sinir(gozlem=KITAP_GOZLEM, boyut=BOYUT) -> list:
    """Ziyaret edilen karelere komşu, ama ziyaret edilmemiş kareler."""
    return sorted({n for k in gozlem for n in komsular(k, boyut) if n not in gozlem})


def sinir_toplami(sorgu, gozlem=KITAP_GOZLEM, p=CUKUR, boyut=BOYUT, ayrintili=False):
    """P(sorgu) = α P(sorgu) Σ_sınır P(b | known, sorgu, sınır) P(sınır)."""
    s = [k for k in sinir(gozlem, boyut) if k != sorgu]
    ham, modeller = {}, {True: [], False: []}
    for q in (True, False):
        toplam = 0.0
        for atama in itertools.product((True, False), repeat=len(s)):
            cukurlar = {k for k, v in zip(s, atama) if v}
            if tutarli(cukurlar | ({sorgu} if q else set()), gozlem, boyut):
                p_sinir = 1.0
                for v in atama:
                    p_sinir *= p if v else 1 - p
                toplam += p_sinir
                modeller[q].append((sorted(cukurlar), round(p_sinir, 4)))
        ham[q] = (p if q else 1 - p) * toplam
    sonuc = ham[True] / (ham[True] + ham[False])
    return (sonuc, modeller) if ayrintili else sonuc


def main() -> None:
    print("=== Kitaptaki durum: [1,1] esintisiz, [1,2] ve [2,1] esintili ===")
    print(f"  Sınır kareler: {sinir()}")
    for k in sinir():
        tam, terim = tam_toplam(k)
        hizli, modeller = sinir_toplami(k, ayrintili=True)
        print(f"  P(çukur {list(k)}) = {hizli:.2f}   (sınırla; tam toplamda {terim} terim: {tam:.4f})")
        for q in (True, False):
            for cukurlar, p in modeller[q]:
                print(f"      sorgu={'çukur' if q else 'boş  '}  diğer sınırdaki çukurlar {cukurlar!s:<18} P(sınır)={p}")
    print("  Mantık ajanı üç karenin de 'bilinmiyor' olduğunu söyler. Olasılık ajanı [2,2]'den kaçınıp")
    print("  [1,3] ya da [3,1]'i seçer (çukur olasılığı 0.31, önsel 0.2'den yüksek ama 0.86'dan çok düşük).")

    print("\n=== Kendi senaryomuz 1: ajan [1,3]'e gidiyor (çukur yok), esinti algılamıyor ===")
    gozlem = {**KITAP_GOZLEM, (1, 3): False}
    for k in sinir(gozlem):
        print(f"  P(çukur {list(k)}) = {sinir_toplami(k, gozlem):.3f}")
    print("  [1,3]'te esinti yok → komşuları [1,4] ve [2,3] boş. [1,2]'deki esintiyi artık yalnızca")
    print("  [2,2] açıklayabilir: P = 1. [2,1]'in esintisi de [2,2] ile açıklandığı için [3,1] hakkında")
    print("  kanıt kalmadı ve olasılığı önsele (0.2) döner. Buna 'açıklayıp götürme' (explaining away) denir.")

    print("\n=== Kendi senaryomuz 2: ajan [3,1]'e gidiyor (çukur yok), esinti algılıyor ===")
    gozlem = {**KITAP_GOZLEM, (3, 1): True}
    for k in sinir(gozlem):
        print(f"  P(çukur {list(k)}) = {sinir_toplami(k, gozlem):.3f}")
    print("  [2,1]'in esintisini artık yalnızca [2,2] açıklayabilir: P = 1; [1,3] önsele döner.")
    print("  [3,1]'deki esinti için [3,2] ya da [4,1]'de en az bir çukur gerekir: 0.2 / (1 − 0.8²) ≈ 0.556.")


if __name__ == "__main__":
    main()
