# Bölüm 23 — Quiz

Cevaplara bakmadan önce kendin yanıtla. Cevaplar dosyanın sonunda.

---

**S1.** Sözcük torbası modeli neyi yok sayar?

A) Sözcüklerin sıklığını
B) Sözcüklerin sırasını
C) Belgenin sınıfını
D) Sözlüğü

**S2.** Trigram modelinde bir sözcüğün olasılığı neye bağlıdır?

**S3.** Laplace düzeltmesi neyi çözer, zayıflığı nedir?

**S4.** Dil modellerini karşılaştırmak için kullanılan şaşkınlık (perplexity) için hangisi doğrudur?

A) Büyük olması iyidir
B) P(c₁:N)^(−1/N) olarak tanımlanır
C) Yalnızca unigram modelleri için tanımlıdır
D) Olasılıkla ilgisi yoktur

**S5.** "Bağlamdan bağımsız" ne demektir?

**S6.** E₀ için hangisi doğrudur?

A) Yalnızca dilbilgisine uygun cümleleri kabul eder
B) Hem fazla üretir hem eksik üretir
C) Her cümleye tek bir ağaç verir
D) Olasılık kullanmaz

**S7.** CYK algoritmasının zaman karmaşıklığı nedir? Dilbilgisinin hangi biçimde olmasını ister?

**S8.** "the wumpus is dead" cümlesinin E₀'daki olasılığı yaklaşık kaçtır?

A) 0.9
B) 1.35 × 10⁻⁶
C) 0.015
D) 1.0

**S9.** Bir ağaç bankasından PCFG nasıl öğrenilir?

**S10.** Bileşimsel anlambilim ne demektir? "3 + (4 ÷ 2)" ağacının kökü nedir?

**S11.** "Chrysler announced record profits" cümlesinde hangi zorluk vardır?

A) Gösterge sözcük
B) Düz değişmece (metonymy)
C) Niceleme
D) Uzak bağımlılık

**S12.** Bağımlılık dilbilgisi ile öbek yapısı dilbilgisi arasındaki fark nedir?

---

## Cevaplar

**S1.** **B.** Yalnızca hangi sözcüklerin kaç kez geçtiğine bakar.

**S2.** Önceki iki sözcüğe: P(wⱼ | wⱼ₋₂ wⱼ₋₁).

**S3.** Görülmemiş olaylara sıfır olasılık verilmesini önler (sayımları 1'den başlatır). Zayıflığı: Çok sayıda görülmemiş olay varken onlara fazla olasılık kütlesi dağıtır; geri çekilme ve ara değerleme daha iyidir.

**S4.** **B.** Düşük şaşkınlık daha iyi modeldir.

**S5.** Bir kural her bağlamda aynı olasılıkla uygulanır; bir NP cümlenin başında da sonunda da aynı kurallarla üretilir.

**S6.** **B.** "Me go I"yı kabul eder, "I think the wumpus is smelly"yi reddeder.

**S7.** O(n³ m) zaman, O(n² m) uzay. Chomsky normal biçimi: X → Y Z ve X → sözcük.

**S8.** **B.** 0.90 × 0.015 × 0.0001 = 1.35 × 10⁻⁶.

**S9.** Her kuralın ağaç bankasındaki sayısını, sol taraf kategorisinin sayısına böl: P(X → α) = sayı(X → α) / sayı(X).

**S10.** Bir öbeğin anlamı alt öbeklerinin anlamlarının bir fonksiyonudur. Kök Exp(5).

**S11.** **B.** Şirket adı, onun adına konuşan kişiyi ya da sözcüyü temsil eder.

**S12.** Öbek yapısı sözcükleri iç içe öbeklere (NP, VP…) gruplar; bağımlılık dilbilgisi sözcükler arasında doğrudan ikili ilişkiler (özne, nesne…) kurar. Birbirine dönüştürülebilirler; bağımlılıklar sözcük sırası serbest diller için daha doğaldır.
