#!/usr/bin/env python3
"""Wumpus dünyasında mantıkla akıl yürütme (kitaptaki örnekler).

Bölüm 1 — Doğruluk tablosu. Kitaptaki küçük bilgi tabanı:
    R1: ¬P11      R2: B11 ⇔ (P12 ∨ P21)      R3: B21 ⇔ (P11 ∨ P22 ∨ P31)
    R4: ¬B11      R5: B21
  7 sembol → 2⁷ = 128 model. KB yalnızca 3 modelde doğrudur.
  KB ⊨ ¬P12 (her 3 modelde P12 yanlış); KB ⊭ ¬P22 (bazı modellerde P22 doğru).

Bölüm 2 — Çözümleme ile kanıt: (B11 ⇔ (P12 ∨ P21)) ∧ ¬B11 ⊢ ¬P12.

Bölüm 3 — Mantıksal ajan. Kitaptaki 4×4 dünya: Wumpus [1,3]'te, çukurlar [3,1], [3,3],
  [4,4]'te, altın [2,3]'te. Ajan algılarını bilgi tabanına ekler ve bir kareye ancak
  KB ⊨ ¬P ∧ ¬W ise (güvenli olduğu **kanıtlanırsa**) girer. Gerektirme DPLL ile denetlenir.

Çalıştırma:
    python wumpus_mantik.py
"""
from __future__ import annotations

from collections import deque
from itertools import combinations

from onerme import (ayristir, cnf, cozumleme, sat_gerektirir, tt_gerektirir, tumce_yaz,
                    ve, veya)

N = 4
WUMPUS = (1, 3)
CUKURLAR = {(3, 1), (3, 3), (4, 4)}
ALTIN = (2, 3)


def komsular(x: int, y: int) -> list[tuple[int, int]]:
    return [(a, b) for a, b in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)) if 1 <= a <= N and 1 <= b <= N]


def P(x, y): return f"P{x}{y}"   # [x,y]'de çukur var  # noqa: E704
def W(x, y): return f"W{x}{y}"   # [x,y]'de wumpus var  # noqa: E704
def B(x, y): return f"B{x}{y}"   # [x,y]'de esinti algılandı  # noqa: E704
def S(x, y): return f"S{x}{y}"   # [x,y]'de koku algılandı  # noqa: E704


# ---------------------------------------------------------------------------
# Bölüm 1 ve 2: kitaptaki küçük bilgi tabanı
# ---------------------------------------------------------------------------

KITAP_KB = ["~P11", "B11 <=> (P12 | P21)", "B21 <=> (P11 | P22 | P31)", "~B11", "B21"]


def kitap_kb():
    return ve(*[ayristir(s) for s in KITAP_KB])


# ---------------------------------------------------------------------------
# Bölüm 3: dünyanın fiziği ve ajan
# ---------------------------------------------------------------------------

def algi(konum) -> dict:
    x, y = konum
    k = komsular(x, y)
    return {
        "koku": WUMPUS in k or WUMPUS == konum,
        "esinti": any(c in CUKURLAR for c in k),
        "parilti": konum == ALTIN,
    }


def fizik_kurallari() -> list:
    """Dünyanın değişmeyen kuralları, CNF tümceleri olarak."""
    tumceler = cnf(ayristir("~P11 & ~W11"))
    for x in range(1, N + 1):
        for y in range(1, N + 1):
            k = komsular(x, y)
            tumceler += cnf(("<=>", B(x, y), veya(*[P(a, b) for a, b in k])))
            tumceler += cnf(("<=>", S(x, y), veya(*[W(a, b) for a, b in k])))
    kareler = [(x, y) for x in range(1, N + 1) for y in range(1, N + 1)]
    tumceler += cnf(veya(*[W(x, y) for x, y in kareler]))          # en az bir wumpus
    for a, b in combinations(kareler, 2):                             # en fazla bir wumpus
        tumceler += cnf(("|", ("~", W(*a)), ("~", W(*b))))
    return tumceler


