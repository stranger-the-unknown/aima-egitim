# Bölüm 1 — Tek Sayfalık Çalışma Özeti

> Hızlı tekrar için. Ayrıntı: `notlar.md`.

## Rasyonel ajan

Ortamdan **algı** alır, **eylem** seçer; başarıyı dışarıdan verilen **performans ölçütüne** göre maksimize etmeye çalışır. “İnsan gibi” olmak şart değildir; **doğru işi doğru zamanda** yapmak esasdır.

| Kavram | Anlam |
|--------|--------|
| Ajan fonksiyonu | Algı geçmişi → eylem (ideal eşleme) |
| Ajan programı | Bu eşlemeyi bilgisayarda koşan kod |

## PEAS şablonu

| | Soru |
|--|------|
| **P**erformance | Neyi başarı sayıyoruz? |
| **E**nvironment | Nerede çalışıyor? |
| **A**ctuators | Ne yapabilir? |
| **S**ensors | Ne görebilir / ölçebilir? |

Yeni görev = önce PEAS doldur.

## Ortam eksenleri (kısa)

| Eksen | Uçlar |
|-------|--------|
| Gözlem | Tam ↔ kısmi |
| Sonuç | Deterministik ↔ stokastik |
| Karar bağı | Epizodik ↔ ardışık |
| Zaman | Statik ↔ dinamik |
| Uzay | Ayrık ↔ sürekli |
| Ajan | Tek ↔ çok |
| Model | Bilinen ↔ bilinmeyen |

Gerçek problemler çoğu eksende **karışıktır**.

## Ajan türleri (basitten zengine)

```
Basit refleks → Modele dayalı → Hedefe dayalı → Faydaya dayalı → Öğrenen
```

| Tür | Ne kullanır? | Ne zaman yeterli? |
|-----|--------------|-------------------|
| Basit refleks | Anlık algı + kurallar | Tam gözlem, basit eşleme |
| Modele dayalı | İç durum / bellek | Kısmi gözlem, geçmiş gerekir |
| Hedefe dayalı | Hedef + arama/plan | “Nereye?” bilinir |
| Faydaya dayalı | Ödünleşim / skor | Birden fazla hedef, maliyet |
| Öğrenen | Deneyimle güncelleme | Ortam değişir veya kurallar yetmez |

Öğrenen ajan parçaları: **performans öğesi**, **eleştirmen**, **öğrenme öğesi**, **problem üreteci**.

## Çalışma kontrol listesi

- [ ] PEAS yazabildim
- [ ] Ortamı 2–3 eksende sınıflandırdım
- [ ] Uygun ajan türünü seçtim
- [ ] `vacuum_agent.py` çalıştırdım

Kaynak: [aima.cs.berkeley.edu](https://aima.cs.berkeley.edu/) · [aimacode](https://github.com/aimacode)
