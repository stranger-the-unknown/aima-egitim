#!/usr/bin/env python3
"""Kitabın klasik CSP örneği: Avustralya haritasını üç renkle boyamak.

Değişkenler: WA, NT, Q, NSW, V, SA, T  ·  Alan: {kırmızı, yeşil, mavi}
Kısıt: komşu bölgeler farklı renk. (T, yani Tazmanya, hiçbir bölgeye komşu değil.)

Kitaptaki gözlemler (testlerle doğrulanır):
  * İleri kontrol: WA=kırmızı, Q=yeşil sonra NT ve SA'nın tek değeri kalır (mavi);
    V=mavi atanınca SA'nın alanı BOŞALIR → hemen geri dönülür.
  * MAC, {WA=kırmızı, Q=yeşil} anında tutarsızlığı görür (NT ve SA ikisi de yalnız mavi
    ama komşular). İleri kontrol bunu kaçırır.
  * LCV: WA=kırmızı, NT=yeşil iken Q için kırmızı, maviden önce gelir
    (mavi, SA'nın son değerini de siler).
  * SA'yı atayınca kalan graf bir ağaçtır → kesme kümesi {SA}.

Çalıştırma:
    python avustralya_csp.py
"""
from __future__ import annotations

from kisit import CSP, ac3, agac_coz, geri_izleme, kesme_kumesi_coz

BOLGELER = ["WA", "NT", "Q", "NSW", "V", "SA", "T"]
KOMSULAR = {
    "WA": ["NT", "SA"], "NT": ["WA", "SA", "Q"], "Q": ["NT", "SA", "NSW"],
    "NSW": ["Q", "SA", "V"], "V": ["SA", "NSW"], "SA": ["WA", "NT", "Q", "NSW", "V"], "T": [],
}
RENKLER = ["kırmızı", "yeşil", "mavi"]


def avustralya(renkler=RENKLER) -> CSP:
    return CSP(BOLGELER, {b: renkler for b in BOLGELER}, KOMSULAR)


def ileri_kontrol_izi(atamalar: list[tuple[str, str]]) -> list[tuple[str, dict]]:
    """Kitaptaki şekildeki gibi: her atamadan sonra ileri kontrolle alanlar."""
    csp = avustralya()
    alanlar = {b: list(RENKLER) for b in BOLGELER}
    iz = [("Başlangıç", {b: list(d) for b, d in alanlar.items()})]
    atanan = set()
    for X, x in atamalar:
        alanlar[X] = [x]
        atanan.add(X)
        for Y in csp.komsular[X]:
            if Y not in atanan:
                alanlar[Y] = [y for y in alanlar[Y] if y != x]
        iz.append((f"{X}={x}", {b: list(d) for b, d in alanlar.items()}))
    return iz


def kisa(renk_listesi: list[str]) -> str:
    return "".join(r[0].upper() for r in renk_listesi) or "∅"


def main() -> None:
    csp = avustralya()

    print("=== İleri kontrolün ilerleyişi (kitaptaki şekil) ===")
    print(f"{'':<14}" + "".join(f"{b:>5}" for b in BOLGELER))
    for etiket, alanlar in ileri_kontrol_izi([("WA", "kırmızı"), ("Q", "yeşil"), ("V", "mavi")]):
        print(f"{etiket:<14}" + "".join(f"{kisa(alanlar[b]):>5}" for b in BOLGELER))
    print("  (K = kırmızı, Y = yeşil, M = mavi) — V=mavi sonrası SA'nın alanı boş: geri dön.")

    print("\n=== MAC, ileri kontrolün kaçırdığını görür ===")
    alanlar = {b: list(RENKLER) for b in BOLGELER}
    alanlar["WA"], alanlar["Q"] = ["kırmızı"], ["yeşil"]
    for Y in ("NT", "SA"):
        alanlar[Y] = ["mavi"]
    alanlar["NSW"] = ["kırmızı", "mavi"]
    tutarli, _ = ac3(csp, alanlar)
    print("  WA=kırmızı, Q=yeşil sonrası: NT={mavi}, SA={mavi} ve NT–SA komşu.")
    print(f"  AC-3 tutarlı buldu mu? {tutarli}  → MAC hemen geri döner, ileri kontrol devam ederdi.")

    print("\n=== LCV: WA=kırmızı, NT=yeşil iken Q'nun değerleri ===")
    for q in ("kırmızı", "mavi"):
        atama = {"WA": "kırmızı", "NT": "yeşil", "Q": q}
        sa = [r for r in RENKLER if csp.tutarli("SA", r, atama)]
        print(f"  Q={q:<8} → SA'nın kalan değerleri: {sa or '∅'}")
    print("  LCV kırmızıyı önce dener: komşulara daha çok seçenek bırakır.")

    print("\n=== Tüm çözümler ve arama maliyetleri ===")
    tum, _ = geri_izleme(csp, tum_cozumler=True)
    print(f"  3 renkle çözüm sayısı: {len(tum)}  (anakara için 3! = 6 × Tazmanya için 3)")
    print(f"  {'değişken seçimi':<16}{'değer sırası':<14}{'çıkarım':<9}{'atama':>7}{'geri dönüş':>12}")
    for ds, dsr, ck in [("sirali", "sirali", "yok"), ("derece", "sirali", "yok"),
                        ("mrv", "sirali", "ileri"), ("mrv", "lcv", "mac")]:
        c, ist = geri_izleme(csp, ds, dsr, ck)
        print(f"  {ds:<16}{dsr:<14}{ck:<9}{ist.atama:>7}{ist.geri_donus:>12}")
    c, _ = geri_izleme(csp, "mrv", "lcv", "mac")
    print(f"  Bir çözüm: {c[0]}")

    print("\n=== Problemin yapısı: kesme kümesi {SA} ===")
    agac = CSP([b for b in BOLGELER if b != "SA"], csp.alanlar,
               {b: [k for k in KOMSULAR[b] if k != "SA"] for b in BOLGELER if b != "SA"})
    print(f"  SA çıkarılınca kalan graf ağaç mı? {'evet' if agac_coz(agac) is not None else 'hayır'}")
    print(f"  Kesme kümesiyle çözüm: {kesme_kumesi_coz(csp, ['SA'])}")
    print("  Kesme kümesi boyutu c için süre O(d^c · (n−c)·d²): burada 3 × küçük bir ağaç.")


if __name__ == "__main__":
    main()
