# Bölüm 22 — Pekiştirmeli öğrenme

> **Kitapta:** AIMA 4. baskı, Bölüm 22 *"Reinforcement Learning"*.
> Önce kitabı oku, sonra bu notlarla pekiştir. Metin özgündür; kitaptan alıntı yoktur.
> Örnekler Bölüm 17'nin 4 × 3 dünyasını ve `mdp.py` kütüphanesini kullanır (ödül geçişe ait, r = −0.04, γ = 1).

## Bu bölümün haritası

| Kitap alt bölümü | Bu nottaki karşılığı | Kod |
|---|---|---|
| 22.1 Learning from Rewards | §1 Ödülden öğrenmek; model tabanlı ve modelsiz ajanlar | — |
| 22.2 Passive Reinforcement Learning | §2 Doğrudan fayda kestirimi, ADP, TD | `pasif_ogrenme.py` |
| 22.3 Active Reinforcement Learning | §3 Keşif, güvenli keşif, Q-öğrenme, SARSA | `aktif_ogrenme.py` |
| 22.4 Generalization in RL | §4 İşlev yaklaşımı, derin RL, ödül şekillendirme, hiyerarşik RL | `yaklasik_ve_politika.py` |
| 22.5 Policy Search | §5 Politika değeri, politika gradyanı, ilişkili örnekleme | `yaklasik_ve_politika.py` |
| 22.6 Apprenticeship and Inverse RL | §6 Taklit öğrenme, ters pekiştirmeli öğrenme | — |
| 22.7 Applications | §7 Oyunlar, robot denetimi | — |

## Öğrenme hedefleri

1. Pekiştirmeli öğrenmeyi denetimli öğrenmeden ayırt etmek; model tabanlı ve modelsiz yaklaşımları karşılaştırmak.
2. Sabit bir politikanın faydalarını doğrudan kestirim, ADP ve TD ile öğrenmek.
3. Keşif–sömürü dengesini, keşif fonksiyonlarını ve GLIE'yi açıklamak.
4. Q-öğrenme ve SARSA güncellemelerini yazmak ve farkını açıklamak.
5. İşlev yaklaşımıyla genellemeyi ve politika araması yöntemlerini tanımak.
6. Taklit öğrenme ve ters pekiştirmeli öğrenmenin ne zaman gerektiğini açıklamak.

---

## 1. Ödülden öğrenmek

Denetimli öğrenmede her durum için doğru eylem söylenir; satrançta bunu sağlayacak bir öğretmen yoktur. Pekiştirmeli öğrenmede ajan dünyayla etkileşir ve ara sıra **ödül** (pekiştirme) alır; amaç beklenen toplam ödülü en büyüklemektir. Ödülü tanımlamak, doğru eylemleri etiketlemekten çoğu zaman çok daha kolaydır. Ödüller **seyrek** olabilir (satrançta yalnızca oyun sonunda); bu öğrenmeyi zorlaştırır.

| Ajan türü | Öğrendiği | Karar |
|---|---|---|
| **Model tabanlı** | Geçiş modeli P(s′\|s, a) (+ ödül) | Modelle planlama (MDP çözme) |
| **Modelsiz: eylem–fayda** | Q(s, a) | argmax_a Q(s, a) |
| **Modelsiz: refleks / politika araması** | π(s) doğrudan | π(s) |

**Pasif öğrenme:** Politika sabit, faydalar öğrenilir. **Aktif öğrenme:** Ne yapacağını da öğrenmek zorunda; keşif gerekir.

---

## 2. Pasif pekiştirmeli öğrenme (`pasif_ogrenme.py`)

Ajan politikası π ile **denemeler** yapar; her deneme (1,1)'den başlayıp bir uç duruma varana kadar sürer. Geçiş modelini ve ödül fonksiyonunu bilmez. Hedef U^π(s) = E[Σ γᵗ R(Sₜ, π(Sₜ), Sₜ₊₁)].

Kitaptaki üç deneme (ödüller her geçişte −0.04, uca girişte ±1):

