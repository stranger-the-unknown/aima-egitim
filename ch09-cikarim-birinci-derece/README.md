# Bölüm 9 — Birinci derece mantıkta çıkarım

> AIMA 4. baskı, Bölüm 9 · *Inference in First-Order Logic*

## Öğrenme hedefleri

1. Önermeselleştirmeyi ve sınırlarını açıklamak.
2. Birleştirmeyi elle ve kodla yapmak (MGU, occurs check, değişken ayırma).
3. Kesin tümcelerle ileri ve geri zincirleme yapmak; Prolog'un tuzaklarını bilmek.
4. FOL cümlelerini CNF'ye çevirmek ve çözümlemeyle kanıtlamak.

## Çalışma sırası

1. Kitapta Bölüm 9'u oku.
2. [`notlar.md`](notlar.md)
3. Örnekleri çalıştır.
4. [`alistirmalar.md`](alistirmalar.md) → [`cozumler/`](cozumler/)
5. [`quiz.md`](quiz.md)

## Dosyalar

| Dosya | İçerik |
|---|---|
| `ornekler/fol_cikarim.py` | Kütüphane: terim ayrıştırıcı, UNIFY (occurs check), değişken ayırma, FOL-FC-ASK, FOL-BC-ASK, çözümleme (destek kümesi, çarpanlama, yanıt çıkarma) |
| `ornekler/birlesim_unification.py` | Kitaptaki UNIFY örnekleri ve diğer durumlar |
| `ornekler/suclu_bati.py` | Kitaptaki suç KB'si: ileri zincirleme (2 tur) ve geri zincirleme kanıt ağacı |
| `ornekler/kedi_cozumleme.py` | Kitaptaki çözümleme kanıtı (Curiosity), yanıt çıkarma, yapıcı olmayan kanıt |
| `ornekler/prolog_yol.py` | Kural sırası ve sonsuz döngü (kitaptaki yol/bağ örneği) |
| `ornekler/geriye_zincir.py` | Kayıp USB: özgün bir geri zincirleme örneği |
| `alistirmalar.md` | 10 alıştırma |
| `cozumler/` | Tüm çözümler (A7–A10 kod) |
| `quiz.md` | 12 soru + cevaplar |

## Kitapla doğrulama

`tests/test_ch09_cikarim.py`:

| Değer | Kitap | Kod |
|---|---|---|
| UNIFY tablosu (4 örnek + değişken ayırma) | {x/Jane}, {x/Bill, y/John}, {y/John, x/Mother(John)}, başarısız, {x/Elizabeth, x17/John} | ✔ |
| Suç KB'si, ileri zincirleme | 1. tur: Sells, Weapon, Hostile; 2. tur: Criminal(West) | ✔ |
| Kedi örneği | ¬Kills(Curiosity, Tuna) ile boş tümce; yanıt Curiosity | ✔ |
| Yol programı | (b) sırası derinlik öncelikli aramada sonsuza iner; ileri zincirleme sonlanır | ✔ |
