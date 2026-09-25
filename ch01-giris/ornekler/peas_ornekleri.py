#!/usr/bin/env python3
"""
Üç senaryo için PEAS tanımları — yapılandırılmış sözlük + güzel yazdırma.

Çalıştırma:
    python peas_ornekleri.py
"""

from __future__ import annotations

from typing import Any


PEAS_ORNEKLERI: list[dict[str, Any]] = [
    {
        "ad": "Otonom (kendi giden) araba",
        "P": [
            "Yolcuları güvenli ve yasal şekilde hedefe ulaştırmak",
            "Süre ve yakıt/enerji verimliliği",
            "Konfor (ani fren/viraj azaltma)",
            "Diğer trafiğe ve yayalara zarar vermemek",
        ],
        "E": [
            "Şehir / otoyol yolları",
            "Trafik, işaretler, hava koşulları",
            "Yayalar, bisikletler, diğer araçlar",
            "Geçici yol çalışmaları",
        ],
        "A": [
            "Direksiyon, gaz, fren",
            "Sinyal ve far kontrolü",
            "Korna / uyarı sesleri",
            "Yolcu arayüzü (ekran, sesli bilgi)",
        ],
        "S": [
            "Kameralar",
            "Radar / lidar (varsa)",
            "GPS ve harita verisi",
            "Hız, ivme, direksiyon açısı sensörleri",
            "Mikrofon (siren vb. için, opsiyonel)",
        ],
    },
    {
        "ad": "Tıbbi teşhis destek sistemi",
        "P": [
            "Doğru ön tanı / ayırıcı tanı listesi üretmek",
            "Kritik vakaları kaçırmamak (duyarlılık)",
            "Gereksiz tetkik önermemek (maliyet / hasta yükü)",
            "Hekim için açıklanabilir öneriler sunmak",
        ],
        "E": [
            "Klinik bilgi sistemi (hasta kayıtları)",
            "Laboratuvar ve görüntüleme sonuçları",
            "Hekim ve hasta etkileşimi",
            "Hastane protokol ve kılavuzları",
        ],
        "A": [
            "Öneri listesi yazdırma / arayüze basma",
            "Ek tetkik önerileri",
            "Risk skoru ve uyarı bayrakları",
            "Rapor özeti oluşturma",
        ],
        "S": [
            "Elektronik hasta kaydı alanları",
            "Laboratuvar değerleri",
            "Görüntüleme raporları / özellikler",
            "Hekim girişleri (şikayet, öykü)",
        ],
    },
    {
        "ad": "Satranç oynayan ajan",
        "P": [
            "Oyunu kazanmak (veya kaybetmemek)",
            "İyi pozisyonel değerlendirme",
            "Süre kontrolüne uymak (zaman aşımına düşmemek)",
        ],
        "E": [
            "8x8 satranç tahtası ve kurallar",
            "Rakip oyuncu (insan veya motor)",
            "Oyun saati / süre sınırları",
        ],
        "A": [
            "Yasal bir hamle seçmek ve tahtaya uygulamak",
            "(Turnuvada) hamleyi arayüze / saate işlemek",
        ],
        "S": [
            "Tahta durumu (taş konumları)",
            "Sıra kimde, rok/en passant hakları",
            "Kalan süre bilgisi",
        ],
    },
]


def yazdir_peas(ornek: dict[str, Any]) -> None:
    print("=" * 60)
    print(f"Senaryo: {ornek['ad']}")
    print("=" * 60)
    etiketler = {
        "P": "Performance (Başarı ölçütü)",
        "E": "Environment (Ortam)",
        "A": "Actuators (Eyleyiciler)",
        "S": "Sensors (Algılayıcılar)",
    }
    for anahtar in ("P", "E", "A", "S"):
        print(f"\n{anahtar} — {etiketler[anahtar]}:")
        for madde in ornek[anahtar]:
            print(f"  • {madde}")
    print()


def main() -> None:
    print("PEAS örnekleri (eğitsel, özgün tarifler)\n")
    for ornek in PEAS_ORNEKLERI:
        yazdir_peas(ornek)
    print(f"Toplam senaryo: {len(PEAS_ORNEKLERI)}")


if __name__ == "__main__":
    main()
