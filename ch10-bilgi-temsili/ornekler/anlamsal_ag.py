#!/usr/bin/env python3
"""Anlamsal ağlar ve doğruluk bakım sistemi (JTMS).

1. Anlamsal ağ: kategoriler ve nesneler düğüm, ilişkiler bağlantıdır.
   - AltKüme (⊂) ve Üye (∈) bağlantıları üzerinden KALITIM
   - Kategoriye bağlı özellikler varsayılandır; daha özel bilgi onu geçersiz kılar.
     Kitaptaki örnek: Kişilerin 2 bacağı vardır; Uzun John Silver'ın 1 bacağı vardır.
   - Çoklu kalıtım çatışabilir (Nixon elması).

2. JTMS (gerekçe tabanlı doğruluk bakım sistemi): her inanç, onu destekleyen
   gerekçelerle saklanır. Bir varsayım GERİ ÇEKİLİNCE, yalnızca desteği kalmayan
   inançlar düşer; bağımsız gerekçesi olanlar kalır.

Çalıştırma:
    python anlamsal_ag.py
"""
from __future__ import annotations

# ---------------------------------------------------------------------------
# 1. Anlamsal ağ
# ---------------------------------------------------------------------------

ALT_KUME = {  # kategori → üst kategoriler
    "Kadınlar": ["Kişiler"], "Erkekler": ["Kişiler"], "Kişiler": ["Memeliler"], "Memeliler": ["Hayvanlar"],
    "Quakerlar": ["Kişiler"], "Cumhuriyetçiler": ["Kişiler"],
}
UYE = {  # nesne → kategoriler
    "Meryem": ["Kadınlar"], "Yahya": ["Erkekler"], "UzunJohnSilver": ["Erkekler"],
    "Nixon": ["Quakerlar", "Cumhuriyetçiler"],
}
OZELLIK = {  # düğüm → {özellik: değer}  (kategori özellikleri varsayılandır)
    "Kişiler": {"bacak": 2},
    "Memeliler": {"sıcakkanlı": True},
    "UzunJohnSilver": {"bacak": 1},
    "Quakerlar": {"pasifist": True},
    "Cumhuriyetçiler": {"pasifist": False},
}
ILISKI = {("Meryem", "kardeşi"): "Yahya"}


def ust_kategoriler(dugum: str) -> list[list[str]]:
    """Düğümden yukarı doğru seviye seviye kategoriler (genişlik öncelikli)."""
    seviyeler, simdiki, gorulen = [], UYE.get(dugum, ALT_KUME.get(dugum, [])), set()
    while simdiki:
        simdiki = [k for k in simdiki if k not in gorulen]
        gorulen |= set(simdiki)
        if simdiki:
            seviyeler.append(simdiki)
        simdiki = [u for k in simdiki for u in ALT_KUME.get(k, [])]
    return seviyeler


def deger(dugum: str, ozellik: str):
    """En özel bilgiyi bul. Aynı seviyede çelişen değerler varsa çatışmayı bildir."""
    if ozellik in OZELLIK.get(dugum, {}):
        return OZELLIK[dugum][ozellik], dugum
    for seviye in ust_kategoriler(dugum):
        bulunan = {k: OZELLIK[k][ozellik] for k in seviye if ozellik in OZELLIK.get(k, {})}
        if len(set(bulunan.values())) > 1:
            return "ÇATIŞMA " + str(bulunan), "çoklu kalıtım"
        if bulunan:
            k, v = next(iter(bulunan.items()))
            return v, k
    return None, None


def uye_mi(nesne: str, kategori: str) -> bool:
    return any(kategori in s for s in ust_kategoriler(nesne))


# ---------------------------------------------------------------------------
# 2. JTMS
# ---------------------------------------------------------------------------

class JTMS:
    def __init__(self) -> None:
        self.varsayimlar: set[str] = set()
        self.gerekceler: dict[str, list[set[str]]] = {}  # inanç → [öncül kümeleri]

    def varsay(self, p: str) -> None:
        self.varsayimlar.add(p)

    def gerekce(self, sonuc: str, onculler: set[str]) -> None:
        self.gerekceler.setdefault(sonuc, []).append(set(onculler))

    def geri_cek(self, p: str) -> None:
        self.varsayimlar.discard(p)

    def inanclar(self) -> set[str]:
        """İÇERİDE olan inançlar: varsayımlar + öncüllerinin hepsi içeride olan gerekçeler (sabit nokta)."""
        iceride = set(self.varsayimlar)
        degisti = True
        while degisti:
            degisti = False
            for s, liste in self.gerekceler.items():
                if s not in iceride and any(g <= iceride for g in liste):
                    iceride.add(s)
                    degisti = True
        return iceride


def main() -> None:
    print("=== Anlamsal ağ: kalıtım ve varsayılanlar ===")
    for nesne, ozellik in [("Meryem", "bacak"), ("UzunJohnSilver", "bacak"),
                           ("Meryem", "sıcakkanlı"), ("Nixon", "pasifist")]:
        v, kaynak = deger(nesne, ozellik)
        print(f"  {ozellik}({nesne}) = {v}   [kaynak: {kaynak}]")
    print(f"  Üye(Meryem, Hayvanlar)? {uye_mi('Meryem', 'Hayvanlar')}")
    print(f"  kardeşi(Meryem) = {ILISKI[('Meryem', 'kardeşi')]}")
    print("  Uzun John Silver'ın kendi değeri (1), Kişiler kategorisinden gelen varsayılanı (2) geçersiz"
          "\n  kılar. Nixon'da iki üst kategori çelişir: ağ tek başına karar veremez.")

    print("\n=== JTMS ===")
    t = JTMS()
    for p in ("Yağmur", "Sulama"):
        t.varsay(p)
    t.gerekce("IslakÇim", {"Yağmur"})
    t.gerekce("IslakÇim", {"Sulama"})
    t.gerekce("KayganYol", {"Yağmur"})
    t.gerekce("Şemsiye", {"Yağmur"})
    print(f"  Varsayımlar: Yağmur, Sulama → inançlar: {sorted(t.inanclar())}")
    t.geri_cek("Yağmur")
    print(f"  Yağmur geri çekildi        → inançlar: {sorted(t.inanclar())}")
    print("  IslakÇim kaldı: Sulama'dan gelen bağımsız bir gerekçesi var. KayganYol ve Şemsiye düştü."
          "\n  Basit bir 'geri al' yaklaşımı ise Yağmur'dan sonra eklenen her şeyi silerdi.")


if __name__ == "__main__":
    main()
