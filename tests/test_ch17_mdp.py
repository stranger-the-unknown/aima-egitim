"""Bölüm 17: kitaptaki değerlerle doğrulama (4. baskı: ödül geçişe aittir)."""
import pytest

from yardimci import yukle

mdp = yukle("ch17-karmasik-kararlar/ornekler/mdp.py")
d43 = yukle("ch17-karmasik-kararlar/ornekler/dort_uc_dunya.py")
dy = yukle("ch17-karmasik-kararlar/ornekler/deger_yineleme.py")
py = yukle("ch17-karmasik-kararlar/ornekler/politika_yineleme.py")
hd = yukle("ch17-karmasik-kararlar/ornekler/haydut.py")
pm = yukle("ch17-karmasik-kararlar/ornekler/pomdp.py")
k17 = yukle("ch17-karmasik-kararlar/cozumler/alistirma_kod.py")

# Kitaptaki Şekil 17.3 (γ = 1, r = −0.04)
SEKIL_17_3 = {
    (1, 3): 0.8516, (2, 3): 0.9078, (3, 3): 0.9578,
    (1, 2): 0.8016, (3, 2): 0.7003,
    (1, 1): 0.7453, (2, 1): 0.6953, (3, 1): 0.6514, (4, 1): 0.4279,
}


def test_gecis_modeli():
    m = mdp.dort_uc()
    assert sorted(m.gecis[((1, 1), "Yukarı")]) == sorted([(0.8, (1, 2)), (0.1, (2, 1)), (0.1, (1, 1))])
    for (s, a), dagilim in m.gecis.items():
        assert sum(p for p, _ in dagilim) == pytest.approx(1.0)
    assert d43.dizi_basari_olasiligi(m, ["Yukarı", "Yukarı", "Sağ", "Sağ", "Sağ"]) == pytest.approx(0.32776)


def test_sekil_17_3_deger_ve_politika_yinelemesi():
    m = mdp.dort_uc()
    U, _ = mdp.deger_yineleme(m, eps=1e-10)
    pi, U_pi, _ = mdp.politika_yineleme(m, {s: "Sağ" if s[1] == 3 else ("Sol" if s == (4, 1) else "Yukarı")
                                            for s in m.durumlar if m.eylemler[s]})
    for s, deger in SEKIL_17_3.items():
        assert U[s] == pytest.approx(deger, abs=5e-5)
        assert U_pi[s] == pytest.approx(deger, abs=5e-5)
    assert U[(4, 3)] == U[(4, 2)] == 0.0            # uç durumların ödülü geçişte; çift sayım yok
    assert pi == m.acgozlu(U)
    assert m.acgozlu(U)[(1, 1)] == "Yukarı"          # kitap: (1, 1)'de en iyisi Yukarı
    assert m.q((3, 1), "Sol", U) > m.q((3, 1), "Yukarı", U)


def test_r_araliklari_dokuz_politika():
    noktalar = [n for n, _ in d43.kirilma_noktalari()]
    for kitap in (-1.6497, -0.7311, -0.4526, -0.0850, -0.0273):
        assert min(abs(n - kitap) for n in noktalar) < 2e-4
    assert len(noktalar) + 1 == 9
    pi = d43.en_iyi_politika(-2.0)
    assert pi[(4, 1)] == ("Yukarı",) and pi[(3, 2)] == ("Sağ",)        # en yakın çıkışa dal
    pi = d43.en_iyi_politika(-0.01)
    assert pi[(4, 1)] == ("Aşağı",) and pi[(3, 2)] == ("Sol",)         # −1'den uzak dur


def test_sonlu_ufuk_ve_indirim():
    pol = d43.sonlu_ufuk(mdp.dort_uc(), 100)
    assert pol[2][(3, 1)] == "Yukarı" and pol[99][(3, 1)] == "Sol"       # N = 3 ve N = 100 (kitap)
    assert k17.a2()["γ = 1.0"] == pytest.approx(0.64)
    assert py.epsilon_ufku(0.5, 0.1) == 5 and py.epsilon_ufku(0.9, 0.1) == 44