```text
(1,1)→(1,2)→(1,3)→(1,2)→(1,3)→(2,3)→(3,3)→(4,3)   +1
(1,1)→(1,2)→(1,3)→(2,3)→(3,3)→(3,2)→(3,3)→(4,3)   +1
(1,1)→(1,2)→(1,3)→(2,3)→(3,3)→(3,2)→(4,2)         −1
```

### 2.1 Doğrudan fayda kestirimi

Bir durumun faydası = o noktadan sonra beklenen toplam ödül (**ödül-kalan**). Her deneme ziyaret edilen her durum için bir örnek verir. 1. denemede (1,1) için 0.76; (1,2) için 0.80 ve 0.88; (1,3) için 0.84 ve 0.92. Sonsuz denemede örnek ortalaması doğru değere yakınsar.

Sorun: Bellman denklemlerini, yani durumların faydaları arasındaki bağı **görmezden gelir**. 2. denemede (3,2) ilk kez görülür ve hemen ardından yüksek faydalı (3,3)'e gidilir; ama yöntem deneme bitene kadar hiçbir şey öğrenmez. Gereğinden büyük bir hipotez uzayında arama yapar; **çok yavaş yakınsar**.

### 2.2 Uyarlamalı dinamik programlama (ADP)

Geçiş modelini sayımlarla öğren (tam gözlenebilir ortamda kolay), sonra sabit politika için Bellman denklemlerini (doğrusal) çöz ya da değiştirilmiş politika yinelemesiyle güncelle:

```text
U(s) = Σ_s′ P̂(s′ | s, π(s)) [R(s, π(s), s′) + γ U(s′)]           (22.2)
```

Üç denemeden: (3,3)'te Sağ dört kez yapılmış, ikisinde (4,3), ikisinde (3,2) → P̂ = 1/2. ADP en verimli yöntemdir (veri açısından); büyük durum uzaylarında (tavla ~10²⁰ durum) denklemleri çözmek imkânsızdır.

### 2.3 Zamansal fark (TD) öğrenmesi

Modeli öğrenmeden, gözlenen her geçişte tahmini ardılıyla uyumlu hâle getir:

```text
U^π(s) ← U^π(s) + α [R(s, π(s), s′) + γ U^π(s′) − U^π(s)]          (22.3)
```

