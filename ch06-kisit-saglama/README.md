# Bölüm 6 — Kısıt sağlama problemleri (CSP)

AIMA 4. baskı, Bölüm 6 ile uyumlu **özgün Türkçe** öğrenme paketi.

**Durum:** 🟢 hazır

## Öğrenme hedefleri

1. Bir sorunu **değişkenler**, **domainler** ve **kısıtlar** olarak modellemek.
2. **Geri dönüşlü arama (backtracking)** ile çözüm aramak.
3. **İleriye kontrol (forward checking)** ve **AC-3** sezgisini açıklamak.
4. **MRV**, **derece** ve **LCV** sezgiselleriyle arama sırasını iyileştirmek.

## Bu klasörde ne var?

| Dosya / klasör | İçerik |
|----------------|--------|
| `notlar.md` | Özgün Türkçe öğretim notları (CSP) |
| `ornekler/harita_boyama_csp.py` | Türkiye bölgeleri harita boyama + backtracking / MRV |
| `ornekler/n_vezir_csp.py` | N-vezir probleminin CSP olarak kısa çözümü |
| `alistirmalar.md` | 5 özgün alıştırma |
| `cozumler/` | İlk 2 alıştırmanın çözümleri |
| `quiz.md` | 5 soru + cevaplar |

## Nasıl çalış?

1. AIMA Bölüm 6’yı oku (yasal nüsha).
2. `notlar.md` ile pekiştir.
3. Örnekleri çalıştır:
   ```bash
   python ornekler/harita_boyama_csp.py
   python ornekler/harita_boyama_csp.py --mrv
   python ornekler/n_vezir_csp.py --n 8
   ```
4. Alıştırmalar → `cozumler/` → `quiz.md`.

## Kaynaklar

- [aima.cs.berkeley.edu](https://aima.cs.berkeley.edu/)
- [github.com/aimacode](https://github.com/aimacode)