def test_sekillendirme():
    m = mdp.dort_uc()
    U, _ = mdp.deger_yineleme(m, eps=1e-10)
    Phi = {s: (0.0 if s in m.uclar else (s[0] * 0.7 - s[1] * 1.3)) for s in m.durumlar}
    U2, _ = mdp.deger_yineleme(d43.sekillendir(m, Phi), eps=1e-10)
    assert d43.en_iyi_eylemler(d43.sekillendir(m, Phi), U2) == d43.en_iyi_eylemler(m, U)
    a7 = k17.a7()
    assert a7["potansiyelle (Φ = −0.2 · uzaklık) politika aynı mı"]
    assert not a7["yaklaşma ödülüyle politika aynı mı"]
    assert a7["yaklaşma ödülüyle 1000 adımda uca varma olasılığı"] < 1e-6


def test_deger_yinelemesi_yakinsama():
    m = mdp.dort_uc(gama=0.9)
    satirlar = dy.hata_ve_politika_kaybi(m, 6)
    assert satirlar[3][1] == pytest.approx(0.51, abs=0.01)    # hata ~0.51 iken ...
    assert satirlar[3][2] == pytest.approx(0.0, abs=1e-9)     # ... politika zaten en iyi
    assert dy.buzulme_orani(m) <= 0.9 + 1e-12
    U, _ = mdp.deger_yineleme(m, eps=1e-3)
    U_gercek, _ = mdp.deger_yineleme(m, eps=1e-12)
    assert mdp.en_cok_hata(U, U_gercek) < 1e-3                # durma koşulu (17.12)


def test_politika_yinelemesi_ve_lp():
    m = mdp.dort_uc(gama=0.9)
    U, _ = mdp.deger_yineleme(m, eps=1e-10)
    pi, U_pi, _ = mdp.politika_yineleme(m)
    pi_k, _, _ = mdp.politika_yineleme(m, k=3)
    assert pi == pi_k == m.acgozlu(U)
    assert mdp.en_cok_hata(U, U_pi) < 1e-8
    assert py.lp_kisitlari_saglanir_mi(m, U) == (True, True)
    assert py.beklenti_maks(m, (3, 2), 6)[1] == m.acgozlu(U)[(3, 2)]


def test_haydut():
    assert hd.indirimli_toplam(hd.M_DIZI, 0.5) == pytest.approx(1.9)
    lam, tablo = hd.deterministik_gittins(hd.M_DIZI, 0.5)
    assert lam == pytest.approx(1.0133, abs=1e-4)
    assert [round(t[3], 4) for t in tablo[:6]] == [0.0, 0.6667, 0.5714, 1.0133, 0.9806, 0.9651]
    assert hd.yeniden_baslatma_degeri(hd.M_DIZI, 0.5) == pytest.approx(2.0266, abs=1e-3)
    g32, g74 = hd.bernoulli_gittins(3, 2), hd.bernoulli_gittins(7, 4)
    assert g32 > g74                                           # keşif bonusu (kitap: 0.7057 > 0.6922)
    assert g32 == pytest.approx(0.7057, abs=3e-3) and g74 == pytest.approx(0.6922, abs=3e-3)


def test_pomdp_iki_durum():
    katmanlar = pm.deger_yineleme(8)
    alfa = {p.eylem: tuple(round(x, 6) for x in p.alfa) for p in katmanlar[0]}
    assert alfa == {"Kal": (0.1, 0.9), "Git": (0.9, 0.1)}
    assert [len(U) for U in katmanlar][1] == 4 and len(katmanlar[7]) == 144   # kitap: 4 ve 144
    for bB in (0.1, 0.3, 0.45):
        assert pm.fayda(katmanlar[7], bB)[1].eylem == "Git"
        assert pm.fayda(katmanlar[7], 1 - bB)[1].eylem == "Kal"
    assert pm.fayda(katmanlar[7], 0.5)[0] < pm.fayda(katmanlar[7], 0.0)[0]
    b = pm.inanc_guncelle({"A": 0.5, "B": 0.5}, "Kal", "B")
    assert b["B"] == pytest.approx(0.6)


def test_pomdp_4x3_inanc():
    s = k17.a9()
    for ad in ("sayı algılayıcısı", "4 bit algılayıcı"):
        assert sum(s[ad].values()) == pytest.approx(1.0)
    assert s["sayı algılayıcısı"][(3, 1)] == pytest.approx(s["sayı algılayıcısı"][(3, 2)])
    assert max(s["4 bit algılayıcı"], key=s["4 bit algılayıcı"].get) == (3, 1)
