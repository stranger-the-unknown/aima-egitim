# Bölüm 3 — Arama yoluyla problem çözme

> AIMA 4. baskı, Bölüm 3 · *Solving Problems by Searching*

## Öğrenme hedefleri

1. Bir problemi beş parçasıyla biçimsel olarak tanımlamak.
2. Arama ağacı ile durum uzayını, ağaç benzeri arama ile graf aramasını ayırt etmek.
3. BFS, UCS, DFS, DLS, IDS ve çift yönlü aramayı tamlık, optimallik, zaman ve bellek açısından karşılaştırmak.
4. A*'ın optimalliğini kabul edilebilirlik ve tutarlılıkla açıklamak.
5. Sezgisel türetmek (gevşetme) ve sezgiselleri etkin dallanma faktörüyle karşılaştırmak.

## Çalışma sırası

1. Kitapta Bölüm 3'ü oku.
2. [`notlar.md`](notlar.md)
3. Örnekleri çalıştır, sonuçları kitaptaki şekillerle karşılaştır.
4. [`alistirmalar.md`](alistirmalar.md) → [`cozumler/`](cozumler/)
5. [`quiz.md`](quiz.md)

## Dosyalar

| Dosya | İçerik |
|---|---|
| `ornekler/arama.py` | Arama kütüphanesi: `Problem`, `Dugum`, en iyi öncelikli arama (UCS, açgözlü, A*, ağırlıklı A*), BFS, DFS, DLS, IDS, IDA*, etkin dallanma |
| `ornekler/romania_arama.py` | Romanya haritası: 8 algoritma, A* izi, çift yönlü UCS |
| `ornekler/sekiz_bulmaca.py` | 8-bulmaca: h1, h2, BFS/A*/IDA*, rastgele bulmacalarda b* karşılaştırması |
| `alistirmalar.md` | 10 alıştırma (★ – ★★★) |
| `cozumler/` | Tüm çözümler (A8–A10 çalıştırılabilir kod) |
| `quiz.md` | 12 soru + cevaplar |

```bash
python ornekler/romania_arama.py
python ornekler/sekiz_bulmaca.py
python cozumler/alistirma8_gevsetme.py
python cozumler/alistirma9_agirlikli.py
python cozumler/alistirma10_kurt_keci_lahana.py
```

## Kitapla doğrulama

`tests/test_ch03_arama.py` şu değerleri kitaptakilerle karşılaştırır:

| Değer | Kitap | Kod |
|---|---|---|
| A* ve UCS, Arad → Bucharest | 418 km (Sibiu – Rimnicu Vilcea – Pitesti) | ✔ |
| Açgözlü arama | 450 km (Fagaras üzerinden) | ✔ |
| A* izinde f değerleri | 366, 393, 413, 415, 417, 418 | ✔ |
| 8-bulmaca örneği: h1, h2, optimal uzunluk | 8, 18, 26 | ✔ |
| Etkin dallanma, N = 52, d = 5 | 1,92 | ✔ |
| N(IDS), N(BFS), b = 10, d = 5 | 123.450, 111.110 | ✔ |
