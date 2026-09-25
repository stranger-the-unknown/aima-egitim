# Bölüm 15 — Olasılıksal programlama (eğitim / hafif)

AIMA 4. baskı, Probabilistic Programming temalarıyla uyumlu **özgün Türkçe** öğrenme paketi.
Derin dil/framework dersi değil; **program = olasılıksal model** sezgisini vermek için hafif tutulmuştur.

**Durum:** 🟢 hazır

## Öğrenme hedefleri

1. “Programı model olarak yazmak” fikrini açıklamak.
2. Üretimsel (generative) süreci: önce örnekle, sonra koşullandır.
3. Bayes ağı ile bağlantıyı (çarpanlar / bağımlılık) yüksek seviyede kurmak.
4. İlişkisel / açık-evren sezgisini (nesne sayısı belli değil) tek paragrafta özetlemek.
5. Reddetme örneklemesi ile küçük bir sorguyu yaklaşık cevaplamak.

## Bu klasörde ne var?

| Dosya / klasör | İçerik |
|----------------|--------|
| `notlar.md` | Özgün Türkçe öğretim notları |
| `ornekler/basit_uretimsel_model.py` | Saf Python üretimsel model + naif koşullandırma |
| `ornekler/reddetme_ornekleme.py` | Reddetme örneklemesi demosu |
| `alistirmalar.md` | 5 özgün alıştırma |
| `cozumler/` | A1 ve A2 çözümleri |
| `quiz.md` | 5 soru + cevaplar |

## Nasıl çalış?

1. AIMA’da olasılıksal programlama bölümünü oku (yasal nüsha) — veya bu notlarla sezgi kur.
2. `notlar.md` ile pekiştir.
3. Örnekleri çalıştır:
   ```bash
   python ornekler/basit_uretimsel_model.py
   python ornekler/reddetme_ornekleme.py
   ```
4. Alıştırmalar → `cozumler/` → `quiz.md`.

## Kaynaklar

- [aima.cs.berkeley.edu](https://aima.cs.berkeley.edu/)
- [github.com/aimacode](https://github.com/aimacode)
