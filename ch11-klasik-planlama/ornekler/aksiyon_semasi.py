#!/usr/bin/env python3
"""STRIPS-benzeri aksiyon şemalarını tanımla ve güzel yazdır.

Özgün eğitim örneği (bloklar dünyası şemaları). Kitap metni değildir.

Resmi referans: https://aima.cs.berkeley.edu/ · https://github.com/aimacode
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Sequence, Tuple


@dataclass(frozen=True)
class AksiyonSemasi:
    ad: str
    parametreler: Tuple[str, ...]
    onkosul: Tuple[str, ...]
    sil: Tuple[str, ...]
    ekle: Tuple[str, ...]
    aciklama: str = ""

    def yazdir(self) -> None:
        params = ", ".join(self.parametreler)
        print(f"┌─ Aksiyon: {self.ad}({params})")
        if self.aciklama:
            print(f"│  Açıklama : {self.aciklama}")
        print(f"│  Önkoşul  : {', '.join(self.onkosul) if self.onkosul else '(yok)'}")
        print(f"│  Sil      : {', '.join(self.sil) if self.sil else '(yok)'}")
        print(f"│  Ekle     : {', '.join(self.ekle) if self.ekle else '(yok)'}")
        print("└" + "─" * 40)


def bloklar_semalari() -> List[AksiyonSemasi]:
    return [
        AksiyonSemasi(
            ad="Kaldir",
            parametreler=("X", "Y"),
            onkosul=("On(X, Y)", "Clear(X)", "ElBos"),
            sil=("On(X, Y)", "ElBos"),
            ekle=("Tutuyor(X)", "Clear(Y)"),
            aciklama="X bloğunu Y üzerinden (veya masadan) kaldır; ele al.",
        ),
        AksiyonSemasi(
            ad="Koy",
            parametreler=("X", "Y"),
            onkosul=("Tutuyor(X)", "Clear(Y)"),
            sil=("Tutuyor(X)", "Clear(Y)"),
            ekle=("On(X, Y)", "ElBos", "Clear(X)"),
            aciklama="Eldeki X'i açık Y'nin üstüne koy.",
        ),
        AksiyonSemasi(
            ad="MasayaKoy",
            parametreler=("X",),
            onkosul=("Tutuyor(X)",),
            sil=("Tutuyor(X)",),
            ekle=("On(X, Masa)", "ElBos", "Clear(X)"),
            aciklama="Eldeki X'i masaya bırak.",
        ),
    ]


def kargo_semalari() -> List[AksiyonSemasi]:
    """İsteğe bağlı ikinci domain: mini kargo / havalimanı sezgisi."""
    return [
        AksiyonSemasi(
            ad="Yukle",
            parametreler=("c", "p", "a"),
            onkosul=("At(c, a)", "At(p, a)", "Kargo(c)", "Ucak(p)"),
            sil=("At(c, a)",),
            ekle=("In(c, p)",),
            aciklama="c kargosunu a havalimanındaki p uçağına yükle.",
        ),
        AksiyonSemasi(
            ad="Bosalt",
            parametreler=("c", "p", "a"),
            onkosul=("In(c, p)", "At(p, a)"),
            sil=("In(c, p)",),
            ekle=("At(c, a)",),
            aciklama="c kargosunu p uçağından a havalimanına boşalt.",
        ),
        AksiyonSemasi(
            ad="Uc",
            parametreler=("p", "from", "to"),
            onkosul=("At(p, from)", "Ucak(p)"),
            sil=("At(p, from)",),
            ekle=("At(p, to)",),
            aciklama="p uçağını from → to uçur.",
        ),
    ]


def demo() -> None:
    print("=== Bloklar dünyası — aksiyon şemaları ===\n")
    for s in bloklar_semalari():
        s.yazdir()
        print()

    print("=== Mini kargo / havalimanı — aksiyon şemaları ===\n")
    for s in kargo_semalari():
        s.yazdir()
        print()

    print("Not: Şema parametreli kalıptır; planlayıcı somut sabitlerle örnekler.")


if __name__ == "__main__":
    demo()
