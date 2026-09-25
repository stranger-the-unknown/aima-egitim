#!/usr/bin/env python3
"""Türkçe doğal dil cümleleri ↔ FOL dizi gösterimi (öğrenme yardımcısı).

Tam bir NLP çevirmeni değildir. El ile tanımlı birkaç örnek çiftiyle
niceleyici / yüklem okuma pratiği yaptırır.

Resmi referans: https://aima.cs.berkeley.edu/ · https://github.com/aimacode
"""
from __future__ import annotations

from typing import List, Tuple

# (turkce, fol_dizisi, kisa_aciklama)
CIFTILER: List[Tuple[str, str, str]] = [
    (
        "Leyla, Deniz'in ebeveynidir.",
        "Ebeveyn(Leyla, Deniz)",
        "İkili yüklem; sabitler Leyla ve Deniz.",
    ),
    (
        "Her öğrenci çalışkandır.",
        "∀x (Ogrenci(x) ⇒ Caliskan(x))",
        "Evrensel niceleyici + implikasyon (yalnız öğrenciler için iddia).",
    ),
    (
        "En az bir ders boştur.",
        "∃x (Ders(x) ∧ Bos(x))",
        "Varoluşsal niceleyici; ∧ ile iki özelliği birleştir.",
    ),
    (
        "Her kedi bir hayvanı sever.",
        "∀x (Kedi(x) ⇒ ∃y (Hayvan(y) ∧ Sever(x, y)))",
        "∀ dışta, ∃ içte: her kedi için (belki farklı) bir hayvan.",
    ),
    (
        "Bir hayvan vardır ki her kedi onu sever.",
        "∃y (Hayvan(y) ∧ ∀x (Kedi(x) ⇒ Sever(x, y)))",
        "∃ dışta, ∀ içte — önceki cümleden FARKLI anlam.",
    ),
    (
        "Deniz'in annesi Ankaralıdır.",
        "Ankarali(anne(Deniz))",
        "Fonksiyon terimi anne(Deniz) + birli yüklem.",
    ),
]


def turkceden_fol(cumle: str) -> None:
    print(f"  TR : {cumle}")
    for tr, fol, aciklama in CIFTILER:
        if tr == cumle:
            print(f"  FOL: {fol}")
            print(f"  Not: {aciklama}")
            return
    print("  FOL: (bu demoda eşleşme yok — sözlüğe ekleyin)")


def foldan_turkce(fol: str) -> None:
    print(f"  FOL: {fol}")
    for tr, f, aciklama in CIFTILER:
        if f == fol:
            print(f"  TR : {tr}")
            print(f"  Not: {aciklama}")
            return
    print("  TR : (bu demoda eşleşme yok)")


def demo() -> None:
    print("=== Türkçe ↔ FOL çeviri demosu ===\n")
    print("--- Türkçe → FOL ---")
    for tr, _, _ in CIFTILER[:4]:
        turkceden_fol(tr)
        print()

    print("--- FOL → Türkçe (niceleyici sırası karşılaştırması) ---")
    foldan_turkce("∀x (Kedi(x) ⇒ ∃y (Hayvan(y) ∧ Sever(x, y)))")
    print()
    foldan_turkce("∃y (Hayvan(y) ∧ ∀x (Kedi(x) ⇒ Sever(x, y)))")
    print()

    print("Özet: Aynı yüklemler, farklı niceleyici sırası → farklı iddia.")
    print("Bu araç ezber sözlüktür; genel dilbilgisi çözücü değildir.")


if __name__ == "__main__":
    demo()
