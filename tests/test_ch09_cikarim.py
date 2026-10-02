"""Bölüm 9: kitaptaki değerlerle doğrulama."""
from yardimci import yukle

fc = yukle("ch09-cikarim-birinci-derece/ornekler/fol_cikarim.py")
sb = yukle("ch09-cikarim-birinci-derece/ornekler/suclu_bati.py")
kc = yukle("ch09-cikarim-birinci-derece/ornekler/kedi_cozumleme.py")
py = yukle("ch09-cikarim-birinci-derece/ornekler/prolog_yol.py")
a7 = yukle("ch09-cikarim-birinci-derece/cozumler/alistirma7_10_kod.py")


def birlestir(a, b):
    t = fc.birlestir(fc.terim(a), fc.terim(b))
    return None if t is None else {v: fc.yaz(x) for v, x in fc.tamamla(t).items()}


def test_kitap_birlestirme_tablosu():
    assert birlestir("Knows(John, x)", "Knows(John, Jane)") == {"x": "Jane"}
    assert birlestir("Knows(John, x)", "Knows(y, Bill)") == {"x": "Bill", "y": "John"}
    assert birlestir("Knows(John, x)", "Knows(y, Mother(y))") == {"y": "John", "x": "Mother(John)"}
    assert birlestir("Knows(John, x)", "Knows(x, Elizabeth)") is None
    assert birlestir("Knows(John, x)", "Knows(x17, Elizabeth)") == {"x": "Elizabeth", "x17": "John"}


def test_mgu_ve_occurs_check():
    assert birlestir("Knows(John, x)", "Knows(y, z)") == {"y": "John", "x": "z"}
    assert birlestir("x", "f(x)") is None
    assert birlestir("P(x, f(x))", "P(f(y), y)") is None


def test_suc_ornegi_ileri_zincirleme_iki_tur():
    teta, turlar = fc.ileri_zincirleme(sb.KURALLAR, sb.OLGULAR, fc.terim("Criminal(x)"))
    assert fc.yaz(fc.tamamla(teta)["x"]) == "West"
    assert len(turlar) == 2
    assert sorted(fc.yaz(f) for f in turlar[0]) == ["Hostile(Nono)", "Sells(West, M1, Nono)", "Weapon(M1)"]
    assert [fc.yaz(f) for f in turlar[1]] == ["Criminal(West)"]


def test_suc_ornegi_geri_zincirleme():
    yanitlar = [fc.yaz(fc.tamamla(t)["x"]) for t in fc.geri_zincirleme(sb.KURALLAR, sb.OLGULAR, fc.terim("Criminal(x)"))]
    assert yanitlar[0] == "West"


def test_kedi_cozumleme_ve_yanit():
    bulundu, adimlar = kc.kanit("~Kills(Curiosity, Tuna)")
    assert bulundu and adimlar[-1][2] == frozenset()
    assert kc.kim_oldurdu(True) == "Yanit(Curiosity)"
    assert kc.kanit("Kills(Jack, Tuna)")[0]  # KB ⊨ ¬Kills(Jack, Tuna)


def test_prolog_kural_sirasi():
    _, ilk_a = py.geri_dene([py.TABAN, py.OZYINELI], "yol(A, q)", sinir=18)
    _, ilk_b6 = py.geri_dene([py.OZYINELI, py.TABAN], "yol(A, q)", sinir=6)
    _, ilk_b18 = py.geri_dene([py.OZYINELI, py.TABAN], "yol(A, q)", sinir=18)
    assert ilk_a <= 3 and ilk_b18 > ilk_b6 > ilk_a
    _, turlar = fc.ileri_zincirleme([py.OZYINELI, py.TABAN], py.OLGULAR)
    assert sum(len(t) for t in turlar) == 7


def test_marcus_ve_tablolama():
    assert a7.a9()[0]
    tablo = a7.tablolu_sor([py.OZYINELI, py.TABAN], py.OLGULAR, fc.terim("yol(A, q)"))
    assert sorted(tablo["yol(A, _0)"][1]) == ["yol(A, B)", "yol(A, C)", "yol(A, D)", "yol(A, E)"]
