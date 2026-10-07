#!/usr/bin/env python3
"""Bütün bölümlerin `notlar.md` dosyalarındaki "## Terimler" tablolarından kök dizinde `SOZLUK.md` üretir.

Aynı Türkçe terim birden çok bölümde geçiyorsa tek satırda birleştirilir; bölüm numaraları listelenir ve
ilk geçtiği bölümün açıklaması kullanılır. Sıralama Türkçe alfabeye göredir.

Çalıştırma (kök dizinden):
    python scripts/sozluk_uret.py
"""
from __future__ import annotations

import re
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
ALFABE = "aâbcçdefgğhıiîjklmnoöprsştuûüvwxyz"


def sirala_anahtari(terim: str) -> list[int]:
    s = terim.replace("İ", "i").replace("I", "ı").lower()
    return [-1 if c == " " else ALFABE.index(c) if c in ALFABE else 100 + ord(c) for c in s]


def terimleri_oku(notlar: Path) -> list[tuple[str, str, str]]:
    satirlar = notlar.read_text(encoding="utf-8").splitlines()
    try:
        bas = next(i for i, s in enumerate(satirlar) if s.strip() == "## Terimler")
    except StopIteration:
        return []
    sonuc = []
    for s in satirlar[bas + 1:]:
        if s.startswith("## "):
            break
        if not s.startswith("|") or set(s.replace("|", "").strip()) <= {"-", " "}:
            continue
        hucre = [h.strip() for h in re.split(r"(?<!\\)\|", s.strip().strip("|"))]
        if len(hucre) >= 3 and hucre[0] != "Türkçe":
            sonuc.append((hucre[0], hucre[1], hucre[2]))
    return sonuc


def main() -> None:
    sozluk: dict[str, dict] = {}
    for klasor in sorted(KOK.glob("ch[0-9][0-9]-*")):
        bolum = int(klasor.name[2:4])
        for tr, en, aciklama in terimleri_oku(klasor / "notlar.md"):
            k = tr.lower()
            if k not in sozluk:
                sozluk[k] = {"tr": tr, "en": en, "aciklama": aciklama, "bolumler": []}
            if bolum not in sozluk[k]["bolumler"]:
                sozluk[k]["bolumler"].append(bolum)
    satirlar = [
        "# Sözlük",
        "",
        "> Bu dosya `python scripts/sozluk_uret.py` ile bölümlerin `notlar.md` dosyalarındaki \"Terimler\" tablolarından",
        "> otomatik üretilir; elle düzenlemeyin, ilgili bölümün tablosunu düzeltip betiği yeniden çalıştırın.",
        "",
        f"{len(sozluk)} terim. Bölüm sütunu terimin geçtiği bölümleri gösterir; açıklama ilk geçtiği bölümden alınır.",
        "",
        "| Türkçe | İngilizce | Kısa açıklama | Bölüm |",
        "|---|---|---|---|",
    ]
    for k in sorted(sozluk, key=sirala_anahtari):
        t = sozluk[k]
        satirlar.append(f"| {t['tr']} | {t['en']} | {t['aciklama']} | {', '.join(map(str, t['bolumler']))} |")
    (KOK / "SOZLUK.md").write_text("\n".join(satirlar) + "\n", encoding="utf-8")
    print(f"SOZLUK.md yazıldı: {len(sozluk)} terim")


if __name__ == "__main__":
    main()
