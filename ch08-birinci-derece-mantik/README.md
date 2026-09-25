# Bölüm 8 — Birinci derece mantık

> AIMA 4. baskı, Bölüm 8 · *First-Order Logic*

## Öğrenme hedefleri

1. FOL'un önerme mantığına göre ne kattığını açıklamak.
2. Cümleleri bir modelde değerlendirmek; niceleyici ve eşitlik hatalarını tanımak.
3. Doğal dili FOL'a çevirmek.
4. Bir alan için sözcük dağarcığı ve aksiyomlar yazmak.
5. Bilgi mühendisliğinin yedi adımını uygulamak.

## Çalışma sırası

1. Kitapta Bölüm 8'i oku.
2. [`notlar.md`](notlar.md)
3. Örnekleri çalıştır.
4. [`alistirmalar.md`](alistirmalar.md) → [`cozumler/`](cozumler/)
5. [`quiz.md`](quiz.md)

## Dosyalar

| Dosya | İçerik |
|---|---|
| `ornekler/fol_model.py` | Modelde değerlendirme; ∀/∧ ve ∃/⇒ hataları; niceleyici sırası; veritabanı anlamı (16 model) |
| `ornekler/fol_ceviri.py` | Türkçe ↔ FOL çeviri örnekleri |
| `ornekler/fol_sozluk.py` | Ebeveyn/Ata olgularından ileri zincirleme |
| `ornekler/akrabalik_turkce.py` | Amca/dayı/hala/teyze/kuzen/dede tanımları; "uncle" ile karşılaştırma |
| `ornekler/tam_toplayici.py` | Kitaptaki C1 tam toplayıcı: yedi adımlık bilgi mühendisliği, sorgu, doğrulama, hata ayıklama |
| `alistirmalar.md` | 10 alıştırma |
| `cozumler/` | Tüm çözümler (A7, A10 kod) |
| `quiz.md` | 12 soru + cevaplar |

```bash
python ornekler/fol_model.py
python ornekler/akrabalik_turkce.py
python ornekler/tam_toplayici.py
```

## Kitapla doğrulama

`tests/test_ch08_fol.py`:

| Değer | Kitap | Kod |
|---|---|---|
| C1: toplam = 0, elde = 1 veren girişler | {1,1,0}, {1,0,1}, {0,1,1} | ✔ |
| C1 tam giriş–çıkış tablosu | doğru toplayıcı | ✔ |
| Veritabanı anlamında model sayısı (2 sabit, 1 ikili ilişki) | 16 | ✔ |
| ∀x Kral(x) ∧ Kişi(x) / ∃x Taç(x) ⇒ Başında(x, John) | tipik hatalar | ✔ (yanlış / anlamsızca doğru) |
