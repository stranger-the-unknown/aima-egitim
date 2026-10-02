#!/usr/bin/env python3
"""Alıştırma 7 çözümü: kaygan süpürge dünyası ve döngüsel planlar.

Kaygan dünya: Süpür deterministik; Sağ/Sol bazen ajanı yerinde bırakır.
AND-OR araması döngüsüz bir plan bulamaz. Çünkü "Sağ" sonsuza kadar başarısız
olabilir ve her döngü, döngüsüz arama tarafından başarısızlık sayılır.
Döngüsel plan: [Süpür, D1: Sağ, eğer durum = 5 ise D1'e dön değilse Süpür]
"""
from __future__ import annotations

import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ornekler"))

import and_or_supurge as ao  # noqa: E402


def kaygan_sonuclar(s: int, eylem: str) -> set[int]:
    konum, sol, sag = ao.DURUM[s]
    if eylem == "Sağ":
        return {ao.NUMARA[("R", sol, sag)], s}
    if eylem == "Sol":
        return {ao.NUMARA[("L", sol, sag)], s}
    return {ao.NUMARA[(konum, False, sag) if konum == "L" else (konum, sol, False)]}


def dongusel_plan_uygula(rng: random.Random, kayma: float = 0.5) -> tuple[bool, int]:
    """Durum 1'den döngüsel planı uygula. Döner: (hedefe ulaşıldı mı, Sağ deneme sayısı)."""
    s = 5  # Süpür deterministik: 1 → 5
    deneme = 0
    while s == 5:            # D1: Sağ; eğer durum = 5 ise D1
        deneme += 1
        if rng.random() >= kayma:
            s = 6
    s = 8                    # Süpür: 6 → 8
    return s in ao.HEDEFLER, deneme


def main() -> None:
    print(f"SONUÇLAR(1, Sağ) = {sorted(kaygan_sonuclar(1, 'Sağ'))}   (2: başarılı, 1: kaydı)")
    eski = ao.sonuclar
    ao.sonuclar = kaygan_sonuclar
    try:
        plan = ao.and_or_arama(1)
    finally:
        ao.sonuclar = eski
    print(f"AND-OR araması (döngüsüz) durum 1'den: {'plan yok' if plan is None else ao.plan_metni(plan)}")
    print("Neden? Durum 5'te Sağ'ın sonucu {5, 6}. Ortam her seferinde 5'i seçebilir;"
          "\n5 zaten yolda olduğu için bu dal döngü sayılır ve reddedilir.\n")

    print("Döngüsel plan: [Süpür, D1: Sağ, eğer durum = 5 ise D1'e dön değilse Süpür]")
    rng = random.Random(0)
    denemeler = [dongusel_plan_uygula(rng)[1] for _ in range(10000)]
    print(f"  %50 kayma ile 10.000 koşu: hepsi hedefe ulaştı, ortalama {sum(denemeler) / len(denemeler):.2f} "
          f"Sağ denemesi (beklenen 1/(1−0,5) = 2), en fazla {max(denemeler)}")
    print("Varsayım: Her deneme bağımsızdır ve başarı olasılığı sıfırdan büyüktür, yani eylem"
          "\n'eninde sonunda' başarılı olur. Kilitli bir kapı gibi hep başarısız olan bir eylemde"
          "\ndöngüsel plan sonsuza kadar döner.")


if __name__ == "__main__":
    main()
