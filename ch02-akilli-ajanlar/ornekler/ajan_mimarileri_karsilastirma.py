#!/usr/bin/env python3
"""
Ajan mimarileri karşılaştırma tablosu — Bölüm 2.

Çalıştırma:
    python ajan_mimarileri_karsilastirma.py
"""

from __future__ import annotations

SATIRLAR = [
    {
        "tur": "Basit refleks",
        "girdi": "Anlık algı",
        "bellek": "Yok",
        "karar": "Kural tablosu",
        "ne_zaman": "Tam gözlem, basit eşleme",
        "ornek": "Termostat; kirliyse-süpür",
    },
    {
        "tur": "Modele dayalı",
        "girdi": "Algı + iç durum",
        "bellek": "Dünya modeli",
        "karar": "Kurallar (duruma göre)",
        "ne_zaman": "Kısmi gözlem, geçmiş gerekir",
        "ornek": "Bellekli süpürge",
    },
    {
        "tur": "Hedefe dayalı",
        "girdi": "Durum + hedef",
        "bellek": "Model (+ plan)",
        "karar": "Arama / planlama",
        "ne_zaman": "Hedef net, yol aranacak",
        "ornek": "Navigasyon, puzzle",
    },
    {
        "tur": "Faydaya dayalı",
        "girdi": "Durum + fayda fn",
        "bellek": "Model",
        "karar": "Beklenen fayda max",
        "ne_zaman": "Ödünleşim / belirsizlik",
        "ornek": "Rota: süre vs yakıt",
    },
    {
        "tur": "Öğrenen ajan",
        "girdi": "Deneyim + ölçüt",
        "bellek": "Güncellenen model/politika",
        "karar": "Öğrenilmiş politika",
        "ne_zaman": "Ortam değişir / model yok",
        "ornek": "RL robot, öneri sistemi",
    },
]

OGRENEN_PARCALAR = [
    ("Performans öğesi", "Asıl davranış — eylem üretir"),
    ("Eleştirmen", "Ölçüte göre geri bildirim verir"),
    ("Öğrenme öğesi", "Performans öğesini günceller"),
    ("Problem üreteci", "Keşif için yeni deneyimler önerir"),
]


def tablo_yazdir() -> None:
    basliklar = ("Tür", "Girdi", "Bellek", "Karar", "Ne zaman?", "Örnek")
    anahtarlar = ("tur", "girdi", "bellek", "karar", "ne_zaman", "ornek")
    genislikler = [16, 22, 24, 22, 28, 22]

    def satir(degerler: tuple[str, ...]) -> str:
        parcalar = []
        for d, g in zip(degerler, genislikler):
            parcalar.append(str(d)[:g].ljust(g))
        return " | ".join(parcalar)

    print("AJAN MİMARİLERİ KARŞILAŞTIRMASI")
    print("=" * (sum(genislikler) + 3 * (len(genislikler) - 1)))
    print(satir(basliklar))
    print("-+-".join("-" * g for g in genislikler))
    for row in SATIRLAR:
        print(satir(tuple(row[k] for k in anahtarlar)))

    print("\nÖĞRENEN AJAN — DÖRT PARÇA")
    print("-" * 50)
    for ad, aciklama in OGRENEN_PARCALAR:
        print(f"  • {ad:18s} → {aciklama}")

    print("\nSeçim ipucu:")
    print("  kısmi gözlem → modele dayalı+")
    print("  hedef var     → hedefe dayalı (+ arama, Blm 3)")
    print("  ödünleşim     → faydaya dayalı")
    print("  model yok     → öğrenen ajan")


def main() -> None:
    tablo_yazdir()


if __name__ == "__main__":
    main()
