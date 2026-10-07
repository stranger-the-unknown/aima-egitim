"""Bölüm 23: kitaptaki dilbilgisi ve örneklerle doğrulama."""
import math

import pytest

from yardimci import yukle

dm = yukle("ch23-dogal-dil/ornekler/dil_modelleri.py")
ay = yukle("ch23-dogal-dil/ornekler/ayristirma.py")
an = yukle("ch23-dogal-dil/ornekler/anlambilim.py")
k23 = yukle("ch23-dogal-dil/cozumler/alistirma_kod.py")


def test_e0_olasiliklari():
    for X in {a for a, _, _ in ay.KURALLAR if not a.endswith(("_S", "_NP", "_Noun"))}:
        assert sum(p for a, _, p in ay.KURALLAR if a == X) == pytest.approx(1.0)


def test_cyk_kitap_ornegi():
    agac, p = ay.ayristir("the wumpus is dead")
    assert agac == "[S [NP [Article the] [Noun wumpus]] [VP [VP [Verb is]] [Adjective dead]]]"   # Şekil 23.4
    assert p == pytest.approx(0.90 * (0.25 * 0.40 * 0.15) * (0.05 * 0.40 * 0.10 * 0.05))
    assert ay.ayristir("I think the wumpus is smelly")[0] is None             # eksik üretim
    assert ay.ayristir("Me go I")[0] is not None                              # fazla üretim
    assert ay.ayristirma_sayisi("i feel the wumpus near 1 3".split()) == 2
    a7 = k23.a7()
    assert a7["VP'ye bağlı"] == pytest.approx(a7["NP'ye bağlı"]) == pytest.approx(a7["CYK'nin bulduğu"])


def test_agac_bankasi_pcfg():
    pcfg = ay.agac_bankasindan_pcfg(ay.AGAC_BANKASI)
    assert pcfg[("S", ("NP", "VP"))] == pytest.approx(6 / 7)
    for X in {k[0] for k in pcfg}:
        assert sum(v for k, v in pcfg.items() if k[0] == X) == pytest.approx(1.0)


def test_dil_modelleri():
    assert dm.ardillik_kurali(2_000_000) == pytest.approx(1 / 2_000_002)
    m = dm.NGram(2, dm.DERLEM)
    assert m.P("okula", ("ayşe",)) > 0 and m.log_olasilik("ayşe okula gitti .".split()) > -math.inf
    assert dm.NGram(3, dm.DERLEM).log_olasilik("öğretmen ders okudu .".split()) == -math.inf
    assert dm.NGram(3, dm.DERLEM, 1).log_olasilik("öğretmen ders okudu .".split()) > -math.inf
    s = k23.a3()
    assert s["ara değerleme 0.6/0.3/0.1"] < s["1-gram (Laplace)"]
    hmm = dm.hmm_egit(dm.ETIKETLI)
    assert dm.viterbi(hmm, "ayşe güzel kitap okudu".split()) == ["AD", "SIFAT", "AD", "FİİL"]


def test_anlambilim():
    assert an.yorumla("3 + (4 ÷ 2)")[0] == 5                                   # kitap: Exp(5)
    assert an.yorumla("3 + 4 × 2")[0] == 11 and an.yorumla("12 - 2 - 3")[0] == 7
    assert an.cumle_anlami("Ali loves Bo") == "Loves(Ali, Bo)"
