# A1–A10 çözümleri

Kodlu kısımlar: `python cozumler/alistirma_kod.py` (bölüm klasöründen).

---

## A1 — Neden politika?

1. Planlanan yol (1,1) → (1,2) → (1,3) → (2,3) → (3,3) → (4,3). Her eylem 0.8 olasılıkla istenen yere gider: 0.8⁵ = **0.32768**.
2. Alttan: Yukarı → sağa kayar (2,1) [0.1]; Yukarı → sağa kayar (3,1) [0.1]; Sağ → yukarı kayar (3,2) [0.1]; Sağ → yukarı kayar (3,3) [0.1]; Sağ → (4,3) [0.8]. Olasılık 0.1⁴ × 0.8 = **0.00008**. Toplam **0.32776**.
3. Dizi üçte iki olasılıkla başarısız olur ve ajan planlamadığı bir durumda kalır. Politika her durumda ne yapılacağını söylediği için kaymalardan sonra da doğru davranır.

## A2 — İndirim

1. γ = 1: 9 × (−0.04) + 1 = **0.64**. γ = 0.9: −0.04 × (1 − 0.9⁹)/0.1 + 0.9⁹ ≈ −0.245 + 0.387 = **0.142**. γ = 0.5: **−0.078** (+1 o kadar uzakta ki adım cezaları ağır basar).
2. (1/0.95) − 1 ≈ **%5.3**.
3. R_max / (1 − γ) = 1 / 0.1 = **10**.

## A3 — Bellman denklemi

1. γ = 1 ile:
   - Yukarı: 0.8(−0.04 + 0.8016) + 0.1(−0.04 + 0.6953) + 0.1(−0.04 + 0.7453) = **0.7453**
   - Aşağı: 0.9(−0.04 + 0.7453) + 0.1(−0.04 + 0.6953) = 0.7003
   - Sol: 0.9(−0.04 + 0.7453) + 0.1(−0.04 + 0.8016) = 0.7109
   - Sağ: 0.8(−0.04 + 0.6953) + 0.1(−0.04 + 0.8016) + 0.1(−0.04 + 0.7453) = 0.6709

   En iyisi Yukarı ve değeri U(1,1) = 0.7453 ile aynı: Bellman denklemi sağlanıyor.
2. - Sol: 0.8(−0.04 + 0.6953) + 0.1(−0.04 + 0.6514) + 0.1(−0.04 + 0.7003) = **0.6514**
   - Yukarı: 0.8(−0.04 + 0.7003) + 0.1(−0.04 + 0.6953) + 0.1(−0.04 + 0.4279) = **0.6325**

   Sol açıkça daha iyidir; r = −0.04'te iki eylem eşit değildir. Kod, iki eylemin yalnızca r ≈ −0.0448'de eşit olduğunu bulur. Kitaptaki Şekil 17.2(a)'nın iki politikası, −0.0850 < r < −0.0273 aralığının iki alt aralığına aittir (Yukarı solda, Sol sağda).

## A4 — Dokuz politika

Kırılma noktaları: −1.6497, −1.5643, −0.7311, −0.4526, −0.0850, −0.0448, −0.0274, −0.0221 → **9 politika**. Kitabın verdiği beş değer bunların arasında. Kitabın saymadığı üç ara kırılma: −1.5643 ((3,1) Sağ'dan Yukarı'ya), −0.0448 ((3,1) Yukarı'dan Sol'a) ve −0.0221 ((4,1) Sol'dan Aşağı'ya, yani duvara: risk sıfır).

**Neden uygun politikadan başlamalı?** γ = 1 iken uç duruma hiç varmayan (uygun olmayan) bir politikanın faydası r < 0 için −∞'dur; politika değerlendirmedeki doğrusal sistem tekil olur. Uygun bir politikadan başlayınca iyileştirme adımları da uygun politikalar üretir.

## A5 — Sonlu ufuk

N = 1–12 için en iyisi **Yukarı**, N ≥ 13 için **Sol**. Sol yolu (3,1) → (2,1) → (1,1) → (1,2) → (1,3) → (2,3) → (3,3) → (4,3) en az 7 adım sürer ve kaymalarla daha uzundur. Az zaman kalınca bu yol hedefe yetişemez; tek şans, (4,2)'ye düşme riskine rağmen Yukarı'dan kısa yoldur. Zaman bol olunca güvenli yol kazanır. Aynı durumda farklı zamanlarda farklı eylem: **durağan olmayan** politika.

## A6 — Politika değerlendirme

1. Denklemler:
   - U(X) = 0.5(1 + 0.5 U(X)) + 0.5(0 + 0.5 U(Y)) ⇒ 3U(X) − U(Y) = 2
   - U(Y) = 0.8(0 + 0.5 U(Y)) + 0.2(2 + 0.5 U(X)) ⇒ 6U(Y) − U(X) = 4

   Çözüm: U(X) = **16/17 ≈ 0.9412**, U(Y) = **14/17 ≈ 0.8235**.
