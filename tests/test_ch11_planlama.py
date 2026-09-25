"""Bölüm 11: kitaptaki örneklerle doğrulama."""
from collections import Counter

from yardimci import yukle

pl = yukle("ch11-klasik-planlama/ornekler/planlama.py")
kp = yukle("ch11-klasik-planlama/ornekler/kitap_problemleri.py")
ky = yukle("ch11-klasik-planlama/ornekler/kritik_yol.py")
hp = yukle("ch11-klasik-planlama/ornekler/hiyerarsik_plan.py")
sb = yukle("ch11-klasik-planlama/ornekler/strips_bloklar.py")
k11 = yukle("ch11-klasik-planlama/cozumler/alistirma4_10_kod.py")

SEZGISELLER = [None, "h_hedef_sayisi", "h_max", "h_add", "h_seviye_toplami"]


def _tum_aramalar(p):
    return [kp.ileri_ara(p, getattr(kp, h) if h else None).plan for h in SEZGISELLER]


def test_hava_kargo():
    p = kp.hava_kargo()
    kitap = ["Load(C1,P1,SFO)", "Fly(P1,SFO,JFK)", "Unload(C1,P1,JFK)",
             "Load(C2,P2,JFK)", "Fly(P2,JFK,SFO)", "Unload(C2,P2,SFO)"]
    assert p.hedef <= kp.plani_uygula(p, kitap)
    bfs, *astar = _tum_aramalar(p)
    assert Counter(bfs) == Counter(kitap)  # aynı eylemler, eşdeğer sıra
    for plan in astar:  # bazı sezgiseller tek uçağın gidip döndüğü başka bir 6 adımlık planı bulur
        assert len(plan) == 6 and p.hedef <= kp.plani_uygula(p, plan)


def test_yedek_lastik():
    p = kp.yedek_lastik()
    assert kp.ileri_ara(p).plan == ["Remove(Flat,Axle)", "Remove(Spare,Trunk)", "PutOn(Spare,Axle)"]
    assert all(len(plan) == 3 for plan in _tum_aramalar(p))
    (ad, g), = kp.geri_ilgili(p, p.hedef)
    assert ad == "PutOn(Spare,Axle)" and g == {"Tire(Spare)", "At(Spare,Ground)"}


def test_bloklar_dunyasi():
    p = kp.bloklar()
    for plan in _tum_aramalar(p):
        assert plan == ["MoveToTable(C,A)", "Move(B,Table,C)", "Move(A,Table,B)"]


def test_sussman_anomalisi():
    assert [basarili for _, _, basarili in kp.sussman_alt_hedefler()] == [False, False]
    plan, basarili = kp.asagidan_yukari()
    assert basarili and plan == ["MoveToTable(C,A)", "Move(B,Table,C)", "Move(A,Table,B)"]


def test_sezgiseller_kabul_edilebilirlik():
    p = kp.bloklar()
    assert pl.h_max(p, p.baslangic) == 2 and pl.h_add(p, p.baslangic) == 3
    r = k11.a6_iki_kargo()
    assert r["h*"] == 5 and r["h_max"] == 2 and r["h_add"] == 6 and r["seviye toplamı"] == 4


def test_kritik_yol():
    ES, LS, bitis = ky.kritik_yol()
    assert bitis == 85
    assert {a: (ES[a], LS[a]) for a in ES} == {
        "MotorTak1": (0, 15), "TekerTak1": (30, 45), "Denetle1": (60, 75),
        "MotorTak2": (0, 0), "TekerTak2": (60, 60), "Denetle2": (75, 75)}
    sure, ES2 = ky.kaynakli_cizelge()
    assert sure == 115 and ES2["MotorTak1"] == 0 and ES2["MotorTak2"] == 30


def test_hiyerarsik():
    hedef = lambda d: d["yer"] == "Havalimanı"  # noqa: E731
    assert hp.hiyerarsik_ara({"yer": "Ev", "araba": True, "nakit": 0}, hedef, ["Git(Ev,Havalimanı)"])[0] == \
        ["Sür(Ev,Otopark)", "Servis(Otopark,Havalimanı)"]
    assert hp.hiyerarsik_ara({"yer": "Ev", "araba": False, "nakit": 100}, hedef, ["Git(Ev,Havalimanı)"])[0] == \
        ["Taksi(Ev,Havalimanı)"]
    assert hp.hiyerarsik_ara({"yer": "Ev", "araba": False, "nakit": 10}, hedef, ["Git(Ev,Havalimanı)"])[0] is None
    plan, _ = hp.hiyerarsik_ara({"konum": (0, 0)}, lambda d: d["konum"] == (2, 1), ["Yürü"],
                                ilkel=hp.izgara_ilkel(), inceltmeler=hp.yuru_inceltmeleri, derinlik_siniri=8)
    assert plan == ["Yukarı", "Yukarı", "Sağ", "Sağ", "Aşağı"]


def test_strips_bloklar():
    s = frozenset({"On(A, Masa)", "On(B, Masa)", "Clear(A)", "Clear(B)", "ElBos"})
    a = next(x for x in sb.bloklar_aksiyonlari(["A", "B"]) if x.ad == "Kaldir(A, Masa)")
    assert a.uygula(s) == {"On(B, Masa)", "Clear(A)", "Clear(B)", "Tutuyor(A)"}


def test_cozumler():
    assert k11.a4_negatifsiz_lastik() == ["Remove(Spare,Trunk)", "PutOn(Spare,Axle)"]
    assert len(kp.ileri_ara(k11.kahve_robotu()).plan) == 6
    assert len(kp.ileri_ara(k11.kahve_robotu("KahveVar(Ofis),KahveVar(Toplantı)", toplanti=True)).plan) == 12
    r = k11.a8_kisa_motor()
    assert r["kaynaksız"] == 70 and r["kritik"] == ["MotorTak1", "TekerTak1", "Denetle1"]
    assert r["kaynaklı"] == 95 and r["tek denetçi"] == 95
    ters = ky.kritik_yol({**ky.SURE, "MotorTak2": 40},
                         ky.ONCELIK + [("MotorTak2", "MotorTak1"), ("TekerTak2", "TekerTak1")])[2]
    assert ters == 110
    assert k11.a9_metro({"yer": "Ev", "araba": False, "nakit": 10, "kart": True})[0] == \
        ["Yürü(Ev,İstasyon)", "Metro(İstasyon,Havalimanı)"]
    assert k11.a9_metro({"yer": "Ev", "araba": False, "nakit": 10, "kart": False})[0] is None
    for p, n in ((kp.yedek_lastik(), 3), (kp.bloklar(), 3), (kp.hava_kargo(), 6)):
        plan, _ = k11.geri_ara(p)
        assert len(plan) == n and p.hedef <= kp.plani_uygula(p, plan)
