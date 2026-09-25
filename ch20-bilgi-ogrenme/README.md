# Bölüm 20 — Olasılıksal modellerle öğrenme

AIMA 4. baskı (US) *Learning Probabilistic Models* temalarıyla uyumlu **özgün Türkçe** öğrenme paketi.
Tam veride parametre öğrenme (MLE / MAP sezgisi), Bayesyen öğrenmeye kısa bakış, eksik veri / EM yüksek seviye.

> Klasör adı müfredatta `ch20-bilgi-ogrenme/`; içerik US baskı Ch.20 (olasılıksal model öğrenme) ile hizalıdır.

**Durum:** 🟢 hazır

## Öğrenme hedefleri

1. Tam gözlemli veride parametre öğrenmeyi tanımlamak.
2. MLE ile MAP arasındaki farkı sezgisel olarak açıklamak.
3. Bayesyen öğrenmenin “sonradan dağılım” fikrini özetlemek.
4. Eksik veri / gizli değişken durumunda EM’in E ve M adımlarını yüksek seviyede anlatmak.
5. Bernoulli / kategorik MLE ve minik EM demosunu kodda görmek.

## Bu klasörde ne var?

| Dosya / klasör | İçerik |
|----------------|--------|
| `notlar.md` | Özgün Türkçe öğretim notları |
| `ornekler/mle_beta_Bernoulli.py` | Bernoulli (ve Beta-önsel sezgisi) MLE |
| `ornekler/em_karisim_mini.py` | İki zar / iki madeni para EM klasik demosu |
| `alistirmalar.md` | 5 özgün alıştırma |
| `cozumler/` | A1 ve A2 çözümleri |
| `quiz.md` | 5 soru + cevaplar |

## Nasıl çalış?

1. AIMA’da olasılıksal modellerle öğrenme bölümünü oku (yasal nüsha).
2. `notlar.md` ile pekiştir.
3. Örnekleri çalıştır:
   ```bash
   python ornekler/mle_beta_Bernoulli.py
   python ornekler/em_karisim_mini.py
   ```
4. Alıştırmalar → `cozumler/` → `quiz.md`.

## Kaynaklar

- [aima.cs.berkeley.edu](https://aima.cs.berkeley.edu/)
- [github.com/aimacode](https://github.com/aimacode)
