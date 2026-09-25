# Bölüm 18 — Çok ajanlı karar verme

AIMA 4. baskı, Multiagent Decision Making temalarıyla uyumlu **özgün Türkçe** öğrenme paketi.
Oyun teorisi temelleri: normal form, baskın strateji, Nash dengesi sezgisi; işbirlikçi / işbirlikçi olmayan oyunlar; oy / sosyal seçim üst düzey bakış.

**Durum:** 🟢 hazır

## Öğrenme hedefleri

1. Normal form oyunu (oyuncular, stratejiler, ödeme matrisi) tanımlamak.
2. Baskın strateji ve en iyi yanıt fikrini açıklamak.
3. Saf Nash dengesini sezgisel olarak tanımak (Mahkûm İkilemi, koordinasyon / tavuk).
4. İşbirlikçi vs işbirlikçi olmayan ayrımını özetlemek.
5. Oy / sosyal seçim problemlerini yüksek düzeyde hatırlamak (Arrow benzeri sezgi yok; yalnızca fikir).

## Bu klasörde ne var?

| Dosya / klasör | İçerik |
|----------------|--------|
| `notlar.md` | Özgün Türkçe öğretim notları |
| `ornekler/mahkum_ikilemi.py` | Mahkûm ikilemi ödemeleri + en iyi yanıt / Nash |
| `ornekler/nash_2x2.py` | Koordinasyon (Stag Hunt) 2×2 saf Nash arama |
| `alistirmalar.md` | 5 özgün alıştırma |
| `cozumler/` | A1 ve A2 çözümleri |
| `quiz.md` | 5 soru + cevaplar |

## Nasıl çalış?

1. AIMA’da çok ajanlı karar / oyun teorisi bölümünü oku (yasal nüsha).
2. `notlar.md` ile pekiştir.
3. Örnekleri çalıştır:
   ```bash
   python ornekler/mahkum_ikilemi.py
   python ornekler/nash_2x2.py
   ```
4. Alıştırmalar → `cozumler/` → `quiz.md`.

## Kaynaklar

- [aima.cs.berkeley.edu](https://aima.cs.berkeley.edu/)
- [github.com/aimacode](https://github.com/aimacode)
