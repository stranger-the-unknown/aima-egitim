# Bölüm 21 — Derin öğrenme

AIMA 4. baskı (US) *Deep Learning* temalarıyla uyumlu **özgün Türkçe** öğrenme paketi.
Çok katmanlı ağ, aktivasyon, kayıp, geriye yayılım sezgisi, aşırı öğrenme / düzenlileştirme — hafif ve eğitici.
Saf numpy ile minik MLP; torch gerekmez.

**Durum:** 🟢 hazır

## Öğrenme hedefleri

1. Çok katmanlı ileri beslemeli ağı katmanlar zinciri olarak açıklamak.
2. Sigmoid / ReLU / tanh farkını karşılaştırmak.
3. Kayıp + gradyan inişi fikrini ve geriye yayılım sezgisini özetlemek.
4. Aşırı öğrenme ve basit düzenlileştirme (ağırlık cezası, erken durdurma) fikirlerini bilmek.
5. XOR üzerinde sıfırdan minik MLP eğitip kaybın düştüğünü görmek.

## Bu klasörde ne var?

| Dosya / klasör | İçerik |
|----------------|--------|
| `notlar.md` | Özgün Türkçe öğretim notları |
| `ornekler/mlp_numpy_mini.py` | XOR üzerinde 2-2-1 MLP (saf numpy) |
| `ornekler/aktivasyon_goster.py` | sigmoid / ReLU / tanh tablo + isteğe bağlı grafik |
| `alistirmalar.md` | 5 özgün alıştırma |
| `cozumler/` | A1 ve A2 çözümleri |
| `quiz.md` | 5 soru + cevaplar |

## Nasıl çalış?

1. AIMA’da derin öğrenme bölümünü oku (yasal nüsha).
2. `notlar.md` ile pekiştir.
3. Örnekleri çalıştır:
   ```bash
   python ornekler/aktivasyon_goster.py
   python ornekler/mlp_numpy_mini.py
   ```
4. Alıştırmalar → `cozumler/` → `quiz.md`.

## Kaynaklar

- [aima.cs.berkeley.edu](https://aima.cs.berkeley.edu/)
- [github.com/aimacode](https://github.com/aimacode)
