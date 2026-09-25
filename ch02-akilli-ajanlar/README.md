# Bölüm 2 — Akıllı ajanlar

> AIMA 4. baskı, Bölüm 2 · *Intelligent Agents*

## Öğrenme hedefleri

1. Ajan fonksiyonu ile ajan programını ayırt etmek; tabloya dayalı ajanın neden pratik olmadığını göstermek.
2. Rasyonelliği dört öğesiyle tanımlamak; rasyonellik ile her şeyi bilmeyi ayırmak.
3. İyi bir performans ölçütü tasarlamak ve kötü ölçütlerin nasıl istismar edildiğini göstermek.
4. Görev ortamlarını PEAS ve yedi eksenle sınıflandırmak.
5. Beş ajan mimarisini, öğrenen ajanın parçalarını ve atomik/ayrışık/yapılandırılmış temsilleri açıklamak.

## Çalışma sırası

1. Kitapta Bölüm 2'yi oku.
2. [`notlar.md`](notlar.md) ile pekiştir.
3. Örnekleri çalıştır (aşağıda).
4. [`alistirmalar.md`](alistirmalar.md) → [`cozumler/`](cozumler/)
5. [`quiz.md`](quiz.md)

## Dosyalar

| Dosya | İçerik |
|---|---|
| `notlar.md` | Kitap bölümleriyle eşlenmiş notlar, örnek sınıflandırmalar, terimler |
| `ornekler/tablo_ajan.py` | Tabloya dayalı ajan ve tablo boyutunun üstel büyümesi |
| `ornekler/performans_olcutu.py` | Yanlış ölçütü istismar eden "hileci" süpürge |
| `ornekler/model_based_vacuum.py` | Basit refleks ve modele dayalı ajan karşılaştırması |
| `ornekler/ajan_mimarileri_karsilastirma.py` | Beş mimarinin özet tablosu |
| `alistirmalar.md` | 9 alıştırma (★ – ★★★) |
| `cozumler/` | Tüm alıştırmaların çözümleri (A6 çalıştırılabilir kod) |
| `quiz.md` | 10 soru + cevaplar |

```bash
python ornekler/tablo_ajan.py
python ornekler/performans_olcutu.py
python ornekler/model_based_vacuum.py
python ornekler/ajan_mimarileri_karsilastirma.py
python cozumler/alistirma6_olcut_onar.py
```

## Kaynaklar

- [aima.cs.berkeley.edu](https://aima.cs.berkeley.edu/) · [github.com/aimacode](https://github.com/aimacode)
