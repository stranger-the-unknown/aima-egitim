# Bölüm 20 — Quiz

Cevaplara bakmadan önce kendin yanıtla. Cevaplar dosyanın sonunda.

---

**S1.** Bayesçi tahmin ile MAP tahmini arasındaki fark nedir?

**S2.** Şeker örneğinde (önsel ⟨0.1, 0.2, 0.4, 0.2, 0.1⟩) bir limonlu şekerden sonra P(sonraki limon) kaçtır?

A) 0.50
B) 0.65
C) 0.75
D) 1.00

**S3.** Düzgün önselde MAP hipotezi neye indirgenir?

A) En basit hipoteze
B) En büyük olabilirlik hipotezine
C) Bayesçi ortalamaya
D) Rastgele bir hipoteze

**S4.** N şekerden c'si kiraz ise θ'nın ML tahmini nedir? Tek bir kiraz şeker görülünce bu tahmin neden sorunludur?

**S5.** Beta(a, b) önselinde bir kiraz şeker gözlenince sonsal nedir?

A) Beta(a, b + 1)
B) Beta(a + 1, b)
C) Beta(a + 1, b + 1)
D) Artık bir Beta dağılımı değildir

**S6.** Gauss gürültülü doğrusal–Gauss modelde en büyük olabilirlik neden en küçük karelere eşittir?

**S7.** Aşağıdakilerden hangisi bir üretici modeldir?

A) Lojistik regresyon
B) Destek vektör makinesi
C) Karar ağacı
D) Naif Bayes

**S8.** Naif Bayes'in olasılıkları neden çoğu zaman aşırı emindir?

**S9.** Gauss karışımında EM'in E ve M adımları ne yapar?

**S10.** EM algoritması için aşağıdakilerden hangisi **doğrudur**?

A) Her zaman global en büyük olabilirliği bulur
B) Her yinelemede log olabilirliği azaltmaz
C) Gizli değişkenlerin etiketlerini kesin olarak belirler
D) Başlangıç noktasından bağımsızdır

**S11.** Kitaptaki kalp hastalığı örneğinde gizli değişken çıkarılınca parametre sayısı ne olur?

A) 78'den 54'e düşer
B) Değişmez
C) 78'den 708'e çıkar
D) 708'den 78'e düşer

**S12.** Tanımlanabilirlik nedir? İki nitelikli karışmış torba modeli neden tanımlanamaz?

---

## Cevaplar

**S1.** Bayesçi tahmin bütün hipotezlerin tahminlerini sonsal olasılıklarıyla ağırlıklandırıp ortalar; MAP yalnızca en olası tek hipotezi kullanır. Az veride MAP çok daha aşırı tahminler yapabilir (3 limondan sonra 1.0, Bayesçi ≈ 0.8).

**S2.** **B.** Sonsal (0, 0.1, 0.4, 0.3, 0.2); P(limon) = 0.1·0.25 + 0.4·0.5 + 0.3·0.75 + 0.2·1 = 0.65.

**S3.** **B.** P(h) sabitse P(d | h) P(h)'yi en büyüklemek P(d | h)'yi en büyüklemektir.

**S4.** θ = c/N. Tek kirazdan sonra θ = 1: "Bu torbada hiç limon yok" der; görülmemiş olaya sıfır olasılık verir. Önsel (Beta) ya da sayımları 1'den başlatmak gerekir.

**S5.** **B.** Beta, Boolean gözlemler için eşlenik önseldir; kiraz a'yı, limon b'yi bir artırır.

**S6.** Log olabilirlikte θ'lara bağlı tek terim −(y − (θ₁x + θ₂))²/(2σ²)'dir; bunu en büyüklemek kare hatayı en küçüklemektir.

**S7.** **D.** Naif Bayes P(sınıf) ve P(nitelikler | sınıf)'ı modeller; örnek üretebilir. Diğerleri doğrudan P(sınıf | nitelikler) ya da sınırı öğrenir.

**S8.** Nitelikleri sınıf verildiğinde bağımsız varsayar. Gerçekte ilişkili nitelikler aynı kanıtı birden çok kez sayar ve çarpım olasılıkları 0 ya da 1'e iter.

**S9.** E: Her noktanın her bileşene ait olma olasılığını (sorumluluk pᵢⱼ) hesaplar. M: Bu olasılıklarla ağırlıklı ortalama, kovaryans ve bileşen ağırlıklarını yeniden hesaplar.

**S10.** **B.** EM log olabilirliği hiçbir yinelemede azaltmaz; ama yerel en büyüğe varır, başlangıca bağlıdır ve gizli değişkenlerin etiketleri (hangi torba "1") tanımlanamaz.

**S11.** **C.** Gizli HeartDisease olmadan belirtiler birbirine ve bütün etkenlere bağlanmak zorunda kalır.

**S12.** Parametrelerin gözlenen verinin dağılımından tek biçimde belirlenebilmesi. İki nitelikte 5 parametre var ama gözlem dağılımında yalnızca 2² − 1 = 3 bağımsız sayı: Sonsuz sayıda farklı parametre aynı dağılımı verir.
