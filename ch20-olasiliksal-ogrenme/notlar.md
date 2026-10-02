# Bölüm 20 — Olasılıksal modelleri öğrenmek

> **Kitapta:** AIMA 4. baskı, Bölüm 20 *"Learning Probabilistic Models"*.
> Önce kitabı oku, sonra bu notlarla pekiştir. Metin özgündür; kitaptan alıntı yoktur.
> (Bu klasörün eski adı `ch20-bilgi-ogrenme` idi; içerikle uyumlu olsun diye değiştirildi.)

## Bu bölümün haritası

| Kitap alt bölümü | Bu nottaki karşılığı | Kod |
|---|---|---|
| 20.1 Statistical Learning | §1 Bayesçi öğrenme, MAP, MDL, en büyük olabilirlik | `istatistiksel_ogrenme.py` |
| 20.2.1 ML parameter learning: discrete | §2.1 Sayımlarla öğrenme, Laplace düzeltmesi | `istatistiksel_ogrenme.py` |
| 20.2.2–20.2.3 Naive Bayes; generative vs discriminative | §2.2 Naif Bayes, üretici ve ayırt edici modeller | `naif_bayes.py` |
| 20.2.4 ML parameter learning: continuous | §2.3 Gauss, doğrusal–Gauss = en küçük kareler | `surekli_modeller.py` |
| 20.2.5–20.2.6 Bayesian parameter learning, Bayesian linear regression | §2.4 Beta önselleri, sanal sayımlar, Bayesçi regresyon | `istatistiksel_ogrenme.py`, `surekli_modeller.py` |
| 20.2.7 Learning Bayes net structures | §2.5 Yapı öğrenme | — |
| 20.2.8 Density estimation with nonparametric models | §2.6 k-NN ve çekirdek yoğunluk kestirimi | `surekli_modeller.py` |
| 20.3 Learning with Hidden Variables: EM | §3 Gizli değişkenler, Gauss karışımı, şeker torbaları, HMM, genel EM | `em_algoritmasi.py` |

## Öğrenme hedefleri

1. Bayesçi, MAP ve en büyük olabilirlik öğrenmeyi karşılaştırmak; önselin rolünü açıklamak.
2. Ayrık bir Bayes ağının parametrelerini sayımlarla öğrenmek; sıfır sayım sorununu düzeltmek.
3. Naif Bayes sınıflandırıcıyı öğrenmek; üretici ve ayırt edici modelleri ayırt etmek.
4. Gauss ve doğrusal–Gauss modeller için en büyük olabilirliği türetmek.
5. Beta önselleriyle Bayesçi parametre öğrenmeyi ve Bayesçi doğrusal regresyonu uygulamak.
6. EM algoritmasını gizli değişkenli bir modelde adım adım izlemek; yerel en büyükleri ve tanımlanabilirliği açıklamak.

---

## 1. İstatistiksel öğrenme (`istatistiksel_ogrenme.py`)

Veri = kanıt (rastgele değişkenlerin değerleri); hipotezler = alanın nasıl işlediğine dair olasılıksal kuramlar.

**Şeker örneği:** Kiraz ve limon aromalı şekerler aynı ambalajda; beş tür torba:

| Torba | h1 | h2 | h3 | h4 | h5 |
|---|---|---|---|---|---|
| kiraz | %100 | %75 | %50 | %25 | %0 |
| önsel | 0.1 | 0.2 | 0.4 | 0.2 | 0.1 |

**Bayesçi öğrenme:** Her hipotezin olasılığını hesapla, tahminleri **bütün** hipotezlerin ağırlıklı ortalamasıyla yap:

```text
P(hᵢ | d) = α P(d | hᵢ) P(hᵢ)                (20.1)
P(X | d)  = Σᵢ P(X | hᵢ) P(hᵢ | d)            (20.2)
P(d | hᵢ) = Πⱼ P(dⱼ | hᵢ)   (i.i.d.)          (20.3)
```

Torba gerçekte h5 ve art arda limonlu şeker çıkıyor (Şekil 20.1):
- 1 limondan sonra h3 hâlâ en olası; 2'den sonra h4; 3 ve fazlasından sonra h5.
- P(sonraki limon): başta 0.5, 1 limondan sonra **0.65**, 3 limondan sonra **≈ 0.8**, tekdüze artarak 1'e gider.

