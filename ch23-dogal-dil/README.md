# Bölüm 23 — Doğal dil işleme (giriş)

AIMA 4. baskı (US) *Natural Language Processing* giriş temalarıyla uyumlu **özgün Türkçe** öğrenme paketi.
Dil modelleri, n-gram, kelime torbası (BoW), gömme vektörlerine yüksek seviye bakış, tipik görevler.
Saf Python / numpy ile minik bigram LM ve BoW sınıfandırıcı; kitap metni yok.

**Durum:** 🟢 hazır

## Öğrenme hedefleri

1. Dil modelinin ne yaptığını (sözcük dizisi olasılığı / sonraki sözcük) açıklamak.
2. n-gram fikrini (özellikle bigram) ve sınırlarını özetlemek.
3. Kelime torbası (BoW) temsilini ve basit naif Bayes tarzı sınıflandırmayı uygulamak.
4. Kelime gömülerini (embeddings) yüksek seviyede tanımak (yoğun vektör, benzerlik).
5. NLP görevlerine (sınıflandırma, NER, çeviri, QA …) genel bakış verebilmek.

## Bu klasörde ne var?

| Dosya / klasör | İçerik |
|----------------|--------|
| `notlar.md` | Özgün Türkçe öğretim notları |
| `ornekler/n_gram_mini.py` | Minik Türkçe derlemden bigram LM; skor / örnek üretim |
| `ornekler/bow_siniflandirma.py` | Duygu / konu BoW + naif Bayes tarzı sayaç |
| `alistirmalar.md` | 5 özgün alıştırma |
| `cozumler/` | A1 ve A2 çözümleri |
| `quiz.md` | 5 soru + cevaplar |

## Nasıl çalış?

1. AIMA’da doğal dil / dil modelleri girişini oku (yasal nüsha).
2. `notlar.md` ile pekiştir.
3. Örnekleri çalıştır:
   ```bash
   python ornekler/n_gram_mini.py
   python ornekler/bow_siniflandirma.py
   ```
4. Alıştırmalar → `cozumler/` → `quiz.md`.

## Kaynaklar

- [aima.cs.berkeley.edu](https://aima.cs.berkeley.edu/)
- [github.com/aimacode](https://github.com/aimacode)
