# Bölüm 3 — Çözüm arama yoluyla problem çözme

AIMA 4. baskı, Bölüm 3 ile uyumlu **özgün Türkçe** öğrenme paketi.

**Durum:** 🟢 hazır

## Öğrenme hedefleri

1. Bir problemi **durum, başlangıç, eylemler, geçiş, hedef testi, yol maliyeti** ile formüle etmek.
2. **Ağaç arama** ile **graf arama** farkını açıklamak (tekrar ziyaret).
3. Kör aramayı ayırt etmek: **BFS**, **DFS**, **UCS** (tekdüze maliyet).
4. Bilgilendirilmiş aramada **açgözlü (greedy)** ve **A\*** sezgisini anlatmak; kabul edilebilir sezgisel fikrini bilmek.
5. Romanya haritası örneğinde algoritmaları çalıştırıp yol, maliyet ve genişletilen düğüm sayısını yorumlamak.

## Bu klasörde ne var?

| Dosya / klasör | İçerik |
|----------------|--------|
| `notlar.md` | Özgün Türkçe öğretim notları |
| `ornekler/romania_arama.py` | BFS, DFS, UCS, A* — klasik Romanya haritası |
| `alistirmalar.md` | 5 özgün alıştırma |
| `cozumler/` | İlk 2 alıştırmanın çözümleri |
| `quiz.md` | 5 soru + cevaplar |

## Nasıl çalış?

1. AIMA Bölüm 3’ü oku (yasal nüsha).
2. `notlar.md` ile pekiştir.
3. Örneği çalıştır:
   ```bash
   python ornekler/romania_arama.py
   python ornekler/romania_arama.py --baslangic Arad --hedef Bucharest
   ```
4. Alıştırmalar → `cozumler/` → `quiz.md`.

## Kaynaklar

- [aima.cs.berkeley.edu](https://aima.cs.berkeley.edu/)
- [github.com/aimacode](https://github.com/aimacode)
