"""Bölüm 4: kitaptaki değerlerle doğrulama."""
import random

from yardimci import yukle

tt = yukle("ch04-karmasik-ortamlar/ornekler/tepe_tirmanma_n_queens.py")
ga = yukle("ch04-karmasik-ortamlar/ornekler/genetik_8vezir.py")
hg = yukle("ch04-karmasik-ortamlar/ornekler/havalimani_gradyan.py")
ao = yukle("ch04-karmasik-ortamlar/ornekler/and_or_supurge.py")
ib = yukle("ch04-karmasik-ortamlar/ornekler/inanc_durumu_supurge.py")
lr = yukle("ch04-karmasik-ortamlar/ornekler/lrta_yildiz.py")
sa = yukle("ch04-karmasik-ortamlar/ornekler/simule_tavlama_demo.py")
kay = yukle("ch04-karmasik-ortamlar/cozumler/alistirma7_kaygan_supurge.py")
uc = yukle("ch04-karmasik-ortamlar/cozumler/alistirma8_uc_kare_algisiz.py")


def test_saldiri_ve_komsu_degerleri_tutarli():
    rng = random.Random(0)
    for _ in range(20):
        t = tt.rastgele_tahta(8, rng)
        for (c, r), h in tt.komsu_degerleri(t).items():
            t2 = t.copy()
            t2[c] = r
            assert tt.saldiri_sayisi(t2) == h


def test_tepe_tirmanma_basari_orani_kitaba_yakin():
    d = tt.deney(1000, 0, tohum=3)
    assert 0.10 <= d["oran"] <= 0.19
    assert 3 <= d["adim_basari"] <= 5 and 2.5 <= d["adim_takilma"] <= 4


def test_yana_hamle_basari_orani_kitaba_yakin():
    assert 0.90 <= tt.deney(400, 100, tohum=3)["oran"] <= 0.98


def test_ga_kitap_uygunluklari():
    assert [ga.uygunluk(b) for b in ga.KITAP_POPULASYON] == [24, 23, 20, 11]
    assert ga.caprazla("32752411", "24748552", 3) == "32748552"
    assert ga.caprazla("24748552", "32752411", 3) == "24752411"
    assert ga.uygunluk("32748152") == 24


def test_ga_cozum_bulur():
    birey, _, _ = ga.genetik_algoritma(tohum=1)
    assert ga.uygunluk(birey) == 28


def test_tavlama_optimumu_bulur():
    import itertools
    random.seed(42)
    _, maliyet, _ = sa.simule_tavlama()
    en_iyi = min(sa.tur_maliyeti([0] + list(p)) for p in itertools.permutations(range(1, 8)))
    assert abs(maliyet - en_iyi) < 1e-9


def test_havalimani_newton_kume_merkezi_ve_gradyan_sifir():
    x, g = hg.newton(hg.rastgele_baslangic(random.Random(4)))
    assert all(abs(gx) < 1e-6 and abs(gy) < 1e-6 for gx, gy in hg.gradyan(x))
    assert g == sorted(g, reverse=True)  # her Newton adımı f'yi azaltır


def test_and_or_kitap_plani():
    assert ao.sonuclar(1, "Süpür") == {5, 7}
    plan = ao.and_or_arama(1)
    assert plan == ["Süpür", {"eger": {5: ["Sağ", "Süpür"], 7: []}}]
    for secici in (min, max):
        assert ao.calistir(plan, 1, secici)[-1] in ao.HEDEFLER


def test_algisiz_plan_ve_inanc_guncelleme():
    plan = ib.algisiz_plan(frozenset(range(1, 9)))
    assert [e for e, _ in plan] == ["Sağ", "Süpür", "Sol", "Süpür"]
    assert plan[-1][1] == {7}
    b = ib.guncelle(frozenset(range(1, 9)), ("Sol", "Kirli"))
    assert b == {1, 3}
    assert ib.guncelle(ib.tahmin(b, "Sağ"), ("Sağ", "Kirli")) == {2}


def test_lrta_kitap_sekli():
    iz = lr.tek_boyut_ornegi()
    assert [h for h, _ in iz] == [
        [8, 9, 2, 2, 4, 3], [8, 9, 3, 2, 4, 3], [8, 9, 3, 4, 4, 3],
        [8, 9, 5, 4, 4, 3], [8, 9, 5, 5, 4, 3]]
    assert [s for _, s in iz] == [2, 3, 2, 3, 4]


def test_lrta_optimale_yakinsar():
    ajan = lr.LRTAAjani()
    uzunluklar = [lr.deneme(ajan) for _ in range(15)]
    assert uzunluklar[-1] == lr.optimal_uzunluk() == 25


def test_kaygan_dunyada_dongusuz_plan_yok():
    eski = ao.sonuclar
    ao.sonuclar = kay.kaygan_sonuclar
    try:
        assert ao.and_or_arama(1) is None
    finally:
        ao.sonuclar = eski


def test_uc_kare_algisiz_plan_7_adim():
    plan, son = uc.algisiz_bfs(frozenset(uc.DURUMLAR))
    assert len(plan) == 7 and all(uc.hedef_mi(s) for s in son)
