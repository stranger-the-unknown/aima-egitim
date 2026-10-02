#!/usr/bin/env python3
"""Karar ağaçları ve karar listeleri (kitaptaki 19.2–19.3, 19.5.1).

Kitaptaki değerler (testlerle doğrulanır):
  * Restoran: 10 nitelik, 2⁶ × 3² × 4² = 9216 olası girdi, yalnızca 12 örnek (Şekil 19.2).
  * Entropi: adil para 1 bit, dört yüzlü zar 2 bit, %99 tura veren para ≈ 0.08 bit.
  * Kazanç(Patrons) ≈ 0.541 bit, Kazanç(Type) = 0 bit; Patrons kök olur.
  * LEARN-DECISION-TREE'nin 12 örnekten bulduğu ağaç (Şekil 19.6): Patrons → Full ise Hungry →
    Type → Thai ise Fri/Sat. Raining ve Reservation hiç kullanılmaz.
  * χ² budama: 3 serbestlik derecesinde %5 için Δ ≥ 7.82, %1 için Δ ≥ 11.35.
  * Karar listesi (Şekil 19.10): WillWait ⇔ (Patrons = Some) ∨ (Patrons = Full ∧ Fri/Sat).

Çalıştırma:
    python karar_agaci.py
"""
from __future__ import annotations

import itertools
import math
import random
from collections import Counter

NITELIKLER = {
    "Alt": ["Yes", "No"], "Bar": ["Yes", "No"], "Fri": ["Yes", "No"], "Hun": ["Yes", "No"],
    "Pat": ["None", "Some", "Full"], "Price": ["$", "$$", "$$$"], "Rain": ["Yes", "No"],
    "Res": ["Yes", "No"], "Type": ["French", "Italian", "Thai", "Burger"],
    "Est": ["0-10", "10-30", "30-60", ">60"],
}
SIRA = list(NITELIKLER)

_TABLO = """
Yes No  No  Yes Some $$$ No  Yes French  0-10  Yes
Yes No  No  Yes Full $   No  No  Thai    30-60 No
No  Yes No  No  Some $   No  No  Burger  0-10  Yes
Yes No  Yes Yes Full $   Yes No  Thai    10-30 Yes
Yes No  Yes No  Full $$$ No  Yes French  >60   No
No  Yes No  Yes Some $$  Yes Yes Italian 0-10  Yes
No  Yes No  No  None $   Yes No  Burger  0-10  No
No  No  No  Yes Some $$  Yes Yes Thai    0-10  Yes
No  Yes Yes No  Full $   Yes No  Burger  >60   No
Yes Yes Yes Yes Full $$$ No  Yes Italian 10-30 No
No  No  No  No  None $   No  No  Thai    0-10  No
Yes Yes Yes Yes Full $   No  No  Burger  30-60 Yes
"""
RESTORAN = [(dict(zip(SIRA, satir.split()[:-1])), satir.split()[-1] == "Yes")
            for satir in _TABLO.strip().splitlines()]


def gercek_agac(x: dict) -> bool:
    """SR'nin gerçek karar ağacı (Şekil 19.3)."""
    if x["Pat"] == "None":
        return False
    if x["Pat"] == "Some":
        return True
    if x["Est"] == ">60":
        return False
    if x["Est"] == "30-60":
        if x["Alt"] == "No":
            return x["Res"] == "Yes" or x["Bar"] == "Yes"
        return x["Fri"] == "Yes"
    if x["Est"] == "10-30":
        if x["Hun"] == "No":
            return True
        return x["Alt"] == "No" or x["Rain"] == "Yes"
    return True


# --- Entropi ve bilgi kazancı -----------------------------------------------------
def entropi(olasiliklar) -> float:
    return -sum(p * math.log2(p) for p in olasiliklar if p > 0)


def B(q: float) -> float:
    return entropi([q, 1 - q])


def kalan(nitelik: str, ornekler) -> float:
    toplam = len(ornekler)
    k = 0.0
    for v in NITELIKLER[nitelik]:
        alt = [y for x, y in ornekler if x[nitelik] == v]
        if alt:
            k += len(alt) / toplam * B(sum(alt) / len(alt))
    return k


