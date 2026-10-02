#!/usr/bin/env python3
"""Olaylar ve zaman: olay hesabı (event calculus) ve Allen aralık ilişkileri.

1. Olay hesabı: Akışkanlar (Açık(Işık)), olaylar (IşığıAç) ve zaman noktaları.
     Happens(e, t)        e olayı t anında oldu
     Initiates(e, f, t)   e, f'yi doğru yapar
     Terminates(e, f, t)  e, f'yi yanlış yapar
     T(f, t)              f, t anında doğrudur
   Kural (ataletle): f, t anında doğrudur ⟺ daha önce bir olay onu başlattı ve arada
   hiçbir olay onu bitirmedi. Bu, Bölüm 7'deki ardıl durum aksiyomlarının zamanlı hâlidir.

2. Allen aralık ilişkileri (kitaptaki tanımlar):
     Meet(i, j)     End(i) = Begin(j)
     Before(i, j)   End(i) < Begin(j)
     During(i, j)   Begin(j) < Begin(i) < End(i) < End(j)
     Overlap(i, j)  Begin(i) < Begin(j) < End(i) < End(j)
     Starts(i, j)   Begin(i) = Begin(j)
     Finishes(i, j) End(i) = End(j)
     Equals(i, j)   Begin(i) = Begin(j) ∧ End(i) = End(j)
   Kitaptaki örnek: Meets(ReignOf(GeorgeVI), ReignOf(ElizabethII)). Burada Osmanlı ve
   Cumhuriyet tarihinden eşdeğer örnekler kullanıyoruz.

Çalıştırma:
    python olay_hesabi.py
"""
from __future__ import annotations

# ---------------------------------------------------------------------------
# 1. Olay hesabı
# ---------------------------------------------------------------------------

BASLATIR = {  # olay → başlattığı akışkanlar
    "IşığıAç": ["Açık(Işık)"],
    "EveGir(Ali)": ["İçeride(Ali)"],
    "KapıyıAç": ["Açık(Kapı)"],
}
BITIRIR = {  # olay → bitirdiği akışkanlar
    "IşığıKapat": ["Açık(Işık)"],
    "EvdenÇık(Ali)": ["İçeride(Ali)"],
    "KapıyıKapat": ["Açık(Kapı)"],
    "ElektrikKesildi": ["Açık(Işık)"],
}
OLAYLAR = [  # Happens(e, t)
    ("KapıyıAç", 1), ("EveGir(Ali)", 2), ("KapıyıKapat", 3), ("IşığıAç", 4),
    ("ElektrikKesildi", 7), ("IşığıAç", 9), ("EvdenÇık(Ali)", 11), ("IşığıKapat", 12),
]


def T(f: str, t: int, olaylar=OLAYLAR) -> bool:
    """f, t anında doğru mu? (t anındaki olayın etkisi t'den sonra başlar)"""
    son_baslatma = max((te for e, te in olaylar if te < t and f in BASLATIR.get(e, [])), default=None)
    if son_baslatma is None:
        return False
    bitirildi_mi = any(son_baslatma < te < t and f in BITIRIR.get(e, []) for e, te in olaylar)
    return not bitirildi_mi


def zaman_cizelgesi(akiskanlar: list[str], son: int = 13) -> str:
    satirlar = ["  " + " " * 12 + "".join(f"{t:>3}" for t in range(son + 1))]
    for f in akiskanlar:
        satirlar.append(f"  {f:<12}" + "".join("  █" if T(f, t) else "  ·" for t in range(son + 1)))
    return "\n".join(satirlar)


# ---------------------------------------------------------------------------
# 2. Allen aralık ilişkileri (kitaptaki tanımlar)
# ---------------------------------------------------------------------------

def Meet(i, j): return i[1] == j[0]  # noqa: E704
def Before(i, j): return i[1] < j[0]  # noqa: E704
def After(j, i): return Before(i, j)  # noqa: E704
def During(i, j): return j[0] < i[0] < i[1] < j[1]  # noqa: E704
def Overlap(i, j): return i[0] < j[0] < i[1] < j[1]  # noqa: E704
def Starts(i, j): return i[0] == j[0]  # noqa: E704
def Finishes(i, j): return i[1] == j[1]  # noqa: E704
def Equals(i, j): return i[0] == j[0] and i[1] == j[1]  # noqa: E704


ILISKILER = {"Meet": Meet, "Before": Before, "After": After, "During": During,
             "Overlap": Overlap, "Starts": Starts, "Finishes": Finishes, "Equals": Equals}

ARALIKLAR = {  # yıl olarak; Sinan'ın doğum yılı yaklaşıktır
    "Saltanat(Fatih)": (1451, 1481),
    "Saltanat(II. Bayezid)": (1481, 1512),
    "Saltanat(Kanuni)": (1520, 1566),
    "Başmimarlık(Sinan)": (1538, 1588),
    "Hayat(Sinan)": (1490, 1588),
    "İnşa(Süleymaniye)": (1550, 1557),
    "Cumhurbaşkanlığı(Atatürk)": (1923, 1938),
    "Cumhurbaşkanlığı(İnönü)": (1938, 1950),
    "Cumhuriyet'in ilk yılı": (1923, 1924),
}


def iliskiler(a: str, b: str) -> list[str]:
    i, j = ARALIKLAR[a], ARALIKLAR[b]
    return [ad for ad, f in ILISKILER.items() if f(i, j)]


def main() -> None:
    print("=== Olay hesabı ===")
    print("Olaylar: " + ", ".join(f"{e}@{t}" for e, t in OLAYLAR))
    print(zaman_cizelgesi(["Açık(Işık)", "İçeride(Ali)", "Açık(Kapı)"]))
    print("  Işık 4'te açıldı, 7'de elektrik kesilince kapandı, 9'da tekrar açıldı, 12'de kapatıldı."
          "\n  Arada hiçbir olay olmayan anlarda da değer korunur: atalet (çerçeve problemi çözümü).")

    print("\n=== Allen aralık ilişkileri ===")
    ciftler = [
        ("Saltanat(Fatih)", "Saltanat(II. Bayezid)"),
        ("Cumhurbaşkanlığı(Atatürk)", "Cumhurbaşkanlığı(İnönü)"),
        ("Saltanat(Fatih)", "Saltanat(Kanuni)"),
        ("İnşa(Süleymaniye)", "Saltanat(Kanuni)"),
        ("Saltanat(Kanuni)", "Başmimarlık(Sinan)"),
        ("Cumhuriyet'in ilk yılı", "Cumhurbaşkanlığı(Atatürk)"),
        ("Başmimarlık(Sinan)", "Hayat(Sinan)"),
    ]
    for a, b in ciftler:
        print(f"  {a:<26} {ARALIKLAR[a]}  —  {b:<26} {ARALIKLAR[b]}:  {', '.join(iliskiler(a, b)) or '—'}")
    print("\n  Kitaptaki Overlap tanımı simetrik değildir: Overlap(i, j) için i, j'den önce başlamalı."
          "\n  Starts ve Finishes burada yalnızca uç eşitliğini ister (Allen'ın özgün tanımından daha gevşek).")


if __name__ == "__main__":
    main()
