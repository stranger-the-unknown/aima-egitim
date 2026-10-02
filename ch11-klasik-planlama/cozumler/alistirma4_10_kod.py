#!/usr/bin/env python3
"""Bölüm 11 alıştırmaları A4, A6–A10: kodlu çözümler.

Çalıştırma (bölüm klasöründen):
    python cozumler/alistirma4_10_kod.py
"""
from __future__ import annotations

import sys
from collections import deque
from dataclasses import replace
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "ornekler"))

import hiyerarsik_plan as hp  # noqa: E402
import kitap_problemleri as kp  # noqa: E402
import kritik_yol as ky  # noqa: E402
from planlama import (Planlama, Sema, atomlar, h_add, h_hedef_sayisi, h_max,  # noqa: E402
                      h_seviye_toplami, ileri_ara, temellendir)


# --- A4: yedek lastikte negatif önkoşulu unutmak --------------------------
def a4_negatifsiz_lastik() -> list[str]:
    """PutOn'un ¬At(Flat,Axle) önkoşulu silinirse planlayıcı ne bulur?"""
    p = kp.yedek_lastik()
    eylemler = [replace(e, on_degil=frozenset()) if e.ad.startswith("PutOn") else e for e in p.eylemler]
    return ileri_ara(Planlama(p.baslangic, p.hedef, eylemler)).plan


# --- A6: h_add'in fazla tahmin ettiği bir durum ----------------------------
def a6_iki_kargo() -> dict:
    """İki kargo da SFO'da, tek uçak (P1) SFO'da; hedef: ikisi de JFK'de."""
    semalar = [
        Sema("Load", ["c", "p", "a"], ["At(c,a)", "At(p,a)", "Cargo(c)", "Plane(p)", "Airport(a)"],
             ekle=["In(c,p)"], sil=["At(c,a)"]),
        Sema("Unload", ["c", "p", "a"], ["In(c,p)", "At(p,a)", "Cargo(c)", "Plane(p)", "Airport(a)"],
             ekle=["At(c,a)"], sil=["In(c,p)"]),
        Sema("Fly", ["p", "from", "to"], ["At(p,from)", "Plane(p)", "Airport(from)", "Airport(to)"],
             ekle=["At(p,to)"], sil=["At(p,from)"], farkli=(("from", "to"),)),
    ]
    bas = atomlar("At(C1,SFO),At(C2,SFO),At(P1,SFO),Cargo(C1),Cargo(C2),Plane(P1),Airport(SFO),Airport(JFK)")
    p = Planlama(bas, atomlar("At(C1,JFK),At(C2,JFK)"),
                 temellendir(semalar, ["C1", "C2", "P1", "SFO", "JFK"], bas, statik=["Cargo", "Plane", "Airport"]))
    return {"h*": len(ileri_ara(p).plan),
            "hedef sayısı": h_hedef_sayisi(p, bas),
            "h_max": h_max(p, bas),
            "h_add": h_add(p, bas),
            "seviye toplamı": h_seviye_toplami(p, bas)}


# --- A7: kahve robotu -------------------------------------------------------
KAHVE_SEMALARI = [
    Sema("Git", ["a", "b"], ["Robot(a)", "Bitisik(a,b)"], ekle=["Robot(b)"], sil=["Robot(a)"]),
    Sema("KahveYap", ["y"], ["Robot(y)", "Makine(y)", "ElBos"], ekle=["Tutuyor"], sil=["ElBos"]),
    Sema("Birak", ["y"], ["Robot(y)", "Tutuyor"], ekle=["KahveVar(y)", "ElBos"], sil=["Tutuyor"]),
]


def kahve_robotu(hedef: str = "KahveVar(Ofis)", toplanti: bool = False) -> Planlama:
    odalar = ["Ofis", "Koridor", "Mutfak"] + (["Toplantı"] if toplanti else [])
    kapilar = [("Ofis", "Koridor"), ("Koridor", "Mutfak")] + ([("Koridor", "Toplantı")] if toplanti else [])
    bitisik = ",".join(f"Bitisik({a},{b}),Bitisik({b},{a})" for a, b in kapilar)
    bas = atomlar(f"Robot(Ofis),Makine(Mutfak),ElBos,{bitisik}")
    eylemler = temellendir(KAHVE_SEMALARI, odalar, bas, statik=["Bitisik", "Makine"])
    return Planlama(bas, atomlar(hedef), eylemler)


# --- A8: kritik yol ve kaynaklar, MotorTak2 = 40 dk -------------------------
def a8_kisa_motor() -> dict:
    sure = {**ky.SURE, "MotorTak2": 40}
    ES, LS, kaynaksiz = ky.kritik_yol(sure)
    kaynakli, ES2 = ky.kaynakli_cizelge(sure)
    tek_denetci, _ = ky.kaynakli_cizelge(sure, kapasite={**ky.KAPASITE, "denetçi": 1})
    return {"kaynaksız": kaynaksiz, "kritik": [a for a in sure if ES[a] == LS[a]],
            "kaynaklı": kaynakli, "ES": ES2, "tek denetçi": tek_denetci}