Bayesçi tahmin, gerçek hipotezi dışlamayan her önselde eninde sonunda doğru hipoteze yakınsar ve veri az da olsa çok da olsa **en iyidir**. Bedeli: Gerçek problemlerde hipotez uzayı çok büyük; toplam (ya da integral) çoğu zaman yaklaşık hesaplanır.

**MAP (en büyük sonsal):** Tek bir en olası hipotezle tahmin. 3 limondan sonra h_MAP = h5 ve "sonraki kesin limon" (1.0) der: Bayesçi tahminden (0.8) çok daha tehlikeli. Veri arttıkça ikisi yaklaşır. MAP bir **en iyileme** (toplam değil), bu yüzden genelde daha kolaydır.

**Önsel ve karmaşıklık:** Karmaşık hipotezlere düşük önsel; ama daha iyi uyum. Mantıksal (belirlenimci) hipotezlerde P(d | h) 0 ya da 1'dir; h_MAP veriyle tutarlı **en basit** kuramdır: **Ockham'ın usturası**.

**MDL bakışı:** h_MAP, −log₂ P(d | h) − log₂ P(h)'yi en küçükler: hipotezi kodlamanın bitleri + hipotez verildiğinde veriyi kodlamanın bitleri. MAP = verinin en çok sıkıştırılması. MDL bunu doğrudan bit sayarak yapar.

**En büyük olabilirlik (ML):** Düzgün önselde MAP, P(d | h)'yi en büyükleyen h_ML'ye indirgenir. İstatistikte yaygın (öznel önsellere güvensizlik); veri çokken iyi yaklaşım, azken sorunlu.

---

## 2. Tam veriyle öğrenme

**Yoğunluk kestirimi:** Verinin üretildiği olasılık modelini öğrenmek (denetimsiz öğrenmenin bir biçimi). **Tam veri:** Her örnekte modelin her değişkeni gözlenmiş. **Parametre öğrenme:** Yapı sabit, sayılar öğrenilir.

### 2.1 Ayrık modellerde en büyük olabilirlik

Yeni bir üreticinin torbası: kiraz oranı θ bilinmiyor. N şekerden c kiraz, ℓ limon:

```text
P(d | h_θ) = θᶜ (1 − θ)^ℓ       L = c log θ + ℓ log(1 − θ)       dL/dθ = c/θ − ℓ/(1 − θ) = 0  ⇒  θ = c/N
```

Genel yöntem: (1) olabilirliği parametrelerin fonksiyonu olarak yaz, (2) log olabilirliğin türevini al, (3) türevi sıfırlayan değeri bul (zor adım; çoğu zaman sayısal en iyileme).

**Ambalaj örneği:** Ambalaj rengi tada bağlı (kırmızı/yeşil): θ = P(kiraz), θ₁ = P(kırmızı | kiraz), θ₂ = P(kırmızı | limon). ML: θ = c/N, θ₁ = r_c/c, θ₂ = r_ℓ/ℓ. **Tam veride Bayes ağı parametre öğrenme her parametre için ayrı bir probleme ayrışır**: Her parametre, kendi değişkeninin ve ebeveynlerinin sayımlarından öğrenilir.

**Sıfır sayım sorunu:** Görülmemiş bir olaya ML sıfır olasılık verir (tek bir kiraz görünce θ = 1). Çare: sayımları 0 yerine 1'den başlatmak (Laplace düzeltmesi).

### 2.2 Naif Bayes (`naif_bayes.py`)

Sınıf C, nitelikler C verildiğinde bağımsız: P(C | x₁..xₙ) = α P(C) Πᵢ P(xᵢ | C). n Boolean nitelikte yalnızca **2n + 1** parametre, arama yok; çok büyük problemlere ölçeklenir, gürültülü ve eksik veriyle iyi başa çıkar. Kitapta restoran probleminde karar ağacının altında kalır (gerçek fonksiyon bir ağaç; naif Bayes onu tam temsil edemez). Ana kusuru: Koşullu bağımsızlık nadiren doğrudur; nitelik çoğaldıkça olasılıklar 0 ya da 1'e yakın, **aşırı emin** olur (A5). Artırılmış (boosted) naif Bayes en etkili genel amaçlı öğrenicilerden biridir.

