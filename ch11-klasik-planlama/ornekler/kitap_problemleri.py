#!/usr/bin/env python3
"""Kitabın üç klasik planlama problemi, PDDL tanımlarıyla birebir.

1. Hava kargo: C1 SFO'da, C2 JFK'de; hedef C1 → JFK, C2 → SFO.
   Kitaptaki plan (6 adım): Load(C1,P1,SFO), Fly(P1,SFO,JFK), Unload(C1,P1,JFK),
                             Load(C2,P2,JFK), Fly(P2,JFK,SFO), Unload(C2,P2,SFO)
   (BFS aynı 6 eylemi farklı ama eşdeğer bir sırayla bulabilir: iki uçağın işleri bağımsızdır.)
2. Yedek lastik: Kitaptaki plan (3 adım): Remove(Flat,Axle), Remove(Spare,Trunk), PutOn(Spare,Axle)
3. Bloklar dünyası (C, A'nın üstünde; hedef A B'nin, B C'nin üstünde):
   Kitaptaki plan (3 adım): MoveToTable(C,A), Move(B,Table,C), Move(A,Table,B)
   Bu problem "Sussman anomalisi" olarak bilinir: alt hedefleri tek tek çözmek işe yaramaz.

Çalıştırma:
    python kitap_problemleri.py
"""
from __future__ import annotations

from dataclasses import replace

from planlama import (Planlama, Sema, atomlar, geri_ilgili, h_add, h_hedef_sayisi, h_max,
                      h_seviye_toplami, ileri_ara, plani_uygula, temellendir)


def hava_kargo() -> Planlama:
    semalar = [
        Sema("Load", ["c", "p", "a"], ["At(c,a)", "At(p,a)", "Cargo(c)", "Plane(p)", "Airport(a)"],
             ekle=["In(c,p)"], sil=["At(c,a)"]),
        Sema("Unload", ["c", "p", "a"], ["In(c,p)", "At(p,a)", "Cargo(c)", "Plane(p)", "Airport(a)"],
             ekle=["At(c,a)"], sil=["In(c,p)"]),
        Sema("Fly", ["p", "from", "to"], ["At(p,from)", "Plane(p)", "Airport(from)", "Airport(to)"],
             ekle=["At(p,to)"], sil=["At(p,from)"], farkli=(("from", "to"),)),
    ]
    bas = atomlar("At(C1,SFO),At(C2,JFK),At(P1,SFO),At(P2,JFK),Cargo(C1),Cargo(C2),"
                  "Plane(P1),Plane(P2),Airport(JFK),Airport(SFO)")
    eylemler = temellendir(semalar, ["C1", "C2", "P1", "P2", "SFO", "JFK"], bas,
                           statik=["Cargo", "Plane", "Airport"])
    return Planlama(bas, atomlar("At(C1,JFK),At(C2,SFO)"), eylemler)


def yedek_lastik() -> Planlama:
    semalar = [
        Sema("Remove", ["obj", "loc"], ["At(obj,loc)"], ekle=["At(obj,Ground)"], sil=["At(obj,loc)"],
             farkli=(("loc", "Ground"),)),
        Sema("PutOn", ["t"], ["Tire(t)", "At(t,Ground)"], ekle=["At(t,Axle)"], sil=["At(t,Ground)"],
             on_degil=("At(Flat,Axle)", "At(Spare,Axle)")),
        Sema("LeaveOvernight", [], [], ekle=[],
             sil=[f"At({t},{y})" for t in ("Spare", "Flat") for y in ("Ground", "Axle", "Trunk")]),
    ]
    bas = atomlar("Tire(Flat),Tire(Spare),At(Flat,Axle),At(Spare,Trunk)")
    # Remove'u yalnızca lastiklere uygulamak için obj'u lastiklerle sınırlıyoruz (Tire statik)
    semalar[0].on = ["Tire(obj)"] + semalar[0].on
    eylemler = temellendir(semalar, ["Flat", "Spare", "Axle", "Trunk", "Ground"], bas, statik=["Tire"])
    # Kitaptaki adlandırma: PutOn(t, Axle)
    eylemler = [replace(e, ad=e.ad[:-1] + ",Axle)") if e.ad.startswith("PutOn") else e for e in eylemler]
    return Planlama(bas, atomlar("At(Spare,Axle)"), eylemler)


