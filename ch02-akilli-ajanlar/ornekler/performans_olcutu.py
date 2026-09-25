#!/usr/bin/env python3
"""Performans ölçütü tuzağı: ajan, ölçtüğünüz şeyi en iyiler, istediğiniz şeyi değil.

Süpürge dünyasına bir eylem ekliyoruz: DOK (süpürgenin haznesini yere boşalt).
İki ajan ve iki ölçüt karşılaştırılıyor:

Ajanlar
  * dürüst ajan: kirliyse süpürür, temizse diğer odaya geçer (basit refleks)
  * hileci ajan: temiz odada tozu geri döker, sonra hemen tekrar süpürür

Ölçütler
  * "süpürülen toz" ölçütü : her başarılı süpürme +1 puan
  * "temiz zemin" ölçütü   : her adımda, temiz olan her oda için +1 puan

Kitaptaki genel ilke: Performans ölçütünü, ajanın *nasıl davranması gerektiğine*
göre değil, *ortamda gerçekte ne olmasını istediğinize* göre tasarlayın.

Çalıştırma:
    python performans_olcutu.py
"""
from __future__ import annotations

from typing import Callable

ODALAR = ("A", "B")
Durum = dict  # {"konum": "A", "A": True/False (kirli mi), "B": ...}
Ajan = Callable[[str, bool, dict], str]


def durust_ajan(konum: str, kirli: bool, _hafiza: dict) -> str:
    if kirli:
        return "SUPUR"
    return "SAG" if konum == "A" else "SOL"


def hileci_ajan(konum: str, kirli: bool, hafiza: dict) -> str:
    """Kirliyse süpür; temizse tozu geri dök (böylece bir sonraki adımda yine süpürebilir)."""
    if kirli:
        hafiza["hazne_dolu"] = True
        return "SUPUR"
    if hafiza.get("hazne_dolu"):
        hafiza["hazne_dolu"] = False
        return "DOK"
    return "SAG" if konum == "A" else "SOL"


def simule(ajan: Ajan, adim: int = 20) -> dict[str, int]:
    """Ajanı çalıştır; iki ölçütü birlikte hesapla."""
    d: Durum = {"konum": "A", "A": True, "B": True}
    hafiza: dict = {}
    supurulen = temiz_puan = 0
    for _ in range(adim):
        eylem = ajan(d["konum"], d[d["konum"]], hafiza)
        if eylem == "SUPUR" and d[d["konum"]]:
            d[d["konum"]] = False
            supurulen += 1
        elif eylem == "DOK":
            d[d["konum"]] = True
        elif eylem == "SAG":
            d["konum"] = "B"
        elif eylem == "SOL":
            d["konum"] = "A"
        temiz_puan += sum(not d[o] for o in ODALAR)
    return {"supurulen_toz": supurulen, "temiz_zemin": temiz_puan}


def main() -> None:
    adim = 20
    print(f"Süpürge dünyası, {adim} adım, başlangıçta iki oda da kirli\n")
    print(f"{'Ajan':<14}{'süpürülen toz':>16}{'temiz zemin':>14}")
    sonuclar = {ad: simule(ajan, adim) for ad, ajan in
                [("dürüst", durust_ajan), ("hileci", hileci_ajan)]}
    for ad, s in sonuclar.items():
        print(f"{ad:<14}{s['supurulen_toz']:>16}{s['temiz_zemin']:>14}")

    kazanan_toz = max(sonuclar, key=lambda a: sonuclar[a]["supurulen_toz"])
    kazanan_zemin = max(sonuclar, key=lambda a: sonuclar[a]["temiz_zemin"])
    print(f"\n'Süpürülen toz' ölçütünün kazananı: {kazanan_toz}")
    print(f"'Temiz zemin' ölçütünün kazananı : {kazanan_zemin}")
    print(
        "\nDers: 'Ne kadar toz süpürdün?' diye ölçerseniz, tozu döküp tekrar süpüren"
        "\najan 'rasyonel' olur. İstediğimiz şey temiz bir zemin olduğu için ölçüt de"
        "\nzeminin durumunu ölçmelidir."
    )


if __name__ == "__main__":
    main()
