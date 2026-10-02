"""Bölüm 3: kitaptaki değerlerle doğrulama (Romanya, 8-bulmaca, IDS)."""
import math

import pytest

from yardimci import yukle

arama = yukle("ch03-cozum-arama/ornekler/arama.py")
rom = yukle("ch03-cozum-arama/ornekler/romania_arama.py")
sb = yukle("ch03-cozum-arama/ornekler/sekiz_bulmaca.py")
gev = yukle("ch03-cozum-arama/cozumler/alistirma8_gevsetme.py")
kkl = yukle("ch03-cozum-arama/cozumler/alistirma10_kurt_keci_lahana.py")

OPTIMAL = ["Arad", "Sibiu", "Rimnicu Vilcea", "Pitesti", "Bucharest"]


def romanya():
    return rom.RomanyaProblemi("Arad", "Bucharest")


def test_a_yildiz_ve_ucs_optimal():
    for s in (arama.a_yildiz(romanya()), arama.tekduze_maliyet(romanya())):
        assert s.maliyet == 418
        assert s.yol == OPTIMAL


def test_acgozlu_fagaras_uzerinden_450():
    s = arama.acgozlu(romanya())
    assert s.maliyet == 450
    assert s.yol == ["Arad", "Sibiu", "Fagaras", "Bucharest"]


def test_a_yildiz_izi_kitaptaki_gibi():
    iz = rom.a_yildiz_izi()
    assert [(sehir, f) for sehir, _, _, f in iz] == [
        ("Arad", 366), ("Sibiu", 393), ("Rimnicu Vilcea", 413),
        ("Fagaras", 415), ("Pitesti", 417), ("Bucharest", 418)]


def test_bfs_ve_ids_en_az_kenar():
    for s in (arama.genislik_oncelikli(romanya()), arama.yinelemeli_derinlesme(romanya())):
        assert len(s.yol) - 1 == 3


def test_cift_yonlu_ucs():
    s = rom.iki_yonlu_ucs("Arad", "Bucharest")
    assert s.cift_yonlu_maliyet == 418 and s.cift_yonlu_yol == OPTIMAL
    # Her şehir çifti için UCS ile aynı maliyet
    for a in rom.HARITA:
        for b in ("Neamt", "Eforie", "Drobeta"):
            if a != b:
                assert rom.iki_yonlu_ucs(a, b).cift_yonlu_maliyet == arama.tekduze_maliyet(
                    rom.RomanyaProblemi(a, b)).maliyet


def test_sld_kabul_edilebilir():
    for sehir in rom.HARITA:
        gercek = arama.tekduze_maliyet(rom.RomanyaProblemi(sehir, "Bucharest")).maliyet
        assert rom.SLD_BUCHAREST[sehir] <= gercek


def test_sekiz_bulmaca_kitap_degerleri():
    p = sb.SekizBulmaca(sb.KITAP_BASLANGIC)
    assert p.h1(sb.KITAP_BASLANGIC) == 8
    assert p.h2(sb.KITAP_BASLANGIC) == 18
    assert len(arama.a_yildiz(p).eylemler) == 26
    assert len(arama.ida_yildiz(sb.SekizBulmaca(sb.KITAP_BASLANGIC)).eylemler) == 26


@pytest.mark.parametrize("tohum", range(5))
def test_sezgiseller_ayni_optimali_bulur(tohum):
    import random
    s = sb.rastgele_bulmaca(20, random.Random(tohum))
    uzunluklar = {len(arama.a_yildiz(sb.SekizBulmaca(s, sezgisel=h)).eylemler) for h in ("h1", "h2")}
    uzunluklar.add(len(arama.genislik_oncelikli(sb.SekizBulmaca(s)).eylemler))
    assert len(uzunluklar) == 1


def test_etkin_dallanma_kitap_ornegi():
    assert round(arama.etkin_dallanma(52, 5), 2) == 1.92


def test_ids_bfs_dugum_sayilari():
    b, d = 10, 5
    assert sum(b**i for i in range(1, d + 1)) == 111_110
    assert sum((d + 1 - i) * b**i for i in range(1, d + 1)) == 123_450


def test_cozulebilirlik_paritesi():
    assert sb.cozulebilir_mi(sb.KITAP_BASLANGIC)
    assert not sb.cozulebilir_mi((0, 2, 1, 3, 4, 5, 6, 7, 8))


def test_gevsek_sezgisel_h1i_baskilar_ve_kabul_edilebilir():
    import random
    rng = random.Random(3)
    for _ in range(30):
        s = sb.rastgele_bulmaca(rng.randint(5, 30), rng)
        p = sb.SekizBulmaca(s)
        gercek = len(arama.a_yildiz(p).eylemler)
        assert p.h1(s) <= gev.h_gevsek(s) <= gercek


def test_tutarsiz_ama_kabul_edilebilir_sezgisel():
    """A7: h1 tutarsız ama kabul edilebilir; A* yine optimal bulur."""
    G = {"S": {"A": 1, "B": 4}, "A": {"S": 1, "B": 2, "G": 5}, "B": {"S": 4, "A": 2, "G": 1}, "G": {"A": 5, "B": 1}}

    class P(arama.Problem):
        def eylemler(self, s): return list(G[s])
        def sonuc(self, s, a): return a
        def eylem_maliyeti(self, s, a, s2): return G[s][s2]

    h1 = {"S": 4, "A": 1, "B": 1, "G": 0}
    s = arama.a_yildiz(P("S", "G"), h=lambda n: h1[n.durum])
    assert s.maliyet == 4 and s.yol == ["S", "A", "B", "G"]


def test_kurt_keci_lahana():
    s = arama.genislik_oncelikli(kkl.KurtKeciLahana())
    assert len(s.eylemler) == 7
    assert all(kkl.guvenli(d) for d in s.yol)
