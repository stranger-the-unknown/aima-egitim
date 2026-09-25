# Bölüm 13 — Olasılıksal akıl yürütme (Bayes ağları)

AIMA 4. baskı, Probabilistic Reasoning / Bayes nets temalarıyla uyumlu **özgün Türkçe** öğrenme paketi.

**Durum:** 🟢 hazır

## Öğrenme hedefleri

1. Bayes ağının yönlü asiklik grafik (DAG) yapısını okumak.
2. CPT (koşullu olasılık tablosu) ile yerel dağılımları yazmak.
3. Koşullu bağımsızlık sezgisini (ebeveynler verildiğinde) açıklamak.
4. Exact çıkarım fikrini **enumeration** ile küçük ağda uygulamak.
5. Örnekleme (prior / rejection / Gibbs) yaklaşımlarını yüksek seviyede ayırt etmek.

## Bu klasörde ne var?

| Dosya / klasör | İçerik |
|----------------|--------|
| `notlar.md` | Özgün Türkçe öğretim notları |
| `ornekler/bayes_agi_kucuk.py` | 4 düğümlü ağ + enumeration ile P(sorgu\|kanıt) |
| `ornekler/cpt_goster.py` | CPT’leri Türkçe başlıklarla yazdırma |
| `alistirmalar.md` | 5 özgün alıştırma |
| `cozumler/` | A1 ve A2 çözümleri |
| `quiz.md` | 5 soru + cevaplar |

## Nasıl çalış?

1. AIMA’da Bayes ağları / olasılıksal akıl yürütme bölümünü oku (yasal nüsha).
2. `notlar.md` ile pekiştir.
3. Örnekleri çalıştır:
   ```bash
   python ornekler/cpt_goster.py
   python ornekler/bayes_agi_kucuk.py
   ```
4. Alıştırmalar → `cozumler/` → `quiz.md`.

## Kaynaklar

- [aima.cs.berkeley.edu](https://aima.cs.berkeley.edu/)
- [github.com/aimacode](https://github.com/aimacode)
