"""Bölüm 7: kitaptaki değerlerle doğrulama."""
import itertools
import random

from yardimci import yukle

on = yukle("ch07-mantiksal-ajanlar/ornekler/onerme.py")
wm = yukle("ch07-mantiksal-ajanlar/ornekler/wumpus_mantik.py")
igz = yukle("ch07-mantiksal-ajanlar/ornekler/ileri_geri_zincirleme.py")


def test_ayristirici_oncelik():
    assert on.ayristir("~A & B | C") == ("|", ("&", ("~", "A"), "B"), "C")
    assert on.ayristir("A => B => C") == ("=>", "A", ("=>", "B", "C"))


def test_cnf_esdeger():
    for metin in ["B11 <=> (P12 | P21)", "(A | B) => (C & ~D)", "~(A <=> B)"]:
        e = on.ayristir(metin)
        tumceler = on.cnf(e)
        semb = sorted(on.semboller(e))
        for d in itertools.product([False, True], repeat=len(semb)):
            m = dict(zip(semb, d))
            cnf_deger = all(any(m[l.lstrip("~")] != l.startswith("~") for l in t) for t in tumceler)
            assert cnf_deger == on.dogru_mu(e, m)


def test_kitap_kb_128_model_3_dogru():
    g, modeller = on.tt_gerektirir(wm.kitap_kb(), on.ayristir("~P12"))
    assert g and len(modeller) == 3
    assert len(on.semboller(wm.kitap_kb())) == 7
    assert not on.tt_gerektirir(wm.kitap_kb(), on.ayristir("~P22"))[0]
    assert not on.tt_gerektirir(wm.kitap_kb(), "P22")[0]


def test_uc_yontem_ayni_yaniti_verir():
    kb = wm.kitap_kb()
    tumceler = on.cnf(kb)
    for sorgu in ["~P12", "~P22", "P22 | P31", "~P21", "B21"]:
        a = on.ayristir(sorgu)
        beklenen = on.tt_gerektirir(kb, a)[0]
        assert on.sat_gerektirir(tumceler, a) == beklenen
        assert on.cozumleme(tumceler, a)[0] == beklenen


def test_ileri_ve_geri_zincirleme():
    assert on.ileri_zincirleme(igz.KURALLAR, igz.GERCEKLER, "Q")[0]
    assert on.geri_zincirleme(igz.KURALLAR, igz.GERCEKLER, "Q")
    assert not on.ileri_zincirleme(igz.KURALLAR, ["A"], "Q")[0]


def test_wumpus_ajani_kitaptaki_cikarimlari_yapar():
    ajan = wm.MantiksalAjan()
    for konum in ((1, 1), (2, 1), (1, 2)):
        ajan.algila(konum, wm.algi(konum))
    assert (1, 3) in ajan.kesin_wumpus
    assert (3, 1) in ajan.kesin_cukur
    assert (2, 2) in ajan.guvenli


def test_wumpus_ajani_altini_bulur_ve_hic_tehlikeye_girmez():
    rota, ajan, altin = wm.kesif(yazdir=False)
    assert altin and rota[-1] == wm.ALTIN
    assert all(k not in wm.CUKURLAR and k != wm.WUMPUS for k in rota)


def test_dpll_ve_walksat_tutarli():
    rng = random.Random(3)
    for _ in range(10):
        t = on.rastgele_3cnf(12, 30, rng)  # m/n = 2.5: neredeyse hep karşılanabilir
        model = on.dpll(t)
        assert model is not None
        tam = {s: model.get(s, False) for s in {l.lstrip("~") for c in t for l in c}}
        assert all(any(tam[l.lstrip("~")] != l.startswith("~") for l in c) for c in t)
        w, _ = on.walksat(t, rng=rng)
        assert w is not None


def test_faz_gecisi_uclari():
    rng = random.Random(0)
    az = sum(on.dpll(on.rastgele_3cnf(20, 40, rng)) is not None for _ in range(10))
    cok = sum(on.dpll(on.rastgele_3cnf(20, 160, rng)) is not None for _ in range(10))
    assert az == 10 and cok == 0