**Üretici model:** Her sınıfın dağılımını modeller (P(girdi | sınıf), P(sınıf)); örnek üretebilir (naif Bayes). **Ayırt edici model:** Doğrudan P(sınıf | girdi) ya da karar sınırını öğrenir (lojistik regresyon, karar ağaçları, SVM). Ayırt ediciler sınırsız veride genellikle daha iyidir; az veride üretici model çoğu zaman öndedir (kitaptaki Ng ve Jordan karşılaştırması: en çok veriyle 15 kümenin 9'unda lojistik regresyon, en az veriyle 14'ünde naif Bayes daha iyi). Kodumuzdaki sentetik veride geçiş ~100 örnekte.

### 2.3 Sürekli modellerde en büyük olabilirlik (`surekli_modeller.py`)

Tek değişkenli Gauss:

```text
μ = (1/N) Σ xⱼ          σ = √((1/N) Σ (xⱼ − μ)²)          (20.4)
```

ML ortalama = örnek ortalaması, ML standart sapma = örnek varyansının karekökü (N'ye bölünür).

**Doğrusal–Gauss model:** y = θ₁x + θ₂ + sabit varyanslı Gauss gürültü. θ'lara göre log olabilirliği en büyüklemek, üsteki (y − (θ₁x + θ₂))²'yi, yani **L₂ kaybını** en küçüklemektir: Gauss gürültüde standart doğrusal regresyon (Bölüm 19) en büyük olabilirlik doğrusudur.

### 2.4 Bayesçi parametre öğrenme

ML az veride kötüdür. Bayesçi yaklaşımda θ, bir rastgele değişken Θ'nın bilinmeyen değeridir; **hipotez önseli** P(Θ).

**Beta dağılımı:** Beta(θ; a, b) = α θ^(a−1) (1 − θ)^(b−1). a ve b **hiperparametreler**. Ortalama a/(a + b); a + b büyüdükçe daha sivri; **Beta(1, 1) = düzgün**.

**Eşlenik önsel:** Beta önseli ve Boolean gözlem → yine Beta. Kiraz görünce a, limon görünce b bir artar. a ve b **sanal sayımlardır**: Beta(a, b), düzgün önselden başlayıp a − 1 kiraz ve b − 1 limon görmüş gibidir. Gerçek oran %75 iken Beta(3,1) → Beta(6,2) → Beta(30,10) dizisi 0.75 çevresinde daralır; çok veride Bayesçi öğrenme ML'ye yakınsar. (Çok değerli değişkenler için Dirichlet, Gauss için Normal–Wishart eşleniktir.)

**Parametre bağımsızlığı** varsayımıyla her parametrenin kendi Beta'sı ayrı güncellenir. Öğrenme sürecinin kendisi bir Bayes ağıdır (Şekil 20.6): Parametreler de düğümdür; öğrenme = bu ağda çıkarım (genelde MCMC).

**Bayesçi doğrusal regresyon** (orijinden geçen doğru y = θx, σ bilinir, önsel N(θ₀, σ₀²)):

```text
θ_N = (σ² θ₀ + σ₀² Σ xᵢyᵢ) / (σ² + σ₀² Σ xᵢ²)          σ_N² = σ² σ₀² / (σ² + σ₀² Σ xᵢ²)
```

Veri orijine yakın toplanırsa Σxᵢ² küçük, σ_N² ≈ σ₀² (eğim az kısıtlanır); veri geniş yayılırsa σ_N² ≈ σ²/Σxᵢ². Tahmin belirsizliği veriden uzaklaştıkça büyür: tek bir "en iyi doğru"nun veremediği bilgi. Kodumuz kapalı biçimi sayısal integralle doğrular.

### 2.5 Bayes ağı yapısını öğrenmek

Bağlantısız bir ağdan ya da bir tahminden başlayıp tepe tırmanma / benzetilmiş tavlamayla bağ ekle, sil, çevir (döngü yaratmadan; çoğu yöntem bir değişken sırası varsayar). İyi yapıya karar vermenin iki yolu:
1. Yapının koşullu bağımsızlık iddialarını veride istatistiksel olarak sınamak.
2. Modelin veriyi ne kadar açıkladığını ölçmek. Saf ML her zaman tam bağlı ağı seçer (ebeveyn eklemek olabilirliği düşürmez); karmaşıklık cezalandırılmalı: **MAP/MDL** cezası ya da yapılar ve parametreler üzerinde ortak önsel (genelde MCMC ile örnekleme). Tablo biçimli dağılımlarda ceza ebeveyn sayısıyla üstel, gürültülü-VEYA'da doğrusal büyür.

### 2.6 Parametrik olmayan yoğunluk kestirimi

- **k-NN yoğunluğu:** Sorgu noktasının çevresinde k komşuyu içeren daire; P(x) ≈ (k/N)/alan. Kitapta k = 3 çok sivri, 40 çok düz, 10 iyi.
- **Çekirdek yoğunluğu:** Her veri noktasına bir çekirdek (ör. genişliği w olan Gauss) koy, ortalamasını al. w çok küçükse sivri, çok büyükse düz; doğru w çapraz doğrulamayla seçilir.

---

## 3. Gizli değişkenlerle öğrenme: EM (`em_algoritmasi.py`)

**Gizli (örtük) değişkenler** veride gözlenmez ama modeli çok küçültebilir. Kitaptaki kalp hastalığı ağı (her değişken 3 değerli): Gizli HeartDisease ile **78** parametre; çıkarılınca belirtiler birbirine bağlanır ve **708** parametre gerekir.

**EM (beklenti en büyükleme):** Gizli değişkenler için beklenen değerleri hesapla (E), bu beklenen değerleri gözlenmiş gibi kullanarak parametreleri yeniden hesapla (M); tekrarla.

### 3.1 Gauss karışımı (denetimsiz kümeleme)

P(x) = Σᵢ P(C = i) P(x | C = i), her bileşen bir Gauss. Bileşen C gizlidir.
1. **E adımı:** pᵢⱼ = P(C = i | xⱼ) = α P(xⱼ | C = i) P(C = i) (her noktanın her bileşene "sorumluluğu").
2. **M adımı:** nᵢ = Σⱼ pᵢⱼ; μᵢ ← Σⱼ pᵢⱼ xⱼ / nᵢ; Σᵢ ← Σⱼ pᵢⱼ (xⱼ − μᵢ)(xⱼ − μᵢ)ᵀ / nᵢ; wᵢ ← nᵢ / N.

EM her yinelemede log olabilirliği **artırır** (genel olarak kanıtlanabilir) ve çoğu durumda bir **yerel** en büyüğe varır. Tuzaklar: Bir bileşen tek noktaya çökerse varyansı 0'a, olabilirliği sonsuza gider; iki bileşen birleşebilir. Önseller ve mantıklı başlangıç yardım eder.

### 3.2 Gizli değişkenli Bayes ağı: karışmış şeker torbaları

İki torba karışmış; her şekerin tadı, ambalajı ve deliği gözleniyor, torbası değil. Torba verildiğinde nitelikler bağımsız (naif Bayes). Parametreler θ (torba 1 önseli), θ_F1, θ_W1, θ_H1, θ_F2, θ_W2, θ_H2. Kitaptaki 1000 şekerlik veri gerçek değerlerle (θ = 0.5, torba 1 için 0.8, torba 2 için 0.3) üretilmiş:

| | kırmızı, delikli | kırmızı, deliksiz | yeşil, delikli | yeşil, deliksiz |
|---|---|---|---|---|
| kiraz | 273 | 93 | 104 | 90 |
| limon | 79 | 100 | 94 | 167 |

Başlangıç θ = 0.6, torba 1 için 0.6, torba 2 için 0.4. E adımında her şeker türü için P(Bag = 1 | gözlem) hesaplanır (örneğin 273 kırmızı delikli kirazın θ'ya katkısı ≈ 0.22797). İlk yinelemeden sonra (kodumuz birebir aynısını bulur):

```text
θ = 0.6124   θ_F1 = 0.6684   θ_W1 = 0.6483   θ_H1 = 0.6558
             θ_F2 = 0.3887   θ_W2 = 0.3817   θ_H2 = 0.3827
```

Log olabilirlik ≈ −2044'ten ≈ −2021'e çıkar (olabilirlik ~e²³ ≈ 10¹⁰ kat artar). 10. yinelemede gerçek modelin olabilirliğini (−1982.214) geçer; sonrası çok yavaşlar (pratikte EM'i Newton–Raphson gibi gradyan yöntemleriyle tamamlamak yaygındır).

**Genel ders:** Gizli değişkenli Bayes ağlarında güncelleme, normalleştirilmiş **beklenen sayımlardır**: θᵢⱼₖ ← N̂(Xᵢ = xᵢⱼ, Uᵢ = uᵢₖ) / N̂(Uᵢ = uᵢₖ). Gereken olasılıklar herhangi bir Bayes ağı çıkarım algoritmasının yan ürünüdür ve her parametre için **yereldir**.

**Tanımlanabilirlik:** Üç nitelikle 7 parametre, 2³ − 1 = 7 bağımsız sayım. Delik atılırsa 5 parametre, yalnızca 3 sayım: Model **tanımlanamaz**, farklı parametreler aynı olabilirliği verir (kodumuzda iki başlangıç, iki farklı çözüm, aynı log olabilirlik). Üç nitelikte bile "torba 1" ile "torba 2" yer değiştirebilir; hiç gözlenmeyen değişkenlerde bu kaçınılmazdır. Simetrik başlangıç (her şey 0.5) EM'i simetrik bir eyer noktasında bırakır (A8); başlangıçları rastgele seçmek daha iyidir.

### 3.3 Saklı Markov modellerini öğrenmek

Geçiş olasılıkları zamanda tekrarlanır (θᵢⱼₜ = θᵢⱼ). Tahmin: Beklenen geçiş sayılarının oranı, θᵢⱼ ← Σₜ N̂(Xₜ₊₁ = j, Xₜ = i) / Σₜ N̂(Xₜ = i). Beklenen sayımlar ileri–geri algoritmasıyla (Bölüm 14) ve **düzleştirmeyle** (filtrelemeyle değil) bulunur: Bir geçişin kanıtı çoğu zaman ondan sonra gelir. (Baum–Welch algoritması.)

### 3.4 EM'in genel biçimi

x gözlenen değerler, Z gizli değişkenler, θ parametreler:

```text
θ⁽ⁱ⁺¹⁾ = argmax_θ Σ_z P(Z = z | x, θ⁽ⁱ⁾) L(x, Z = z | θ)
```

E adımı: "tamamlanmış" verinin log olabilirliğinin, gizli değişkenlerin sonsalına göre beklentisi. M adımı: bu beklentiyi θ'ya göre en büyüklemek. E adımı hesaplanamıyorsa yaklaşık çıkarım (MCMC, değişimsel yöntemler, döngülü inanç yayılımı) yeterlidir.

### 3.5 Gizli değişkenli yapı öğrenme

Hangi gizli değişkenlerin olduğunu ve neye bağlandığını da öğrenmek zordur. Basit yol: dış döngüde yapıyı ara, iç döngüde her aday yapı için parametreleri EM ile öğren (pahalı). **Yapısal EM:** Mevcut yapıyla beklenen sayımları hesapla, bu sayımlarla M adımında aday yapıların olabilirliğini değerlendir; böylece sayımları yeniden hesaplamadan birkaç yapı değişikliği yapılabilir. Arama yapı uzayındadır (yapı + parametre uzayında değil). Kitaba göre yapı öğrenme problemi henüz çözülmüş sayılmaz.

---

## Sık yapılan hatalar

| Yanılgı | Doğrusu |
|---|---|
| "MAP ile Bayesçi tahmin aynıdır." | MAP tek hipoteze güvenir; az veride çok daha aşırı tahmin yapar (3 limondan sonra 1.0 vs 0.8). |
| "En büyük olabilirlik her zaman makuldür." | Az veride aşırıdır (tek kiraz → θ = 1); önsel ya da düzeltme gerekir. |
| "Önsel önemsizdir." | Az veride sonucu belirler; çok veride etkisi kaybolur. |
| "Naif Bayes olasılıkları güvenilirdir." | Bağımsızlık yanlışsa olasılıklar 0 ve 1'e itilir; sıralama iyi olsa da kalibrasyon kötüdür. |
| "ML standart sapma N − 1'e bölünür." | ML tahmini N'ye böler (yansız tahmin N − 1'e). |
| "EM global en iyiyi bulur." | Yerel en büyüğe varır; başlangıca bağlıdır, simetrik başlangıçta takılır. |
| "Gizli değişkenler modeli karmaşıklaştırır." | Çoğu zaman parametre sayısını büyük ölçüde azaltır (78'e karşı 708). |
| "Her gizli değişkenli model öğrenilebilir." | Gözlemler parametreleri belirlemeye yetmezse model tanımlanamaz. |

## Kendini yokla

1. Bayesçi öğrenme, MAP ve ML arasındaki farkı şeker örneğiyle açıkla.
2. MAP neden Ockham'ın usturasının bir biçimidir? MDL ile ilişkisi nedir?
3. θ_ML = c/N sonucunu türet.
4. Tam veride Bayes ağı parametre öğrenme neden her parametre için ayrı bir probleme ayrışır?
5. Beta önselinde a ve b neden "sanal sayım" sayılır?
6. Doğrusal–Gauss modelde en büyük olabilirlik neden en küçük karelere eşittir?
7. Üretici ve ayırt edici modeller arasındaki fark nedir? Hangisi az veride daha iyidir?
8. Gauss karışımında E ve M adımlarını yaz.
9. EM log olabilirliği neden azaltmaz? Hangi tuzaklara düşebilir?
10. Tanımlanabilirlik nedir? İki nitelikli torba modeli neden tanımlanamaz?

## Kod rehberi

```bash
python ornekler/istatistiksel_ogrenme.py # şeker torbaları: Bayesçi, MAP, ML, MDL; ambalaj ağı; Beta önselleri
python ornekler/naif_bayes.py            # naif Bayes (restoran), üretici vs ayırt edici
python ornekler/surekli_modeller.py      # Gauss ML, doğrusal–Gauss, Bayesçi regresyon, yoğunluk kestirimi
python ornekler/em_algoritmasi.py        # şeker torbaları EM (kitap değerleri), tanımlanabilirlik, Gauss karışımı
python cozumler/alistirma_kod.py         # A3, A5–A10
```

## Terimler

| Türkçe | İngilizce | Kısa açıklama |
|---|---|---|
| Bayesçi öğrenme | Bayesian learning | Bütün hipotezlerle ağırlıklı tahmin |
| hipotez önseli | hypothesis prior | P(h) |
| olabilirlik | likelihood | P(d \| h) |
| en büyük sonsal (MAP) | maximum a posteriori | En olası tek hipotez |
| en kısa betimleme uzunluğu (MDL) | minimum description length | Bit cinsinden en kısa açıklama |
| en büyük olabilirlik (ML) | maximum likelihood | P(d \| h)'yi en büyükleyen hipotez |
| yoğunluk kestirimi | density estimation | Olasılık modelini veriden öğrenmek |
| tam veri | complete data | Her değişken gözlenmiş |
| parametre öğrenme | parameter learning | Sabit yapıda sayıları öğrenmek |
| log olabilirlik | log likelihood | Olabilirliğin logaritması |
| naif Bayes | naive Bayes | Sınıf verildiğinde bağımsız nitelikler |
| üretici / ayırt edici model | generative / discriminative model | P(x \| c) / P(c \| x) |
| doğrusal–Gauss model | linear–Gaussian model | Ortalaması doğrusal Gauss |
| beta dağılımı | beta distribution | [0, 1] üzerinde Beta(a, b) |
| hiperparametre | hyperparameter | Önselin parametresi |
| eşlenik önsel | conjugate prior | Güncellemede aynı aileye düşen önsel |
| sanal sayım | virtual count | Önselin sayım olarak yorumu |
| parametre bağımsızlığı | parameter independence | Parametrelerin önselde bağımsızlığı |
| Dirichlet dağılımı | Dirichlet distribution | Çok değerli değişkenler için eşlenik |
| bilgi vermeyen önsel | uninformative prior | Geniş, düz önsel |
| Bayesçi doğrusal regresyon | Bayesian linear regression | Ağırlıklar üzerinde dağılım |
| yapı öğrenme | structure learning | Bayes ağının bağlarını öğrenmek |
| çekirdek yoğunluk kestirimi | kernel density estimation | Noktalara çekirdek koyup ortalama |
| gizli (örtük) değişken | hidden (latent) variable | Gözlenmeyen değişken |
| beklenti en büyükleme (EM) | expectation–maximization | E ve M adımlarını tekrarlama |
| Gauss karışımı | mixture of Gaussians | Gauss bileşenlerin ağırlıklı toplamı |
| sorumluluk | responsibility | pᵢⱼ = P(C = i \| xⱼ) |
| beklenen sayım | expected count | N̂: olasılıklarla ağırlıklı sayım |
| tanımlanabilirlik | identifiability | Parametrelerin veriden tek belirlenmesi |
| Baum–Welch algoritması | Baum–Welch algorithm | HMM için EM |
| yapısal EM | structural EM | Gizli değişkenli yapı arama |
