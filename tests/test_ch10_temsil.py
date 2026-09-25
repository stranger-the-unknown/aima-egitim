"""Bölüm 10: kitaptaki örneklerle doğrulama."""
from yardimci import yukle

va = yukle("ch10-bilgi-temsili/ornekler/varsayilan_akil.py")
oh = yukle("ch10-bilgi-temsili/ornekler/olay_hesabi.py")
mb = yukle("ch10-bilgi-temsili/ornekler/modal_bilgi.py")
aa = yukle("ch10-bilgi-temsili/ornekler/anlamsal_ag.py")
k10 = yukle("ch10-bilgi-temsili/cozumler/alistirma6_10_kod.py")


def test_nixon_elmasi():
    tum = va.modeller(va.NIXON_ATOMLAR, va.nixon_kb)
    tercih = va.tercih_edilen(tum, ["Ab2", "Ab3"])
    assert len(tercih) == 2
    assert {(m["Pasifist"], m["Ab2"], m["Ab3"]) for m in tercih} == {(True, True, False), (False, False, True)}
    assert va.sonuc(tercih, "Pasifist").startswith("bilinmiyor")
    assert va.sonuc(va.oncelikli(tum, [["Ab3"], ["Ab2"]]), "Pasifist").startswith("EVET")
    assert len(va.nixon_genislemeleri()) == 2


def test_tweety_monoton_degil():
    for penguen, beklenen in ((False, "EVET"), (True, "HAYIR")):
        atomlar, kb = va.tweety_kb(penguen)
        assert va.sonuc(va.tercih_edilen(va.modeller(atomlar, kb), ["Ab1"]), "Ucar").startswith(beklenen)


def test_olay_hesabi_atalet():
    assert not oh.T("Açık(Işık)", 4) and oh.T("Açık(Işık)", 5) and oh.T("Açık(Işık)", 7)
    assert not oh.T("Açık(Işık)", 8) and oh.T("Açık(Işık)", 10) and not oh.T("Açık(Işık)", 13)


def test_allen_iliskileri():
    beklenen = {
        ("Saltanat(Fatih)", "Saltanat(II. Bayezid)"): ["Meet"],
        ("Saltanat(Fatih)", "Saltanat(Kanuni)"): ["Before"],
        ("İnşa(Süleymaniye)", "Saltanat(Kanuni)"): ["During"],
        ("Saltanat(Kanuni)", "Başmimarlık(Sinan)"): ["Overlap"],
        ("Cumhuriyet'in ilk yılı", "Cumhurbaşkanlığı(Atatürk)"): ["Starts"],
        ("Başmimarlık(Sinan)", "Hayat(Sinan)"): ["Finishes"],
    }
    for (a, b), iliski in beklenen.items():
        assert oh.iliskiler(a, b) == iliski
    assert not oh.Overlap(oh.ARALIKLAR["Başmimarlık(Sinan)"], oh.ARALIKLAR["Saltanat(Kanuni)"])


def test_goendergesel_gecirimsizlik():
    w0 = "w0 (gerçek)"
    assert mb.ayni_kisi("Süpermen", "Clark")(w0)
    assert mb.K("Lois", mb.ucar("Süpermen"))(w0)
    assert not mb.K("Lois", mb.ucar("Clark"))(w0)
    assert not mb.de_re("wa") and mb.de_dicto("wa")


def test_anlamsal_ag_ve_jtms():
    assert aa.deger("Meryem", "bacak")[0] == 2
    assert aa.deger("UzunJohnSilver", "bacak")[0] == 1
    assert str(aa.deger("Nixon", "pasifist")[0]).startswith("ÇATIŞMA")
    t = aa.JTMS()
    t.varsay("Yağmur"); t.varsay("Sulama")
    t.gerekce("IslakÇim", {"Yağmur"}); t.gerekce("IslakÇim", {"Sulama"}); t.gerekce("KayganYol", {"Yağmur"})
    t.geri_cek("Yağmur")
    assert t.inanclar() == {"Sulama", "IslakÇim"}


def test_cozumler():
    duz, ozgul = k10.a9()
    assert len(duz) == 2 and va.sonuc(ozgul, "Yetiskin").startswith("HAYIR")
    assert k10.etiket("Gökkuşağı") == [{"Güneş", "Yağmur"}, {"Güneş", "Sulama"}]
    assert k10.a8()["K(Gün ≤ 31)"] and not k10.a8()["∃g K(Gün = g)"]