def kazanc(nitelik: str, ornekler) -> float:
    p = sum(y for _, y in ornekler)
    return B(p / len(ornekler)) - kalan(nitelik, ornekler)


# --- LEARN-DECISION-TREE -------------------------------------------------------------
def cogunluk(ornekler) -> bool:
    sayim = Counter(y for _, y in ornekler)
    return sayim[True] >= sayim[False] if sayim[True] != sayim[False] else True


def agac_ogren(ornekler, nitelikler, ebeveyn=()):
    """Ağaç: bool (yaprak) ya da (nitelik, {değer: alt ağaç})."""
    if not ornekler:
        return cogunluk(ebeveyn)
    if len({y for _, y in ornekler}) == 1:
        return ornekler[0][1]
    if not nitelikler:
        return cogunluk(ornekler)
    A = max(nitelikler, key=lambda a: kazanc(a, ornekler))     # eşitlikte ilk nitelik
    dallar = {}
    for v in NITELIKLER[A]:
        alt = [(x, y) for x, y in ornekler if x[A] == v]
        dallar[v] = agac_ogren(alt, [a for a in nitelikler if a != A], ornekler)
    return (A, dallar)


def siniflandir(agac, x: dict) -> bool:
    while not isinstance(agac, bool):
        A, dallar = agac
        agac = dallar[x[A]]
    return agac


def agac_yaz(agac, girinti: str = "  ") -> str:
    if isinstance(agac, bool):
        return girinti + ("Yes" if agac else "No")
    A, dallar = agac
    satirlar = []
    for v, alt in dallar.items():
        if isinstance(alt, bool):
            satirlar.append(f"{girinti}{A} = {v}: {'Yes' if alt else 'No'}")
        else:
            satirlar.append(f"{girinti}{A} = {v}:")
            satirlar.append(agac_yaz(alt, girinti + "    "))
    return "\n".join(satirlar)


def dugum_sayisi(agac) -> int:
    return 1 if isinstance(agac, bool) else 1 + sum(dugum_sayisi(a) for a in agac[1].values())


# --- χ² budama -------------------------------------------------------------------------
def ki_kare_3_cdf(x: float) -> float:
    """3 serbestlik dereceli χ² dağılımının birikimli fonksiyonu (kapalı biçim)."""
    return math.erf(math.sqrt(x / 2)) - math.sqrt(2 * x / math.pi) * math.exp(-x / 2)


def ki_kare_3_esik(alfa: float) -> float:
    alt, ust = 0.0, 50.0
    while ust - alt > 1e-9:
        orta = (alt + ust) / 2
        alt, ust = (orta, ust) if 1 - ki_kare_3_cdf(orta) > alfa else (alt, orta)
    return (alt + ust) / 2


def sapma(nitelik: str, ornekler) -> float:
    """Δ = Σ (p_k − p̂_k)²/p̂_k + (n_k − n̂_k)²/n̂_k."""
    p = sum(y for _, y in ornekler)
    n = len(ornekler) - p
    d = 0.0
    for v in NITELIKLER[nitelik]:
        alt = [y for x, y in ornekler if x[nitelik] == v]
        if not alt:
            continue
        pk, nk = sum(alt), len(alt) - sum(alt)
        ph, nh = p * len(alt) / (p + n), n * len(alt) / (p + n)
        d += (pk - ph) ** 2 / ph + (nk - nh) ** 2 / nh
    return d


# --- Karar listeleri ---------------------------------------------------------------------
def karar_listesi_ogren(ornekler, k: int = 2):
    """DECISION-LIST-LEARNING: Örneklerin tek sınıflı, boş olmayan bir alt kümesine uyan en küçük testi
    (en çok k literal) bul, listeye ekle, o örnekleri çıkar. Testler (nitelik, değer) çiftlerinin birleşimi."""
    literaller = [(a, v) for a in SIRA for v in NITELIKLER[a]]
    liste = []
    kalanlar = list(ornekler)
    while kalanlar:
        for boyut in range(1, k + 1):
            adaylar = []
            for test in itertools.combinations(literaller, boyut):
                if len({a for a, _ in test}) < boyut:
                    continue
                uyan = [y for x, y in kalanlar if all(x[a] == v for a, v in test)]
                if uyan and len(set(uyan)) == 1:
                    adaylar.append((len(uyan), test, uyan[0]))
            if adaylar:
                _, test, sonuc = max(adaylar, key=lambda t: t[0])   # en çok örneği kapsayan
                liste.append((test, sonuc))
                kalanlar = [(x, y) for x, y in kalanlar if not all(x[a] == v for a, v in test)]
                break
        else:
            return None
    return liste


