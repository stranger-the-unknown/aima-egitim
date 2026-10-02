# Bölüm 19 — Örneklerden öğrenme

> **Kitapta:** AIMA 4. baskı, Bölüm 19 *"Learning from Examples"*.
> Önce kitabı oku, sonra bu notlarla pekiştir. Metin özgündür; kitaptan alıntı yoktur.

## Bu bölümün haritası

| Kitap alt bölümü | Bu nottaki karşılığı | Kod |
|---|---|---|
| 19.1 Forms of Learning | §1 Neyi, hangi geri bildirimle öğreniriz | — |
| 19.2 Supervised Learning | §2 Hipotez uzayı, genelleme, restoran örneği | `karar_agaci.py` |
| 19.3 Learning Decision Trees | §3 İfade gücü, öğrenme, bilgi kazancı, aşırı uydurma, χ² budama | `karar_agaci.py` |
| 19.4 Model Selection and Optimization | §4 Doğrulama, çapraz doğrulama, kayıp, düzenlileştirme, hiperparametreler | `model_secimi.py` |
| 19.5 The Theory of Learning | §5 PAC öğrenme, karar listeleri | `model_secimi.py`, `karar_agaci.py` |
| 19.6 Linear Regression and Classification | §6 Regresyon, gradyan inişi, L1/L2, algılayıcı, lojistik regresyon | `dogrusal_modeller.py` |
| 19.7 Nonparametric Models | §7 k-NN, boyutların laneti, k-d ağacı, LSH, yerel regresyon, SVM, çekirdek | `parametrik_olmayan.py` |
| 19.8 Ensemble Learning | §8 Torbalama, rastgele ormanlar, yığma, AdaBoost, gradyan artırma, çevrimiçi öğrenme | `topluluk.py` |
| 19.9 Developing Machine Learning Systems | §9 Problem tanımı, veri, model seçimi, güven ve açıklanabilirlik | — |

## Öğrenme hedefleri

1. Denetimli, denetimsiz ve pekiştirmeli öğrenmeyi ayırt etmek; sınıflandırma ile regresyonu tanımak.
2. Bilgi kazancıyla bir karar ağacını elle ve kodla öğrenmek; aşırı uydurmayı budamayla azaltmak.
3. Eğitim, doğrulama ve test kümelerini doğru kullanmak; çapraz doğrulamayla model seçmek.
4. Kayıp fonksiyonu, düzenlileştirme ve hiperparametre ayarı kavramlarını açıklamak.
5. PAC sınırıyla gereken örnek sayısını tahmin etmek.
6. Doğrusal regresyonu kapalı biçimde ve gradyan inişiyle çözmek; algılayıcı ve lojistik regresyonu uygulamak.
7. k-NN, SVM ve çekirdek hilesinin ne zaman işe yaradığını açıklamak; boyutların lanetini sayılarla göstermek.
8. Topluluk yöntemlerinin neden işe yaradığını açıklamak.

---

## 1. Öğrenmenin biçimleri

Bir ajanın her bileşeni öğrenilebilir (Bölüm 2): koşul–eylem kuralları, algıdan dünya özellikleri, eylemlerin sonuçları, fayda, eylem değerleri, hedefler. Kitabın örneği: insan sürücüyü izleyen otonom araba fren kuralını, otobüs tanımayı, ıslak yolda frenin etkisini ve yolcu şikâyetlerinden fayda fonksiyonunun bir parçasını öğrenebilir.

**Tümevarım:** Gözlemlerden genel kural çıkarmak; tümdengelimin (Bölüm 7) aksine sonuç yanlış olabilir. Bu bölümde girdi **ayrışık** bir temsil (nitelik vektörü).

