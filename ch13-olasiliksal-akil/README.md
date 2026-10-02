# Bölüm 13 — Olasılıksal akıl yürütme (Bayes ağları)

> AIMA 4. baskı, Bölüm 13 · *Probabilistic Reasoning*

## Öğrenme hedefleri

1. Bir alanı Bayes ağı olarak modellemek ve ağın tam ortak dağılımı nasıl tanımladığını açıklamak.
2. Düğüm sırasının ağın büyüklüğünü neden değiştirdiğini göstermek.
3. Ağdan koşullu bağımsızlıkları okumak (ebeveynler, Markov örtüsü, d-ayrım).
4. Numaralandırma ve değişken elemeyle kesin çıkarım yapmak; karmaşıklığı tartışmak.
5. Örnekleme yöntemlerini uygulamak ve gözlem ile müdahale arasındaki farkı açıklamak.

## Çalışma sırası

1. Kitapta Bölüm 13'ü oku.
2. [`notlar.md`](notlar.md)
3. Örnekleri çalıştır.
4. [`alistirmalar.md`](alistirmalar.md) → [`cozumler/`](cozumler/)
5. [`quiz.md`](quiz.md)

## Dosyalar

| Dosya | İçerik |
|---|---|
| `ornekler/bayes_agi.py` | Kütüphane: Boole Bayes ağı, numaralandırma, faktörlerle değişken eleme, örnekleme (önsel, ret, olabilirlik ağırlıklandırma, Gibbs), Markov örtüsü, do-işleci, gürültülü-VEYA |
| `ornekler/hirsiz_alarmi.py` | Kitabın hırsız alarmı ağı: 0.000628, P(B \| j, m) = 0.284, açıklayıp götürme, düğüm sırası 10 / 13 / 31 |
| `ornekler/yerel_dagilimlar.py` | Gürültülü-VEYA ateş tablosu; probit ve expit |
| `ornekler/ornekleme.py` | Yağmurlama ağı: 0.324, ret örneklemesi → ⟨0.3, 0.7⟩, olabilirlik ağırlıklandırma, Gibbs |
| `ornekler/nedensel.py` | Gözlem ve müdahale: 0.3'e karşı 0.5; arka kapı ayarlaması |
| `ornekler/bayes_agi_kucuk.py` | Özgün ofis alarmı ağı (başlangıç için basit numaralandırma) |
| `ornekler/cpt_goster.py` | CPT'leri okunaklı yazdırma |
| `alistirmalar.md` | 10 alıştırma |
| `cozumler/` | Tüm çözümler (A4–A10 kod) |
| `quiz.md` | 12 soru + cevaplar |

## Kitapla doğrulama

`tests/test_ch13_bayes_aglari.py`:

| Değer | Kitap | Kod |
|---|---|---|
| P(j, m, a, ¬b, ¬e) | ≈ 0.000628 (standart CPT ile) | ✔ |
| P(b \| j, m) normalize edilmeden | α 0.00059224 / α 0.0014919 | ✔ |
| P(Burglary \| j, m) | ≈ ⟨0.284, 0.716⟩ | ✔ |
| Düğüm sırası parametre sayısı | 10, 13, 31 | ✔ |
| Gürültülü-VEYA ateş tablosu | 0.0, 0.9, 0.8, 0.98, 0.4, 0.94, 0.88, 0.988 | ✔ |
| S_PS(true, false, true, true) | 0.324 | ✔ |
| P(Rain \| Sprinkler = true) | ⟨0.3, 0.7⟩ | ✔ |

> Not: Elimizdeki PDF'te Şekil 13.2'nin Alarm tablosu hatalı basılmış. Ayrıntı `notlar.md` §1'de.
