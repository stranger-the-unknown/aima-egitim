# A3–A10 çözümleri

Kodlu kısımlar: `python cozumler/alistirma_kod.py` (bölüm klasöründen).

---

## A3 — Hırsız ağında bir dünya

P(j, ¬m, ¬a, ¬b, ¬e) = P(j | ¬a) P(¬m | ¬a) P(¬a | ¬b, ¬e) P(¬b) P(¬e)
= 0.05 × 0.99 × 0.999 × 0.999 × 0.998 ≈ **0.0493**

Hırsız yok, deprem yok, alarm çalmıyor, Mary aramıyor, ama John arıyor. John'un P(j | ¬a) = 0.05 olasılıkla telefon zilini alarmla karıştırması bu durumu açıklar. Şaşırtıcı biçimde oldukça olası bir dünya: Yaklaşık 20 günde bir.

## A4 — Numaralandırma elle

Gizli değişken: **Earthquake**. JohnCalls ve MaryCalls, sorgunun (Burglary) ya da kanıtın (Alarm) atası değildir, bu yüzden toplamları 1'dir ve hesaptan çıkar.

```text
P(b, a)  = P(b)  Σ_e P(e) P(a | b, e)  = 0.001 × (0.002 × 0.95 + 0.998 × 0.94)  ≈ 0.000940
P(¬b, a) = P(¬b) Σ_e P(e) P(a | ¬b, e) = 0.999 × (0.002 × 0.29 + 0.998 × 0.001) ≈ 0.001576
P(b | a) = 0.000940 / (0.000940 + 0.001576) ≈ 0.374
```

P(Burglary | alarm, earthquake) ≈ **0.003**. Deprem, alarmı zaten açıklıyor. Hırsızlık olasılığı önsele (0.001) yakın bir değere düşer. Bunun adı **açıklayıp götürme** (explaining away): Ortak bir etkinin (Alarm) iki nedeni, etki gözlendiğinde birbirine bağımlı hâle gelir.

## A5 — Bağımsızlıkları oku

1. Markov örtüsü(Sprinkler) = ebeveyn {Cloudy} ∪ çocuk {WetGrass} ∪ çocuğun diğer ebeveyni {Rain} = **{Cloudy, WetGrass, Rain}**.
2. - **Sprinkler ⊥ Rain? Hayır.** Ortak nedenleri Cloudy üzerinden bağlılar (ahlaki grafikte S – C – R yolu açık).
   - **Sprinkler ⊥ Rain | Cloudy? Evet.** Ata alt grafiği {S, R, C}. WetGrass yok, bu yüzden S ile R ahlaki bağla birleşmez. Tek yol C üzerinden, C verilince kesilir.
   - **Sprinkler ⊥ Rain | Cloudy, WetGrass? Hayır.** WetGrass artık alt grafikte. S ve R'nin ortak çocuğu olduğu için ahlaki grafikte doğrudan birleşirler. Islak çimeni gördükten sonra yağmurlamanın açık olduğunu öğrenmek yağmur olasılığını düşürür (açıklayıp götürme).
3. **Evet.** Cloudy, WetGrass'ın torunu değil. WetGrass ebeveynleri (S, R) verildiğinde torunu olmayanlardan bağımsızdır.

Kod dört cevabı tam ortak dağılımdan sayısal olarak doğrular.

## A6 — Ters sıra

| Sıra | Ebeveynler | Parametre |
|---|---|---|
| C, S, R, W | S←C; R←C; W←S,R | 1 + 2 + 2 + 4 = **9** |
| W, S, R, C | S←W; R←W,S; C←S,R | 1 + 2 + 4 + 4 = **11** |

Ters sırada Rain, WetGrass ve Sprinkler'a bağlı olmak zorunda (ıslak çimen verildiğinde Sprinkler ve Rain bağımlı). Cloudy'nin ise WetGrass'a ihtiyacı yok, çünkü S ve R verildiğinde WetGrass Cloudy hakkında yeni bir şey söylemez. Fark hırsız ağındaki kadar büyük değil, ama yine tanısal yön daha pahalı.

## A7 — Gürültülü-VEYA

1. P(¬öksürük | grip, alerji) = 0.3 × 0.4 = 0.12 → **P(öksürük) = 0.88**.
2. Hiçbir neden yokken P(öksürük) = **0**. Gerçekçi değil: Toz, sigara, astım gibi listelenmemiş nedenler var.
3. Sızıntıyla P(¬öksürük | nedenler) = (1 − 0.1) × Π q:
   - grip + alerji: 1 − 0.9 × 0.12 = **0.892**
   - hiçbiri: 1 − 0.9 = **0.1**

## A8 — İlgisiz değişkenler

Sorgunun ve kanıtın ataları: {Burglary, JohnCalls, Alarm, Earthquake}. **MaryCalls ilgisizdir.** Σ_m P(m | a) = 1 olduğu için hesaptan çıkar.

Sonuç ikisinde de P(b | j) ≈ 0.0163. Çarpma sayısı: numaralandırma **38**, eleme **14**. Numaralandırma MaryCalls'u da gezer ve aynı alt ifadeleri tekrar hesaplar.

## A9 — 3-SAT'ı Bayes ağına indirgemek

1. **P(S = true) = 0.5625 > 0**: Cümle karşılanabilir.
2. Her atamanın olasılığı 2⁻⁴ = 1/16. Karşılayan atama sayısı = P(S = true) × 16 = **9**. Kaba kuvvet de 9 bulur.
3. Bayes ağında kesin çıkarım yapabilen bir algoritma 3-SAT'ı çözebilir, bu yüzden çıkarım **NP-zordur**. Karşılayan atamaları **saymak** da mümkün olduğu için aslında **#P-zordur**. Yine de pratik ağların çoğu (çok ağaçlar, seyrek ağlar) verimli çözülür.

## A10 — Örnekleme yöntemlerini karşılaştır

Bir çalıştırmanın sonuçları (tohum 7; sayılar rastgelelikle biraz değişir):

| Yöntem | N = 10 000 | N = 100 000 |
|---|---|---|
| Ret (kabul edilen) | 0.333 (24 örnek) | 0.314 (188 örnek) |
| Olabilirlik ağırlıklandırma | 0.287 | 0.284 |
| Gibbs (100 000 adım) | — | 0.287 |

Kesin değer 0.284.

1. P(j, m) ≈ 0.0021: 10 000 örnekten yalnızca ~21'i kanıtla uyuşur. Ret örneklemesi örneklerin %99.8'ini çöpe atar.
2. Olabilirlik ağırlıklandırma, çünkü bütün örnekleri kullanır. Gibbs de iyi, ama ardışık örnekler birbirine bağımlıdır ve ısınma gerekir.
3. Kanıt yapraklarda olduğu için örnekler kanıttan habersiz üretilir: Çoğunda alarm çalmaz ve ağırlık küçüktür (0.05 × 0.01). Tahmini, alarmın çaldığı az sayıda ağır örnek belirler. Bu yüzden varyans yüksektir. Kanıt köklerde olsaydı örnekler kanıta uygun üretilirdi ve ağırlıklandırma çok daha verimli olurdu.