- Çıktı sonlu kümeden: **sınıflandırma**. Çıktı sayı: **regresyon** (adı Galton'un "ortalamaya dönüş" makalesinden).
- **Denetimli öğrenme:** Girdi–çıktı çiftleri (**etiketler**). **Denetimsiz öğrenme:** Açık geri bildirim yok; en yaygın görev **kümeleme**. **Pekiştirmeli öğrenme:** Ödül ve cezalar (Bölüm 22).

---

## 2. Denetimli öğrenme

Görev: Bilinmeyen y = f(x)'ten üretilmiş N eğitim çifti verildiğinde f'ye yakın bir **hipotez** h bul. h, **hipotez uzayı** (model sınıfı) H'den seçilir; yᵢ'ler **temel gerçektir** (ground truth).

- **Tutarlı hipotez:** Her eğitim örneğinde h(xᵢ) = yᵢ. Sürekli çıktıda **en iyi uyum** aranır.
- Asıl ölçü **genellemedir**: Görülmemiş **test kümesindeki** başarı.
- Kitabın Şekil 19.1'i: Doğrular az uydurur (**eksik uydurma**), noktaları birleştiren parçalı doğrular ve yüksek dereceli polinomlar veri kümesi değişince çok değişir (**varyans**, **aşırı uydurma**).
- **Yanlılık:** Hipotez uzayının farklı veri kümelerinde bile belli yönde sapma eğilimi. **Yanlılık–varyans dengesi.**
- **Ockham'ın usturası:** Veriyle uyumlu en basit hipotezi tercih et. Bayesçi bakış: h* = argmax P(veri | h) P(h); basit hipotezlere yüksek önsel.
- İfade gücü ile hesaplama karmaşıklığı arasında da bir denge vardır.

**Restoran örneği** (Şekil 19.2): WillWait (masa için bekleyecek miyiz?) tahmini; 10 nitelik (Alternate, Bar, Fri/Sat, Hungry, Patrons, Price, Raining, Reservation, Type, WaitEstimate). 2⁶ × 3² × 4² = **9216** olası girdi, yalnızca **12** örnek; geri kalan 9204'ün çıktısını tahmin etmek tümevarımın özüdür.

---

## 3. Karar ağaçları (`karar_agaci.py`)

**Karar ağacı:** İç düğümler nitelik testleri, dallar değerler, yapraklar kararlar. Boolean bir karar ağacı, kökten "evet" yapraklarına giden yolların **ayırıcı normal biçimidir**; her önerme mantığı fonksiyonu ifade edilebilir. Ama bazıları için ağaç üstel büyür: **çoğunluk** ve **eşlik** (parity) fonksiyonları; sürekli niteliklerde çapraz sınırlar (y > A₁ + A₂). n Boolean nitelikte 2^(2ⁿ) fonksiyon vardır; 20 nitelikte ≈ 10^300 000. Hepsini kısa temsil eden bir temsil olamaz.

### 3.1 Öğrenme algoritması

En küçük tutarlı ağacı bulmak zordur; **LEARN-DECISION-TREE** açgözlü böl ve yönet uygular: En önemli niteliği teste koy, alt problemleri özyinelemeli çöz. Dört durum:
1. Kalan örneklerin hepsi aynı sınıfta → o sınıf.
2. Karışık → en iyi nitelikle böl.
3. Örnek kalmadı → **ebeveyndeki** çoğunluk sınıfı.
4. Nitelik kalmadı ama karışık → çoğunluk (gürültü, belirlenimci olmayan alan ya da gözlenemeyen nitelik).

12 örnekten öğrenilen ağaç (Şekil 19.6; kodumuz birebir aynısını bulur):

```text
Patrons = None  → No
Patrons = Some  → Yes
Patrons = Full  → Hungry = No  → No
                  Hungry = Yes → Type = French → Yes, Italian → No, Burger → Yes,
                                  Thai → Fri/Sat = Yes → Yes, No → No
```

Gerçek ağaçtan (Şekil 19.3) farklı ama daha basit ve 12 örneğin hepsiyle tutarlı. Raining ve Reservation'ı kullanmaz; "hafta sonu Tayland yemeği" gibi beklenmedik bir örüntüyü yakalar; hiç görmediği durumlarda (dolu restoran, 0–10 dakika bekleme) hata yapabilir.

**Öğrenme eğrisi:** Eğitim kümesi büyüdükçe test doğruluğu artar ("mutlu grafikler"). Kodumuzda gerçek ağaçtan üretilen örneklerle 5 örnekte ~%66, 80 örnekte ~%96.

### 3.2 Nitelik seçimi: bilgi kazancı

**Entropi** (bit): H(V) = −Σ P(vₖ) log₂ P(vₖ). Adil para 1 bit, dört yüzlü zar 2 bit, %99 tura veren para ≈ 0.08 bit. Boolean için B(q) = −(q log₂ q + (1 − q) log₂ (1 − q)).

```text
Kalan(A) = Σₖ (pₖ + nₖ)/(p + n) · B(pₖ/(pₖ + nₖ))        Kazanç(A) = B(p/(p + n)) − Kalan(A)
```

Restoranda B(6/12) = 1 bit. **Kazanç(Patrons) ≈ 0.541**, **Kazanç(Type) = 0**: Patrons köke gider. (Diğerleri: WaitEstimate 0.208, Hungry ve Price 0.196, …)

### 3.3 Genelleme, aşırı uydurma ve budama

Nitelik sayısı arttıkça aşırı uydurma olasılığı artar, örnek sayısı arttıkça azalır.

**Karar ağacı budama:** Önce tam ağacı kur. Yalnızca yaprak çocukları olan bir test düğümü ilgisiz görünüyorsa onu yaprakla değiştir; tekrarla.

**χ² budama:** Sıfır hipotezi "nitelik ilgisiz". Beklenen sayılar p̂ₖ = p (pₖ + nₖ)/(p + n), n̂ₖ = n (pₖ + nₖ)/(p + n);

```text
Δ = Σₖ (pₖ − p̂ₖ)²/p̂ₖ + (nₖ − n̂ₖ)²/n̂ₖ   ~   χ² (d − 1 serbestlik derecesi)
```

Type (4 değer, 3 serbestlik): %5 düzeyinde Δ ≥ 7.82, %1'de Δ ≥ 11.35 gerekir. Etiket gürültüsünde budanmış ağaçlar hem daha küçük hem daha iyidir (A6: %20 gürültüde test doğruluğu 0.75'ten 0.84'e).

**Erken durdurmanın tuzağı:** "İyi nitelik yoksa dur" kuralı XOR gibi durumları kaçırır: Tek başına hiçbir nitelik bilgilendirici değildir, ama birlikte çok bilgilendiricidir. Önce kur, sonra buda.

### 3.4 Uygulanabilirliği genişletmek

- **Eksik veri:** Hem sınıflandırmada hem kazanç hesabında ele alınmalı.
- **Sürekli ve çok değerli nitelikler:** **Bölme noktası** testleri (Weight > 160); sıralayıp yalnızca sınıfın değiştiği noktaları dene. Çok değerli niteliklerde (posta kodu) **kazanç oranı** (A5) ya da A = vₖ eşitlik testleri.
- **Sürekli çıktı:** **Regresyon ağacı** (yapraklarda doğrusal fonksiyonlar). Sınıflandırma ve regresyon ağaçlarının ortak adı **CART**.

---

## 4. Model seçimi ve en iyileme (`model_secimi.py`)

**Durağanlık varsayımı:** Gelecek örnekler geçmişe benzer; örnekler **bağımsız ve özdeş dağılımlı (i.i.d.)**.

**Hata oranı:** h(x) ≠ y olma oranı. Bir hipotezi test kümesinde ölçmek doğrudur; ama farklı **hiperparametreleri** (model sınıfının "düğmeleri": χ² eşiği, polinom derecesi) test kümesine bakarak denemek, test kümesini dolaylı olarak "kopya çekmek" için kullanmak demektir. Üç küme gerekir:

1. **Eğitim kümesi:** Aday modelleri eğit.
2. **Doğrulama (geliştirme) kümesi:** Adayları karşılaştır, en iyisini seç.
3. **Test kümesi:** Her şey bittikten sonra bir kez, yansız değerlendirme.

**k katlı çapraz doğrulama:** Veriyi k parçaya böl; her turda bir parça doğrulama, gerisi eğitim; ortalamayı al. Yaygın k = 5 ya da 10; uç durum k = N: **birini dışarıda bırak (LOOCV)**.

**Model seçimi** (hipotez uzayını seçmek) ve **en iyileme** (uzay içinde en iyi hipotezi bulmak; eğitim). MODEL-SELECTION karmaşıklığı (ağaç düğüm sayısı, polinom derecesi) artırıp en düşük doğrulama hatasını seçer.

- Eğitim hatası karmaşıklıkla hep azalır.
- Doğrulama hatası çoğu zaman **U biçimlidir** (kitapta karar ağacı için en iyi boyut 7). Bazı model sınıflarında (derin ağlar, çekirdek makineleri, rastgele ormanlar, artırılmış topluluklar) veriyi tam uydurduktan (**interpolasyon**) sonra bile doğrulama hatası yeniden düşebilir; kitaptaki MNIST örneğinde en iyisi 1 000 000 parametre.

### 4.1 Hata oranından kayba

Hatalar eşit maliyetli değildir: Önemli bir postayı spam sanmak, spam'ı kaçırmaktan kötüdür. **Kayıp fonksiyonu** L(x, y, ŷ): Doğru yerine ŷ kullanmanın kaybettirdiği fayda. Basitleştirilmiş L(y, ŷ); örnek L(spam, spam değil) = 1, L(spam değil, spam) = 10.

| Kayıp | Formül |
|---|---|
| Mutlak değer (L₁) | \|y − ŷ\| |
| Kare hata (L₂) | (y − ŷ)² |
| 0/1 (L₀/₁) | y = ŷ ise 0, değilse 1 |

**Genelleme kaybı** GenLoss(h) = Σ L(y, h(x)) P(x, y) (bilinmez); **ampirik kayıp** EmpLoss(h) = (1/N) Σ L(y, h(x)). ĥ* ≠ f olmasının dört nedeni: **gerçekleştirilemezlik** (f, H'de yok), **varyans**, **gürültü**, **hesaplama karmaşıklığı**. Küçük ölçekli öğrenmede yaklaşım ve kestirim hatası, büyük ölçekli öğrenmede hesaplama sınırları baskındır.

### 4.2 Düzenlileştirme

```text
Cost(h) = EmpLoss(h) + λ Complexity(h)
```

Karmaşık hipotezleri açıkça cezalandırmak: **düzenlileştirme**. Polinomlar için katsayıların kareleri toplamı iyi bir düzenlileştirme fonksiyonudur. **Nitelik seçimi** de bir sadeleştirmedir (χ² budama bir tür nitelik seçimidir). **En kısa betimleme uzunluğu (MDL):** Hipotezi ve hatalarını bit cinsinden kodla, toplamı en küçükle.

### 4.3 Hiperparametre ayarı

Elle ayar; **ızgara araması** (bütün birleşimler; paralelleştirilebilir); **rastgele arama** (sürekli değerler için iyi); **Bayesçi en iyileme** (hiperparametre → doğrulama kaybı fonksiyonunu öğren; keşif–sömürü dengesi, üst güven sınırları, Gauss süreçleri); **popülasyon tabanlı eğitim** (genetik algoritma benzeri).

---

## 5. Öğrenme kuramı

**PAC öğrenme** (olasılıkla yaklaşık doğru): Tutarlı hipotezlerin hepsi, yüksek olasılıkla (≥ 1 − δ) gerçek fonksiyonun **ε-topu** içindedir (hata ≤ ε). "Çok yanlış" bir hipotezin N örnekle tutarlı olma olasılığı ≤ (1 − ε)ᴺ; birleşim sınırı ve 1 − ε ≤ e^(−ε) ile

```text
N ≥ (1/ε) (ln(1/δ) + ln |H|)                                   (19.1)
```

Bu **örnek karmaşıklığıdır**. Bütün Boolean fonksiyonlarında |H| = 2^(2ⁿ): Gereken örnek 2ⁿ gibi büyür, yani neredeyse bütün olası girdileri görmek gerekir. Kaçış yolları: önsel bilgi, basit hipotezleri tercih etmek, **öğrenilebilir alt uzaylara** odaklanmak.

**Karar listeleri:** Sırayla denenen testler (literal bağlaçları); tutan testin sonucu döndürülür. k-DL: Test başına en çok k literal. k-DT ⊆ k-DL. |k-DL(n)| ≤ 3^c c!, c = |Conj(n, k)| = O(nᵏ) → gereken örnek n'de **polinom**. DECISION-LIST-LEARNING: Örneklerin tek sınıflı bir alt kümesine uyan bir test bul, listeye ekle, o örnekleri çıkar.

Kitabın Şekil 19.10'daki liste (Patrons = Some → Yes; Patrons = Full ∧ Fri/Sat → Yes; değilse No) bir **gösterim örneğidir**; 12 örnekle tam tutarlı değildir (x5: Full, Cuma, ama No). Kodumuzun öğrendiği liste tutarlıdır.

---

## 6. Doğrusal regresyon ve sınıflandırma (`dogrusal_modeller.py`)

### 6.1 Tek değişkenli regresyon

h_w(x) = w₁x + w₀. Kare kayıp (Gauss'tan beri; gürültü normal dağılımlıysa en olası ağırlıkları verir) Σ (yⱼ − (w₁xⱼ + w₀))². Kısmi türevleri sıfırlayınca **kapalı biçim** (19.3). Kitabın Berkeley ev fiyatı örneğinde y = 0.232x + 246. Kayıp yüzeyi **dışbükeydir**: tek bir global en küçük.

### 6.2 Gradyan inişi

Ağırlık uzayında, kaybın en dik azaldığı yöne **öğrenme hızı** α ile adım at:

```text
w₀ ← w₀ + α Σ (y − h_w(x))          w₁ ← w₁ + α Σ (y − h_w(x)) x
```

- **Toplu gradyan inişi:** Her adımda bütün örnekler (bir tur = **epoch**).
- **Stokastik gradyan inişi (SGD):** Her adımda bir örnek ya da **mini toplu**. Kitabın örneği: N = 10 000, m = 100 → her adım 100 kat ucuz, standart hata yalnızca 10 kat artar.
- SGD'nin yakınsaması garanti değildir; zamanla azalan öğrenme hızı (benzetilmiş tavlamadaki gibi) garanti eder.

### 6.3 Çok değişkenli regresyon

h_w(x) = w · x (x₀ = 1 eklenerek). **Normal denklemler:** w* = (XᵀX)⁻¹Xᵀy (19.7). Çok boyutta aşırı uydurma riski artar → düzenlileştirme: Complexity = Σ|wᵢ|^q.

- **L₁ (q = 1):** **Seyrek** model; ilgisiz niteliklerin ağırlıkları tam sıfır olur (elmas biçimli bölge eksenlerde köşelidir). İlgisiz nitelik sayısına logaritmik örnek gerekir.
- **L₂ (q = 2):** Ağırlıkları küçültür ama sıfırlamaz; dönmeye göre değişmezdir.

### 6.4 Sert eşikli doğrusal sınıflandırıcı

**Karar sınırı**; doğrusal ise **doğrusal ayırıcı**, veri **doğrusal ayrılabilir**. Kitabın deprem/patlama örneği: x₂ = 1.7x₁ − 4.9, yani w = ⟨−4.9, 1.7, −1⟩; h_w(x) = Threshold(w · x). Gradyan neredeyse her yerde sıfır olduğundan **algılayıcı öğrenme kuralı**:

```text
wᵢ ← wᵢ + α (y − h_w(x)) xᵢ
```

Veri doğrusal ayrılabilirse yakınsar (kitapta 63 örnekte 657 adım). Ayrılabilir değilse salınır; azalan α ile en küçük hatalı çözüme yaklaşır.

### 6.5 Lojistik regresyon

Sert eşik yerine **lojistik fonksiyon** (sigmoid) 1/(1 + e^(−z)): türevlenebilir, çıktı bir olasılık. Kayıp L₂ ise güncelleme w ← w + α (y − h_w(x)) h_w(x)(1 − h_w(x)) x. Sınırın yakınındaki örnekler 0.5'e yakın olasılık alır; gürültülü ve ayrılamayan veride daha düzgün davranır.

---

## 7. Parametrik olmayan modeller (`parametrik_olmayan.py`)

**Parametrik model:** Sabit sayıda parametre; veri ne kadar çok olursa olsun aynı. **Parametrik olmayan:** Örnekleri (ya da bir kısmını) saklar; "örnek tabanlı / bellek tabanlı" öğrenme.

### 7.1 En yakın komşular

Sorgunun k en yakın komşusunun çoğunluk oyu (regresyonda ortalama ya da yerel regresyon). k = 1 aşırı uydurur; kitabın deprem verisinde k = 5 iyi.
- **Minkowski uzaklığı** L^p (p = 2 Öklid, p = 1 Manhattan; Boolean'da **Hamming**).
- Birimler değişince komşular değişir: Her boyutu **normalleştir** (ortalama 0, sapma 1). Kodumuzda bir boyutun birimi değişince doğruluk 0.84'ten 0.66'ya düşer, normalleştirince geri gelir.

**Boyutların laneti:** N nokta birim küpte düzgün; k komşuyu içeren komşuluğun kenarı ℓ = (k/N)^(1/n). k = 10, N = 10⁶: n = 2'de **0.003**, n = 3'te **%2**, n = 17'de **yarısı**, n = 200'de **%94**. Ayrıca dış %1'lik kabuktaki nokta oranı 1 boyutta %2, 200 boyutta %98'den fazla: Neredeyse her nokta bir uç değerdir.

### 7.2 k-d ağaçları ve LSH

**k-d ağacı:** Her düzeyde bir boyutta ortancaya göre böl. Sorgu kendi dalına iner; öbür dala yalnızca bölme düzlemi en iyi uzaklıktan yakınsa bakar. Örnek sayısı boyutun üstelinden (2ⁿ) çok olmalı: Binlerce örnekle ~10, milyonlarca örnekle ~20 boyuta kadar iyi.

**Yere duyarlı karıştırma (LSH):** Yakın noktaları aynı kovaya koyma olasılığı yüksek karma fonksiyonları; ℓ rastgele izdüşüm ve ℓ karma tablosu; adayların birleşiminde gerçek uzaklığa bak. **Yaklaşık** en yakın komşu; milyonlarca görüntüde pratik.

### 7.3 Parametrik olmayan regresyon

Noktaları birleştirmek, k-NN ortalaması (süreksiz), k-NN doğrusal regresyonu, **yerel ağırlıklı regresyon** (çekirdek ağırlıklı; genişlik bir hiperparametre). Uçlarda k-NN ortalaması içeri çekilir, yerel doğrusal regresyon eğilimi korur.

### 7.4 Destek vektör makineleri

2000'lerin başının en popüler yöntemi; üç çekici özelliği:
1. **En büyük marjlı ayırıcı:** Örneklere en uzak karar sınırı. **Marj:** ayırıcıdan en yakın örneğe uzaklığın iki katı. İyi genelleme.
2. **Çekirdek hilesi:** Doğrusal ayrılamayan veriyi daha yüksek boyuta gömmek.
3. **Parametrik olmayan ama seyrek:** Ayırıcıyı yalnızca **destek vektörleri** (sınıra en yakın örnekler) belirler.

Çözüm bir **ikinci dereceden programlama** problemidir; ikil biçimde veriler yalnızca iç çarpımlar xⱼ · xₖ olarak geçer.

**Çekirdek hilesi:** Çember içi/dışı veri doğrusal ayrılamaz. F(x) = (x₁², x₂², √2 x₁x₂) ile 3 boyutta ayrılır ve F(x) · F(z) = (x · z)²: Yüksek boyuttaki iç çarpım, düşük boyutta bir **çekirdek fonksiyonuyla** hesaplanır; F'yi hiç hesaplamaya gerek yok. **Polinom çekirdeği** (1 + x · z)^d; Mercer koşulunu sağlayan her fonksiyon bir çekirdektir. Merkezi orijinde olmayan bir çember için (x₁, x₂, x₁² + x₂²) özellikleri (sabit terimle birlikte) yeter (A9).

---

## 8. Topluluk öğrenmesi (`topluluk.py`)

Birden çok **temel modelin** tahminlerini birleştirmek. İki neden:
- **Yanlılığı azaltmak:** Topluluk, temel modellerden daha ifade gücüne sahip olabilir (üç doğrusal ayırıcı bir üçgen bölge tanımlar).
- **Varyansı azaltmak:** Bağımsız 5 sınıflandırıcı, her biri %75 doğru → çoğunluk oyu **%89**; 17 sınıflandırıcıyla **%99** (gerçekte bağımsız değiller, kazanç daha az).

| Yöntem | Fikir |
|---|---|
| **Torbalama** (bagging) | K **bootstrap** örneklemi (yerine koyarak), K model, oylama/ortalama. Varyansı azaltır; karar ağaçlarıyla sık kullanılır. Kodumuzda %15 etiket gürültüsünde test doğruluğu 0.72 → 0.79 |
| **Rastgele ormanlar** | Torbalama + her bölmede niteliklerin rastgele bir alt kümesi (ve **aşırı rastgele ağaçlar**). Aşırı uydurmaya dirençli, ayarı kolay |
| **Yığma** (stacking) | Farklı model sınıflarının tahminlerini girdi alan bir üst model (ör. ağırlıklı ortalama) |
| **Artırma** (boosting) | **Ağırlıklı eğitim kümesi:** Yanlış sınıflandırılan örneklerin ağırlığı artar; iyi hipotezler daha çok oy alır. **AdaBoost**, zayıf öğrenenleri (rastgeleden ε iyi) istenen doğruluğa çıkarır |
| **Gradyan artırma** | Her yeni ağaç kaybın gradyanı yönünde düzeltir (GBM, GBRT). Kitaba göre XGBoost, KDDCup'ta ilk 10 takımın hepsince kullanıldı |

**Karar kütüğü:** Tek testli ağaç. Kitapta restoran verisinde tek kütük %81'de kalırken AdaBoost (K = 5) %93'e çıkar; K = 20'de eğitim hatası sıfır olur, test doğruluğu yine de bir süre artar (Şekil 19.9(b)'deki davranış).

### 8.1 Çevrimiçi öğrenme

Veri i.i.d. değilse (zamanla değişiyorsa): Her adımda tahmin et, sonra doğruyu öğren. **Rastgele ağırlıklı çoğunluk:** K uzmanın ağırlığıyla orantılı rastgele birini seç; yanılan uzmanların ağırlığını β ile çarp.

```text
M < (M* ln(1/β) + ln K) / (1 − β)
```

M* en iyi uzmanın hatası. K = 10: β = 1/2 → **1.39 M* + 4.6**; β = 3/4 → **1.15 M* + 9.2**. Sınır her dizi için geçerlidir (düşmanca bile). β'yi uygun seçerek **pişmanlıksız öğrenme**: Deneme başına ortalama pişmanlık 0'a gider.

---

## 9. Makine öğrenmesi sistemi geliştirmek

1. **Problem tanımı:** Hangi kullanıcı, hangi amaç, hangi kayıp? Basit bir referans çözümle başla.
2. **Veri toplama, değerlendirme, yönetim:** İzinler, gizlilik, adalet (Bölüm 27). Veri akışlarını izle. **Veri artırma** (sınırlı veride), **dengesiz sınıflar** (dolandırıcılık: %99.99 doğruluk anlamsız; çoğunluğu **alt örnekle**, azınlığı **üst örnekle** ya da kayıpta ağırlıklandır), **uç değerler** (doğrusal regresyon hassas; log dönüşümü; ağaç toplulukları dayanıklı). Ön işleme: nicemleme, **one-hot kodlama**, **özellik mühendisliği** (tarihten "hafta sonu mu?"). **Keşifsel veri analizi** (Tukey).
3. **Model seçimi ve eğitim:** Tablo verisinde rastgele orman / gradyan artırma, görüntü ve konuşmada derin ağlar, az veride SVM. Sınıflandırmada **ROC eğrisi** ve **AUC**, **karışıklık matrisi**.
4. **Güven, yorumlanabilirlik, açıklanabilirlik:** Kaynak kontrolü, test, inceleme, **izleme**, **hesap verebilirlik**. **Yorumlanabilir** model: Modelin kendisine bakarak anlaşılır (karar ağaçları, doğrusal regresyon). **Açıklanabilir** model: Ayrı bir süreç "neden bu çıktı?" sorusunu yanıtlar (ör. LIME).
5. **İşletim, izleme, bakım:** Veri akışları ve dünya değiştikçe modeli izlemek ve yeniden eğitmek.

---

## Sık yapılan hatalar

| Yanılgı | Doğrusu |
|---|---|
| "Eğitim kümesinde mükemmel olan model iyidir." | Ölçü genellemedir; tam uydurma aşırı uydurma olabilir. |
| "Hiperparametreleri test kümesine bakarak ayarlamak sorun değil." | Test kümesi dolaylı olarak kirlenir; doğrulama kümesi ya da çapraz doğrulama kullan. |
| "Bilgi kazancı en yüksek nitelik her zaman en iyisidir." | Çok değerli niteliklerde (kimlik, posta kodu) yanıltır; kazanç oranı kullan. |
| "İyi nitelik yoksa ağacı büyütmeyi durdur." | XOR gibi birleşik etkileri kaçırır; kur ve sonra buda. |
| "Daha karmaşık model her zaman daha çok aşırı uydurur." | Bazı model sınıflarında doğrulama hatası interpolasyondan sonra yeniden düşer. |
| "L1 ve L2 düzenlileştirme aynı şeyi yapar." | L1 seyrek model verir; L2 yalnızca küçültür. |
| "k-NN her boyutta iyi çalışır." | Boyutların laneti: Yüksek boyutta "yakın" komşu yoktur. |
| "Niteliklerin birimleri önemsizdir." | Uzaklık tabanlı yöntemlerde birim değişimi sonucu değiştirir; normalleştir. |
| "Topluluk her zaman daha iyidir." | Modeller birbirinin aynısıysa (ilişkiliyse) kazanç azdır; çeşitlilik gerekir. |

## Kendini yokla

1. Denetimli, denetimsiz ve pekiştirmeli öğrenme arasındaki fark nedir?
2. Restoran verisinde Kazanç(Patrons) neden Kazanç(Type)'dan büyüktür?
3. LEARN-DECISION-TREE'nin dört durumu nelerdir? "Örnek kalmadı" durumunda neden ebeveynin çoğunluğu döndürülür?
4. χ² budamada sıfır hipotezi nedir?
5. Neden üç ayrı veri kümesi gerekir?
6. PAC sınırı N ≥ (1/ε)(ln(1/δ) + ln|H|) neyi garanti eder?
7. Toplu ve stokastik gradyan inişini karşılaştır.
8. L1 düzenlileştirme neden seyrek modeller üretir?
9. Boyutların laneti k-NN'yi nasıl etkiler?
10. Çekirdek hilesi neden "hile"dir?
11. AdaBoost örnek ağırlıklarını nasıl değiştirir?

## Kod rehberi

```bash
python ornekler/karar_agaci.py        # restoran: entropi, kazanç, Şekil 19.6 ağacı, χ², karar listesi, öğrenme eğrisi
python ornekler/model_secimi.py       # çapraz doğrulamayla polinom derecesi, kayıplar, PAC, boyutların laneti
python ornekler/dogrusal_modeller.py  # regresyon (kapalı biçim, gradyan inişi), L1/L2, algılayıcı, lojistik
python ornekler/parametrik_olmayan.py # k-NN, normalleştirme, k-d ağacı, yerel regresyon, SVM, çekirdek hilesi
python ornekler/topluluk.py           # çoğunluk oyu, AdaBoost, torbalama, rastgele ağırlıklı çoğunluk
python cozumler/alistirma_kod.py      # A3–A6, A8–A10
```

## Terimler

| Türkçe | İngilizce | Kısa açıklama |
|---|---|---|
| tümevarım | induction | Örneklerden genel kural |
| sınıflandırma / regresyon | classification / regression | Ayrık / sayısal çıktı |
| denetimli / denetimsiz / pekiştirmeli öğrenme | supervised / unsupervised / reinforcement learning | Geri bildirim türleri |
| etiket | label | Örneğin doğru çıktısı |
| kümeleme | clustering | Benzer örnekleri gruplamak |
| hipotez / hipotez uzayı | hypothesis / hypothesis space | Öğrenilen fonksiyon / adaylar |
| model sınıfı | model class | Hipotez uzayının diğer adı |
| temel gerçek | ground truth | Gerçek çıktı |
| tutarlı hipotez | consistent hypothesis | Bütün eğitim örneklerine uyan |
| genelleme | generalization | Görülmemiş örneklerdeki başarı |
| eksik / aşırı uydurma | underfitting / overfitting | Çok basit / ezberleyen model |
| yanlılık / varyans | bias / variance | Sistematik sapma / veri kümesine duyarlılık |
| Ockham'ın usturası | Ockham's razor | En basit tutarlı hipotez |
| karar ağacı | decision tree | Nitelik testleriyle karar |
| olumlu / olumsuz örnek | positive / negative example | Boolean sınıflandırmada |
| çoğunluk değeri | plurality value | En sık çıktı |
| öğrenme eğrisi | learning curve | Örnek sayısına göre doğruluk |
| entropi | entropy | Belirsizlik ölçüsü (bit) |
| bilgi kazancı | information gain | Entropideki beklenen azalma |
| kazanç oranı | gain ratio | Kazanç / bölünme bilgisi |
| karar ağacı budama | decision tree pruning | İlgisiz testleri kaldırmak |
| χ² budama | χ² pruning | İstatistiksel anlamlılıkla budama |
| sıfır hipotezi | null hypothesis | "Örüntü yok" varsayımı |
| erken durdurma | early stopping | Bölmeyi erken bitirmek |
| bölme noktası | split point | Sürekli nitelikte eşik testi |
| regresyon ağacı / CART | regression tree / CART | Sayısal çıktılı ağaç |
| durağanlık / i.i.d. | stationarity / i.i.d. | Örnekler bağımsız ve özdeş dağılımlı |
| hata oranı | error rate | Yanlış tahmin oranı |
| eğitim / doğrulama / test kümesi | training / validation / test set | Üç ayrı veri |
| hiperparametre | hyperparameter | Model sınıfının ayarı |
| k katlı çapraz doğrulama | k-fold cross-validation | Dönüşümlü doğrulama |
| birini dışarıda bırak | leave-one-out (LOOCV) | k = N |
| model seçimi / en iyileme | model selection / optimization | Uzayı seçmek / içinde aramak |
| interpolasyon | interpolation | Eğitim verisini tam uydurma |
| kayıp fonksiyonu | loss function | Yanlış tahminin bedeli |
| genelleme / ampirik kayıp | generalization / empirical loss | Beklenen / örnekteki kayıp |
| gerçekleştirilebilir | realizable | f, H içinde |
| düzenlileştirme | regularization | Karmaşıklık cezası |
| nitelik seçimi | feature selection | İlgisiz nitelikleri atmak |
| en kısa betimleme uzunluğu | minimum description length (MDL) | Bit cinsinden toplam uzunluk |
| ızgara / rastgele arama | grid / random search | Hiperparametre arama |
| Bayesçi en iyileme | Bayesian optimization | Kayıp fonksiyonunu öğrenerek arama |
| PAC öğrenme | probably approximately correct learning | (ε, δ) garantili öğrenme |
| örnek karmaşıklığı | sample complexity | Gereken örnek sayısı |
| karar listesi | decision list | Sıralı testler |
| doğrusal regresyon | linear regression | Doğrusal fonksiyon uydurma |
| ağırlık uzayı | weight space | Parametrelerin uzayı |
| gradyan inişi | gradient descent | Kaybın tersine adım |
| öğrenme hızı | learning rate | Adım büyüklüğü α |
| toplu / stokastik / mini toplu | batch / stochastic / minibatch | Adımda kullanılan örnek sayısı |
| tur | epoch | Bütün verinin bir geçişi |
| normal denklemler | normal equations | (XᵀX)⁻¹Xᵀy |
| seyrek model | sparse model | Çok ağırlığı sıfır |
| karar sınırı / doğrusal ayırıcı | decision boundary / linear separator | Sınıfları ayıran yüzey |
| doğrusal ayrılabilir | linearly separable | Bir doğruyla ayrılabilen |
| algılayıcı öğrenme kuralı | perceptron learning rule | Hata varsa ağırlığı düzelt |
| lojistik regresyon | logistic regression | Sigmoid çıkışlı sınıflandırıcı |
| parametrik olmayan model | nonparametric model | Örnekleri saklayan model |
| k en yakın komşu | k-nearest neighbors | Komşuların oyu |
| Minkowski / Hamming uzaklığı | Minkowski / Hamming distance | Uzaklık ölçüleri |
| normalleştirme | normalization | Boyutları aynı ölçeğe getirmek |
| boyutların laneti | curse of dimensionality | Yüksek boyutta komşuluk kaybı |
| k-d ağacı | k-d tree | Boyut boyut bölen ağaç |
| yere duyarlı karıştırma | locality-sensitive hashing (LSH) | Yaklaşık en yakın komşu |
| yerel ağırlıklı regresyon | locally weighted regression | Çekirdekle ağırlıklı yerel model |
| destek vektör makinesi | support vector machine (SVM) | En büyük marjlı ayırıcı |
| marj / destek vektörü | margin / support vector | Ayırıcının boşluğu / sınırdaki örnek |
| çekirdek fonksiyonu / hilesi | kernel function / trick | Yüksek boyuttaki iç çarpımı hesaplamak |
| topluluk öğrenmesi | ensemble learning | Modelleri birleştirmek |
| torbalama / bootstrap | bagging / bootstrap | Yerine koyarak örneklemle topluluk |
| rastgele orman | random forest | Rastgele nitelikli ağaç topluluğu |
| yığma | stacking | Modellerin üstüne model |
| artırma / AdaBoost | boosting / AdaBoost | Ağırlıklı örneklerle ardışık modeller |
| karar kütüğü | decision stump | Tek testli ağaç |
| gradyan artırma | gradient boosting | Gradyan yönünde ağaç ekleme |
| çevrimiçi öğrenme | online learning | Veri akarken öğrenme |
| rastgele ağırlıklı çoğunluk | randomized weighted majority | Uzman ağırlıklarıyla tahmin |
| pişmanlıksız öğrenme | no-regret learning | Ortalama pişmanlık → 0 |
| veri artırma | data augmentation | Yapay örnek üretmek |
| alt / üst örnekleme | undersampling / oversampling | Sınıf dengesi |
| uç değer | outlier | Diğerlerinden çok farklı örnek |
| one-hot kodlama | one-hot encoding | Kategoriyi Boolean vektöre çevirme |
| özellik mühendisliği | feature engineering | Yararlı nitelik üretmek |
| keşifsel veri analizi | exploratory data analysis | Veriyi görselleştirip incelemek |
| ROC eğrisi / AUC | ROC curve / AUC | Duyarlılık–yanlış alarm dengesi |
| karışıklık matrisi | confusion matrix | Gerçek × tahmin tablosu |
| yorumlanabilirlik / açıklanabilirlik | interpretability / explainability | Modelden / ayrı süreçten anlamak |
