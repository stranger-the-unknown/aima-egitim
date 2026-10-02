# Bölüm 17 — Karmaşık kararlar almak

> **Kitapta:** AIMA 4. baskı, Bölüm 17 *"Making Complex Decisions"*.
> Önce kitabı oku, sonra bu notlarla pekiştir. Metin özgündür; kitaptan alıntı yoktur.

## Bu bölümün haritası

| Kitap alt bölümü | Bu nottaki karşılığı | Kod |
|---|---|---|
| 17.1 Sequential Decision Problems | §1 MDP, politika, zaman üzerinden fayda, Bellman denklemi, ödül ölçekleri, DDN | `mdp.py`, `dort_uc_dunya.py` |
| 17.2 Algorithms for MDPs | §2 Değer yinelemesi, politika yinelemesi, LP, çevrimiçi algoritmalar | `deger_yineleme.py`, `politika_yineleme.py` |
| 17.3 Bandit Problems | §3 Gittins indeksi, Bernoulli haydudu, UCB, Thompson, seçim problemleri | `haydut.py` |
| 17.4 Partially Observable MDPs | §4 İnanç durumları, inanç MDP'si | `pomdp.py`, `cozumler/alistirma_kod.py` (A9) |
| 17.5 Algorithms for Solving POMDPs | §5 Koşullu planlarla değer yinelemesi, çevrimiçi POMDP ajanları | `pomdp.py` |

## Öğrenme hedefleri

1. Bir sıralı karar problemini MDP olarak tanımlamak (durumlar, eylemler, geçiş modeli, ödül).
2. İndirimli toplamsal ödülü ve neden kullanıldığını açıklamak.
3. Bellman denklemini yazmak; değer yinelemesi ve politika yinelemesiyle çözmek.
4. Değer yinelemesinin neden yakınsadığını (büzülme) ve hata sınırlarını yorumlamak.
5. Ödül şekillendirmenin en iyi politikayı neden değiştirmediğini göstermek.
6. Haydut problemlerinde keşif–sömürü dengesini ve Gittins indeksini açıklamak.
7. POMDP'de inanç durumunu güncellemek ve faydanın inanç üzerinde parçalı doğrusal ve dışbükey olduğunu göstermek.

---

## Büyük resim

Bölüm 16'daki kararlar **tek seferlikti**. Burada ajanın faydası bir **eylem dizisine** bağlıdır: Bugünkü eylem yarın hangi durumda olacağını, dolayısıyla yarınki seçenekleri belirler.

| | Belirlenimci | Stokastik |
|---|---|---|
| Tam gözlemlenebilir | Arama (Bölüm 3) | **MDP** (§1–2) |
| Kısmen gözlemlenebilir | Duyarsız / koşullu planlama (Bölüm 4, 11) | **POMDP** (§4–5) |

---

## 1. Sıralı karar problemleri (`mdp.py`, `dort_uc_dunya.py`)

### 1.1 4 × 3 dünya

Kitabın koşu örneği: 4 sütun × 3 satırlık ızgara, (2, 2) duvar, (4, 3) = +1 ve (4, 2) = −1 uç durumlar, başlangıç (1, 1). Eylemler: Yukarı, Aşağı, Sol, Sağ.

- **Geçiş modeli:** Eylem 0.8 olasılıkla istenen yöne, 0.1'er olasılıkla **dik** yönlere gider. Duvara çarpan yerinde kalır.
- **Ödül:** Uç durumlara giren geçişler +1 ve −1; diğer bütün geçişler **r = −0.04**. Negatif ödül ajanı acele etmeye iter.

Belirlenimci olsaydı [Yukarı, Yukarı, Sağ, Sağ, Sağ] yeterdi. Stokastik dünyada bu dizi hedefe yalnızca 0.8⁵ = 0.32768 olasılıkla, öbür yoldan şans eseri 0.1⁴ × 0.8 olasılıkla ulaşır: toplam **0.32776**. Sabit bir dizi işe yaramaz.

**Dikkat (4. baskı):** Ödül **geçişe** aittir, R(s, a, s′). Eski baskılarda ödül duruma aitti, R(s); bu yüzden eski baskıdaki faydalar (0.812, 0.868, …) 4. baskıdakilerden farklıdır. Uç durumların faydası 0'dır; ödülleri yalnızca **girişte bir kez** alınır. (Bu deponun ilk sürümündeki değer yinelemesi kodu uç ödülünü iki kez sayıyordu; yeni kodda düzeltildi.)

### 1.2 MDP

**Markov karar süreci** (MDP): tam gözlemlenebilir, stokastik, Markov geçişli ve toplamsal ödüllü bir sıralı karar problemi:

