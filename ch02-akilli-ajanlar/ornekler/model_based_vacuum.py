#!/usr/bin/env python3
"""
Modele dayalı süpürge ajanı — Bölüm 2 eğitici örnek.

İki oda (A, B). Basit refleks sadece bulunduğu odayı bilir;
modele dayalı ajan her iki odanın durumunu iç bellekte tutar
ve her yer temizlenince beklemeye geçer.

Çalıştırma:
    python model_based_vacuum.py
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Dict, List, Optional, Tuple


class Konum(str, Enum):
    A = "A"
    B = "B"


class Durum(str, Enum):
    TEMIZ = "Temiz"
    KIRLI = "Kirli"
    BILINMIYOR = "?"  # henüz gözlenmedi


class Eylem(str, Enum):
    SOL = "Sol"
    SAG = "Sağ"
    SUPUR = "Süpür"
    BEKLE = "Bekle"


@dataclass
class Ortam:
    """İki odalı ortam. Ajan yalnızca bulunduğu odayı doğrudan algılar."""

    ajan_konumu: Konum = Konum.A
    odalar: Dict[Konum, Durum] = field(
        default_factory=lambda: {Konum.A: Durum.KIRLI, Konum.B: Durum.KIRLI}
    )
    adim: int = 0
    gunluk: List[str] = field(default_factory=list)

    def algila(self) -> Tuple[Konum, Durum]:
        return self.ajan_konumu, self.odalar[self.ajan_konumu]

    def uygula(self, eylem: Eylem) -> None:
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
            f"Adım {self.adim}: {onceki} → {eylem.value} → {self.ozet()}"
        )

    def ozet(self) -> str:
        a = self.odalar[Konum.A].value
        b = self.odalar[Konum.B].value
        return f"[A:{a}, B:{b}, ajan@{self.ajan_konumu.value}]"

    def her_sey_temiz(self) -> bool:
        return all(d == Durum.TEMIZ for d in self.odalar.values())


def basit_refleks(algı: Tuple[Konum, Durum], _bellek: Optional[dict] = None) -> Eylem:
    """Belleksiz: kirliyse süpür, değilse diğer odaya git (mekik)."""
    konum, durum = algı
    if durum == Durum.KIRLI:
        return Eylem.SUPUR
    return Eylem.SAG if konum == Konum.A else Eylem.SOL


class ModeleDayaliAjan:
    """
    İç model: her odanın bilinen durumu.
    Algı geldikçe belleği günceller; her yer temizse bekler.
    """

    def __init__(self) -> None:
        self.bellek: Dict[Konum, Durum] = {
            Konum.A: Durum.BILINMIYOR,
            Konum.B: Durum.BILINMIYOR,
        }

    def karar(self, algı: Tuple[Konum, Durum]) -> Eylem:
        konum, durum = algı
        self.bellek[konum] = durum  # mevcut odayı güncelle

        if durum == Durum.KIRLI:
            return Eylem.SUPUR

        # Süpürdükten sonra bellekte bu oda temiz sayılır
        self.bellek[konum] = Durum.TEMIZ

        diger = Konum.B if konum == Konum.A else Konum.A
        diger_durum = self.bellek[diger]

        # Diğer oda kirli veya bilinmiyor → oraya git
        if diger_durum in (Durum.KIRLI, Durum.BILINMIYOR):
            return Eylem.SAG if diger == Konum.B else Eylem.SOL

        # Her iki oda da temiz (veya bilinen temiz) → bekle
        return Eylem.BEKLE


def simulasyon(
    ajan_fn: Callable,
    etiket: str,
    baslangic: Konum = Konum.A,
    oda_a: Durum = Durum.KIRLI,
    oda_b: Durum = Durum.KIRLI,
    max_adim: int = 12,
    ajan_nesnesi: Optional[ModeleDayaliAjan] = None,
) -> Ortam:
    ortam = Ortam(
        ajan_konumu=baslangic,
        odalar={Konum.A: oda_a, Konum.B: oda_b},
    )
    print(f"=== {etiket} ===")
    print(f"Başlangıç: {ortam.ozet()} | max_adim={max_adim}\n")

    for _ in range(max_adim):
        algı = ortam.algila()
        if ajan_nesnesi is not None:
            eylem = ajan_nesnesi.karar(algı)
            bellek_ozet = (
                f"bellek={{A:{ajan_nesnesi.bellek[Konum.A].value}, "
                f"B:{ajan_nesnesi.bellek[Konum.B].value}}}"
            )
        else:
            eylem = ajan_fn(algı)
            bellek_ozet = "bellek=yok"

        print(
            f"Algı: {algı[0].value}/{algı[1].value} | {bellek_ozet} → {eylem.value}"
        )
        ortam.uygula(eylem)

        if eylem == Eylem.BEKLE and ortam.her_sey_temiz():
            print("\n(Durma: her yer temiz, ajan bekliyor.)")
            break
        if ajan_nesnesi is None and ortam.her_sey_temiz() and eylem == Eylem.BEKLE:
            break

    print("\n--- Günlük ---")
    for s in ortam.gunluk:
        print(s)
    print(f"Toplam adım: {ortam.adim}")
    print(f"Temiz oda: {sum(1 for d in ortam.odalar.values() if d == Durum.TEMIZ)}/2\n")
    return ortam


def karsilastir() -> None:
    print("# Senaryo: A=Kirli, B=Kirli, ajan=A\n")
    o1 = simulasyon(basit_refleks, "Basit refleks", max_adim=10)
    ajan = ModeleDayaliAjan()
    o2 = simulasyon(
        lambda a: ajan.karar(a),
        "Modele dayalı (bellekli)",
        max_adim=10,
        ajan_nesnesi=ajan,
    )

    print("=" * 50)
    print("KARŞILAŞTIRMA")
    print(f"  Basit refleks adım sayısı : {o1.adim}")
    print(f"  Modele dayalı adım sayısı : {o2.adim}")
    print(
        "  Not: Basit refleks temizlendikten sonra da mekik atar; "
        "modele dayalı ajan iş bitince bekler."
    )


def main() -> None:
    karsilastir()
    print("\n" + "=" * 50 + "\n")
    print("# Senaryo 2: A=Temiz, B=Kirli, ajan=A\n")
    simulasyon(basit_refleks, "Basit refleks", oda_a=Durum.TEMIZ, oda_b=Durum.KIRLI, max_adim=8)
    ajan2 = ModeleDayaliAjan()
    simulasyon(
        lambda a: ajan2.karar(a),
        "Modele dayalı",
        oda_a=Durum.TEMIZ,
        oda_b=Durum.KIRLI,
        max_adim=8,
        ajan_nesnesi=ajan2,
    )


if __name__ == "__main__":
    main()
