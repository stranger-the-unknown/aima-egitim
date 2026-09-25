#!/usr/bin/env python3
"""Önerme mantığı araç kutusu (Bölüm 7).

Cümleleri metinden oku, doğruluk tablosuyla gerektirmeyi denetle, CNF'ye çevir,
çözümleme (resolution), ileri/geri zincirleme, DPLL ve WalkSAT uygula.

Sözdizimi (öncelik sırası yüksekten düşüğe):
    ~A          değil (¬)
    A & B       ve    (∧)
    A | B       veya  (∨)
    A => B      ise   (⇒)
    A <=> B     ancak ve ancak (⇔)
Semboller harf/rakam/alt çizgi içerebilir: B11, P21, W_1_3 …

İfade gösterimi: sembol = str; bileşik ifade = demet:
    ("~", A)  ("&", A, B)  ("|", A, B)  ("=>", A, B)  ("<=>", A, B)
Tümce (clause): literallerden oluşan frozenset; literal "P" ya da "~P".

Çalıştırınca küçük bir kendi kendini sınama yapar:
    python onerme.py
"""
from __future__ import annotations

import itertools
import random
import re
from typing import Iterable, Optional, Union

Ifade = Union[str, tuple]
Tumce = frozenset

# ---------------------------------------------------------------------------
# Ayrıştırma ve yazdırma
# ---------------------------------------------------------------------------

_JETON = re.compile(r"\s*(<=>|=>|[~&|()]|[A-Za-z_][A-Za-z0-9_]*)")
_ONCELIK = {"<=>": 1, "=>": 2, "|": 3, "&": 4}
_SAG_BIRLESMELI = {"=>"}


def ayristir(metin: str) -> Ifade:
    """Metni ifade ağacına çevir. Örnek: ayristir("B11 <=> (P12 | P21)")."""
    jetonlar = []
    konum = 0
    metin = metin.strip()
    while konum < len(metin):
        m = _JETON.match(metin, konum)
        if not m:
            raise ValueError(f"tanınmayan karakter: {metin[konum:]!r}")
        jetonlar.append(m.group(1))
        konum = m.end()
    i = 0

    def birincil() -> Ifade:
        nonlocal i
        j = jetonlar[i]
        if j == "~":
            i += 1
            return ("~", birincil())
        if j == "(":
            i += 1
            e = ifade(0)
            if jetonlar[i] != ")":
                raise ValueError("')' bekleniyordu")
            i += 1
            return e
        i += 1
        return j

    def ifade(en_az: int) -> Ifade:
        nonlocal i
        sol = birincil()
        while i < len(jetonlar) and jetonlar[i] in _ONCELIK and _ONCELIK[jetonlar[i]] >= en_az:
            op = jetonlar[i]
            i += 1
            sonraki = _ONCELIK[op] if op in _SAG_BIRLESMELI else _ONCELIK[op] + 1
            sag = ifade(sonraki)
            sol = (op, sol, sag)
        return sol

    sonuc = ifade(0)
    if i != len(jetonlar):
        raise ValueError(f"fazladan jeton: {jetonlar[i:]}")
    return sonuc


_GOSTER = {"~": "¬", "&": " ∧ ", "|": " ∨ ", "=>": " ⇒ ", "<=>": " ⇔ "}


def yaz(e: Ifade) -> str:
    if isinstance(e, str):
        return e
    if e[0] == "~":
        return "¬" + yaz(e[1])
    return "(" + _GOSTER[e[0]].join(yaz(a) for a in e[1:]) + ")"


def semboller(e: Ifade) -> set[str]:
    if isinstance(e, str):
        return {e}
    return set().union(*(semboller(a) for a in e[1:]))


def ve(*ifadeler: Ifade) -> Ifade:
    ifadeler = [e for e in ifadeler if e is not None]
    sonuc = ifadeler[0]
    for e in ifadeler[1:]:
        sonuc = ("&", sonuc, e)
    return sonuc


def veya(*ifadeler: Ifade) -> Ifade:
    sonuc = ifadeler[0]
    for e in ifadeler[1:]:
        sonuc = ("|", sonuc, e)
    return sonuc