2. | adım | U(X) | U(Y) | en büyük hata |
   |---|---|---|---|
   | 0 | 0 | 0 | 0.941 |
   | 1 | 0.5 | 0.4 | 0.441 |
   | 2 | 0.725 | 0.61 | 0.216 |
   | 3 | 0.834 | 0.717 | 0.108 |

   Hata her adımda yaklaşık yarıya iniyor: büzülme çarpanı γ = 0.5.

## A7 — Tehlikeli yardım

1. Politika değişir ve ajan **hiçbir zaman uca varmaz** (1000 adımda olasılık ~0). Örneğin (2,3)'ten sola gidip geri gelen bir döngü her turda +0.2 − 2 × 0.04 = +0.12 kazandırır; γ = 0.99'da bu, +1'e varmaktan çok daha değerlidir: U(1,1) 0.70'ten 4.71'e çıkar. Ajan "yaklaşma"yı öğrenmedi; bonusu sömürmeyi öğrendi.
2. Φ = −0.2 × uzaklık ile şekillendirmede bir döngünün toplam ek ödülü γ < 1'de yaklaşık sıfırdır (γ = 1'de tam sıfır); döngü kazandırmaz ve politika **değişmez** (şekillendirme teoremi).
3. Φ(4,2) = −0.2 alınırsa (3,1)'deki eylem Yukarı'dan Sol'a döner. Teoremin kanıtı U′ = U − Φ eşitliğine dayanır; uç durumda U′ = 0 olduğundan bu eşitlik ancak Φ(uç) = 0 ise tutar. Aksi hâlde −1'e düşmek fazladan −0.2γ ile cezalandırılmış olur ve risk dengesi değişir.

## A8 — Gittins indeksi

1. Oranlar: T = 1 → 1.0; T = 2 → 1/1.8 = 0.556; T = 3 → 1/2.44 = 0.41; T = 4 → (1 + 0.512 × 10)/2.952 = **2.0732**; sonrasında azalır. İndeks 2.0732, en iyi durma zamanı **T = 4**.
2. | (s, f) | tahmin | Gittins | keşif bonusu |
   |---|---|---|---|
   | (2, 1) | 0.6667 | 0.8001 | 0.133 |
   | (4, 2) | 0.6667 | 0.7539 | 0.087 |
   | (8, 4) | 0.6667 | 0.7187 | 0.052 |
   | (16, 8) | 0.6667 | 0.6957 | 0.029 |

   Tahmin aynı ama bonus deneme sayısı arttıkça küçülür: Çok denenmiş bir kol hakkında öğrenilecek az şey kalmıştır. Sonsuz denemede indeks tahmine eşit olur.

## A9 — 4 × 3 POMDP'de inanç

Komşu duvar sayısı: (3,1), (3,2), (3,3) için 1, diğer yedi durum için 2 (engel (2,2) ve ızgara kenarı duvar sayılır; uç durum (4,2) duvar değildir).

1. Sol sonrası (algılamadan önce) olasılıklar: (3,1) ve (3,2) her biri 1/9, (3,3) 0.2/9 vb. "1 duvar" gözlemiyle: **(3,1) = (3,2) = 0.340**, (3,3), (1,3), (1,1) 0.068, diğerleri daha az. (3,1) ile (3,2) eşittir: (3,2)'deki kütle Sol ile duvara çarpıp yerinde kalır, (3,1)'e ise (4,1)'den gelir; ikisi de 1/9.
2. "Yalnızca güneyde duvar" gözlemiyle: **(3,1) = 0.689**, (1,1) = 0.138, (2,1) = (2,3) = 0.077. (3,2)'nin duvarı batıda, (3,3)'ünkü kuzeyde olduğundan ikisi de iki bit yanlış okuma gerektirir.
3. Kitabın ifadesi 4 bitlik (yönü bilen) algılayıcı için doğrudur. Yalnızca sayıyı bilen algılayıcıda (3,1) ile (3,2) ayırt edilemez. **Algılayıcı modeli, inancı en az geçiş modeli kadar belirler.**

## A10 — Algılayıcı ne kadar değerli?

| doğruluk | U(0) | U(0.5) | U(0) − U(0.5) |
|---|---|---|---|
| 0.5 | 5.664 | 4.000 | 1.664 |
| 0.6 | 5.737 | 4.661 | 1.076 |
| 0.9 | 6.640 | 6.240 | 0.400 |
| 1.0 | 7.200 | 6.800 | 0.400 |

1. Doğruluk 0.5'te algılayıcı hiçbir şey söylemez. b(B) = 0.5'te iki eylem de inancı 0.5'te bırakır ve her adımda B'ye girme olasılığı 0.5'tir: 8 × 0.5 = **4**.
2. İyi bir algılayıcıyla ajan nerede olduğunu hızla öğrenir; başlangıçtaki belirsizliğin bedeli (U(0) − U(0.5)) 1.66'dan 0.40'a iner. 0.9 ile 1.0 arasında fark kalmaz: İlk adımdan sonra yalnızca hareketin rastlantısallığı kalır. Bu, POMDP'lerde bilginin değerinin doğrudan görünümüdür.
