# Katkı rehberi

Bu depo AIMA 4. baskıyı bölüm bölüm çalışmak için hazırlandı; 28 bölümün hepsi tamam. Bu rehber, mevcut bir bölümü düzeltirken ya da genişletirken uyulacak kuralları anlatır.

## Telif kuralları (zorunlu)

1. Kitaptan **uzun alıntı** ya da **yakın parafraz** yok; tek tük kısa terim ve şekil/denklem numarası dışında metin aktarılmaz.
2. Notlar **özgün Türkçe** öğretim diliyle yazılır.
3. Kod, kamuya açık algoritmaların **eğitici** Python uygulamasıdır.
4. Alıştırmalar ve quizler **özgündür** (kitap sorularının kopyası değil).
5. Resmi kaynaklara bağlantı verin: [aima.cs.berkeley.edu](https://aima.cs.berkeley.edu/), [aimacode](https://github.com/aimacode).

## Kitapla doğrulama

- Notlardaki her sayı, tanım ve örnek **kitabın 4. baskısıyla** karşılaştırılır. 3. baskının değerleri farklı olabilir (ör. Bölüm 17'de ödül geçişe aittir).
- Kitaptaki sayısal örnekler (tablolar, şekillerdeki değerler) mümkünse kodla yeniden üretilir ve testle doğrulanır; bölüm `README.md`'sindeki **"Kitapla doğrulama"** tablosuna eklenir.
- Kitapta olmayan seçimler (yapay veri, parametreler, eşikler) notlarda ve README'de "bizim varsayımımız / bizim seçimimiz" diye açıkça işaretlenir.
- Kitapta tutarsızlık ya da baskı hatası bulunursa notta açıklanır (ör. Bölüm 13'teki Alarm tablosu).
- Kitabı karşılaştırmak için PDF'i metne çevirin (poppler-utils) ve çıktıyı depoya koymayın:

```bash
pdftotext -layout "Artificial-Intelligence-A-Modern-Approach-4th edition.pdf" aima.txt
```

  PDF sayfa numarası ≈ kitap sayfa numarası + 13.

## Bölüm klasörünün düzeni

```
chNN-kisa-baslik/
├── README.md        # öğrenme hedefleri, dosyalar, kitapla doğrulama tablosu
├── notlar.md        # kitabın alt bölümlerine eşleme tablosu, notlar, sık yapılan hatalar,
│                    # kendini yokla, kod rehberi, "## Terimler" tablosu
├── ornekler/        # çalıştırılabilir Python
├── alistirmalar.md  # 8–10 özgün alıştırma (★ / ★★ / ★★★)
├── cozumler/
│   ├── alistirma1_10.md   # bütün çözümler (Bölüm 16–28 düzeni; 1–15'te çözümler birkaç dosyaya bölünmüş)
│   └── alistirma_kod.py   # kodlu çözümler (ornekler/'i sys.path ile içe aktarır)
└── quiz.md          # 10–12 soru; çoktan seçmeli cevap harfleri dağıtılmış; cevaplar sonda
```

`notlar.md`'deki **Terimler** tablosu `| Türkçe | İngilizce | Kısa açıklama |` biçiminde olmalı; [`SOZLUK.md`](SOZLUK.md) bu tablolardan üretilir. Tabloyu değiştirdikten sonra:

```bash
python scripts/sozluk_uret.py
```

`SOZLUK.md` elle düzenlenmez.

## Kod kuralları

- **Python 3.10 uyumlu** yazın (CI 3.10, 3.12 ve 3.13'te çalışır). 3.12'ye özgü yazımlardan kaçının; ör. f-string içinde dıştakiyle aynı tırnağı kullanmak.
- Bağımlılık yalnızca `numpy` ve `matplotlib`; yenisi gerekirse `requirements.txt` güncellenir ve gerekçesi yazılır.
- Her `ornekler/*.py` ve `cozumler/alistirma_kod.py` doğrudan çalıştırılabilir olmalı (`if __name__ == "__main__":`), pencere açmamalı ve **180 saniyenin altında** bitmeli (duman testi her betiği çalıştırır).
- **Modül adları bölümler arasında benzersiz** olmalı (ör. Bölüm 14'te `lokalizasyon.py` varken Bölüm 26'daki dosya `robot_lokalizasyon.py`). Başka bölümün kodu gerekiyorsa `sys.path`'e o bölümün `ornekler/` klasörü eklenerek içe aktarılır (Bölüm 22 → Bölüm 17'nin `mdp.py`'si, Bölüm 20 → Bölüm 19'un `karar_agaci.py`'si).
- Yorumlar, değişken adları ve çıktılar Türkçe olabilir; kitaptaki algoritma adları ve şekil numaraları docstring'de belirtilir.
- Rastgelelik için `np.random.default_rng(tohum)` kullanın; çıktılar tekrarlanabilir olsun.

## Testler

Her bölümün `tests/test_chNN_*.py` dosyası vardır; dosyaları `tests/yardimci.py`'deki `yukle("chNN-.../ornekler/x.py")` ile yükler. Kitaptaki sayılar ve kodun önemli özellikleri burada doğrulanır.

```bash
python scripts/check_setup.py
python -m pytest -q                         # bütün testler (~10 dk; duman testi her betiği çalıştırır)
python -m pytest -q tests/test_ch26_robotik.py
python -m pytest -q tests/test_duman.py -k ch26
```

`pytest.ini`'de `-q` olduğu için özet satırı görünmezse `-o addopts=""` ekleyin.

## Git düzeni

- Geliştirme `egitim-iyilestirme` dalında yapılır; `main`'e pull request ile gelir.
- Push'tan önce `git fetch` yapın; aynı hesaptan başka bir dal da push edilebilir, **force-push kullanmayın**.
- Commit mesajı örnekleri:

```
Bölüm 26 (yarım): MCL/EKF, C-uzayı ve planlayıcılar + testler
Bölüm 26: robotik tamamlandı (notlar, alıştırmalar, quiz, README)
```

## Okurken fark ettikleriniz

Çalışırken anlaşılmayan bir anlatım, yanlış görünen bir sayı, çalışmayan bir kod ya da zor bir alıştırma görürseniz yerel `bekleyen-isler.md` dosyasına (git'e girmez) not alın: ne oldu, nerede (bölüm, dosya, §), önemi. Bir sonraki geliştirme döneminde bu liste ele alınır.