# ---------------------------------------------------------------------------
# Anlam: model ve doğruluk tablosu
# ---------------------------------------------------------------------------

def dogru_mu(e: Ifade, model: dict) -> bool:
    if isinstance(e, str):
        return model[e]
    op = e[0]
    if op == "~":
        return not dogru_mu(e[1], model)
    a, b = dogru_mu(e[1], model), dogru_mu(e[2], model)
    return {"&": a and b, "|": a or b, "=>": (not a) or b, "<=>": a == b}[op]


def tt_gerektirir(kb: Ifade, alfa: Ifade) -> tuple[bool, list[dict]]:
    """TT-ENTAILS: tüm modelleri sırala. Döner: (KB ⊨ α mı, KB'nin doğru olduğu modeller)."""
    semb = sorted(semboller(kb) | semboller(alfa))
    kb_modelleri = []
    gerektirir = True
    for degerler in itertools.product([False, True], repeat=len(semb)):
        model = dict(zip(semb, degerler))
        if dogru_mu(kb, model):
            kb_modelleri.append(model)
            if not dogru_mu(alfa, model):
                gerektirir = False
    return gerektirir, kb_modelleri


# ---------------------------------------------------------------------------
# CNF dönüşümü
# ---------------------------------------------------------------------------

def _esdegerlik_kaldir(e: Ifade) -> Ifade:
    if isinstance(e, str):
        return e
    args = [_esdegerlik_kaldir(a) for a in e[1:]]
    if e[0] == "<=>":
        a, b = args
        return ("&", ("|", ("~", a), b), ("|", ("~", b), a))
    if e[0] == "=>":
        a, b = args
        return ("|", ("~", a), b)
    return (e[0], *args)


def _degil_ice(e: Ifade) -> Ifade:
    """De Morgan ve çift değilleme ile ¬'yi sembollere kadar it."""
    if isinstance(e, str):
        return e
    if e[0] == "~":
        a = e[1]
        if isinstance(a, str):
            return e
        if a[0] == "~":
            return _degil_ice(a[1])
        if a[0] == "&":
            return ("|", _degil_ice(("~", a[1])), _degil_ice(("~", a[2])))
        if a[0] == "|":
            return ("&", _degil_ice(("~", a[1])), _degil_ice(("~", a[2])))
    return (e[0], *[_degil_ice(a) for a in e[1:]])


def _tumcelere(e: Ifade) -> list[set]:
    """∨'yi ∧ üzerine dağıtarak tümce listesi üret."""
    if isinstance(e, str):
        return [{e}]
    if e[0] == "~":
        return [{"~" + e[1]}]
    if e[0] == "&":
        return _tumcelere(e[1]) + _tumcelere(e[2])
    # "|": iki tarafın tümcelerinin tüm çiftlerini birleştir
    return [a | b for a in _tumcelere(e[1]) for b in _tumcelere(e[2])]


def degil_lit(lit: str) -> str:
    return lit[1:] if lit.startswith("~") else "~" + lit


def cnf(e: Ifade | str) -> list[Tumce]:
    """CNF tümceleri (totolojiler atılır, tekrarlar birleştirilir)."""
    if isinstance(e, str) and not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", e):
        e = ayristir(e)
    tumceler = []
    for t in _tumcelere(_degil_ice(_esdegerlik_kaldir(e))):
        if any(degil_lit(lit) in t for lit in t):
            continue  # P ∨ ¬P: her zaman doğru
        ft = frozenset(t)
        if ft not in tumceler:
            tumceler.append(ft)
    return tumceler


def tumce_yaz(t: Tumce) -> str:
    if not t:
        return "□"
    return " ∨ ".join(sorted((("¬" + l[1:]) if l.startswith("~") else l) for l in t))


# ---------------------------------------------------------------------------
# Çözümleme (resolution)
# ---------------------------------------------------------------------------