- durumlar (başlangıç s₀ ile), her durumda eylemler A(s),
- geçiş modeli P(s′ | s, a) (Markov: yalnızca s'ye bağlı),
- ödül fonksiyonu R(s, a, s′) (±R_max ile sınırlı).

Bir eylem dizisi çözüm olamaz. Çözüm bir **politikadır**: π(s) her durumda ne yapılacağını söyler. **En iyi politika** π*, ortaya çıkan geçmişlerin beklenen faydasını en büyükler. Politika, aslında bir **basit refleks ajanını** tanımlar; ama fayda temelli bir ajanın bilgisinden hesaplanmıştır.

**Risk ile ödül dengesi:** En iyi politika r'ye bağlıdır. Kodumuzla bulunan ve kitapla örtüşen kırılma noktaları:

| r aralığı | Davranış |
|---|---|
| r < −1.6497 | Hayat o kadar acı ki ajan en yakın çıkışa koşar, −1 bile olsa |
| −0.7311 < r < −0.4526 | (2,1), (3,1), (3,2)'den +1'e kısa yol; (4,1)'den doğrudan −1'e |
| −0.0850 < r < −0.0273 | Kitaptaki Şekil 17.2(a): (3,1)'den uzun ama güvenli yol |
| −0.0274 < r < 0 | Hiç risk almaz; (3,2)'de −1'den uzağa, duvara doğru gider |
| r > 0 | Hayat güzel; ajan uç durumlardan kaçar, sonsuz ödül toplar |

r < 0 için **toplam 9** farklı en iyi politika vardır (kitap bunu bir alıştırma olarak sorar; `dort_uc_dunya.py` hepsini bulur).

**Kitaptaki küçük bir pürüz:** Kitap (3,1)'de Sol ile Yukarı'nın "tam olarak eşit" olduğunu, bu yüzden Şekil 17.2(a)'da iki politika bulunduğunu söyler. Şekil 17.3'teki faydalarla hesaplayınca r = −0.04'te Q((3,1), Sol) = 0.6514, Q((3,1), Yukarı) = 0.6325 çıkar: Sol açıkça daha iyidir. İki eylem yalnızca **r ≈ −0.0448**'de eşittir; −0.0850 < r < −0.0448 aralığında Yukarı, −0.0448 < r < −0.0273 aralığında Sol en iyidir. Şekildeki iki politika bu iki alt aralığa aittir.

### 1.3 Zaman üzerinden fayda

**Sonlu ufuk:** N adımdan sonra hiçbir şey önemli değil. Bu durumda en iyi eylem **kalan zamana** bağlıdır: **durağan olmayan** politika. Kitaptaki örnek: (3,1)'den N = 3 kalmışsa Yukarı (risk al), N = 100 ise Sol (güvenli yol). Kodumuza göre geçiş 13 adımda olur (A5).

**Sonsuz ufuk:** Sabit son yok; en iyi politika **durağandır**. (Uç durumlar yine olabilir.)

**İndirimli toplamsal ödül:**

```text
U_h([s₀, a₀, s₁, …]) = R(s₀, a₀, s₁) + γ R(s₁, a₁, s₂) + γ² R(s₂, a₂, s₃) + …,   0 ≤ γ ≤ 1
```

γ = 1 ise saf toplamsal ödül. Neden indirim?

1. **Deneysel:** İnsanlar ve hayvanlar yakın ödülü daha çok önemser.
2. **Ekonomik:** Erken gelen para yatırılabilir. γ, (1/γ) − 1 **faiz oranına** denktir: γ = 0.9 → %11.1.
3. **Belirsizlik:** Her adımda 1 − γ olasılıkla dünyanın "bitmesi" gibi düşünülebilir.
4. **Durağan tercihler:** "Yarından başlayan bir geleceği ötekine tercih ediyorsan, bugünden başlasa da tercih et." Bu varsayımı sağlayan **tek** fayda biçimi indirimli toplamdır.
5. **Sonsuzluklar:** γ < 1 ve ödüller sınırlıysa her geçmişin faydası sonludur: `U_h ≤ R_max / (1 − γ)`.

Sonsuzluklara diğer çözümler: **Uygun (proper) politikalar** (bir uç duruma varmak garanti; γ = 1 kullanılabilir; r > 0'daki politika uygun değildir) ve **adım başına ortalama ödül**.

### 1.4 En iyi politika ve durumların faydası

```text
U^π(s) = E[ Σ_t γ^t R(S_t, π(S_t), S_{t+1}) ]                (17.2)
```

İndirimli sonsuz ufukta en iyi politika **başlangıç durumundan bağımsızdır**. U(s) = U^{π*}(s), bir durumun **gerçek faydasıdır**.

4 × 3 dünyada (γ = 1, r = −0.04) kitaptaki Şekil 17.3, kodumuzla birebir:

```text
0.8516  0.9078  0.9578    +1
0.8016  (duvar) 0.7003    −1
0.7453  0.6953  0.6514  0.4279
```

**MEU ile eylem seçimi:**

```text
π*(s) = argmax_a Σ_s′ P(s′ | s, a) [R(s, a, s′) + γ U(s′)]    (17.4)
```

**Bellman denklemi** (Bellman, 1957):

```text
U(s) = max_a Σ_s′ P(s′ | s, a) [R(s, a, s′) + γ U(s′)]       (17.5)
```

Bir durumun faydası = bir sonraki geçişin beklenen ödülü + sonraki durumun indirimli faydası (en iyi eylemle). n durum için n denklem; faydalar bunların **tek** çözümüdür.

**Q-fonksiyonu** (eylem–fayda fonksiyonu): `U(s) = max_a Q(s, a)`, `π*(s) = argmax_a Q(s, a)` ve

```text
Q(s, a) = Σ_s′ P(s′ | s, a) [R(s, a, s′) + γ max_a′ Q(s′, a′)]   (17.8)
```

Q-fonksiyonu Bölüm 22'de (pekiştirmeli öğrenme) merkezî olacak.

### 1.5 Ödül ölçekleri ve şekillendirme

- Pozitif afin dönüşüm `R′ = m R + b` (m > 0) en iyi politikayı değiştirmez (Bölüm 16'daki gibi).
- **Şekillendirme teoremi:** Herhangi bir Φ(s) için

```text
R′(s, a, s′) = R(s, a, s′) + γ Φ(s′) − Φ(s)                     (17.9)
```

en iyi politikayı değiştirmez. Kanıt: Q′(s, a) = Q(s, a) − Φ(s), M′'nün Bellman denklemini sağlar; argmax değişmez. Sezgi: γ = 1'de bir yol boyunca eklenen ödüllerin toplamı Φ(B) − Φ(A)'ya iner, her yol aynı miktarda kazanır.

Φ **potansiyel** diye adlandırılır. Yüksek faydalı durumlarda yüksek Φ, ajanı "yokuş yukarı" yönlendirir. Φ = U seçilirse anlık ödüle göre açgözlü politika en iyidir (ama U'yu bilmek gerekir: bedava öğle yemeği yok). Hayvan eğitmenlerinin her doğru adımda verdiği küçük ödül bunun karşılığıdır.

**Dikkat:** Potansiyele dayanmayan bir "yaklaşma ödülü" (hedefe yaklaşınca bonus, uzaklaşınca ceza yok) ajanın **döngüde dönüp bonus toplamasına** yol açabilir (A7). Uç durumlarda Φ = 0 olmalıdır; değilse uç durumlara giriş ödülü bozulur.

### 1.6 MDP'lerin temsili

- Tablo: P ve R için |S|² |A| giriş (4 × 3 dünyada 11² × 4 = 484).
- **Dinamik karar ağları (DDN):** DBN'lere (Bölüm 14) karar, ödül ve fayda düğümleri eklenir. Durum birkaç değişkene ayrışır (**ayrışık temsil**); atomik temsile göre üstel kazanç sağlar. Kitaptaki örnekler: şarj olabilen gezgin robot (konum, hız, şarj durumu, pil seviyesi) ve **Tetris** (7 × 7 × 2²⁰⁰ ≈ 10⁶² durum; her politika eninde sonunda biter, yani uygundur).

---

## 2. MDP algoritmaları

### 2.1 Değer yinelemesi (`deger_yineleme.py`)

Bellman denklemleri doğrusal değildir (max yüzünden). Yinelemeli çözüm, **Bellman güncellemesi**:

```text
U_{i+1}(s) ← max_a Σ_s′ P(s′ | s, a) [R(s, a, s′) + γ U_i(s′)]     (17.10)
```

Bütün durumlar aynı anda güncellenir. Sonsuz kez uygulanırsa tek çözüme yakınsar. Bilgi, yerel güncellemelerle durum uzayında **yayılır**: Hedefe uzak durumlar önce negatif ödül biriktirir, hedefe giden yol bulununca faydaları yükselir.

**Neden yakınsar? Büzülme.** Bellman güncellemesi B, **en büyük norm** (‖U‖ = max_s |U(s)|) altında γ çarpanlı bir büzülmedir:

```text
‖B U − B U′‖ ≤ γ ‖U − U′‖                                     (17.11)
```

Büzülmenin tek bir sabit noktası vardır ve tekrarlanan uygulama oraya üstel hızla gider. Hata her adımda en az γ katına iner.

| Sonuç | Formül |
|---|---|
| ε hatası için yeterli yineleme | N = ⌈log(2 R_max / (ε(1 − γ))) / log(1/γ)⌉ |
| Durma koşulu | ‖U_{i+1} − U_i‖ < ε(1 − γ)/γ ⇒ ‖U_{i+1} − U‖ < ε (17.12) |
| Politika kaybı | ‖U_i − U‖ < ε ⇒ ‖U^{π_i} − U‖ < 2ε (17.13) |

N, ε'a az bağlıdır ama γ → 1 iken hızla büyür (γ = 0.99'da yüzlerce, 0.999'da binlerce yineleme). Küçük γ hızlıdır ama ajanı **kısa görüşlü** yapar.

**Politika, faydalardan çok önce doğru olur:** 4 × 3 dünyada γ = 0.9 ile politika 3. güncellemede en iyi olur; faydalardaki en büyük hata 4. güncellemede bile ~0.51'dir (kitap aynı gözlemi U₀'ı da sayarak "i = 5" diye verir).

### 2.2 Politika yinelemesi (`politika_yineleme.py`)

Bir π₀'dan başlayıp iki adımı tekrarla:

1. **Politika değerlendirme:** U_i = U^{π_i}. Politika sabitken max kalkar, denklemler **doğrusaldır**:
   `U_i(s) = Σ_s′ P(s′ | s, π_i(s)) [R(s, π_i(s), s′) + γ U_i(s′)]` (17.14). n denklem O(n³)'te tam çözülür.
2. **Politika iyileştirme:** U_i'ye göre tek adım ileri bakan MEU politikası π_{i+1}.

İyileştirme hiçbir şeyi değiştirmeyince durur; U_i Bellman güncellemesinin sabit noktasıdır, π_i en iyidir. Sonlu sayıda politika olduğu ve her adım iyileştirdiği için sonlu adımda biter. Pratikte genellikle çok az yineleme yeter (4 × 3 dünyada 3–6).

**Değiştirilmiş politika yinelemesi:** Tam çözüm yerine k basit (max'sız) Bellman güncellemesi. Büyük durum uzaylarında O(n³)'ten kaçınır.

**Eşzamansız politika yinelemesi:** Her adımda **herhangi bir alt kümeyi** güncelle (iyileştirme ya da değerlendirme). Belli koşullarla yine en iyiye yakınsar; iyi bir politikanın gerçekten ulaşacağı durumlara odaklanmayı sağlar.

### 2.3 Doğrusal programlama

Değişkenler U(s); her s ve a için `U(s) ≥ Σ_s′ P(s′|s,a)[R + γU(s′)]` kısıtlarıyla Σ U(s)'yi en küçükle. LP polinom zamanda çözüldüğü için MDP'ler de durum ve eylem sayısında polinom zamanda çözülür. Pratikte LP çözücüler dinamik programlamadan genellikle yavaştır; durum sayısı da zaten çok büyüktür.

### 2.4 Çevrimiçi algoritmalar

Tetris gibi 10⁶² durumlu problemlerde çevrim dışı çözüm imkânsız. Her karar anında hesap yapılır (Bölüm 5'teki oyun ağaçları gibi):

- **Beklenti-maks** (expectimax): Maks ve şans düğümleri sırayla; yapraklarda değerlendirme fonksiyonu. 4 × 3 dünyada (3,2)'den derinlik 1'de ajan güvenli ama yararsız Sol'u seçer; derinlik 2'den itibaren doğru eylem Yukarı'yı bulur.
- **ε-ufku:** Hata ε'dan küçük kalsın diye gereken derinlik `H = ⌈log_γ(ε(1 − γ)/R_max)⌉`. Kitap: γ = 0.5, ε = 0.1, R_max = 1 → H = **5**; γ = 0.9 → H = **44**.
- **Şans düğümlerinde örnekleme:** Dallanma çok büyükse N örnekle ortalama al.
- **Gerçek zamanlı dinamik programlama (RTDP):** Ağaç aslında bir graftır (aynı durum tekrar gelir); keşfedilen alt MDP'yi Bellman denklemleriyle çöz. LRTA*'ya (Bölüm 4) benzer.
- **UCT** (Bölüm 5'teki MCTS) aslında MDP'ler için geliştirildi. 4 × 3 dünyada pek parlak değil: Kitaba göre toplam 0.4 ödüle ulaşmak için hamle başına ortalama 160 deneme gerekir, en iyi politika ise başlangıçtan 0.7453 alır. Neden: Ağaç kurar (graf değil) ve dünya çok "döngülü"dür. Tetris'te daha iyi çalışır.

---

## 3. Haydut problemleri (`haydut.py`)

**n kollu haydut:** n kolu olan bir kumar makinesi; her kolun arkasında bilinmeyen bir ödül dağılımı var. Her adımda bir kol çekilir. **Sömürü** (şimdiye kadarki en iyi kol) ile **keşif** (az bilinen kollar) arasındaki temel denge. Uygulamalar: yeni tedaviler, yatırımlar, araştırma projeleri, reklam seçimi.

Kitaptaki tanım: Her kol bir **Markov ödül süreci** (tek eylemli MDP); toplam problem, durumu kolların durumlarının çarpımı olan bir MDP'dir. Kollar bağımsızdır; yalnızca aynı anda tek kol çekilebildiği için birbirine bağlıdır.

### 3.1 Deterministik örnek ve Gittins indeksi

γ = 0.5; M kolu 0, 2, 0, 7.2, 0, 0, … verir, M₁ kolu hep 1.

| Strateji | Fayda |
|---|---|
| Hep M | 0 + 0.5 × 2 + 0.125 × 7.2 = **1.9** |
| Hep M₁ | Σ 0.5ᵗ = **2.0** |
| S: M'yi 4 kez çek, sonra M₁ | **2.025** (en iyisi) |

**Tek kollu haydut:** Bir kol ile sabit λ veren bir kol. **Durma zamanı** T: Kaç kez çekip sabit kola geçileceği. Kayıtsızlık noktasındaki λ, kolun **Gittins indeksidir**:

```text
λ = max_T  E[Σ_{t<T} γᵗ R_t] / E[Σ_{t<T} γᵗ]                     (17.15)
```

Pay fayda, payda "indirimli zaman": birim indirimli zamanda elde edilebilecek en büyük fayda. M için tablo (kitapla aynı):

| T | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| Σ γᵗ R_t | 0 | 1.0 | 1.0 | 1.9 | 1.9 | 1.9 |
| Σ γᵗ | 1.0 | 1.5 | 1.75 | 1.875 | 1.9375 | 1.9688 |
| oran | 0 | 0.6667 | 0.5714 | **1.0133** | 0.9806 | 0.9651 |

**Gittins'in sonucu:** En yüksek indeksli kolu çek, indeksleri güncelle: Bu **en iyi** politikadır. İndeks yalnızca kolun kendisine bağlıdır; ilk karar O(n), sonrakiler O(1).

**Hesaplama: yeniden başlatma MDP'si.** Kolun her durumuna "başa dön ve oradan devam et" eylemi eklenir. Gittins indeksi = (1 − γ) × bu MDP'nin başlangıç durumundaki değeri. M için değer 2.0267, λ = 2.0267 × 0.5 = 1.0133.

### 3.2 Bernoulli haydudu

Her kol 1 ya da 0 verir, olasılığı μᵢ bilinmez. Durum (s, f) = başarı ve başarısızlık sayıları, (1, 1)'den başlar; sonraki çekiş s/(s+f) olasılıkla 1 verir. Sonsuz durumlu olduğundan s + f ≤ 100'de kesilmiş MDP çözülür (γ = 0.9).

**Keşif bonusu:** Az denenmiş kolun indeksi, tahmini daha düşük olsa bile daha yüksek olabilir. Kitabın örneği: (3, 2)'nin tahmini 0.6, (7, 4)'ünki 0.6364; ama indeksler (3, 2) için daha büyük. Kitap 0.7057 ve 0.6922 verir. Bizim iki farklı yöntemle (kalibrasyon ve yeniden başlatma MDP'si) bulduğumuz değerler **0.7072** ve **0.6940**. Fark küçüktür (büyük olasılıkla kesme ayrıntısından) ve sıralama aynıdır.

### 3.3 Yaklaşık politikalar

- **UCB** (üst güven sınırı): `UCB(Mᵢ) = μ̂ᵢ + g(N)/√Nᵢ`. Kitabın önerdiği g(N) = (2 log(1 + N log² N))^{1/2}. Tam bir indeks değildir (toplam N'ye bağlı).
- **Thompson örneklemesi:** Her kolun değerinin sonsal dağılımından bir örnek çek, en büyüğünü seç. Kol, en iyi olma olasılığıyla seçilmiş olur.
- **Pişmanlık:** Her zaman en iyi kolu bilen "kâhine" göre kayıp. Lai ve Robbins (1985): Hiçbir algoritmanın pişmanlığı O(log N)'den yavaş büyüyemez. UCB ve Thompson bu hızı yakalar.

### 3.4 İndekslenemeyen türler

- **Seçim problemi:** Amaç başarı sayısını değil, en iyi seçeneği hızla bulmaktır (bakteri üzerinde ilaç testi, tedarikçi seçimi). Burada **indeks fonksiyonu yoktur**. MCTS'nin seçim problemine haydut sezgisi (UCB) uygulaması bu açıdan şaşırtıcıdır; seçim problemleri genelde daha fazla keşif ister.
- **Haydut süper süreci (BSP):** Her kol tam bir MDP. Yerel olarak en iyi politikaları birleştirmek **yanlıştır**: Başka işlerin beklemesi, her işte daha açgözlü (erken ödüllü) davranmayı kârlı kılar. Kitaptaki örnek: 4 alışveriş merkezi inşa eden bir müteahhit, ilk dükkânı 15. hafta yerine 5. haftada açan pahalı planı seçerse kiralar 5, 10, 15, 20. haftalarda başlar (15, 30, 45, 60 yerine). Kavramlar: **fırsat maliyeti**, **baskın politika**.

---

## 4. Kısmen gözlemlenebilir MDP'ler (`pomdp.py`)

**POMDP** = MDP + **algılayıcı modeli** P(e | s). Ajan hangi durumda olduğunu bilmez, bu yüzden π(s)'yi uygulayamaz.

**İnanç durumu** b: Durumlar üzerinde bir olasılık dağılımı (Bölüm 4'teki küme yerine). Örneğin 4 × 3 POMDP'de başlangıç inancı 9 uç olmayan durumda 1/9. Güncelleme, Bölüm 14'teki filtrelemenin eylemli hâlidir:

```text
b′(s′) = α P(e | s′) Σ_s P(s′ | s, a) b(s)        b′ = α FORWARD(b, a, e)    (17.16)
```

**Temel fikir:** En iyi eylem yalnızca **inanç durumuna** bağlıdır: π*(b). Döngü: (1) a = π*(b) yap, (2) e'yi algıla, (3) b ← FORWARD(b, a, e).

POMDP, sürekli bir inanç uzayında bir MDP'ye dönüşür (4 × 3 dünyada 11 boyutlu). Eylemler fiziksel durumu olduğu kadar inancı da değiştirir; bu yüzden **bilginin değeri** (Bölüm 16) kararın bir parçası olur.

**Algılayıcı modeli önemlidir (A9):** 4 × 3 POMDP'de düzgün inançtan Sol yapılıp algılayıcı "1 komşu duvar" derse, duvar **sayısını** ölçen bir algılayıcıyla (3,1) ve (3,2) eşit olasılıklıdır (~0.34). Duvarın **yönünü** de söyleyen 4 bitlik algılayıcıyla ("yalnızca güneyde duvar") (3,1) açık ara en olasıdır (~0.69).

---

## 5. POMDP algoritmaları

### 5.1 Koşullu planlarla değer yinelemesi

Belli bir b için en iyi politika bir **koşullu plana** denktir (Bölüm 4). İki gözlem:

1. Sabit bir p planının fiziksel s durumundan başlayınca faydası α_p(s) ise, b'deki beklenen fayda `b · α_p`: b'de **doğrusal** (bir hiperdüzlem).
2. `U(b) = max_p b · α_p`: Hiperdüzlemlerin maksimumu, yani **parçalı doğrusal ve dışbükey**.

Plan faydalarının özyinelemesi (p, ilk eylemi a ve e gözlemi için alt planı p.e olan plan):

```text
α_p(s) = Σ_s′ P(s′ | s, a) [R(s, a, s′) + γ Σ_e P(e | s′) α_{p.e}(s′)]      (17.18)
```

**İki durumlu dünya** (kitap): A ve B; Kal 0.9 olasılıkla yerinde kalır, Git 0.9 olasılıkla değiştirir; B'ye giren geçişin ödülü 1; algılayıcı 0.6 doğru; γ = 1.

- α[Kal] = (0.1, 0.9), α[Git] = (0.9, 0.1). Tek adımda: b(B) > 0.5 ise Kal.
- Derinlik 2: 8 plan, **4'ü baskın değil** (diğerleri her yerde başka bir plandan kötü).
- Derinlik 8: Budamasız 2²⁵⁵ plan olurdu; **144** baskın olmayan plan kalır. Kodumuz kitaptaki sayıları birebir verir.
- En iyi politika yine "b(B) > 0.5 ise Kal". Ara inançlarda fayda düşüktür: Ajan iyi eylemi seçecek bilgiye sahip değildir. POMDP'lerde en iyi politikalar bu yüzden sık sık **bilgi toplayan** eylemler içerir.

Genel POMDP'lerde en iyi politikayı bulmak **PSPACE-zor**dur. Değer yinelemesi küçük problemlerde bile umutsuzdur: n baskın olmayan plandan bir sonraki düzeyde |A| · n^|E| plan üretilir (4 bitlik algılayıcıyla |E| = 16).

### 5.2 Çevrimiçi POMDP ajanları

Beklenti-maks ağacı, fiziksel durumlar yerine **inanç durumları** üzerinde: Şans düğümlerinin dalları olası gözlemler. Derinlik d için O(|A|^d · |E|^d), koşullu plan sayısından çok daha az. Şans düğümlerinde örnekleme; büyük uzaylarda inanç yerine **parçacık filtresi** (Bölüm 14); uzun ufuklar için UCT benzeri denemeler. Parçacık filtresi + UCT = **POMCP**.

DDN tabanlı çevrimiçi POMDP ajanlarının artıları: kısmi gözlem ve stokastikliği ele alır, beklenmedik kanıtla planını değiştirir, bilgi toplamayı planlar, zaman baskısında "zarif" bozulur. Eksik olan: Çok uzun zaman ölçekleri (masa kurmak milyonlarca motor eylemi ister); hiyerarşik planlama (Bölüm 11.4) gerekir.

---

## Sık yapılan hatalar

| Yanılgı | Doğrusu |
|---|---|
| "Stokastik dünyada da bir eylem dizisi yeter." | Çözüm bir politikadır; her ulaşılabilecek durum için bir eylem gerekir. |
| "Uç durumun faydası, onun ödülüdür (+1)." | 4. baskıda ödül geçişe aittir; uç durumların faydası 0, ödül girişte bir kez alınır. İki kez saymak klasik bir hatadır. |
| "Eski baskıdaki 0.812, 0.868… değerleri 4. baskıda da geçerli." | 4. baskıda faydalar 0.8516, 0.9078… (ödül tanımı değişti). |
| "Değer yinelemesi tam yakınsamadan politika kullanılamaz." | Politika genellikle faydalardan çok önce en iyi olur; politika kaybı ≤ 2ε. |
| "γ'yı küçük tutmak her zaman iyidir; hızlı yakınsar." | Ajan kısa görüşlü olur; uzun vadeli sonuçları kaçırır. |
| "Hedefe yaklaşınca ödül vermek ajanı hep hızlandırır." | Potansiyele dayanmayan ödül döngüleri ödüllendirebilir; yalnızca γΦ(s′) − Φ(s) biçimi güvenlidir. |
| "Haydutta en iyi kol her zaman en yüksek tahminli koldur." | Gittins indeksi keşif bonusu içerir: Az denenmiş kol daha değerli olabilir. |
| "POMDP'de ajan en olası durumu seçip MDP politikasını uygulasın." | En iyi eylem bütün inanç dağılımına bağlıdır; bilgi toplamak da bir eylemdir. |

## Kendini yokla

1. MDP'nin dört bileşeni nedir? Politika neden bir eylem dizisinden farklıdır?
2. Sonlu ufukta en iyi politika neden durağan değildir?
3. İndirimli ödülü haklı çıkaran beş nedeni say.
4. Bellman denklemini yaz. Neden doğrusal değildir?
5. Değer yinelemesi neden yakınsar? Hata her adımda nasıl azalır?
6. Politika yinelemesinde politika değerlendirme adımı neden doğrusaldır?
7. Şekillendirme teoremi neyi söyler? Uç durumlarda Φ neden 0 olmalıdır?
8. Gittins indeksi nedir? Neden yalnızca kolun kendisine bağlıdır?
9. UCB ile Thompson örneklemesi arasındaki fark nedir?
10. POMDP'de faydanın inanç üzerinde parçalı doğrusal ve dışbükey olması nereden gelir?

## Kod rehberi

```bash
python ornekler/mdp.py              # kütüphane: 4 × 3 dünya, değer ve politika yinelemesi
python ornekler/dort_uc_dunya.py    # Şekil 17.3, r aralıkları ve 9 politika, sonlu ufuk, şekillendirme
python ornekler/deger_yineleme.py   # hata ve politika kaybı, büzülme, yineleme sınırları
python ornekler/politika_yineleme.py  # PI, değiştirilmiş PI, LP kısıtları, beklenti-maks, ε-ufku
python ornekler/haydut.py           # Gittins indeksi, Bernoulli haydudu, UCB ve Thompson
python ornekler/pomdp.py            # iki durumlu POMDP: inanç güncellemesi, α-vektörleri, 144 plan
python cozumler/alistirma_kod.py    # A2, A4, A5, A7–A10
```

## Terimler

| Türkçe | İngilizce | Kısa açıklama |
|---|---|---|
| sıralı karar problemi | sequential decision problem | Faydası eylem dizisine bağlı problem |
| Markov karar süreci | Markov decision process (MDP) | Tam gözlemli, stokastik, Markov, toplamsal ödüllü |
| geçiş modeli | transition model | P(s′ \| s, a) |
| ödül fonksiyonu | reward function | R(s, a, s′) |
| politika | policy | Her durum için bir eylem: π(s) |
| en iyi politika | optimal policy | Beklenen faydayı en büyükleyen π* |
| sonlu / sonsuz ufuk | finite / infinite horizon | Sabit bir son olup olmaması |
| durağan / durağan olmayan politika | stationary / nonstationary policy | Zamana bağlı olup olmaması |
| indirimli toplamsal ödül | additive discounted reward | Σ γᵗ R_t |
| indirim çarpanı | discount factor | γ ∈ [0, 1] |
| durağan tercih | stationary preference | Yarının tercihi bugün de geçerli |
| uygun politika | proper policy | Bir uç duruma varması garanti |
| Bellman denklemi / güncellemesi | Bellman equation / update | U(s) = max_a Σ P [R + γU] |
| eylem–fayda fonksiyonu | action-utility (Q) function | Q(s, a) |
| şekillendirme teoremi | shaping theorem | R + γΦ(s′) − Φ(s) politikayı korur |
| potansiyel | potential | Şekillendirmedeki Φ(s) |
| dinamik karar ağı | dynamic decision network (DDN) | Karar ve ödül düğümlü DBN |
| değer yinelemesi | value iteration | Bellman güncellemesini tekrarlama |
| büzülme | contraction | ‖f(x) − f(y)‖ ≤ γ ‖x − y‖ |
| en büyük norm | max norm | max_s \|U(s)\| |
| politika kaybı | policy loss | ‖U^{π_i} − U‖ |
| politika yinelemesi | policy iteration | Değerlendir + iyileştir |
| değiştirilmiş politika yinelemesi | modified policy iteration | Yaklaşık değerlendirme ile PI |
| eşzamansız politika yinelemesi | asynchronous policy iteration | Herhangi bir alt kümeyi güncelleme |
| beklenti-maks | expectimax | Maks ve şans düğümlü ağaç araması |
| gerçek zamanlı dinamik programlama | real-time dynamic programming (RTDP) | Keşfedilen alt MDP'yi çözmek |
| n kollu haydut | n-armed bandit | Bilinmeyen ödüllü n kol |
| keşif / sömürü | exploration / exploitation | Bilgi toplama / bilineni kullanma |
| Markov ödül süreci | Markov reward process | Tek eylemli MDP |
| durma zamanı | stopping time | Sabit kola geçiş anı |
| Gittins indeksi | Gittins index | Birim indirimli zamandaki en büyük fayda |
| yeniden başlatma MDP'si | restart MDP | Gittins indeksini hesaplama yolu |
| Bernoulli haydudu | Bernoulli bandit | 0/1 ödüllü kollar |
| üst güven sınırı | upper confidence bound (UCB) | Tahmin + belirsizlik bonusu |
| Thompson örneklemesi | Thompson sampling | Sonsaldan örnekle, en iyiyi seç |
| pişmanlık | regret | Kâhine göre kayıp |
| seçim problemi | selection problem | En iyiyi bulma; indeks yok |
| haydut süper süreci | bandit superprocess (BSP) | Her kolu bir MDP olan haydut |
| fırsat maliyeti | opportunity cost | Başka kola harcanmayan zamanın bedeli |
| kısmen gözlemlenebilir MDP | partially observable MDP (POMDP) | MDP + algılayıcı modeli |
| algılayıcı modeli | sensor model | P(e \| s) |
| inanç durumu | belief state | Durumlar üzerinde olasılık dağılımı |
| koşullu plan | conditional plan | Gözleme göre dallanan plan |
| baskın plan | dominated plan | Her inançta başka bir plandan kötü |
| parçalı doğrusal dışbükey | piecewise linear and convex | Hiperdüzlemlerin maksimumu |
| kısmen gözlemlenebilir Monte Carlo planlama | POMCP | Parçacık filtresi + UCT |
