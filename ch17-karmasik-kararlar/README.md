# Bölüm 17 — Karmaşık kararlar alma (MDP)

AIMA 4. baskı, Making Complex Decisions temalarıyla uyumlu **özgün Türkçe** öğrenme paketi.
Sıralı kararlar, Markov karar süreci (MDP), Bellman denklemleri, değer yineleme ve politika yineleme sezgisi.

**Durum:** 🟢 hazır

## Öğrenme hedefleri

1. Tek adımlı MEU ile sıralı karar farkını açıklamak.
2. MDP beşlisini (S, A, T, R, γ) tanımlamak.
3. Bellman denkleminin “en iyi devam” fikrini yorumlamak.
4. Değer yinelemenin yardımcı tahminlerle güncelleme olarak çalıştığını göstermek.
5. Sabit politikayı değerlendirmek / bir politika iyileştirme adımını demoda görmek.

## Bu klasörde ne var?

| Dosya / klasör | İçerik |
|----------------|--------|
| `notlar.md` | Özgün Türkçe öğretim notları |
| `ornekler/deger_yineleme.py` | Küçük gridworld değer yineleme + açgözlü politika |
| `ornekler/politika_degerlendirme.py` | Sabit politika değerlendirme / bir PI adımı |
| `alistirmalar.md` | 5 özgün alıştırma |
| `cozumler/` | A1 ve A2 çözümleri |
| `quiz.md` | 5 soru + cevaplar |

## Nasıl çalış?

1. AIMA’da karmaşık kararlar / MDP bölümünü oku (yasal nüsha).
2. `notlar.md` ile pekiştir.
3. Örnekleri çalıştır:
   ```bash
   python ornekler/deger_yineleme.py
   python ornekler/politika_degerlendirme.py
   ```
4. Alıştırmalar → `cozumler/` → `quiz.md`.

## Kaynaklar

- [aima.cs.berkeley.edu](https://aima.cs.berkeley.edu/)
- [github.com/aimacode](https://github.com/aimacode)
