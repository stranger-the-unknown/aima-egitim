"""Bölüm 5: kitaptaki değerlerle doğrulama."""
import math
import random

from yardimci import yukle

xox = yukle("ch05-rakip-arama/ornekler/minimax_tictactoe.py")
ag = yukle("ch05-rakip-arama/ornekler/oyun_agaci.py")
mc = yukle("ch05-rakip-arama/ornekler/mcts_xox.py")
em = yukle("ch05-rakip-arama/ornekler/beklenti_minimax.py")
d4 = yukle("ch05-rakip-arama/ornekler/dortlu_ab.py")
a7 = yukle("ch05-rakip-arama/cozumler/alistirma7_xox_degerlendirme.py")


def test_xox_agac_istatistigi():
    assert xox.oyun_agaci_istatistigi() == (549_946, 255_168, 5_478)


def test_xox_minimax_degeri_sifir_ve_ab_ayni():
    bos = [xox.Boş] * 9
    assert xox.minimax(bos, True) == xox.alphabeta(bos, True) == 0


def test_hizli_kazan_hemen_kazanani_secer():
    xox.HIZLI_KAZAN = True
    try:
        assert xox.en_iyi_hamle(list("X.O.X.O.."), xox.X, True)[0] == 8
    finally:
        xox.HIZLI_KAZAN = False


def test_kitaptaki_iki_katli_agac():
    assert [ag.minimax(c, False) for c in ag.KITAP_AGACI] == [3, 2, 2]
    assert ag.minimax(ag.KITAP_AGACI) == 3
    iz = []
    assert ag.alfa_beta(ag.KITAP_AGACI, iz=iz) == 3
    assert [v for _, v in iz] == [3, 12, 8, 2, 14, 5, 2]  # C'nin 4 ve 6'sı budandı


def test_mukemmel_siralama_knuth_moore():
    rng = random.Random(1)
    for b, d in [(2, 5), (3, 4), (4, 3)]:
        t = ag.rastgele_agac(b, d, rng)
        iyi = ag.sirala(t, en_iyi_once=True)
        assert ag.alfa_beta(iyi) == ag.minimax(t)
        assert ag.degerlendirilen(iyi) == b ** math.ceil(d / 2) + b ** (d // 2) - 1


def test_ucb1_kitap_ornegi():
    cocuk = {"60/79": (60, 79), "1/10": (1, 10), "2/11": (2, 11)}
    sec = lambda C: max(cocuk, key=lambda k: mc.ucb1(*cocuk[k], 100, C))  # noqa: E731
    assert sec(1.4) == "60/79"
    assert sec(1.5) == "2/11"


def test_mcts_kazanani_ve_savunmayi_bulur():
    assert mc.mcts(list("XO.OX...."), "X", 1000)[0] == 8
    assert mc.mcts(list("XX..O...."), "O", 1000)[0] == 2


def test_sirayi_koruyan_donusum():
    assert em.en_iyi_hamle(em.ornek_agac(1, 2, 3, 4))[0] == "a1"
    assert em.en_iyi_hamle(em.ornek_agac(1, 20, 30, 400))[0] == "a2"


def test_dortlu_siralama_ve_tt_degeri_degistirmez():
    rng = random.Random(5)
    t, s = d4.Tahta(), d4.X
    for _ in range(8):
        t = t.oyna(rng.choice(t.gecerli()), s)
        s = d4.O if s == d4.X else d4.X
    degerler = {d4.Arama(a, b).negamax(t, 4, -math.inf, math.inf, s)
                for a, b in ((False, False), (True, False), (True, True))}
    assert len(degerler) == 1


def test_dortlu_kazanan_hamleyi_gorur():
    t = d4.Tahta()
    for c in (0, 0, 1, 1, 2, 2):  # X: 0,1,2 alt sırada; O üstlerinde
        t = t.oyna(c, d4.X if t.h[0][c] == d4.BOS else d4.O)
    assert d4.Arama().en_iyi_hamle(t, d4.X, 2) == 3


def test_xox_degerlendirme_cift_derinlik_guvenli():
    assert not a7.kaybedebilir_mi(2, xox.O)
    assert a7.kaybedebilir_mi(1, xox.O)
