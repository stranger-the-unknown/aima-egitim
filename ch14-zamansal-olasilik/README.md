# Bölüm 14 — Zamansal olasılıksal modeller

AIMA 4. baskı, Probabilistic Reasoning over Time temalarıyla uyumlu **özgün Türkçe** öğrenme paketi.

**Durum:** 🟢 hazır

## Öğrenme hedefleri

1. Zamansal modeli (geçiş + duyucu) yüksek seviyede tanımlamak.
2. Filtreleme, kestirim (prediction) ve yumuşatma (smoothing) sezgilerini ayırt etmek.
3. HMM’nin gizli durum / gözlem ayrımını okumak.
4. Forward filtreleme ile sonsalı adım adım güncellemek.
5. Viterbi ile en olası durum dizisini bulmak (küçük örnek).
6. Kalman filtresinin “sürekli Gaussian” sezgisini (yüksek seviye) özetlemek.

## Bu klasörde ne var?

| Dosya / klasör | İçerik |
|----------------|--------|
| `notlar.md` | Özgün Türkçe öğretim notları |
| `ornekler/hmm_filtreleme.py` | Hava/şemsiye oyuncağı + forward filtreleme |
| `ornekler/viterbi_kucuk.py` | Aynı HMM üzerinde Viterbi en olası yol |
| `alistirmalar.md` | 5 özgün alıştırma |
| `cozumler/` | A1 ve A2 çözümleri |
| `quiz.md` | 5 soru + cevaplar |

## Nasıl çalış?

1. AIMA’da zamansal modeller / HMM bölümünü oku (yasal nüsha).
2. `notlar.md` ile pekiştir.
3. Örnekleri çalıştır:
   ```bash
   python ornekler/hmm_filtreleme.py
   python ornekler/viterbi_kucuk.py
   ```
4. Alıştırmalar → `cozumler/` → `quiz.md`.

## Kaynaklar

- [aima.cs.berkeley.edu](https://aima.cs.berkeley.edu/)
- [github.com/aimacode](https://github.com/aimacode)
