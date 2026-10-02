#!/usr/bin/env python3
"""Alıştırma 6 çözümü: hareket cezası eklenince hangi ajan en iyi?

"Temiz zemin" ölçütüne her hareket için −0,5 puan ekliyoruz.
Dürüst (refleks) ajan iş bittikten sonra da gidip geldiği için ceza toplar.
Modele dayalı ajan iki odanın temiz olduğunu bildiğinde durur.
"""
from __future__ import annotations

HAREKET_CEZASI = 0.5


def durust(konum, kirli, _h):
    if kirli:
        return "SUPUR"
    return "SAG" if konum == "A" else "SOL"


def modelli(konum, kirli, h):
    """h = {oda: kirli mi} — yalnızca gördüğümüz odalar kayıtlı."""
    h[konum] = False  # bu oda ya zaten temiz ya da şimdi temizlenecek
    if kirli:
        return "SUPUR"
    diger = "B" if konum == "A" else "A"
    if h.get(diger) is False:
        return "BEKLE"
    return "SAG" if konum == "A" else "SOL"


def simule(ajan, adim=20):
    d = {"konum": "A", "A": True, "B": True}
    h: dict = {}
    puan = 0.0
    for _ in range(adim):
        e = ajan(d["konum"], d[d["konum"]], h)
        if e == "SUPUR":
            d[d["konum"]] = False
        elif e in ("SAG", "SOL"):
            d["konum"] = "B" if e == "SAG" else "A"
            puan -= HAREKET_CEZASI
        puan += (not d["A"]) + (not d["B"])
    return puan


def main():
    print(f"Ölçüt: her adımda temiz oda başına +1, her hareket için −{HAREKET_CEZASI}\n")
    for ad, ajan in [("dürüst (refleks)", durust), ("modele dayalı", modelli)]:
        print(f"  {ad:<18} → {simule(ajan):6.1f} puan")
    print(
        "\nHareket cezası eklenince refleks ajanı artık rasyonel değil: iş bittikten"
        "\nsonra gidip gelmek puan kaybettiriyor. Modele dayalı ajan diğer odanın temiz"
        "\nolduğunu hatırladığı için bekler ve daha yüksek puan alır."
    )


if __name__ == "__main__":
    main()
