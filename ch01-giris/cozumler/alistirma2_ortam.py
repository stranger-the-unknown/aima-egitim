#!/usr/bin/env python3
"""
Alıştırma 2 çözümü: üç senaryonun ortam özelliklerini yazdırır.
Öğrenci cevabıyla karşılaştırmak için örnek sınıflandırma.
"""

from __future__ import annotations


SENARYOLAR = [
    {
        "ad": "İki odalı süpürge dünyası",
        "ozellikler": {
            "Gözlemlenebilirlik": "Tam — ajan bulunduğu odanın durumunu net görür (bu modelde).",
            "Determinizm": "Deterministik — süpür → temiz; hareket → diğer oda.",
            "Epizodiklik": "Ardışık — önceki temizlik sonraki adımları etkiler.",
            "Dinamiklik": "Statik — ajan düşünürken başka bir şey odayı kirletmez.",
            "Süreklilik": "Ayrık — iki konum, iki durum, sonlu eylemler.",
            "Ajan sayısı": "Tek ajan.",
        },
    },
    {
        "ad": "Çevrimiçi satranç (insan rakip, süre sınırlı)",
        "ozellikler": {
            "Gözlemlenebilirlik": "Tam tahta — taşlar görünür; rakibin iç planı gizli.",
            "Determinizm": "Kurallar deterministik; rakip hamlesi stratejik belirsizlik yaratır.",
            "Epizodiklik": "Ardışık — her hamle sonraki durumu belirler.",
            "Dinamiklik": "Yarı dinamik — süre akar; düşünürken saat tükenir.",
            "Süreklilik": "Ayrık durum (taş konumları); zaman süreklidir.",
            "Ajan sayısı": "Çok ajan — siz + rakip.",
        },
    },
    {
        "ad": "Yoğun yağmurda otonom araç",
        "ozellikler": {
            "Gözlemlenebilirlik": "Kısmi — yağmur sensör gürültüsü, kör noktalar.",
            "Determinizm": "Stokastik — yol tutuşu, diğer sürücüler, kayma belirsiz.",
            "Epizodiklik": "Ardışık — uzun süreli trafik etkileşimi.",
            "Dinamiklik": "Dinamik — dünya siz planlarken değişir.",
            "Süreklilik": "Sürekli — hız, açı, konum sürekli değerler.",
            "Ajan sayısı": "Çok ajan — diğer araçlar, yayalar.",
        },
    },
]


def main() -> None:
    for s in SENARYOLAR:
        print("=" * 60)
        print(s["ad"])
        print("=" * 60)
        for k, v in s["ozellikler"].items():
            print(f"  {k}: {v}")
        print()


if __name__ == "__main__":
    main()
