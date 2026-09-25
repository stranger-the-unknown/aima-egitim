# Bölüm 11 — Klasik planlama

AIMA 4. baskı, Klasik Planlama temalarıyla uyumlu **özgün Türkçe** öğrenme paketi.

**Durum:** 🟢 hazır

## Öğrenme hedefleri

1. **STRIPS-benzeri** aksiyonları anlatmak: önkoşul, add, delete.
2. Durumu liteller kümesi olarak görmek; planı aksiyon dizisi olarak tanımlamak.
3. **İleri (forward)** ve **geri (backward)** durum-uzayı arama sezgisini ayırt etmek.
4. Planlama grafiği / sezgisel maliyet fikrini yüksek seviyede özetlemek (tam GraphPlan değil).
5. Küçük bir bloklar dünyasında BFS ile plan üretmek.

## Bu klasörde ne var?

| Dosya / klasör | İçerik |
|----------------|--------|
| `notlar.md` | Özgün Türkçe öğretim notları |
| `ornekler/aksiyon_semasi.py` | Aksiyon şemalarını güzel yazdırma |
| `ornekler/strips_bloklar.py` | Bloklar dünyası STRIPS + BFS planlayıcı |
| `alistirmalar.md` | 5 özgün alıştırma |
| `cozumler/` | A1 ve A2 çözümleri |
| `quiz.md` | 5 soru + cevaplar |

## Nasıl çalış?

1. AIMA’da klasik planlama bölümünü oku (yasal nüsha).
2. `notlar.md` ile pekiştir.
3. Örnekleri çalıştır:
   ```bash
   python ornekler/aksiyon_semasi.py
   python ornekler/strips_bloklar.py
   ```
4. Alıştırmalar → `cozumler/` → `quiz.md`.

## Kaynaklar

- [aima.cs.berkeley.edu](https://aima.cs.berkeley.edu/)
- [github.com/aimacode](https://github.com/aimacode)