def liste_siniflandir(liste, x) -> bool:
    for test, sonuc in liste:
        if all(x[a] == v for a, v in test):
            return sonuc
    return False


# --- Öğrenme eğrisi ------------------------------------------------------------------------
def rastgele_ornek(rng: random.Random) -> tuple[dict, bool]:
    x = {a: rng.choice(v) for a, v in NITELIKLER.items()}
    return x, gercek_agac(x)


def ogrenme_egrisi(boyutlar=(5, 10, 20, 40, 80), deneme: int = 20, tohum: int = 0) -> dict:
    """100 rastgele örnek; her boyutta eğitim/test bölmesi 'deneme' kez tekrarlanır."""
    rng = random.Random(tohum)
    sonuc = {}
    for N in boyutlar:
        dogruluk = []
        for _ in range(deneme):
            veri = [rastgele_ornek(rng) for _ in range(100)]
            egitim, test = veri[:N], veri[N:]
            agac = agac_ogren(egitim, SIRA)
            dogruluk.append(sum(siniflandir(agac, x) == y for x, y in test) / len(test))
        sonuc[N] = sum(dogruluk) / len(dogruluk)
    return sonuc


def main() -> None:
    olasi = math.prod(len(v) for v in NITELIKLER.values())
    print(f"=== Restoran verisi: {len(RESTORAN)} örnek, {olasi} olası girdi ===")
    print(f"  Gerçek ağaç 12 örneğin hepsini doğru sınıflandırıyor mu? {all(gercek_agac(x) == y for x, y in RESTORAN)}")

    print("\n=== Entropi ===")
    print(f"  adil para {entropi([0.5, 0.5]):.2f} bit, dört yüzlü zar {entropi([0.25] * 4):.2f} bit, "
          f"%99 tura {B(0.99):.2f} bit, restoran çıktısı B(6/12) = {B(0.5):.2f} bit")

    print("\n=== Bilgi kazancı (bütün nitelikler) ===")
    for a in sorted(SIRA, key=lambda a: -kazanc(a, RESTORAN)):
        print(f"  Kazanç({a:<5}) = {kazanc(a, RESTORAN):.3f} bit")

    agac = agac_ogren(RESTORAN, SIRA)
    print(f"\n=== 12 örnekten öğrenilen ağaç (Şekil 19.6), {dugum_sayisi(agac)} düğüm ===")
    print(agac_yaz(agac))

    print("\n=== χ² budama (3 serbestlik derecesi) ===")
    print(f"  %5 eşiği {ki_kare_3_esik(0.05):.3f}, %1 eşiği {ki_kare_3_esik(0.01):.3f}  (kitap yuvarlayarak 7.82 ve 11.35)")
    print(f"  Kökte Δ(Type) = {sapma('Type', RESTORAN):.2f} → anlamsız (budanır)")
    dolu = [(x, y) for x, y in RESTORAN if x["Pat"] == "Full"]
    print(f"  Patrons = Full düğümünde Δ(Type) = {sapma('Type', dolu):.2f} (yalnızca {len(dolu)} örnek)")

    print("\n=== Karar listesi (en çok 2 literal) ===")
    liste = karar_listesi_ogren(RESTORAN)
    for test, sonuc in liste:
        print(f"  {' ∧ '.join(f'{a} = {v}' for a, v in test)} → {'Yes' if sonuc else 'No'}")
    print(f"  12 örnekle tutarlı mı? {all(liste_siniflandir(liste, x) == y for x, y in RESTORAN)}")

    print("\n=== Öğrenme eğrisi (gerçek ağaçtan üretilen örnekler, 20 deneme) ===")
    for N, d in ogrenme_egrisi().items():
        print(f"  eğitim kümesi {N:>3}: test doğruluğu {d:.3f}")


if __name__ == "__main__":
    main()