def cozumle(ci: Tumce, cj: Tumce) -> list[Tumce]:
    """İki tümcenin tüm çözümleyicileri (totolojiler hariç)."""
    sonuc = []
    for lit in ci:
        if degil_lit(lit) in cj:
            yeni = (ci - {lit}) | (cj - {degil_lit(lit)})
            if not any(degil_lit(x) in yeni for x in yeni):
                sonuc.append(frozenset(yeni))
    return sonuc


def cozumleme(kb: Iterable[Tumce], alfa: Ifade, iz: bool = False):
    """PL-RESOLUTION: KB ∧ ¬α tutarsızsa KB ⊨ α.

    Döner: (sonuç, istatistik, kanıt adımları). Kanıt adımları: (tümce1, tümce2, çözümleyici).
    """
    tumceler = set(kb) | set(cnf(("~", alfa)))
    ebeveyn: dict = {}
    uretilen = 0
    while True:
        yeni = set()
        liste = list(tumceler)
        for i in range(len(liste)):
            for j in range(i + 1, len(liste)):
                for r in cozumle(liste[i], liste[j]):
                    uretilen += 1
                    if r not in tumceler and r not in yeni:
                        ebeveyn[r] = (liste[i], liste[j])
                    if not r:
                        return True, {"uretilen": uretilen, "tumce": len(tumceler)}, _kanit(ebeveyn, r)
                    yeni.add(r)
        if yeni <= tumceler:
            return False, {"uretilen": uretilen, "tumce": len(tumceler)}, []
        tumceler |= yeni


def _kanit(ebeveyn: dict, bos: Tumce) -> list:
    adimlar, yigin, gorulen = [], [bos], set()
    while yigin:
        t = yigin.pop()
        if t in ebeveyn and t not in gorulen:
            gorulen.add(t)
            a, b = ebeveyn[t]
            adimlar.append((a, b, t))
            yigin += [a, b]
    return adimlar[::-1]


# ---------------------------------------------------------------------------
# Horn tümceleri: ileri ve geri zincirleme
# ---------------------------------------------------------------------------

def ileri_zincirleme(kurallar: list[tuple[list[str], str]], gercekler: list[str], q: str):
    """PL-FC-ENTAILS. kurallar: (öncüller, sonuç). Döner: (q çıkarıldı mı, çıkarım sırası)."""
    sayac = {i: len(onc) for i, (onc, _) in enumerate(kurallar)}
    cikarilan: set[str] = set()
    gundem = list(gercekler)
    sira = []
    while gundem:
        p = gundem.pop(0)
        if p == q:
            sira.append(p)
            return True, sira
        if p in cikarilan:
            continue
        cikarilan.add(p)
        sira.append(p)
        for i, (onc, sonuc) in enumerate(kurallar):
            if p in onc:
                sayac[i] -= 1
                if sayac[i] == 0:
                    gundem.append(sonuc)
    return False, sira


def geri_zincirleme(kurallar: list[tuple[list[str], str]], gercekler: list[str], q: str,
                    yol: tuple = (), iz: Optional[list] = None) -> bool:
    """Hedeften geriye: q için sonucu q olan bir kuralın tüm öncüllerini kanıtla."""
    if iz is not None:
        iz.append("  " * len(yol) + q)
    if q in gercekler:
        return True
    if q in yol:
        return False  # döngü
    for onc, sonuc in kurallar:
        if sonuc == q and all(geri_zincirleme(kurallar, gercekler, p, yol + (q,), iz) for p in onc):
            return True
    return False


# ---------------------------------------------------------------------------
# SAT: DPLL ve WalkSAT
# ---------------------------------------------------------------------------

def _tumce_durumu(t: Tumce, model: dict):
    """(doğru mu, atanmamış literaller). Tümce doğruysa ikinci değer boş liste."""
    kalan = []
    for lit in t:
        s = lit.lstrip("~")
        if s in model:
            if model[s] != lit.startswith("~"):
                return True, []
        else:
            kalan.append(lit)
    return False, kalan


