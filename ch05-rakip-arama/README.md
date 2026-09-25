# Bölüm 5 — Rakip arama ve oyunlar

AIMA 4. baskı, Bölüm 5 ile uyumlu **özgün Türkçe** öğrenme paketi.

**Durum:** 🟢 hazır

## Öğrenme hedefleri

1. Deterministik, sıfır toplamlı, mükemmel bilgili oyunlarda **minimax** fikrini uygulamak.
2. **Alpha-beta budama** ile aynı sonucu daha az düğümle bulmayı anlamak.
3. Derinlik sınırı + **değerlendirme fonksiyonu** ile “kusurlu karar”ı açıklamak.
4. Tic-tac-toe örneğinde ajan–ajan veya pozisyondan en iyi hamleyi hesaplamak.

## Bu klasörde ne var?

| Dosya / klasör | İçerik |
|----------------|--------|
| `notlar.md` | Özgün Türkçe öğretim notları |
| `ornekler/minimax_tictactoe.py` | Minimax (+ isteğe bağlı alpha-beta) XOX |
| `alistirmalar.md` | 5 özgün alıştırma |
| `cozumler/` | İlk 2 alıştırmanın çözümleri |
| `quiz.md` | 5 soru + cevaplar |

## Nasıl çalış?

1. AIMA Bölüm 5’i oku (yasal nüsha).
2. `notlar.md` ile pekiştir.
3. Örneği çalıştır:
   ```bash
   python ornekler/minimax_tictactoe.py --mod ajan-ajan
   python ornekler/minimax_tictactoe.py --mod en-iyi --tahta "X.O.X.O.."
   python ornekler/minimax_tictactoe.py --mod ajan-ajan --alpha-beta
   ```
4. Alıştırmalar → `cozumler/` → `quiz.md`.

## Kaynaklar

- [aima.cs.berkeley.edu](https://aima.cs.berkeley.edu/)
- [github.com/aimacode](https://github.com/aimacode)
