# Bölüm 4 — Karmaşık ortamlarda arama

AIMA 4. baskı, Bölüm 4 ile uyumlu **özgün Türkçe** öğrenme paketi.

**Durum:** 🟢 hazır

## Öğrenme hedefleri

1. **Yerel arama**nın ne zaman uygun olduğunu bilmek: durum uzayı büyük, yol değil *durum kalitesi* önemli.
2. **Tepe tırmanma**, **simüle tavlama** ve **genetik algoritma** sezgilerini kendi sözlerinizle anlatmak.
3. **Yerel ışın araması** fikrini (birden fazla durum tutmak) açıklamak.
4. Belirsiz / kısmi gözlemde **inanç durumu** aramasının sezgisini kavramak.
5. **Çevrimiçi** arama ile **çevrimdışı** plan farkını ayırt etmek.

## Bu klasörde ne var?

| Dosya / klasör | İçerik |
|----------------|--------|
| `notlar.md` | Özgün Türkçe öğretim notları |
| `ornekler/tepe_tirmanma_n_queens.py` | 8-vezir tepe tırmanma + rastgele yeniden başlatma |
| `ornekler/simule_tavlama_demo.py` | Küçük TSP üzerinde simüle tavlama |
| `alistirmalar.md` | 5 özgün alıştırma |
| `cozumler/` | İlk 2 alıştırmanın çözümleri |
| `quiz.md` | 5 soru + cevaplar |

## Nasıl çalış?

1. AIMA Bölüm 4’ü oku (yasal nüsha).
2. `notlar.md` ile pekiştir.
3. Örnekleri çalıştır:
   ```bash
   python ornekler/tepe_tirmanma_n_queens.py
   python ornekler/tepe_tirmanma_n_queens.py --yeniden-baslat 20
   python ornekler/simule_tavlama_demo.py
   ```
4. Alıştırmalar → `cozumler/` → `quiz.md`.

## Kaynaklar

- [aima.cs.berkeley.edu](https://aima.cs.berkeley.edu/)
- [github.com/aimacode](https://github.com/aimacode)
