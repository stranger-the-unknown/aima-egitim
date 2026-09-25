# Bölüm 19 — Örneklerden öğrenme

AIMA 4. baskı, Learning from Examples temalarıyla uyumlu **özgün Türkçe** öğrenme paketi.
Denetimli öğrenme, hipotez uzayı, karar ağacı sezgisi, aşırı öğrenme / train-test, doğrusal sınıflandırma taslağı.

**Durum:** 🟢 hazır

## Öğrenme hedefleri

1. Denetimli öğrenmeyi (girdi → etiket) tanımlamak.
2. Hipotez uzayı ve genelleme fikrini açıklamak.
3. Karar ağacı bölme sezgisini (bilgi kazancı fikri) yorumlamak.
4. Aşırı öğrenme ve train/test ayrımını gerekçelendirmek.
5. Basit doğrusal sınıflandırıcı / perceptron güncellemesini demoda görmek.

## Bu klasörde ne var?

| Dosya / klasör | İçerik |
|----------------|--------|
| `notlar.md` | Özgün Türkçe öğretim notları |
| `ornekler/karar_agaci_mini.py` | Küçük kategorik veri + el yapımı / ID3 tarzı ağaç |
| `ornekler/lineer_siniflandirma.py` | Perceptron (sıfırdan) 2B sentetik veri |
| `alistirmalar.md` | 5 özgün alıştırma |
| `cozumler/` | A1 ve A2 çözümleri |
| `quiz.md` | 5 soru + cevaplar |

## Nasıl çalış?

1. AIMA’da örneklerden öğrenme bölümünü oku (yasal nüsha).
2. `notlar.md` ile pekiştir.
3. Örnekleri çalıştır:
   ```bash
   python ornekler/karar_agaci_mini.py
   python ornekler/lineer_siniflandirma.py
   ```
4. Alıştırmalar → `cozumler/` → `quiz.md`.

## Kaynaklar

- [aima.cs.berkeley.edu](https://aima.cs.berkeley.edu/)
- [github.com/aimacode](https://github.com/aimacode)