Köşeli parantez bir **hata** terimidir (Bölüm 19'daki güncellemelere benzer). Kitaptaki örnek: 1. denemeden sonra U(1,3) = 0.84, U(2,3) = 0.96; (1,3) → (2,3) geçişi hedefi −0.04 + 0.96 = 0.92 yapar ve U(1,3)'ü yukarı çeker. Nadir geçişler nadiren gözlendiği için ortalamada doğru değere gider; α ziyaret sayısıyla uygun biçimde azalırsa (kitapta α(n) = 60/(59 + n)) yakınsar.

**TD ile ADP'nin farkı:** TD gözlenen tek ardılı kullanır ve geçiş başına bir düzeltme yapar; ADP bütün ardılların olasılıklarını kullanır ve tutarlılık için gerektiği kadar düzeltme yapar. TD, ADP'nin kaba ama ucuz bir yaklaşımı gibidir; daha çok gürültülüdür ve daha yavaş öğrenir. Arada **öncelikli süpürme** gibi yöntemler: yalnızca büyük değişiklik bekleyen durumları güncellemek.

Kodumuzda en iyi politika (3,1) ve (4,1)'e hiç gitmediği için pasif ajan bu durumları öğrenemez; az ziyaret edilen (3,2) gibi durumlarda bütün yöntemlerin hatası büyüktür, TD en gürültülüsüdür.

---

## 3. Aktif pekiştirmeli öğrenme (`aktif_ogrenme.py`)

Ajan ne yapacağına kendisi karar verir. Tam bir model (bütün eylemler için) öğrenmeli ve en iyi faydaları bulmalı:

```text
U(s) = max_a Σ_s′ P(s′ | s, a) [R(s, a, s′) + γ U(s′)]                (22.4)
```

### 3.1 Keşif

**Açgözlü ajan** öğrendiği modele göre en iyi eylemi seçer. Kitapta 8 denemede, kaybı 0.235 olan alt-en iyi bir politikaya yakınsar ve bir daha hiç değişmez: Eylemler yalnızca ödül getirmez, **bilgi** de getirir. Öğrenilen model gerçek dünya değildir. Kodumuzda da açgözlü ADP kötü bir politikaya takılır.

**Keşif–sömürü:** Bölüm 17'deki haydut problemlerinin genellemesi. **GLIE** (sonsuz keşifte sınırda açgözlü): Her durumda her eylemi sınırsız kez dene, ama zamanla açgözlüleş. Basit örnek: t. adımda 1/t olasılıkla rastgele eylem.

**Keşif fonksiyonu:** İyimser fayda U⁺ ile

```text
U⁺(s) ← max_a f( Σ_s′ P(s′|s,a)[R(s,a,s′) + γ U⁺(s′)],  N(s, a) )     (22.5)
f(u, n) = R⁺ eğer n < Nₑ, yoksa u
```

Kitapta R⁺ = 2, Nₑ = 5. Sağ tarafta U değil **U⁺** olması önemlidir: Keşfin yararı keşfedilmemiş bölgelerin kenarından geriye yayılır; keşfedilmemiş bölgelere giden eylemler de çekici olur. Keşifçi ADP hızla sıfır politika kaybına yaklaşır (kodumuzda 50 denemede ~0.013).

### 3.2 Güvenli keşif

Benzetimde kaza "sıfırla" düğmesiyle biter; gerçek dünyada ise birçok eylem **geri döndürülemez** (Bölüm 4.5'teki çevrimiçi arama ajanları gibi) ve en kötü durumda ajan hiçbir eylemin etkisi olmayan emici bir duruma düşer (kitaptaki örnek: yavru ay balığının erişkinliğe kadar yaşama olasılığı ~10⁻⁸). Yaklaşımlar: **Bayesçi pekiştirmeli öğrenme** (olası ortam modelleri üzerinde önsel, beklenen faydayı en büyüklemek) ve **sağlam denetim** (makul modellerin en kötüsünde en iyi politika); ayrıca gösterimlerden başlamak.

### 3.3 Zamansal fark Q-öğrenme

Model öğrenmeden Q(s, a)'yı öğren; karar için ileri bakmaya gerek yok:

```text
Q(s, a) ← Q(s, a) + α [R(s, a, s′) + γ max_a′ Q(s′, a′) − Q(s, a)]     (22.7)
```

**SARSA** (durum, eylem, ödül, durum, eylem): Ardıl durumda **gerçekten seçilen** eylemin Q değeriyle güncelle:

```text
Q(s, a) ← Q(s, a) + α [R(s, a, s′) + γ Q(s′, a′) − Q(s, a)]            (22.8)
```

- Ajan hep açgözlüyse ikisi aynıdır.
- Keşif varken farklıdır: Q-öğrenme **politika dışı** (off-policy) öğrenir; keşif eyleminin kötü sonucu en iyi eylemin değerini etkilemez. SARSA **politikaya bağlıdır** (on-policy): Fiilen izlenen (keşifli) politikanın değerini öğrenir; keşif kötü sonuç verirse eylemi cezalandırır. Keşif politikası denetlenemiyorsa (ör. başka biri kullanıyorsa) Q-öğrenme; politika sabit kalacaksa SARSA daha gerçekçidir.
- Q-öğrenme modelsizdir: Karmaşık ortamlarda bile modeli öğrenmeye gerek yoktur; ama ADP'den daha yavaş öğrenir ve bilgiyi daha az verimli kullanır.

**Bizim gözlemimiz:** Modelsiz Q-öğrenmede her eylemi yalnızca Nₑ = 5 kez denemek yetmeyebilir. α ilk güncellemelerde ~1 olduğundan erken Q tahminleri tek bir gürültülü örneğe bağlıdır; ajan sonra açgözlü davranıp o eylemleri bir daha denemezse yanlış tahminler kalıcı olur (kodumuzda kayıp ~0.47'de takılır). Azalan ε'lu (ε = 1/√t, GLIE) keşifle Q-öğrenme ve SARSA en iyiye yaklaşır. ADP'de bu sorun daha azdır: Model sayımları zamanla iyileşir ve planlama her şeyi yeniden hesaplar.

---

## 4. Pekiştirmeli öğrenmede genelleme (`yaklasik_ve_politika.py`)

Tablo biçimli U ya da Q, gerçek problemlerde imkânsızdır (satranç ~10⁴⁰, tavla ~10²⁰ durum). **İşlev yaklaşımı:** Faydayı az parametreli bir fonksiyonla temsil et; görülmemiş durumlara genelleme sağlar.

**Doğrusal yaklaşım** (22.9): Û_θ(x, y) = θ₀ + θ₁x + θ₂y. Kitap: θ = (0.5, 0.2, 0.1) → Û(1, 1) = 0.8.

**Doğrudan fayda kestirimiyle:** Her deneme (durum, ödül-kalan) örnekleri verir; denetimli öğrenme (en küçük kareler). Çevrimiçi **delta kuralı** (Widrow–Hoff):

```text
θᵢ ← θᵢ + α [uⱼ(s) − Û_θ(s)] ∂Û_θ(s)/∂θᵢ                               (22.10)
```

Kitaptaki örnekte u(1,1) = 0.4 iken Û(1,1) = 0.8: θ₀, θ₁, θ₂ hepsi 0.4α azalır. Tek bir gözlem **bütün** durumların tahminini değiştirir: genelleme budur.

**TD ile:** θᵢ ← θᵢ + α[R(s, a, s′) + γ Û_θ(s′) − Û_θ(s)] ∂Û_θ(s)/∂θᵢ (Q-öğrenme için benzeri). Doğrusal yaklaşımla pasif TD'nin yakınsadığı gösterilmiştir; ama kitap, işlev yaklaşımıyla ıraksama örneklerinin de bulunduğunu not eder.

Özellikler problemi iyi yakalamalıdır: 4 × 3 dünyada (1, x, y) özellikleri −1 durumunun yakınındaki düşüşü yakalayamaz (RMS hata ~0.07); doğru bir ek özellik hatayı azaltır (A8). Hedefe Manhattan uzaklığı bu ızgarada x ve y'nin doğrusal bir birleşimi olduğu için yeni bir şey katmaz.

**Derin pekiştirmeli öğrenme:** Q ya da U için derin ağ (§4.3). DQN, Atari oyunlarında ham piksellerden insan düzeyinde oynadı; AlphaGo ve AlphaZero değer ve politika ağlarını ağaç aramasıyla birleştirdi. Kararsızlık ve aşırı uyma riskleri vardır.

**Ödül şekillendirme:** "İlerleme" için ek **sözde ödüller** (robot topa dokunursa). Dikkat: Ajan sözde ödülü sömürebilir (topa dokunup durmak). Bölüm 17'deki şekillendirme teoremi: Potansiyele dayalı ek ödül (γΦ(s′) − Φ(s)) en iyi politikayı değiştirmez.

**Hiyerarşik pekiştirmeli öğrenme:** Uzun ufuklu görevleri alt görevlere bölmek. Ajan, seçim noktaları öğrenmeyle doldurulacak bir **kısmi programla** başlar; seçim durumları üzerinde bir MDP çözülür. Kitaptaki örnek: robot futbolunda "keepaway" (top saklama).

---

## 5. Politika araması

Politikayı doğrudan parametreleyip iyileştir: π_θ. Yaygın gösterim **softmax**: π_θ(s, a) = e^{β Q̂_θ(s,a)} / Σ_a′ e^{β Q̂_θ(s,a′)}; β büyükse sert max, küçükse rastgele seçime yakın.

- **Politika değeri** ρ(θ): π_θ ile beklenen ödül-kalan. Kapalı biçimi varsa gradyanı izle; yoksa denemelerle değerlendir.
- **Ampirik gradyan:** Her parametreyi biraz değiştirip politika değerinin değişimini ölç (tepe tırmanma). Stokastik ortamda çok deneme gerekir.
- **Politika gradyanı (REINFORCE):** Gradyanı denemelerden doğrudan tahmin et: ∇ρ(θ) ≈ ortalama[G · ∇ log π_θ(s, a)]. Kodumuzda tablo biçimli softmax politika 4 × 3 dünyada birkaç yüz-bin bölümde en iyiye yaklaşır (yüksek varyanslıdır; temel çizgi çıkarmak yardım eder).
- **İlişkili örnekleme:** İki politikayı karşılaştırırken aynı rastgele sayı dizilerini kullan (benzetimde rastgelelik sabitlenir). PEGASUS bu fikirle; ilk tam kararlı otonom helikopter uçuşunu başaran algoritmalardan biri.

---

## 6. Çıraklık ve ters pekiştirmeli öğrenme

Ödül fonksiyonunu yazmak zor olabilir (araba sürmek: güvenlik, hız, konfor, yasalar…). Uzman gösterimlerinden öğrenmek:

- **Taklit öğrenme (davranış klonlama):** Gözlenen (durum, eylem) çiftlerinden denetimli öğrenmeyle π(s). Sorun: Öğretmenin hiç girmediği durumlarda küçük hatalar birikir ve felakete gider; en iyi ihtimalle öğretmeni kopyalar, aşamaz.
- **Ters pekiştirmeli öğrenme (IRL):** Davranıştan **ödül fonksiyonunu** öğren; sonra o ödülle en iyi politikayı bul. Uzmanın "yaklaşık rasyonel" olduğu varsayılır (ör. softmax ile hata yapan bir uzman, Boltzmann rasyonelliği). Ödül özelliklerin doğrusal bir birleşimi ise **özellik eşleştirme**: Öğrenilen politikanın beklenen özellik sayımları uzmanınkiyle eşleşsin.
- IRL, Bölüm 16 ve 18'deki **yardım oyunlarının** bir parçasıdır: İnsanın tercihlerini davranışından öğrenmek.

---

## 7. Uygulamalar

- **Oyunlar:** Samuel'in dama programı, TD-Gammon (tavla, kendi kendine oynayarak), DQN (Atari), AlphaGo / AlphaZero, StarCraft.
- **Robot denetimi:** Ters sarkaç (araba üzerinde direk), helikopter akrobasisi, yürüme ve el becerisi. Gerçek robotta deneme pahalı ve tehlikeli: benzetimde öğrenip aktarmak (sim-to-real), gösterimlerden başlamak.

---

## Sık yapılan hatalar

| Yanılgı | Doğrusu |
|---|---|
| "Pekiştirmeli öğrenme, etiketsiz denetimli öğrenmedir." | Geri bildirim seyrek ve gecikmeli bir ödüldür; hangi eylemin ödülü getirdiği (kredi ataması) bilinmez. |
| "Doğrudan fayda kestirimi Bellman denklemini kullanır." | Kullanmaz; bu yüzden yavaştır. ADP ve TD kullanır. |
| "TD, geçiş modelini öğrenir." | Modelsizdir; yalnızca gözlenen ardılı kullanır. |
| "En iyi bilinen eylemi her zaman seçmek en iyisidir." | Açgözlü ajan keşfetmediği için kötü politikalara takılır. |
| "Q-öğrenme ile SARSA aynıdır." | Keşif varken farklıdır: Q-öğrenme politika dışı, SARSA politikaya bağlı. |
| "Her eylemi birkaç kez denemek yeter." | Modelsiz yöntemlerde gürültülü erken tahminler kalıcı olabilir; GLIE tarzı sürekli keşif gerekir. |
| "Sözde ödül eklemek her zaman yardım eder." | Ajan sözde ödülü sömürebilir; potansiyele dayalı şekillendirme güvenlidir. |
| "Taklit öğrenme uzmanı aşar." | En iyi ihtimalle kopyalar; IRL ödülü öğrenip daha iyisini bulabilir. |

## Kendini yokla

1. Pasif ve aktif pekiştirmeli öğrenme arasındaki fark nedir?
2. Kitabın ilk denemesinde (1,1), (1,2), (1,3) için ödül-kalan örnekleri nelerdir?
3. Doğrudan fayda kestirimi neden yavaş yakınsar?
4. TD güncellemesini yaz. ADP'den farkı nedir?
5. Açgözlü ajan neden kötü bir politikaya takılabilir? GLIE nedir?
6. Keşif fonksiyonunda neden U değil U⁺ kullanılır?
7. Q-öğrenme ve SARSA güncellemelerini yaz; hangisi politika dışıdır?
8. Doğrusal işlev yaklaşımında tek bir gözlem neden bütün durumların tahminini değiştirir?
9. Politika araması nedir? Softmax politika neden kullanılır?
10. Taklit öğrenme ile ters pekiştirmeli öğrenme arasındaki fark nedir?

## Kod rehberi

```bash
python ornekler/pasif_ogrenme.py        # kitabın üç denemesi: doğrudan kestirim, ADP, TD; benzetimle karşılaştırma
python ornekler/aktif_ogrenme.py        # açgözlü vs keşifçi ADP, Q-öğrenme (Nₑ vs GLIE), SARSA
python ornekler/yaklasik_ve_politika.py # doğrusal işlev yaklaşımı, delta kuralı, TD + yaklaşım, REINFORCE
python cozumler/alistirma_kod.py        # A2, A3, A6, A8, A9
```

## Terimler

| Türkçe | İngilizce | Kısa açıklama |
|---|---|---|
| pekiştirmeli öğrenme | reinforcement learning | Ödüllerden öğrenme |
| ödül / pekiştirme | reward / reinforcement | Ortamın sayısal geri bildirimi |
| seyrek ödül | sparse reward | Nadiren gelen ödül |
| model tabanlı / modelsiz | model-based / model-free | Geçiş modeli öğrenilir / öğrenilmez |
| eylem–fayda öğrenme | action-utility learning | Q-fonksiyonunu öğrenmek |
| pasif / aktif öğrenme | passive / active learning | Sabit politika / politika da öğrenilir |
| deneme | trial | Başlangıçtan uca bir bölüm |
| doğrudan fayda kestirimi | direct utility estimation | Ödül-kalan ortalaması |
| ödül-kalan | reward-to-go | Bir noktadan sonraki toplam ödül |
| uyarlamalı dinamik programlama | adaptive dynamic programming (ADP) | Modeli öğren, MDP'yi çöz |
| zamansal fark öğrenmesi | temporal-difference (TD) learning | Ardılla uyum için düzeltme |
| öncelikli süpürme | prioritized sweeping | Büyük değişimli durumları önce güncelleme |
| açgözlü ajan | greedy agent | Hep en iyi bilineni seçen ajan |
| keşif / sömürü | exploration / exploitation | Bilgi toplama / bilineni kullanma |
| GLIE | greedy in the limit of infinite exploration | Sonsuz keşifte sınırda açgözlü |
| keşif fonksiyonu | exploration function | f(u, n): iyimserlik |
| güvenli keşif | safe exploration | Geri dönüşsüz durumlardan kaçınmak |
| Q-öğrenme | Q-learning | Modelsiz, politika dışı TD |
| SARSA | SARSA | Politikaya bağlı TD |
| politika dışı / politikaya bağlı | off-policy / on-policy | Öğrenilen politika ≠ / = izlenen |
| işlev yaklaşımı | function approximation | Faydayı parametreli fonksiyonla temsil |
| delta kuralı | delta rule (Widrow–Hoff) | Çevrimiçi en küçük kareler güncellemesi |
| derin pekiştirmeli öğrenme | deep reinforcement learning | Derin ağla işlev yaklaşımı |
| ödül şekillendirme / sözde ödül | reward shaping / pseudoreward | İlerleme için ek ödül |
| hiyerarşik pekiştirmeli öğrenme | hierarchical reinforcement learning | Alt görevlerle öğrenme |
| kısmi program | partial program | Seçim noktaları öğrenilecek program |
| politika araması | policy search | Politikayı doğrudan iyileştirme |
| politika değeri | policy value | ρ(θ) |
| politika gradyanı | policy gradient | ∇ρ(θ) |
| ampirik gradyan | empirical gradient | Denemelerle sayısal gradyan |
| ilişkili örnekleme | correlated sampling | Aynı rastgelelikle karşılaştırma |
| çıraklık öğrenmesi | apprenticeship learning | Uzmandan öğrenme |
| taklit öğrenme / davranış klonlama | imitation learning / behavioral cloning | Eylemleri denetimli öğrenmek |
| ters pekiştirmeli öğrenme | inverse reinforcement learning (IRL) | Davranıştan ödülü öğrenmek |
| özellik eşleştirme | feature matching | Beklenen özellik sayımlarını eşleştirme |
