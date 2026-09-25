# Bölüm 26 — Robotik

AIMA 4. baskı (US) *Robotics* giriş temalarıyla uyumlu **özgün Türkçe** öğrenme paketi.
Algı–eylem döngüsü, konfigürasyon uzayı sezgisi, lokalizasyon/haritalama taslağı,
yol planlama vs kontrol, insan–robot etkileşimi (üst düzey).
Saf numpy ile ızgara lokalizasyonu ve potansiyel alan yolu; kitap metni yok.

**Durum:** 🟢 hazır

## Öğrenme hedefleri

1. Robotikte algı → durum tahmini → eylem döngüsünü açıklamak.
2. Konfigürasyon uzayı (C-space) fikrini sezgisel olarak anlatmak.
3. Lokalizasyon ve haritalama (SLAM taslağı) farkını özetlemek.
4. Yol planlama ile kontrolün rollerini ayırmak.
5. İnsan–robot etkileşiminde güvenlik ve iletişim ihtiyacını yüksek düzeyde belirtmek.

## Bu klasörde ne var?

| Dosya / klasör | İçerik |
|----------------|--------|
| `notlar.md` | Özgün Türkçe öğretim notları |
| `ornekler/grid_lokalizasyon.py` | Ayrık Bayes filtresi ile 1D/2D koridor lokalizasyonu |
| `ornekler/potansiyel_alan_path.py` | Çekim/itme potansiyel alanı ızgara yolu |
| `alistirmalar.md` | 5 özgün alıştırma |
| `cozumler/` | A1 ve A2 çözümleri |
| `quiz.md` | 5 soru + cevaplar |

## Nasıl çalış?

1. AIMA’da robotik girişini oku (yasal nüsha).
2. `notlar.md` ile pekiştir.
3. Örnekleri çalıştır:
   ```bash
   python ornekler/grid_lokalizasyon.py
   python ornekler/potansiyel_alan_path.py
   ```
4. Alıştırmalar → `cozumler/` → `quiz.md`.

## Kaynaklar

- [aima.cs.berkeley.edu](https://aima.cs.berkeley.edu/)
- [github.com/aimacode](https://github.com/aimacode)
