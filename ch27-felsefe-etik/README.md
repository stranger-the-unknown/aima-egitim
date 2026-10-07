# Bölüm 27 — Yapay zekânın felsefesi, etiği ve güvenliği

> AIMA 4. baskı, Bölüm 27 · *Philosophy, Ethics, and Safety of AI*

## Öğrenme hedefleri

1. Zayıf ve güçlü YZ ayrımını, Turing'in öngördüğü itirazları ve yanıtlarını açıklamak.
2. Çin odası argümanını ve bilinç sorusunu tarafsızca özetlemek.
3. Otonom silahlar, gözetim ve işin geleceği tartışmalarının argümanlarını sıralamak.
4. k-anonimlik, fark saldırısı, diferansiyel mahremiyet ve federe öğrenmeyi hesaplamalı olarak göstermek.
5. Adalet ölçütlerini tanımlamak; kalibrasyon ile fırsat eşitliğinin çatışmasını göstermek.
6. Güvenlik mühendisliği, düşük etki ve değer hizalama sorununu örneklerle açıklamak.

## Çalışma sırası

1. Kitapta Bölüm 27'yi oku.
2. [`notlar.md`](notlar.md)
3. Örnekleri çalıştır (yalnızca numpy gerekir; bütün veriler yapaydır).
4. [`alistirmalar.md`](alistirmalar.md) → [`cozumler/`](cozumler/)
5. [`quiz.md`](quiz.md)

## Dosyalar

| Dosya | İçerik |
|---|---|
| `ornekler/mahremiyet.py` | Yeniden tanımlama, k-anonimlik, fark saldırısı, Laplace mekanizması (ε-DP), güvenli toplama, federe SGD |
| `ornekler/adalet.py` | Kalibrasyon ve fırsat eşitliği, grup eşikleri, farkında olmayarak adalet (vekil), örneklem boyu dengesizliği |
| `ornekler/guvenlik.py` | Hata ağacı analizi, düşük etki, şartname oyunu, sor/uygula kararı, tekillik hesabı ve S eğrisi |
| `alistirmalar.md` | 10 alıştırma (2 tartışma, 8 hesap/kod) |
| `cozumler/` | Tüm çözümler (A3–A10 kod) |
| `quiz.md` | 12 soru + cevaplar |

## Kitapla doğrulama

`tests/test_ch27_felsefe_etik.py`:

| Değer | Kitap | Kod |
|---|---|---|
| Fark saldırısı | $81 234 / 12 ve $81 199 / 13 → tek kişinin maaşı | ✔ $80 779 |
| ε-diferansiyel mahremiyet | \|log P(Q(D) = y) − log P(Q(D + r) = y)\| ≤ ε | ✔ Laplace mekanizması tam ε verir |
| Güvenli toplama | Maskelerin toplamı sıfırsa sunucu doğru ortalamayı bulur | ✔ |
| Kalibrasyon vs fırsat eşitliği | Taban oranlar farklıysa ikisi birlikte sağlanamaz (Kleinberg vd.) | ✔ |
| Farkında olmama | Model korunan özniteliği vekillerden çıkarır | ✔ |
| Örneklem dengesizliği | Doğrusal model çoğunluğa uyar | ✔ |
| Hata ağacı | VE/VEYA ağacıyla toplam arıza olasılığı | ✔ |
| Düşük etki | Fayda − değişikliklerin ağırlıklı toplamı | ✔ |
| Tekillik | "24 yılda 2 yıl yaklaştı, bu hızla 336 yıl" | ✔ |

Kitaptaki gerçek sayılar (Sweeney'nin %87'si, COMPAS'ın %60/%61 ve %45/%23'ü, %33 hata oranı…) notlarda aktarılır; kodlar bunları yapay verilerle benzer mekanizmalar üzerinden gösterir, gerçek verileri yeniden üretmez.
