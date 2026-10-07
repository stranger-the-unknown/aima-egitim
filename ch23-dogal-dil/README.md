# Bölüm 23 — Doğal dil işleme

> AIMA 4. baskı, Bölüm 23 · *Natural Language Processing*

## Öğrenme hedefleri

1. Sözcük torbası ve n-gram dil modellerini kurmak; düzeltme yapmak.
2. Şaşkınlıkla modelleri karşılaştırmak; HMM ile sözcük türü etiketlemek.
3. PCFG ile cümle olasılığı hesaplamak; CYK ile en olası ağacı bulmak.
4. Ağaç bankasından PCFG öğrenmek.
5. Bileşimsel anlambilimi uygulamak.
6. Gerçek dilin zorluklarını ve temel NLP görevlerini tanımak.

## Çalışma sırası

1. Kitapta Bölüm 23'ü oku.
2. [`notlar.md`](notlar.md)
3. Örnekleri çalıştır.
4. [`alistirmalar.md`](alistirmalar.md) → [`cozumler/`](cozumler/)
5. [`quiz.md`](quiz.md)

## Dosyalar

| Dosya | İçerik |
|---|---|
| `ornekler/dil_modelleri.py` | Naif Bayes sözcük torbası, n-gram, Laplace, ara değerleme, şaşkınlık, HMM + Viterbi etiketleme |
| `ornekler/ayristirma.py` | E₀ PCFG (Şekil 23.2–23.3), olasılıksal CYK, belirsizlik, ağaç bankasından PCFG |
| `ornekler/anlambilim.py` | Aritmetik dilbilgisi ve bileşimsel anlambilim, λ-hesabıyla cümle anlamı |
| `alistirmalar.md` | 10 alıştırma |
| `cozumler/` | Tüm çözümler (A3, A5, A7, A8, A9 kod) |
| `quiz.md` | 12 soru + cevaplar |

## Kitapla doğrulama

`tests/test_ch23_dogal_dil.py`:

| Değer | Kitap | Kod |
|---|---|---|
| E₀ kural olasılıkları | her kategori için toplam 1 | ✔ |
| "the wumpus is dead" | Şekil 23.4'teki ağaç; P = 1.35 × 10⁻⁶ | ✔ |
| Fazla / eksik üretim | "Me go I" kabul, "I think …" ret | ✔ ("go" sözlüğe bizim eklememiz) |
| Sözcük torbası sayıları | P(ekonomi) = 0.1, P(stocks \| ekonomi) = 0.007 | ✔ |
| Ardıllık kuralı | 1/(N + 2) | ✔ |
| Aritmetik dilbilgisi | 3 + (4 ÷ 2) → Exp(5) | ✔ |
| λ-hesabı | "Ali loves Bo" → Loves(Ali, Bo) | ✔ |
