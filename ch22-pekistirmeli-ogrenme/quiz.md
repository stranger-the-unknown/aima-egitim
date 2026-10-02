# Bölüm 22 — Quiz

Cevaplara bakmadan önce kendin yanıtla. Cevaplar dosyanın sonunda.

---

**S1.** Pekiştirmeli öğrenmeyi denetimli öğrenmeden ayıran temel özellik nedir?

**S2.** Kitabın ilk denemesinde (1,1) için ödül-kalan örneği kaçtır?

A) 0.64
B) 0.76
C) 0.80
D) 1.00

**S3.** Doğrudan fayda kestirimi neden yavaş yakınsar?

**S4.** Hangi yöntem geçiş modelini öğrenir?

A) TD öğrenmesi
B) Q-öğrenme
C) ADP
D) SARSA

**S5.** TD güncellemesini yaz. Neden modelsizdir?

**S6.** Açgözlü bir ADP ajanının sorunu nedir?

**S7.** Keşif fonksiyonu f(u, n) için kitaptaki örnek değerler nelerdir?

A) R⁺ = 1, Nₑ = 1
B) R⁺ = 2, Nₑ = 5
C) R⁺ = 10, Nₑ = 100
D) R⁺ = 0, Nₑ = 5

**S8.** Q-öğrenme ile SARSA arasındaki fark nedir?

**S9.** Hangisi politika dışı (off-policy) bir yöntemdir?

A) SARSA
B) Q-öğrenme
C) Pasif TD
D) Doğrudan fayda kestirimi

**S10.** Doğrusal işlev yaklaşımında θ = (0.5, 0.2, 0.1) ise Û(1, 1) kaçtır? Tek bir gözlem neden diğer durumları da etkiler?

**S11.** Politika araması nedir? Politika gradyanının yüksek varyansı nasıl azaltılabilir?

**S12.** Ters pekiştirmeli öğrenme neyi öğrenir ve taklit öğrenmeden neden daha güçlü olabilir?

---

## Cevaplar

**S1.** Doğru eylem söylenmez; ajan yalnızca (çoğu zaman seyrek ve gecikmeli) ödül alır ve hangi eylemlerin ödülden sorumlu olduğunu kendisi çıkarmak zorundadır.

**S2.** **B.** 6 × (−0.04) + 1 = 0.76.

**S3.** Durumların faydaları arasındaki Bellman bağlarını kullanmaz; her durumu bağımsız bir ortalama olarak öğrenir ve bilgiyi ancak deneme bitince günceller.

**S4.** **C.** ADP geçiş olasılıklarını sayımlarla öğrenir ve MDP'yi çözer.

**S5.** U(s) ← U(s) + α[R(s, π(s), s′) + γU(s′) − U(s)]. Yalnızca gözlenen ardılı kullanır; P(s′|s, a) hiçbir yerde geçmez.

**S6.** Öğrendiği (yanlış olabilen) modele göre en iyiyi seçer, başka eylemleri denemez; bu yüzden alt-en iyi bir politikaya takılabilir (kitapta kayıp 0.235).

**S7.** **B.** f(u, n) = R⁺ eğer n < Nₑ, yoksa u.

**S8.** Q-öğrenme ardıldaki en iyi eylemin değerini (max) kullanır; SARSA gerçekten seçilen eylemin değerini kullanır. Keşif varken Q-öğrenme açgözlü politikanın, SARSA izlenen politikanın değerini öğrenir.

**S9.** **B.**

**S10.** 0.5 + 0.2 + 0.1 = 0.8. Parametreler bütün durumlarca paylaşılır; bir gözlem θ'yı değiştirince her durumun tahmini değişir (genelleme).

**S11.** Politikayı doğrudan parametreleyip politika değerini (beklenen ödülü) en büyükleyecek biçimde iyileştirmek. Varyans: getiriden temel çizgi çıkarmak, çok bölümün ortalaması, ilişkili örnekleme (aynı rastgelelik), değer fonksiyonuyla birleştirmek (aktör–eleştirmen).

**S12.** Uzmanın davranışını açıklayan ödül fonksiyonunu öğrenir. Ödül, görülmemiş durumlara da uygulanabilir ve onunla planlama yaparak uzmanın hatalarını tekrarlamadan daha iyi politikalar bulunabilir; taklit öğrenme en iyi ihtimalle uzmanı kopyalar ve görülmemiş durumlarda hata biriktirir.