class MantiksalAjan:
    def __init__(self) -> None:
        self.kb = fizik_kurallari()
        self.ziyaret: set = set()
        self.guvenli: set = {(1, 1)}
        self.kesin_cukur: set = set()
        self.kesin_wumpus: set = set()

    def algila(self, konum, a: dict) -> None:
        self.ziyaret.add(konum)
        x, y = konum
        self.kb += cnf(B(x, y) if a["esinti"] else ("~", B(x, y)))
        self.kb += cnf(S(x, y) if a["koku"] else ("~", S(x, y)))
        self.guncelle()

    def guncelle(self) -> None:
        """Bilinmeyen her kare için: güvenli mi, kesin çukur mu, kesin wumpus mu?"""
        for x in range(1, N + 1):
            for y in range(1, N + 1):
                if (x, y) in self.guvenli:
                    continue
                if sat_gerektirir(self.kb, ("&", ("~", P(x, y)), ("~", W(x, y)))):
                    self.guvenli.add((x, y))
                elif sat_gerektirir(self.kb, P(x, y)):
                    self.kesin_cukur.add((x, y))
                elif sat_gerektirir(self.kb, W(x, y)):
                    self.kesin_wumpus.add((x, y))

    def sonraki_hedef(self, konum):
        """Güvenli kareler üzerinden en yakın, ziyaret edilmemiş güvenli kare."""
        sinir = deque([(konum, [konum])])
        gorulen = {konum}
        adaylar = []
        while sinir:
            k, yol = sinir.popleft()
            if k not in self.ziyaret:
                adaylar.append((len(yol), k[1], k[0], yol))
                continue
            for n in komsular(*k):
                if n in self.guvenli and n not in gorulen:
                    gorulen.add(n)
                    sinir.append((n, yol + [n]))
        return min(adaylar)[3] if adaylar else None


def tahta(ajan: MantiksalAjan, konum) -> str:
    satirlar = []
    for y in range(N, 0, -1):
        hucreler = []
        for x in range(1, N + 1):
            k = (x, y)
            if k == konum:
                h = "A"
            elif k in ajan.kesin_wumpus:
                h = "W!"
            elif k in ajan.kesin_cukur:
                h = "P!"
            elif k in ajan.ziyaret:
                h = "✓"
            elif k in ajan.guvenli:
                h = "ok"
            else:
                h = "?"
            hucreler.append(f"{h:^4}")
        satirlar.append(f"  {y} " + "|".join(hucreler))
    satirlar.append("     " + "    ".join(str(x) for x in range(1, N + 1)))
    return "\n".join(satirlar)


def kesif(en_fazla_adim: int = 30, yazdir: bool = True) -> tuple[list, MantiksalAjan, bool]:
    ajan = MantiksalAjan()
    konum, rota, altin = (1, 1), [(1, 1)], False
    for _ in range(en_fazla_adim):
        a = algi(konum)
        ajan.algila(konum, a)
        if yazdir:
            algilar = [ad for ad, v in a.items() if v] or ["hiçbir şey"]
            print(f"\n[{konum[0]},{konum[1]}] algı: {', '.join(algilar)}")
            print(tahta(ajan, konum))
        if a["parilti"]:
            altin = True
            break
        yol = ajan.sonraki_hedef(konum)
        if yol is None:
            break
        rota += yol[1:]
        konum = yol[-1]
    return rota, ajan, altin


def main() -> None:
    print("=== Bölüm 1: doğruluk tablosuyla gerektirme ===")
    kb = kitap_kb()
    for alfa in ("~P12", "~P22"):
        g, modeller = tt_gerektirir(kb, ayristir(alfa))
        print(f"  KB ⊨ {alfa:<5}? {g}   (128 modelden KB'nin doğru olduğu: {len(modeller)})")
    print("  KB'nin doğru olduğu 3 model (yalnızca P değişkenleri):")
    for m in tt_gerektirir(kb, ayristir("~P12"))[1]:
        print("    " + ", ".join(f"{s}={'D' if m[s] else 'Y'}" for s in ("P12", "P21", "P22", "P31")))

    print("\n=== Bölüm 2: çözümleme ile ¬P12 kanıtı ===")
    kb2 = cnf(ve(ayristir("B11 <=> (P12 | P21)"), ayristir("~B11")))
    print("  KB tümceleri: " + " ; ".join(tumce_yaz(t) for t in kb2) + "   + sorgunun değili: P12")
    sonuc, ist, adimlar = cozumleme(kb2, ayristir("~P12"))
    for a, b, r in adimlar:
        print(f"    ({tumce_yaz(a)})  +  ({tumce_yaz(b)})  →  {tumce_yaz(r)}")
    print(f"  Boş tümce türetildi: KB ⊨ ¬P12 = {sonuc}  ({ist['uretilen']} çözümleyici üretildi)")

    print("\n=== Bölüm 3: mantıksal ajan kitaptaki 4×4 dünyada ===")
    print("  (A: ajan, ✓: ziyaret edildi, ok: güvenli olduğu kanıtlandı, P!/W!: kesin çukur/wumpus, ?: bilinmiyor)")
    rota, ajan, altin = kesif()
    print(f"\nRota: {' → '.join(f'[{x},{y}]' for x, y in rota)}")
    print(f"Altın bulundu mu? {altin}.  Çıkarılan: wumpus {sorted(ajan.kesin_wumpus)}, çukurlar {sorted(ajan.kesin_cukur)}")
    print("Ajan hiçbir zaman güvenli olduğu KANITLANMAMIŞ bir kareye girmedi.")


if __name__ == "__main__":
    main()
