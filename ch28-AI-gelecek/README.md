# Bölüm 28 — Yapay zekânın geleceği

> AIMA 4. baskı, Bölüm 28 · *The Future of AI*

## Öğrenme hedefleri

1. YZ bileşenlerinin her birinde nerede olduğumuzu ve neyin eksik olduğunu önceki bölümlere bağlayarak açıklamak.
2. Kaba kuvvetin neden yetmediğini sayısal bir örnekle göstermek.
3. Her an kesilebilir algoritmaları, karar kuramsal üst-akıl yürütmeyi ve sınırlı en iyiliği açıklamak.
4. Dar ve genel YZ tartışmasını ve YZ mühendisliğinin olgunlaşma sorununu değerlendirmek.

## Çalışma sırası

1. Kitapta Bölüm 28'i oku.
2. [`notlar.md`](notlar.md)
3. Örnekleri çalıştır (yalnızca numpy gerekir).
4. [`alistirmalar.md`](alistirmalar.md) → [`cozumler/`](cozumler/)
5. [`quiz.md`](quiz.md)
6. Kitabı bitirdin: [`../BITIRME.md`](../BITIRME.md)

## Dosyalar

| Dosya | İçerik |
|---|---|
| `ornekler/hesaplama_sinirlari.py` | Borges hesabı, kaynak eğilimlerinden katlanma süreleri, her an kesilebilir algoritma, hesaplamanın değeri, sınırlı en iyilik (oyuncak) |
| `ornekler/yetenek_haritasi.py` | Kitap dışı: AIMA bölümlerinden modern araçlara kişisel çalışma yol haritası (`--yol …`) |
| `ornekler/proje_fikirleri.py` | Kitap dışı: bölümlere göre 1–2 haftalık portföy proje fikirleri |
| `alistirmalar.md` | 8 alıştırma (5 hesap/kod, 3 yansıtma) |
| `cozumler/` | Tüm çözümler (A2–A6 kod) |
| `quiz.md` | 10 soru + cevaplar |

## Kitapla doğrulama

`tests/test_ch28_ai_gelecek.py`:

| Değer | Kitap | Kod |
|---|---|---|
| Borges hesabı | 10⁵¹ işlem/s ile bir yılda yalnızca 11 sözcüklük diziler | ✔ (100 000 sözcüklük sözlük bizim varsayımımız) |
| arXiv makaleleri | 2009–2017 arasında iki yılda bir ikiye | ✔ |
| Süper bilgisayar hızı | 1969–2019 arasında 10¹⁰ kattan fazla | ✔ ~1.5 yılda bir ikiye (bizim hesabımız) |
| Her an kesilebilirlik | Niteliği zamanla artar | ✔ |
| Üst-akıl yürütme | Hesaplamanın değeri = karar iyileşmesi − gecikme maliyeti; miyopi sorunu | ✔ |
| Sınırlı en iyilik | Sabit mimaride en iyi program | ✔ oyuncak örnek |