def dpll(tumceler: list[Tumce], model: Optional[dict] = None, ist: Optional[dict] = None,
         bilgi_sezgiseli: bool = True) -> Optional[dict]:
    """DPLL: erken sonlandırma, saf sembol ve birim tümce sezgiselleriyle. Döner: model ya da None."""
    model = dict(model or {})
    ist = ist if ist is not None else {}
    ist["cagri"] = ist.get("cagri", 0) + 1
    acik = []
    for t in tumceler:
        dogru, kalan = _tumce_durumu(t, model)
        if dogru:
            continue
        if not kalan:
            return None  # yanlış tümce: bu dal başarısız
        acik.append(kalan)
    if not acik:
        return model  # her tümce doğru
    if bilgi_sezgiseli:
        # Birim tümce: tek atanmamış literal kaldıysa onu doğru yap
        for kalan in acik:
            if len(kalan) == 1:
                lit = kalan[0]
                return dpll(tumceler, {**model, lit.lstrip("~"): not lit.startswith("~")}, ist)
        # Saf sembol: açık tümcelerde hep aynı işaretle görünen sembol
        isaret: dict = {}
        for kalan in acik:
            for lit in kalan:
                s = lit.lstrip("~")
                isaret.setdefault(s, set()).add(not lit.startswith("~"))
        for s, isaretler in isaret.items():
            if len(isaretler) == 1:
                return dpll(tumceler, {**model, s: isaretler.pop()}, ist)
    s = acik[0][0].lstrip("~")
    return (dpll(tumceler, {**model, s: True}, ist, bilgi_sezgiseli)
            or dpll(tumceler, {**model, s: False}, ist, bilgi_sezgiseli))


def sat_gerektirir(kb: list[Tumce], alfa: Ifade) -> bool:
    """KB ⊨ α ⟺ KB ∧ ¬α karşılanamaz (DPLL ile)."""
    return dpll(list(kb) + cnf(("~", alfa))) is None


def walksat(tumceler: list[Tumce], p: float = 0.5, max_cevirme: int = 10_000,
            rng: Optional[random.Random] = None):
    """WALKSAT: rastgele model, sonra yanlış bir tümcede bir sembolü çevir. Döner: (model|None, çevirme)."""
    rng = rng or random.Random(0)
    semb = sorted({lit.lstrip("~") for t in tumceler for lit in t})
    model = {s: rng.random() < 0.5 for s in semb}

    def dogru(t):
        return any(model[l.lstrip("~")] != l.startswith("~") for l in t)

    for i in range(max_cevirme):
        yanlislar = [t for t in tumceler if not dogru(t)]
        if not yanlislar:
            return model, i
        t = rng.choice(yanlislar)
        if rng.random() < p:
            s = rng.choice(sorted(t)).lstrip("~")
        else:
            def yanlis_sayisi(s):
                model[s] = not model[s]
                n = sum(1 for u in tumceler if not dogru(u))
                model[s] = not model[s]
                return n
            s = min((l.lstrip("~") for l in sorted(t)), key=yanlis_sayisi)
        model[s] = not model[s]
    return None, max_cevirme


def rastgele_3cnf(n: int, m: int, rng: random.Random) -> list[Tumce]:
    """n sembol, m tümce; her tümce 3 farklı sembolden, rastgele işaretlerle."""
    tumceler = []
    for _ in range(m):
        s = rng.sample(range(1, n + 1), 3)
        tumceler.append(frozenset(("~" if rng.random() < 0.5 else "") + f"X{v}" for v in s))
    return tumceler


if __name__ == "__main__":
    e = ayristir("B11 <=> (P12 | P21)")
    print("İfade:", yaz(e))
    print("CNF  :", " ∧ ".join(f"({tumce_yaz(t)})" for t in cnf(e)))
    kb = ve(ayristir("~P11"), e, ayristir("~B11"))
    print("TT: KB ⊨ ¬P12 ?", tt_gerektirir(kb, ayristir("~P12"))[0])
    print("DPLL: KB ⊨ ¬P12 ?", sat_gerektirir(cnf(kb), ayristir("~P12")))
    print("Çözümleme:", cozumleme(cnf(kb), ayristir("~P12"))[0])
