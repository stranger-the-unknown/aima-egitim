#!/usr/bin/env python3
"""2×2 tehlikeli ızgara — esinti/koku algısından güvenli kare çıkarımı.

Özgün eğitim senaryosu (kitap anlatısının kopyası değil).
Kurallar:
  - Çukur komşusunda esinti hissedilir (ve tersi: esinti ⇒ en az bir komşuda çukur).
  - Bu demoda çukur konumunu gizli tutarız; ajan yalnızca algı + mantıkla ilerler.
  - Başlangıç (0,0) güvenli kabul edilir.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple

Coord = Tuple[int, int]
N = 2  # 2×2 ızgara


def komsular(c: Coord) -> List[Coord]:
    x, y = c
    aday = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    return [(a, b) for a, b in aday if 0 <= a < N and 0 <= b < N]


@dataclass
class IzgaraDunyasi:
    """Gizli gerçek dünya (simülasyon için). Ajan bunu doğrudan görmez."""
    cukurlar: Set[Coord] = field(default_factory=set)
    yaratik: Optional[Coord] = None

    def algi(self, konum: Coord) -> Dict[str, bool]:
        esinti = any(k in self.cukurlar for k in komsular(konum))
        koku = self.yaratik is not None and self.yaratik in komsular(konum)
        # Bu demoda parıltı / diğer duyular yok
        return {"esinti": esinti, "koku": koku}


@dataclass
class AjanBilgisi:
    ziyaret: Set[Coord] = field(default_factory=set)
    algi_kaydi: Dict[Coord, Dict[str, bool]] = field(default_factory=dict)
    # Kesin bildiklerimiz
    guvenli: Set[Coord] = field(default_factory=set)
    cukur_var: Set[Coord] = field(default_factory=set)  # kesin çukur
    cukur_yok: Set[Coord] = field(default_factory=set)
    # Şüpheli: henüz elenemeyen olası çukur adayları
    olasi_cukur: Set[Coord] = field(default_factory=set)

    def tell_algi(self, konum: Coord, algi: Dict[str, bool]) -> None:
        self.ziyaret.add(konum)
        self.algi_kaydi[konum] = algi
        self.guvenli.add(konum)
        self.cukur_yok.add(konum)
        self.olasi_cukur.discard(konum)
        self._cikarim()

    def _cikarim(self) -> None:
        """Basit kurallar (özgün, eğitimsel):

        1) Bir karede esinti YOKSA → tüm komşularında çukur YOK (güvenli aday).
        2) Esinti VARSA → komşulardan en az biri çukur; bilinen güvenli/çukur-yok
           dışındakiler olası_cukur'a eklenir.
        3) Esintili bir karenin komşularından yalnızca **bir** şüpheli kaldıysa
           o kare kesin çukur sayılır (tek aday elimasyonu).
        """
        degisti = True
        while degisti:
            degisti = False
            for konum, algi in list(self.algi_kaydi.items()):
                ks = komsular(konum)
                if not algi["esinti"]:
                    for k in ks:
                        if k not in self.cukur_yok:
                            self.cukur_yok.add(k)
                            self.guvenli.add(k)
                            self.olasi_cukur.discard(k)
                            degisti = True
                else:
                    # esinti var
                    adaylar = [k for k in ks if k not in self.cukur_yok]
                    for k in adaylar:
                        if k not in self.cukur_var and k not in self.ziyaret:
                            if k not in self.olasi_cukur:
                                self.olasi_cukur.add(k)
                                degisti = True
                    # tek aday
                    supheli = [k for k in ks if k not in self.cukur_yok and k not in self.ziyaret]
                    if len(supheli) == 1:
                        tek = supheli[0]
                        if tek not in self.cukur_var:
                            self.cukur_var.add(tek)
                            self.olasi_cukur.discard(tek)
                            self.guvenli.discard(tek)
                            degisti = True
                            # Bu çukur, diğer esintileri de açıklayabilir → yeniden
                            print(f"  [çıkarım] Tek aday: {tek} kesin çukur.")


def tahta_yazdir(ajan: AjanBilgisi, ajan_konum: Coord) -> None:
    print("\nIzgara durumu (A=ajan, G=güvenli, ?=şüpheli, C=kesin çukur, .=bilinmiyor):")
    for y in range(N - 1, -1, -1):
        hucreler = []
        for x in range(N):
            c = (x, y)
            if c == ajan_konum:
                isaret = "A"
            elif c in ajan.cukur_var:
                isaret = "C"
            elif c in ajan.guvenli:
                isaret = "G"
            elif c in ajan.olasi_cukur:
                isaret = "?"
            else:
                isaret = "."
            hucreler.append(f"{isaret}({x},{y})")
        print("  " + "  ".join(hucreler))


def demo() -> None:
    print("=== 2×2 tehlikeli ızgara mantık demosu ===")
    print("Gizli dünya: çukur (1,1)'de. Ajan (0,0)'dan başlar.\n")

    dunya = IzgaraDunyasi(cukurlar={(1, 1)}, yaratik=None)
    ajan = AjanBilgisi()
    konum: Coord = (0, 0)

    # Adım 1: (0,0)
    algi0 = dunya.algi(konum)
    print(f"Konum {konum} algı: esinti={algi0['esinti']}, koku={algi0['koku']}")
    ajan.tell_algi(konum, algi0)
    tahta_yazdir(ajan, konum)
    print(f"Güvenli bilinenler: {sorted(ajan.guvenli)}")
    print(f"Olası çukur: {sorted(ajan.olasi_cukur)}")
    print(f"Kesin çukur: {sorted(ajan.cukur_var)}")

    # Esinti yoksa (0,1) ve (1,0) güvenli olur — adım at
    adaylar = [c for c in sorted(ajan.guvenli) if c not in ajan.ziyaret]
    if not adaylar:
        print("\nGüvenli yeni kare yok; duruluyor.")
        return

    sonraki = adaylar[0]
    print(f"\n— Güvenli kareye git: {sonraki} —")
    konum = sonraki
    algi1 = dunya.algi(konum)
    print(f"Konum {konum} algı: esinti={algi1['esinti']}, koku={algi1['koku']}")
    ajan.tell_algi(konum, algi1)
    tahta_yazdir(ajan, konum)
    print(f"Güvenli: {sorted(ajan.guvenli)}")
    print(f"Olası çukur: {sorted(ajan.olasi_cukur)}")
    print(f"Kesin çukur: {sorted(ajan.cukur_var)}")

    # Üçüncü güvenli varsa git
    adaylar = [c for c in sorted(ajan.guvenli) if c not in ajan.ziyaret]
    if adaylar:
        sonraki = adaylar[0]
        print(f"\n— Güvenli kareye git: {sonraki} —")
        konum = sonraki
        algi2 = dunya.algi(konum)
        print(f"Konum {konum} algı: esinti={algi2['esinti']}, koku={algi2['koku']}")
        ajan.tell_algi(konum, algi2)
        tahta_yazdir(ajan, konum)
        print(f"Güvenli: {sorted(ajan.guvenli)}")
        print(f"Olası çukur: {sorted(ajan.olasi_cukur)}")
        print(f"Kesin çukur: {sorted(ajan.cukur_var)}")

    print("\nÖzet: Algı + 'esinti yok ⇒ komşular güvenli' + tek-aday elimasyonu")
    print("ile ajan çukura girmeden bilgiyi güncelledi.")


if __name__ == "__main__":
    demo()
