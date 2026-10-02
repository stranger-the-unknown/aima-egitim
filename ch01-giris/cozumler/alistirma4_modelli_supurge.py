#!/usr/bin/env python3
"""Alıştırma 4 çözümü: basit refleks ajanı ile modele dayalı ajanı karşılaştır.

Modele dayalı ajan, her odanın en son gördüğü durumunu hatırlar.
İki odanın da temiz olduğunu *biliyorsa* hareket etmez (Bekle).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ornekler"))

from vacuum_agent import Durum, Eylem, Konum, Ortam, basit_refleks_ajan  # noqa: E402


class ModelliAjan:
    """İç durum: {oda: bilinen durum}. Başta hiçbir şey bilinmiyor (None)."""

    def __init__(self) -> None:
        self.model: dict[Konum, Durum | None] = {Konum.A: None, Konum.B: None}

    def __call__(self, algi: tuple[Konum, Durum]) -> Eylem:
        konum, durum = algi
        self.model[konum] = durum          # gördüğünü kaydet
        if durum == Durum.KIRLI:
            self.model[konum] = Durum.TEMIZ  # süpüreceğim → temiz olacak
            return Eylem.SUPUR
        if all(d == Durum.TEMIZ for d in self.model.values()):
            return Eylem.BEKLE              # her şeyin temiz olduğunu biliyorum
        return Eylem.SAG if konum == Konum.A else Eylem.SOL


def calistir(ajan, adim: int = 10) -> tuple[int, int, bool]:
    """(hareket sayısı, süpürme sayısı, sonda her şey temiz mi) döndür."""
    ortam = Ortam(ajan_konumu=Konum.A, odalar={Konum.A: Durum.KIRLI, Konum.B: Durum.KIRLI})
    hareket = supurme = 0
    for _ in range(adim):
        eylem = ajan(ortam.algila())
        hareket += eylem in (Eylem.SOL, Eylem.SAG)
        supurme += eylem == Eylem.SUPUR
        ortam.uygula(eylem)
    return hareket, supurme, ortam.her_sey_temiz()


def main() -> None:
    print("10 adım, başlangıç: A=Kirli, B=Kirli, ajan A'da\n")
    print(f"{'Ajan':<16} {'hareket':>8} {'süpürme':>8} {'temiz mi':>9}")
    for ad, ajan in [("basit refleks", basit_refleks_ajan), ("modele dayalı", ModelliAjan())]:
        h, s, t = calistir(ajan)
        print(f"{ad:<16} {h:>8} {s:>8} {str(t):>9}")
    print(
        "\nİki ajan da odaları temizler. Ama refleks ajanı iş bittikten sonra da gidip gelir"
        "\n(her hareket enerji harcar). Modele dayalı ajan, *görmediği* odanın durumunu"
        "\nhafızasından bildiği için durabilir. Tek bir algı 'diğer oda temiz mi?' sorusunu"
        "\nyanıtlamaya yetmez; bu yüzden bellek gerekir."
    )


if __name__ == "__main__":
    main()
