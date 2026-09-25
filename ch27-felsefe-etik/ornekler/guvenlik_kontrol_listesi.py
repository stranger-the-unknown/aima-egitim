#!/usr/bin/env python3
"""AI proje güvenlik / etik kontrol listesi şablonu yazdırır.

Doldurulası maddeler; vaaz yok. Markdown veya düz metin.
Özgün eğitim. Kitap metni yok.
https://aima.cs.berkeley.edu/ · https://github.com/aimacode
"""
from __future__ import annotations

import argparse
from datetime import date
from typing import List, Tuple

# (bölüm, maddeler)
BOLUMLER: List[Tuple[str, List[str]]] = [
    (
        "1. Amaç ve bağlam",
        [
            "Sistemin birincil amacı tek cümlede yazıldı mı?",
            "Kullanılmayacağı bağlamlar (out-of-scope) listelendi mi?",
            "Etkilenen paydaşlar (kullanıcı, üçüncü kişiler, operatör) sayıldı mı?",
        ],
    ),
    (
        "2. Veri ve gizlilik",
        [
            "Eğitim / çıkarım verisi kaynağı ve yasal dayanak belgelendi mi?",
            "Kişisel veri varsa anonimleştirme / minimizasyon planı var mı?",
            "Saklama süresi ve silme politikası tanımlı mı?",
            "Yeniden kimlikleme riski değerlendirildi mi?",
        ],
    ),
    (
        "3. Adillik ve temsil",
        [
            "Kritik demografik / kullanım grupları için hata oranları ayrı ölçülebiliyor mu?",
            "Tarihsel yanlılık taşıyan etiketler / proxy özellikler gözden geçirildi mi?",
            "“Eşit muamele” vs “eşit sonuç” hedefi bilinçli seçildi mi?",
        ],
    ),
    (
        "4. Güvenlik ve kötüye kullanım",
        [
            "Makul kötüye kullanım senaryoları (en az 3) yazıldı mı?",
            "Zarar eşiği yüksek çıktılarda insan onayı / rate limit var mı?",
            "Acil durdurma / model geri çekme prosedürü biliniyor mu?",
            "Bağımlı servislerin (API, araç çağrısı) yetki sınırı var mı?",
        ],
    ),
    (
        "5. Açıklama ve hesap verebilirlik",
        [
            "Kullanıcıya sistemin sınırları anlaşılır dille anlatılıyor mu?",
            "Karar / öneri loglanıyor mu (kim, ne zaman, hangi girdi özeti)?",
            "İtiraz / düzeltme kanalı tanımlı mı?",
            "Sorumlu rol (ürün, ML, hukuk, güvenlik) atanmış mı?",
        ],
    ),
    (
        "6. İzleme ve bakım",
        [
            "Canlıda sapma (data drift) ve kalite metrikleri izleniyor mu?",
            "Olay müdahale runbook’u var mı?",
            "Yeniden eğitim / sürümleme etiketi kullanılıyor mu?",
        ],
    ),
]


def yazdir(markdown: bool, proje: str) -> None:
    baslik = f"AI güvenlik / etik kontrol listesi — {proje}"
    if markdown:
        print(f"# {baslik}\n")
        print(f"_Tarih: {date.today().isoformat()} — şablon; projenize göre uyarlayın._\n")
    else:
        print(baslik)
        print(f"Tarih: {date.today().isoformat()}")
        print("=" * 60)

    for bolum, maddeler in BOLUMLER:
        if markdown:
            print(f"## {bolum}\n")
            for m in maddeler:
                print(f"- [ ] {m}")
            print()
        else:
            print(f"\n{bolum}")
            print("-" * len(bolum))
            for m in maddeler:
                print(f"  [ ] {m}")

    if markdown:
        print("---\n")
        print("Not: Bu liste vaaz değil; ekip tartışması ve dokümantasyon için çerçevedir.")
    else:
        print("\nNot: Bu liste vaaz değil; ekip tartışması ve dokümantasyon için çerçevedir.")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--md", action="store_true", help="Markdown çıktı")
    p.add_argument("--proje", default="(proje adı)", help="Proje adı")
    args = p.parse_args()
    yazdir(args.md, args.proje)


if __name__ == "__main__":
    main()
