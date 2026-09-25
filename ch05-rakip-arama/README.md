# Bölüm 5 — Rakip arama ve oyunlar

> AIMA 4. baskı, Bölüm 5 · *Adversarial Search and Games*

## Öğrenme hedefleri

1. Bir oyunu biçimsel olarak tanımlamak; minimax değerini hesaplamak.
2. Alfa-beta budamayı izlemek ve hamle sıralamasının etkisini sayısal olarak göstermek.
3. Sezgisel alfa-betanın bileşenlerini (değerlendirme, kesme, sessizlik, transpozisyon tablosu) açıklamak.
4. MCTS'i ve UCB1'i uygulamak.
5. Şans düğümlü oyunlarda beklenti-minimaksı açıklamak.

## Çalışma sırası

1. Kitapta Bölüm 5'i oku.
2. [`notlar.md`](notlar.md)
3. Örnekleri çalıştır.
4. [`alistirmalar.md`](alistirmalar.md) → [`cozumler/`](cozumler/)
5. [`quiz.md`](quiz.md)

## Dosyalar

| Dosya | İçerik |
|---|---|
| `ornekler/minimax_tictactoe.py` | XOX: minimax, alfa-beta, ağaç istatistikleri, "hızlı kazan" seçeneği |
| `ornekler/oyun_agaci.py` | Kitaptaki iki katlı ağaç, alfa-beta izi, hamle sıralaması deneyi |
| `ornekler/dortlu_ab.py` | Dört-Bir-Arada: sezgisel alfa-beta, EVAL, sıralama, sınır bayraklı TT; `--oyna` |
| `ornekler/mcts_xox.py` | UCT-MCTS, kitaptaki UCB1 örneği, minimax'a karşı maçlar |
| `ornekler/beklenti_minimax.py` | Şans düğümleri; sırayı koruyan dönüşümün kararı değiştirmesi |
| `alistirmalar.md` | 10 alıştırma |
| `cozumler/` | Tüm çözümler (A7, A8, A10 kod) |
| `quiz.md` | 12 soru + cevaplar |

```bash
python ornekler/minimax_tictactoe.py --mod istatistik
python ornekler/oyun_agaci.py
python ornekler/dortlu_ab.py
python ornekler/mcts_xox.py
python ornekler/beklenti_minimax.py
```

## Kitapla doğrulama

`tests/test_ch05_oyunlar.py`:

| Değer | Kitap | Kod |
|---|---|---|
| XOX farklı durum sayısı | 5.478 | ✔ |
| XOX yaprak sayısı | < 9! = 362.880 | ✔ (255.168) |
| İki katlı ağaç: B, C, D, A | 3, 2, 2, 3 | ✔ |
| Alfa-betanın budadığı yapraklar | C'nin 4 ve 6 yaprakları | ✔ |
| UCB1, ebeveyn 100; C = 1,4 / C = 1,5 | 60/79 / 2/11 seçilir | ✔ |
| Sırayı koruyan dönüşüm | [1,2,3,4] → a1, [1,20,30,400] → a2 | ✔ |
| Mükemmel sıralamada yaprak sayısı | ≈ b^(m/2) | ✔ (Knuth–Moore, tam eşitlik) |
