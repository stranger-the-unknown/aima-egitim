# Bölüm 24 — Derin öğrenme ile doğal dil

AIMA 4. baskı (US) *Deep Learning for Natural Language Processing* temalarıyla uyumlu **özgün Türkçe** öğrenme paketi.
Kelime gömüleri, dizi modelleri (RNN/LSTM yüksek seviye), dikkat / transformer iskeleti, aktarım öğrenmesi fikri.
Saf numpy ile kosinüs benzerliği ve minik dikkat skoru demosu; torch/tensorflow gerekmez. Kitap metni yok.

**Durum:** 🟢 hazır

## Öğrenme hedefleri

1. Kelime gömüsü (embedding) sezgisini ve kosinüs benzerliğini açıklamak.
2. RNN / LSTM’i yüksek seviyede (sıra, bellek, gradyan sorunu) özetlemek.
3. Dikkat (attention) skorunun softmax(QKᵀ) fikrini sayısal olarak izlemek.
4. Transformer iskeletini (self-attention + feed-forward) kabaca çizmek.
5. Aktarım öğrenmesi (önceden eğitilmiş model → göreve uyarlama) fikrini anlatmak.

## Bu klasörde ne var?

| Dosya / klasör | İçerik |
|----------------|--------|
| `notlar.md` | Özgün Türkçe öğretim notları |
| `ornekler/embedding_benzerlik.py` | Elle / toy gömü + Türkçe sözcük kosinüs demosu |
| `ornekler/dikkat_skoru.py` | Minik Q,K → softmax(QKᵀ) dikkat skorları |
| `alistirmalar.md` | 5 özgün alıştırma |
| `cozumler/` | A1 ve A2 çözümleri |
| `quiz.md` | 5 soru + cevaplar |

## Nasıl çalış?

1. AIMA’da derin NLP / gömü / dikkat girişini oku (yasal nüsha).
2. `notlar.md` ile pekiştir.
3. Örnekleri çalıştır:
   ```bash
   python ornekler/embedding_benzerlik.py
   python ornekler/dikkat_skoru.py
   ```
4. Alıştırmalar → `cozumler/` → `quiz.md`.

## Kaynaklar

- [aima.cs.berkeley.edu](https://aima.cs.berkeley.edu/)
- [github.com/aimacode](https://github.com/aimacode)
