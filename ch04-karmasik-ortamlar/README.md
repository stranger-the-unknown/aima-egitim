# Bölüm 4 — Karmaşık ortamlarda arama

> AIMA 4. baskı, Bölüm 4 · *Search in Complex Environments*

## Öğrenme hedefleri

1. Yerel aramanın ne zaman uygun olduğunu açıklamak; tepe tırmanmanın tuzaklarını ve çarelerini sayısal olarak göstermek.
2. Benzetilmiş tavlamayı, ışın aramasını ve genetik algoritmayı karşılaştırmak.
3. Sürekli uzaylarda gradyan ve Newton adımını uygulamak.
4. Deterministik olmayan eylemler için AND-OR araması ile koşullu plan üretmek.
5. İnanç durumlarıyla algısız ve kısmi gözlemli problemleri çözmek.
6. Çevrimiçi aramayı ve LRTA*'ı açıklamak.

## Çalışma sırası

1. Kitapta Bölüm 4'ü oku.
2. [`notlar.md`](notlar.md)
3. Örnekleri çalıştır, sonuçları kitaptakilerle karşılaştır.
4. [`alistirmalar.md`](alistirmalar.md) → [`cozumler/`](cozumler/)
5. [`quiz.md`](quiz.md)

## Dosyalar

| Dosya | İçerik |
|---|---|
| `ornekler/tepe_tirmanma_n_queens.py` | En dik tırmanış, yana hamle, yeniden başlatma; `--deney` ile kitaptaki %14/%94 istatistiği |
| `ornekler/simule_tavlama_demo.py` | TSP'de benzetilmiş tavlama; kaba kuvvet optimumu ve tepe tırmanmayla karşılaştırma |
| `ornekler/genetik_8vezir.py` | Genetik algoritma; kitaptaki uygunluk değerleri ve çaprazlama örneği |
| `ornekler/havalimani_gradyan.py` | Sürekli uzay: 3 havalimanı, deneysel gradyan, gradyan inişi, Newton (k-ortalamalar) |
| `ornekler/and_or_supurge.py` | Kararsız süpürge, AND-OR araması, kitaptaki koşullu plan |
| `ornekler/inanc_durumu_supurge.py` | Algısız süpürge planı ve yerel algılı inanç güncelleme |
| `ornekler/lrta_yildiz.py` | LRTA*: kitaptaki tek boyutlu şekil + bilinmeyen labirent |
| `alistirmalar.md` | 10 alıştırma |
| `cozumler/` | Tüm çözümler (A6–A10 çalıştırılabilir kod) |
| `quiz.md` | 12 soru + cevaplar |

## Kitapla doğrulama

`tests/test_ch04_karmasik.py`:

| Değer | Kitap | Kod |
|---|---|---|
| 8-vezir en dik tırmanış başarısı | %14 | ✔ (%10–%19 aralığı) |
| 100 yana hamleyle başarı | %94 | ✔ (%90–%98 aralığı) |
| GA uygunlukları 24748552 / 32752411 / 24415124 / 32543213 | 24 / 23 / 20 / 11 | ✔ |
| Çaprazlama 327\|52411 × 247\|48552 | 32748552 | ✔ |
| SONUÇLAR(1, Süpür), kararsız süpürge | {5, 7} | ✔ |
| Koşullu plan, durum 1 | [Süpür, eğer 5 ise [Sağ, Süpür]] | ✔ |
| Algısız süpürge planı | [Sağ, Süpür, Sol, Süpür] | ✔ |
| İlk algı [Sol, Kirli] ile inanç | {1, 3} | ✔ |
| LRTA* tek boyutlu şekil (a)–(e) | 8 9 2 2 4 3 → … → 8 9 5 5 4 3 | ✔ |
