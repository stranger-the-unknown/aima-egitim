#!/usr/bin/env python3
"""Bilgi mühendisliği örneği: bir bitlik tam toplayıcı devresi (kitaptaki C1).

Kitaptaki yedi adımlık süreç:
  1. Görevi belirle         : devre doğru topluyor mu? (doğrulama)
  2. İlgili bilgiyi topla   : kapılar, bağlantılar, sinyaller
  3. Sözcük dağarcığı       : Kapı(x), Tip(x) = XOR/AND/OR, Bağlı(u1, u2), Sinyal(u), Giriş(n, x), Çıkış(n, x)
  4. Genel alan bilgisi     : "bağlı uçların sinyali eşittir", "AND kapısının çıkışı …"
  5. Problem örneği         : C1'in kapıları ve bağlantıları
  6. Sorgular               : ∃ i1,i2,i3 … toplam = 0 ∧ elde = 1 ?
  7. Hata ayıkla            : bilgi tabanını boz ve davranışı izle

C1: iki XOR (X1, X2), iki AND (A1, A2), bir OR (O1). Bağlantılar kitaptakiyle aynıdır.
Kitaptaki sorgu yanıtı: toplam = 0 ve elde = 1 veren girişler
    {i1=1, i2=1, i3=0}, {1, 0, 1}, {0, 1, 1}

Çalıştırma:
    python tam_toplayici.py
"""
from __future__ import annotations

from itertools import product

# 5. adım: problem örneği (kitaptaki C1)
KAPILAR = {"X1": "XOR", "X2": "XOR", "A1": "AND", "A2": "AND", "O1": "OR"}
BAGLANTILAR = [
    (("Çıkış", 1, "X1"), ("Giriş", 1, "X2")),
    (("Çıkış", 1, "X1"), ("Giriş", 2, "A2")),
    (("Çıkış", 1, "A2"), ("Giriş", 1, "O1")),
    (("Çıkış", 1, "A1"), ("Giriş", 2, "O1")),
    (("Çıkış", 1, "X2"), ("Çıkış", 1, "C1")),
    (("Çıkış", 1, "O1"), ("Çıkış", 2, "C1")),
    (("Giriş", 1, "C1"), ("Giriş", 1, "X1")),
    (("Giriş", 1, "C1"), ("Giriş", 1, "A1")),
    (("Giriş", 2, "C1"), ("Giriş", 2, "X1")),
    (("Giriş", 2, "C1"), ("Giriş", 2, "A1")),
    (("Giriş", 3, "C1"), ("Giriş", 2, "X2")),
    (("Giriş", 3, "C1"), ("Giriş", 1, "A2")),
]

# 4. adım: genel alan bilgisi (kapı davranışları)
KAPI_KURALI = {
    "AND": lambda a, b: int(a and b),
    "OR": lambda a, b: int(a or b),
    "XOR": lambda a, b: int(a != b),
}


def sinyalleri_cikar(girisler: tuple[int, int, int], kapilar=KAPILAR, baglantilar=BAGLANTILAR) -> dict:
    """İleri zincirleme: sinyal bilinen uçlardan bağlı uçlara ve kapı çıkışlarına yayılır.

    Aksiyomlar (kod karşılığı):
      ∀u1,u2 Bağlı(u1,u2) ⇒ Sinyal(u1) = Sinyal(u2)
      ∀g Tip(g) = AND ⇒ (Sinyal(Çıkış(1,g)) = 1 ⇔ ∀n Sinyal(Giriş(n,g)) = 1)   (OR, XOR benzer)
    """
    sinyal = {("Giriş", i + 1, "C1"): v for i, v in enumerate(girisler)}
    degisti = True
    while degisti:
        degisti = False
        for u1, u2 in baglantilar:  # bağlantılar iki yönlüdür (Bağlı simetriktir)
            for a, b in ((u1, u2), (u2, u1)):
                if a in sinyal and b not in sinyal:
                    sinyal[b] = sinyal[a]
                    degisti = True
        for g, tip in kapilar.items():
            g1, g2, cik = ("Giriş", 1, g), ("Giriş", 2, g), ("Çıkış", 1, g)
            if g1 in sinyal and g2 in sinyal and cik not in sinyal:
                sinyal[cik] = KAPI_KURALI[tip](sinyal[g1], sinyal[g2])
                degisti = True
    return sinyal


def cikislar(girisler, **kw) -> tuple:
    s = sinyalleri_cikar(girisler, **kw)
    return s.get(("Çıkış", 1, "C1")), s.get(("Çıkış", 2, "C1"))


def sorgu(toplam: int, elde: int, **kw) -> list[tuple[int, int, int]]:
    """ASKVARS: çıkışları verilen değerler olan tüm giriş atamaları."""
    return [g for g in product((0, 1), repeat=3) if cikislar(g, **kw) == (toplam, elde)]


def dogrula(**kw) -> list[tuple]:
    """Devre gerçekten topluyor mu? Hatalı girişleri döndür."""
    hatalar = []
    for g in product((0, 1), repeat=3):
        beklenen = (sum(g) % 2, sum(g) // 2)
        if cikislar(g, **kw) != beklenen:
            hatalar.append((g, cikislar(g, **kw), beklenen))
    return hatalar


def main() -> None:
    print("Kapılar:", ", ".join(f"{g}={t}" for g, t in KAPILAR.items()))
    print(f"Bağlantı sayısı: {len(BAGLANTILAR)}\n")

    print("Sorgu: toplam = 0 ve elde = 1 veren girişler (kitap: 110, 101, 011)")
    for g in sorgu(0, 1):
        print(f"  i1={g[0]}, i2={g[1]}, i3={g[2]}")

    print("\nTam giriş–çıkış tablosu:")
    print("  i1 i2 i3 │ toplam elde │ i1+i2+i3")
    for g in product((0, 1), repeat=3):
        o1, o2 = cikislar(g)
        print(f"   {g[0]}  {g[1]}  {g[2]} │   {o1}     {o2}   │    {sum(g)}")
    print(f"Doğrulama: hata sayısı = {len(dogrula())}  → devre doğru toplayıcıdır.\n")

    print("7. adım, hata ayıklama: A2'nin girişini yanlış bağlayalım (X1 yerine doğrudan In(1,C1)).")
    bozuk = [b for b in BAGLANTILAR if b != (("Çıkış", 1, "X1"), ("Giriş", 2, "A2"))]
    bozuk.append((("Giriş", 1, "C1"), ("Giriş", 2, "A2")))
    for g, gercek, beklenen in dogrula(baglantilar=bozuk):
        print(f"  giriş {g}: çıkış {gercek}, olması gereken {beklenen}")
    print("Hatalı satırlar, hangi kapının yanlış çıktı verdiğini aramaya başlamak için ipucu verir.")


if __name__ == "__main__":
    main()