def bloklar(hedef: str = "On(A,B),On(B,C)", baslangic: str = None) -> Planlama:
    semalar = [
        Sema("Move", ["b", "x", "y"], ["On(b,x)", "Clear(b)", "Clear(y)", "Block(b)", "Block(y)"],
             ekle=["On(b,y)", "Clear(x)"], sil=["On(b,x)", "Clear(y)"],
             farkli=(("b", "x"), ("b", "y"), ("x", "y"))),
        Sema("MoveToTable", ["b", "x"], ["On(b,x)", "Clear(b)", "Block(b)", "Block(x)"],
             ekle=["On(b,Table)", "Clear(x)"], sil=["On(b,x)"]),
    ]
    bas = atomlar(baslangic or "On(A,Table),On(B,Table),On(C,A),Block(A),Block(B),Block(C),"
                               "Clear(B),Clear(C),Clear(Table)")
    eylemler = temellendir(semalar, ["A", "B", "C", "Table"], bas, statik=["Block"])
    return Planlama(bas, atomlar(hedef), eylemler)


def sussman_alt_hedefler() -> list[tuple[str, list[str], bool]]:
    """Alt hedefleri sırayla, birbirinden habersiz çöz: sonunda ikisi birden sağlanıyor mu?"""
    sonuc = []
    for sira in (["On(A,B)", "On(B,C)"], ["On(B,C)", "On(A,B)"]):
        p = bloklar()
        s = p.baslangic
        plan = []
        for g in sira:
            alt = Planlama(s, frozenset({g}), p.eylemler)
            parca = ileri_ara(alt).plan
            plan += parca
            s = plani_uygula(alt, parca)
        sonuc.append((" sonra ".join(sira), plan, p.hedef <= s))
    return sonuc


def asagidan_yukari() -> tuple[list[str], bool]:
    """Kitaptaki çözüm yolu: Kule hedefinde alt hedefler aşağıdan yukarı sıralanabilir.
    On(C,Table) da hedefe eklenip önce o, sonra On(B,C), sonra On(A,B) çözülür."""
    p = bloklar("On(A,B),On(B,C),On(C,Table)")
    s, plan = p.baslangic, []
    for g in ["On(C,Table)", "On(B,C)", "On(A,B)"]:
        alt = Planlama(s, frozenset({g}), p.eylemler)
        parca = ileri_ara(alt).plan
        plan += parca
        s = plani_uygula(alt, parca)
    return plan, p.hedef <= s


def karsilastir(ad: str, p: Planlama) -> None:
    print(f"\n=== {ad} ===  ({len(p.eylemler)} temel eylem)")
    for h_ad, h in [("BFS", None), ("A* hedef sayısı", h_hedef_sayisi), ("A* h_max", h_max),
                    ("A* h_add (kabul edilemez)", h_add), ("A* seviye toplamı", h_seviye_toplami)]:
        s = ileri_ara(p, h)
        print(f"  {h_ad:<27} plan uzunluğu {len(s.plan):>2}, genişletilen düğüm {s.genisletilen:>5}")
    print("  Plan: " + ", ".join(ileri_ara(p).plan))


def main() -> None:
    karsilastir("Hava kargo", hava_kargo())
    karsilastir("Yedek lastik", yedek_lastik())
    karsilastir("Bloklar dünyası", bloklar())

    print("\n=== Geri (regression) arama: yedek lastik hedefi için ilgili eylemler ===")
    for ad, g in geri_ilgili(yedek_lastik(), atomlar("At(Spare,Axle)")):
        print(f"  {ad}: gerilemiş hedef = {sorted(g)}  (+ negatif önkoşullar ¬At(Flat,Axle), ¬At(Spare,Axle))")

    print("\n=== Sussman anomalisi: alt hedefleri tek tek çözmek ===")
    for sira, plan, basarili in sussman_alt_hedefler():
        print(f"  {sira}: {', '.join(plan)}  → iki hedef birden sağlandı mı? {basarili}")
    print("  İki sırada da ilk alt hedefin çözümü, ikincisini sağlarken bozuluyor ya da"
          "\n  ikincisini imkânsız kılıyor. Hedefler birbirinden bağımsız değil; planlayıcı onları"
          "\n  birlikte düşünmeli (tam arama 3 adımlık planı bulur).")
    plan, basarili = asagidan_yukari()
    print(f"\n  Aşağıdan yukarı (On(C,Table), On(B,C), On(A,B)): {', '.join(plan)}  → {basarili}")
    print("  Kule tabandan kurulunca hiçbir alt hedef bozulmuyor: alt hedefler sıralanabilir.")


if __name__ == "__main__":
    main()
