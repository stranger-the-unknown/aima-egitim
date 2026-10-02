#!/usr/bin/env python3
"""Hiyerarşik planlama: üst düzey eylemler (HLA) ve inceltmeler.

Kitaptaki fikir: "Havalimanına git" gibi bir üst düzey eylemin birkaç **inceltmesi**
vardır. Her inceltme, daha alt düzey eylemlerden oluşan bir dizidir. Plan, yalnızca
ilkel (doğrudan uygulanabilir) eylemler kalana kadar inceltilir.

    Git(Ev, Havalimanı) → [Sür(Ev, UzunSüreliOtopark), Servis(UzunSüreliOtopark, Havalimanı)]
                        | [Taksi(Ev, Havalimanı)]
    Yürü((x,y), (x',y')) → [] (zaten oradaysa)
                         | [Sağ, Yürü(...)] | [Sol, …] | [Yukarı, …] | [Aşağı, …]

HIERARCHICAL-SEARCH (genişlik öncelikli): Kuyrukta planlar var. İlk HLA'yı bul, onun
her inceltmesiyle yeni planlar üret. HLA kalmadıysa plan ilkel eylemlerden oluşur;
başlangıçtan uygulanabiliyor ve hedefi sağlıyorsa çözümdür.

Çalıştırma:
    python hiyerarsik_plan.py
"""
from __future__ import annotations

from collections import deque

# İlkel eylemler: (önkoşul(durum) → bool, etki(durum) → yeni durum)
ILKEL = {
    "Sür(Ev,Otopark)": (lambda d: d["araba"] and d["yer"] == "Ev",
                        lambda d: {**d, "yer": "Otopark"}),
    "Servis(Otopark,Havalimanı)": (lambda d: d["yer"] == "Otopark",
                                   lambda d: {**d, "yer": "Havalimanı"}),
    "Taksi(Ev,Havalimanı)": (lambda d: d["yer"] == "Ev" and d["nakit"] >= 50,
                             lambda d: {**d, "yer": "Havalimanı", "nakit": d["nakit"] - 50}),
}

INCELTMELER = {
    "Git(Ev,Havalimanı)": [
        ["Sür(Ev,Otopark)", "Servis(Otopark,Havalimanı)"],
        ["Taksi(Ev,Havalimanı)"],
    ],
}


def hiyerarsik_ara(baslangic: dict, hedef, ust: list[str], ilkel=ILKEL, inceltmeler=INCELTMELER,
                   derinlik_siniri: int = 50):
    """Döner: (ilkel plan ya da None, denenen plan sayısı)."""
    kuyruk = deque([ust])
    denenen = 0
    while kuyruk:
        plan = kuyruk.popleft()
        denenen += 1
        hla_indeksi = next((i for i, e in enumerate(plan) if e not in ilkel), None)
        if hla_indeksi is None:
            d = dict(baslangic)
            gecerli = True
            for e in plan:
                on, etki = ilkel[e]
                if not on(d):
                    gecerli = False
                    break
                d = etki(d)
            if gecerli and hedef(d):
                return plan, denenen
            continue
        if len(plan) > derinlik_siniri:
            continue
        hla = plan[hla_indeksi]
        for inceltme in inceltmeler(hla) if callable(inceltmeler) else inceltmeler.get(hla, []):
            kuyruk.append(plan[:hla_indeksi] + inceltme + plan[hla_indeksi + 1:])
    return None, denenen


# --- Yürü: özyineli inceltme (ızgarada gezinme) ---------------------------
YON = {"Sağ": (1, 0), "Sol": (-1, 0), "Yukarı": (0, 1), "Aşağı": (0, -1)}
DUVARLAR = {(1, 0), (1, 1)}
BOYUT = 3


def izgara_ilkel():
    def hareket(dx, dy):
        def on(d):
            x, y = d["konum"][0] + dx, d["konum"][1] + dy
            return 0 <= x < BOYUT and 0 <= y < BOYUT and (x, y) not in DUVARLAR
        return on, lambda d: {**d, "konum": (d["konum"][0] + dx, d["konum"][1] + dy)}
    return {ad: hareket(*v) for ad, v in YON.items()}


def yuru_inceltmeleri(hla: str) -> list[list[str]]:
    """"Yürü": ya dur (boş inceltme) ya bir adım at ve yürümeye devam et."""
    return [[]] + [[ad, hla] for ad in YON]


def main() -> None:
    hedef = lambda d: d["yer"] == "Havalimanı"  # noqa: E731
    print("=== Git(Ev, Havalimanı) ===")
    for durum in ({"yer": "Ev", "araba": True, "nakit": 0},
                  {"yer": "Ev", "araba": False, "nakit": 100},
                  {"yer": "Ev", "araba": False, "nakit": 10}):
        plan, n = hiyerarsik_ara(durum, hedef, ["Git(Ev,Havalimanı)"])
        print(f"  araba={durum['araba']!s:<5} nakit={durum['nakit']:>3} → {plan or 'plan yok'}  ({n} plan denendi)")

    print("\n=== Yürü((0,0) → (2,1)), özyineli inceltme; (1,0) ve (1,1) duvar ===")
    ilkel = izgara_ilkel()
    plan, n = hiyerarsik_ara({"konum": (0, 0)}, lambda d: d["konum"] == (2, 1), ["Yürü"],
                             ilkel=ilkel, inceltmeler=yuru_inceltmeleri, derinlik_siniri=8)
    print(f"  Plan: {plan}  ({n} plan denendi)")
    print("  Genişlik öncelikli olduğu için en az adımlı ilkel plan bulunur. Üst düzey"
          "\n  eylemler arama uzayını 'anlamlı' planlarla sınırlar: Bir insan seyahati planlarken"
          "\n  kas hareketlerini değil, 'taksiye bin' gibi adımları düşünür.")


if __name__ == "__main__":
    main()
