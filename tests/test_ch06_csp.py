"""Bölüm 6: kitaptaki değerlerle ve bağımsız hesaplarla doğrulama."""
from itertools import product

from yardimci import yukle

ks = yukle("ch06-kisit-saglama/ornekler/kisit.py")
av = yukle("ch06-kisit-saglama/ornekler/avustralya_csp.py")
tr = yukle("ch06-kisit-saglama/ornekler/harita_boyama_csp.py")
nv = yukle("ch06-kisit-saglama/ornekler/n_vezir_csp.py")
mc = yukle("ch06-kisit-saglama/ornekler/min_catisma_vezir.py")
sd = yukle("ch06-kisit-saglama/ornekler/sudoku_csp.py")
kr = yukle("ch06-kisit-saglama/ornekler/kriptaritmetik.py")
k7 = yukle("ch06-kisit-saglama/cozumler/alistirma7_9_10_kod.py")


def kaba_kuvvet_boyama(bolgeler, komsular, renkler):
    sayi = 0
    for renk in product(renkler, repeat=len(bolgeler)):
        a = dict(zip(bolgeler, renk))
        sayi += all(a[x] != a[y] for x in bolgeler for y in komsular[x])
    return sayi


def test_avustralya_18_cozum_tum_ayarlarda():
    assert kaba_kuvvet_boyama(av.BOLGELER, av.KOMSULAR, av.RENKLER) == 18
    for ayar in [("sirali", "sirali", "yok"), ("mrv", "lcv", "ileri"), ("derece", "sirali", "mac")]:
        c, _ = ks.geri_izleme(av.avustralya(), *ayar, tum_cozumler=True)
        assert len(c) == 18 and all(av.avustralya().cozum_mu(x) for x in c)


def test_ileri_kontrol_izi_kitaptaki_gibi():
    iz = av.ileri_kontrol_izi([("WA", "kırmızı"), ("Q", "yeşil"), ("V", "mavi")])
    assert iz[1][1]["NT"] == ["yeşil", "mavi"] and iz[1][1]["SA"] == ["yeşil", "mavi"]
    assert iz[2][1]["NT"] == ["mavi"] and iz[2][1]["SA"] == ["mavi"] and iz[2][1]["NSW"] == ["kırmızı", "mavi"]
    assert iz[3][1]["SA"] == [] and iz[3][1]["NSW"] == ["kırmızı"]


def test_mac_erken_tutarsizlik():
    csp = av.avustralya()
    alan = {b: list(av.RENKLER) for b in av.BOLGELER}
    alan["WA"], alan["Q"] = ["kırmızı"], ["yeşil"]
    assert ks.ac3(csp, alan)[0] is False
    alan2 = {b: list(av.RENKLER) for b in av.BOLGELER}
    alan2["WA"] = ["kırmızı"]
    assert ks.ac3(csp, alan2)[0] is True


def test_lcv_kirmiziyi_once_dener():
    csp = av.avustralya()
    atama = {"WA": "kırmızı", "NT": "yeşil"}
    kalan = {q: sum(csp.tutarli("SA", r, {**atama, "Q": q}) for r in av.RENKLER) for q in ("kırmızı", "mavi")}
    assert kalan["kırmızı"] > kalan["mavi"] == 0


def test_kesme_kumesi_ve_agac_cozucu():
    assert av.KOMSULAR["SA"] and k7.agac_mi(set(av.BOLGELER) - {"SA"}, av.KOMSULAR)
    assert av.avustralya().cozum_mu(ks.kesme_kumesi_coz(av.avustralya(), ["SA"]))


def test_turkiye_3_renk_yetmez_4_yeter():
    assert kaba_kuvvet_boyama(tr.BOLGELER, tr.KOMSULUK, tr.RENKLER[:3]) == 0
    assert kaba_kuvvet_boyama(tr.BOLGELER, tr.KOMSULUK, tr.RENKLER[:4]) > 0
    assert tr.coz(3)[0] == [] and tr.coz(4, True, True)[0]
    # komşuluk simetrik olmalı
    assert all(a in tr.KOMSULUK[b] for a in tr.BOLGELER for b in tr.KOMSULUK[a])
    assert "Guneydogu" not in tr.KOMSULUK["IcAnadolu"] and "Doguanadolu" in tr.KOMSULUK["Akdeniz"]


def test_turkiye_en_kucuk_kesme_kumesi_2():
    assert len(k7.en_kucuk_kesme_kumesi(tr.BOLGELER, tr.KOMSULUK)) == 2


def test_n_vezir_cozum_sayilari():
    for n, beklenen in [(4, 2), (5, 10), (6, 4)]:
        c, _ = ks.geri_izleme(nv.n_vezir(n), "mrv", "sirali", "ileri", tum_cozumler=True)
        assert len(c) == beklenen
    assert ks.geri_izleme(nv.n_vezir(3))[0] == []


def test_min_catisma_buyuk_n_az_adim():
    for n in (1000, 3000):
        tahta, adim = mc.min_catisma(n, tohum=1)
        assert tahta is not None and mc.dogru_mu(tahta) and adim < 500


def test_sudoku_ac3_kolayi_cozer():
    s = sd.coz(sd.KOLAY)
    assert s["atama"] == 0 and s["ac3_sonrasi_bos"] == 0
    csp = sd.sudoku(sd.KOLAY)
    assert csp.cozum_mu(s["cozum"])


def test_kriptaritmetik():
    cozumler, _ = kr.coz("TWO+TWO=FOUR")
    assert len(cozumler) == 7 == len(kr.kaba_kuvvet("TWO+TWO=FOUR"))
    assert all(a["F"] == 1 for a in cozumler)
    assert kr.goster("SEND+MORE=MONEY", kr.coz("SEND+MORE=MONEY")[0][0]) == "9567 + 1085 = 10652"