# --- A9: hiyerarşik planlamaya metro inceltmesi -----------------------------
ILKEL_METRO = {
    **hp.ILKEL,
    "Yürü(Ev,İstasyon)": (lambda d: d["yer"] == "Ev", lambda d: {**d, "yer": "İstasyon"}),
    "Metro(İstasyon,Havalimanı)": (lambda d: d["yer"] == "İstasyon" and d.get("kart", False),
                                   lambda d: {**d, "yer": "Havalimanı"}),
}
INCELTMELER_METRO = {
    "Git(Ev,Havalimanı)": hp.INCELTMELER["Git(Ev,Havalimanı)"] + [["Yürü(Ev,İstasyon)", "Metro(İstasyon,Havalimanı)"]],
}


def a9_metro(durum: dict):
    return hp.hiyerarsik_ara(durum, lambda d: d["yer"] == "Havalimanı", ["Git(Ev,Havalimanı)"],
                             ilkel=ILKEL_METRO, inceltmeler=INCELTMELER_METRO)


# --- A10: geri (regression) arama -------------------------------------------
def geri_ara(p: Planlama):
    """Hedeften geriye BFS. Alt hedef = (pozitif atomlar, negatif atomlar).
    İlgili eylem: pozitif bir hedef atomu ekler ya da negatif bir hedef atomunu siler;
    hiçbir pozitif hedefi silmez, hiçbir negatif hedefi eklemez.
    Gerileme: poz' = (poz − EKLE) ∪ ÖN,  neg' = (neg − SİL) ∪ ÖN_DEĞİL.
    Başlangıç durumu alt hedefi sağlıyorsa (poz ⊆ s0, neg ∩ s0 = ∅) plan bulunmuştur.
    Döner: (plan, genişletilen alt hedef sayısı)."""
    baslangic = (frozenset(p.hedef), frozenset())
    sinir = deque([(baslangic, [])])
    gorulen = {baslangic}
    genis = 0
    while sinir:
        (poz, neg), plan = sinir.popleft()
        if poz <= p.baslangic and not (neg & p.baslangic):
            return plan, genis
        genis += 1
        for e in p.eylemler:
            if not (e.ekle & poz or e.sil & neg):
                continue                      # ilgisiz
            if e.sil & poz or e.ekle & neg:
                continue                      # tutarsız: bir hedefi bozar
            poz2 = (poz - e.ekle) | e.on
            neg2 = (neg - e.sil) | e.on_degil
            if poz2 & neg2:
                continue                      # hem doğru hem yanlış olamaz
            alt = (frozenset(poz2), frozenset(neg2))
            if alt not in gorulen:
                gorulen.add(alt)
                sinir.append((alt, [e.ad] + plan))
    return None, genis


def main() -> None:
    print("=== A4: ¬At(Flat,Axle) önkoşulu olmadan ===")
    print("  Plan:", a4_negatifsiz_lastik())
    print("  Patlak lastik hâlâ akstayken yedeği de takıyoruz: model gerçeği yansıtmıyor.")

    print("\n=== A6: iki kargo, tek uçak ===")
    for ad, deger in a6_iki_kargo().items():
        print(f"  {ad:<15} {deger}")
    print("  h_add > h*: Fly(P1,SFO,JFK) iki hedefe birden hizmet ediyor ama h_add onu iki kez sayıyor.")

    print("\n=== A7: kahve robotu ===")
    p = kahve_robotu()
    print(f"  Tek fincan ({len(p.eylemler)} temel eylem): {ileri_ara(p).plan}")
    p2 = kahve_robotu("KahveVar(Ofis),KahveVar(Toplantı)", toplanti=True)
    for ad, h in [("BFS", None), ("A* h_max", h_max), ("A* h_add", h_add)]:
        s = ileri_ara(p2, h)
        print(f"  İki fincan, {ad:<9}: {len(s.plan)} adım, {s.genisletilen} düğüm genişletildi")
    print("  Plan:", ", ".join(ileri_ara(p2).plan))

    print("\n=== A8: MotorTak2 = 40 dk ===")
    r = a8_kisa_motor()
    print(f"  Kaynaksız: {r['kaynaksız']} dk, kritik yol: {r['kritik']}")
    print(f"  Kaynaklı (1 vinç, 1 istasyon, 2 denetçi): {r['kaynaklı']} dk")
    print(ky.zaman_cizelgesi(r["ES"], {**ky.SURE, "MotorTak2": 40}))
    print(f"  Tek denetçiyle: {r['tek denetçi']} dk")

    print("\n=== A9: metro inceltmesi ===")
    for durum in ({"yer": "Ev", "araba": False, "nakit": 10, "kart": True},
                  {"yer": "Ev", "araba": False, "nakit": 10, "kart": False},
                  {"yer": "Ev", "araba": True, "nakit": 100, "kart": True}):
        plan, n = a9_metro(durum)
        print(f"  {durum} → {plan or 'plan yok'} ({n} plan denendi)")

    print("\n=== A10: geri arama ===")
    for ad, p in [("Yedek lastik", kp.yedek_lastik()), ("Bloklar", kp.bloklar()), ("Hava kargo", kp.hava_kargo())]:
        plan, geri_n = geri_ara(p)
        ileri_n = ileri_ara(p).genisletilen
        print(f"  {ad:<13} {len(plan)} adım, geri {geri_n:>4} / ileri {ileri_n:>3} düğüm: {', '.join(plan)}")


if __name__ == "__main__":
    main()
