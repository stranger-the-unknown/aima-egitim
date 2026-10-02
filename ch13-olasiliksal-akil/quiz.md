# Bölüm 13 — Quiz

Cevaplara bakmadan önce kendin yanıtla. Cevaplar dosyanın sonunda.

---

**S1.** Bir Bayes ağının üç bileşeni nedir?

**S2.** Hırsız ağında P(j, m, a, ¬b, ¬e) nasıl hesaplanır?

A) P(j) P(m) P(a) P(¬b) P(¬e)
B) P(j | a) P(m | a) P(a | ¬b, ¬e) P(¬b) P(¬e)
C) P(j, m | a) P(a)
D) P(a | j, m) P(¬b | a) P(¬e | a)

**S3.** Her düğümün en fazla k Boole ebeveyni olan n düğümlü bir ağ kaç sayıyla tanımlanır? Tam ortak tablo kaç sayı ister?

**S4.** Hırsız ağı M, J, E, B, A sırasıyla kurulursa kaç parametre gerekir?

A) 10
B) 13
C) 20
D) 31

**S5.** Burglary'nin Markov örtüsü hangisidir?

A) {Alarm}
B) {Alarm, JohnCalls, MaryCalls}
C) {Alarm, Earthquake}
D) {Earthquake}

**S6.** Burglary ile Earthquake koşulsuz bağımsızdır. Alarm verildiğinde de bağımsız mıdırlar? Neden?

**S7.** Gürültülü-VEYA modelinde q_cold = 0.6, q_flu = 0.2 ise P(fever | cold, flu, ¬malaria) nedir?

A) 0.12
B) 0.8
C) 0.88
D) 0.4

**S8.** Hırsız ağında P(Burglary | johnCalls, maryCalls) yaklaşık kaçtır? Neden bu kadar düşük?

**S9.** Değişken eleme numaralandırmadan neden daha hızlıdır? Hangi değişkenler hesaba hiç girmez?

**S10.** Bayes ağında kesin çıkarım genel olarak hangi karmaşıklıktadır? Hangi ağ türünde doğrusal zamanlıdır?

**S11.** Kanıt olasılığı çok küçükse hangi örnekleme yöntemi en çok zarar görür?

A) Olabilirlik ağırlıklandırma
B) Gibbs örneklemesi
C) Doğrudan örnekleme ile P(e)'yi tahmin etmek
D) Ret örneklemesi

**S12.** Yağmurlama ağında P(Rain | Sprinkler = true) = 0.3 iken P(Rain | do(Sprinkler = true)) nedir? Neden farklı?

---

## Cevaplar

1. (1) Rastgele değişkenlere karşılık gelen düğümler, (2) döngüsüz yönlü bağlar (DAG), (3) her düğüm için P(Xᵢ | Ebeveynler(Xᵢ)) koşullu olasılık tablosu.
2. **B.** Ortak olasılık, her değişkenin ebeveynleri verildiğindeki olasılıklarının çarpımıdır: 0.90 × 0.70 × 0.001 × 0.999 × 0.998 ≈ 0.000628.
3. Ağ: en fazla n · 2ᵏ. Tam tablo: 2ⁿ (bağımsız sayı olarak 2ⁿ − 1). n = 30, k = 5 için 960'a karşı bir milyardan fazla.
4. **D.** Bu kötü sırada her düğüm bütün öncüllerine bağlanmak zorunda kalır: 1 + 2 + 4 + 8 + 16 = 31, tam tablo kadar.
5. **C.** Ebeveyni yok, çocuğu Alarm, Alarm'ın diğer ebeveyni Earthquake.
6. Hayır. Alarm ortak çocukları. Alarm gözlenince iki neden rakip açıklamalar hâline gelir: Birini öğrenmek diğerinin olasılığını değiştirir (açıklayıp götürme). d-ayrımda ahlaki grafik Burglary ile Earthquake'i birleştirir.
7. **C.** P(¬fever) = 0.6 × 0.2 = 0.12, P(fever) = 0.88.
8. Yaklaşık **0.284**. Önsel olasılık çok küçük (0.001). İki komşunun da yanlış alarm ya da karıştırma yüzünden araması, gerçek bir hırsızlıktan daha olası kalır.
9. Numaralandırma aynı alt ifadeleri (P(j | a) P(m | a) gibi) tekrar tekrar hesaplar. Değişken eleme ara sonuçları faktör olarak saklar. Sorgunun ya da kanıtın **atası olmayan** değişkenler ilgisizdir, hesaba hiç girmez.
10. NP-zor (hatta #P-zor): 3-SAT bir Bayes ağına indirgenebilir. Tekil bağlı ağlarda (çok ağaçlar) ağın boyutunda doğrusaldır.
11. **D.** Kanıtla uyuşmayan örnekler atıldığı için kabul edilen örnek sayısı P(e) ile orantılı düşer.
12. **0.5** (= P(Rain)). Yağmurlamanın açık olduğunu **görmek**, havanın bulutsuz olduğuna kanıttır ve yağmur olasılığını düşürür. Yağmurlamayı **açmak** ise havayı değiştirmez: do(Sprinkler) Sprinkler'a gelen bağı keser, yalnızca Sprinkler'ın torunlarını etkiler.
