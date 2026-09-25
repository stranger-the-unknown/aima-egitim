#!/usr/bin/env python3
"""
Klasik süpürge dünyası (Vacuum World) — eğitici örnek.

İki oda (A ve B). Her oda Temiz veya Kirli olabilir.
Basit refleks ajanı: sadece mevcut algıya bakarak karar verir.

Çalıştırma:
    python vacuum_agent.py
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List


class Konum(str, Enum):
    A = "A"
    B = "B"


class Durum(str, Enum):
    TEMIZ = "Temiz"
    KIRLI = "Kirli"


class Eylem(str, Enum):
    SOL = "Sol"
    SAG = "Sağ"
    SUPUR = "Süpür"
    BEKLE = "Bekle"


@dataclass
class Ortam:
    """İki odalı basit ortam. Ajanın konumu ve odaların kirlilik durumu."""

    ajan_konumu: Konum = Konum.A
    odalar: dict = field(default_factory=lambda: {Konum.A: Durum.KIRLI, Konum.B: Durum.KIRLI})
    adim: int = 0
    gunluk: List[str] = field(default_factory=list)

    def algila(self) -> tuple[Konum, Durum]:
        """Ajanın bulunduğu odanın konumunu ve durumunu döndürür (tam gözlem varsayımı)."""
        return self.ajan_konumu, self.odalar[self.ajan_konumu]

    def uygula(self, eylem: Eylem) -> None:
        """Eylemi ortamda uygula ve günlüğe yaz."""
        onceki = self.ozet()
        if eylem == Eylem.SUPUR:
            self.odalar[self.ajan_konumu] = Durum.TEMIZ
        elif eylem == Eylem.SOL:
            self.ajan_konumu = Konum.A
        elif eylem == Eylem.SAG:
            self.ajan_konumu = Konum.B
        elif eylem == Eylem.BEKLE:
            pass
        else:
            raise ValueError(f"Bilinmeyen eylem: {eylem}")

        self.adim += 1
        self.gunluk.append(
            f"Adım {self.adim}: {onceki} → eylem={eylem.value} → {self.ozet()}"
        )

    def ozet(self) -> str:
        a = self.odalar[Konum.A].value
        b = self.odalar[Konum.B].value
        return f"[A:{a}, B:{b}, ajan@{self.ajan_konumu.value}]"

    def her_sey_temiz(self) -> bool:
        return all(d == Durum.TEMIZ for d in self.odalar.values())


def basit_refleks_ajan(algı: tuple[Konum, Durum]) -> Eylem:
    """
    Basit refleks kuralları (bellek yok):

    - Bulunduğun oda kirliyse → Süpür
    - A'daysan ve temizse → Sağ'a git
    - B'deysen ve temizse → Sol'a git

    Not: Bu ajan 'diğer oda temiz mi?' bilgisini kullanmaz;
    sürekli iki oda arasında gidip gelebilir. Eğitim için kasıtlı sade.
    """
    konum, durum = algı
    if durum == Durum.KIRLI:
        return Eylem.SUPUR
    if konum == Konum.A:
        return Eylem.SAG
    return Eylem.SOL


def simulasyon(
    baslangic_konum: Konum = Konum.A,
    oda_a: Durum = Durum.KIRLI,
    oda_b: Durum = Durum.KIRLI,
    max_adim: int = 8,
) -> Ortam:
    """Ortam + ajan döngüsünü çalıştır; günlüğü doldur."""
    ortam = Ortam(
        ajan_konumu=baslangic_konum,
        odalar={Konum.A: oda_a, Konum.B: oda_b},
    )
    print("=== Süpürge Dünyası Simülasyonu ===")
    print(f"Başlangıç: {ortam.ozet()}")
    print(f"Maksimum adım: {max_adim}\n")

    for _ in range(max_adim):
        algı = ortam.algila()
        eylem = basit_refleks_ajan(algı)
        print(f"Algı: konum={algı[0].value}, durum={algı[1].value} → seçilen eylem: {eylem.value}")
        ortam.uygula(eylem)
        if ortam.her_sey_temiz() and ortam.ajan_konumu == Konum.A:
            # İsteğe bağlı erken durma koşulu (eğitsel): her yer temiz ve A'ya döndü
            print("\n(Erken durma: her iki oda temiz ve ajan A'da.)")
            break

    print("\n--- Günlük ---")
    for satir in ortam.gunluk:
        print(satir)

    performans = sum(1 for d in ortam.odalar.values() if d == Durum.TEMIZ)
    print(f"\nPerformans (temiz oda sayısı / 2): {performans}/2")
    print(f"Toplam adım: {ortam.adim}")
    return ortam


def main() -> None:
    # Senaryo 1: her iki oda kirli, ajan A'da
    print("Senaryo 1: A=Kirli, B=Kirli, ajan=A\n")
    simulasyon(Konum.A, Durum.KIRLI, Durum.KIRLI, max_adim=6)

    print("\n" + "=" * 50 + "\n")

    # Senaryo 2: sadece B kirli, ajan A'da
    print("Senaryo 2: A=Temiz, B=Kirli, ajan=A\n")
    simulasyon(Konum.A, Durum.TEMIZ, Durum.KIRLI, max_adim=6)


if __name__ == "__main__":
    main()
