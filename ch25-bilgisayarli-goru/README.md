# Bölüm 25 — Bilgisayarlı görü

AIMA 4. baskı (US) *Computer Vision* giriş temalarıyla uyumlu **özgün Türkçe** öğrenme paketi.
Görüntü = dizi; konvolüsyon sezgisi; kenar özellikleri; sınıflandırma / tespit / segmentasyon özeti.
Saf numpy ile minik 2D konvolüsyon ve histogram özellik demosu; ağır CNN framework şart değil. Kitap metni yok.

**Durum:** 🟢 hazır

## Öğrenme hedefleri

1. Görüntüyü sayı dizisi (piksel ızgarası) olarak açıklamak.
2. 2D konvolüsyon / filtre sezgisini küçük bir örnekte uygulamak.
3. Kenar özelliklerinin (Sobel tarzı çekirdek) ne işe yaradığını özetlemek.
4. Histogram özelliği ile kaba benzerlik / sınıf ayrımını denemek.
5. Sınıflandırma, nesne tespiti ve segmentasyonu birbirinden ayırmak.

## Bu klasörde ne var?

| Dosya / klasör | İçerik |
|----------------|--------|
| `notlar.md` | Özgün Türkçe öğretim notları |
| `ornekler/konvolusyon_mini.py` | Küçük numpy görüntü + kenar çekirdeği |
| `ornekler/histogram_ozellik.py` | Gri/renk histogram + uzaklık / toy sınıf |
| `alistirmalar.md` | 5 özgün alıştırma |
| `cozumler/` | A1 ve A2 çözümleri |
| `quiz.md` | 5 soru + cevaplar |

## Nasıl çalış?

1. AIMA’da bilgisayarlı görü girişini oku (yasal nüsha).
2. `notlar.md` ile pekiştir.
3. Örnekleri çalıştır:
   ```bash
   python ornekler/konvolusyon_mini.py
   python ornekler/histogram_ozellik.py
   ```
4. Alıştırmalar → `cozumler/` → `quiz.md`.

## Kaynaklar

- [aima.cs.berkeley.edu](https://aima.cs.berkeley.edu/)
- [github.com/aimacode](https://github.com/aimacode)
