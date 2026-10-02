# Bölüm 21 — Derin öğrenme

> **Kitapta:** AIMA 4. baskı, Bölüm 21 *"Deep Learning"*.
> Önce kitabı oku, sonra bu notlarla pekiştir. Metin özgündür; kitaptan alıntı yoktur.
> Kodlar yalnızca numpy kullanır: Amaç çerçeve öğrenmek değil, mekanizmayı görmek.

## Bu bölümün haritası

| Kitap alt bölümü | Bu nottaki karşılığı | Kod |
|---|---|---|
| 21.1 Simple Feedforward Networks | §1 Birimler, aktivasyonlar, hesap grafiği, geri yayılım | `hesap_grafigi.py` |
| 21.2 Computation Graphs for Deep Learning | §2 Girdi kodlama, çıktı katmanları, kayıplar, gizli katmanlar | `hesap_grafigi.py` |
| 21.3 Convolutional Networks | §3 Evrişim, adım, alıcı alan, havuzlama, tensörler, artık ağlar | `cnn.py` |
| 21.4 Learning Algorithms | §4 SGD, momentum, hesap grafiğinde gradyan, toplu normalleştirme | `mlp_egitim.py` |
| 21.5 Generalization | §5 Mimari seçimi, mimari arama, ağırlık bozunumu, dropout | `mlp_egitim.py` |
| 21.6 Recurrent Neural Networks | §6 RNN, zamanda geri yayılım, LSTM | `rnn.py` |
| 21.7 Unsupervised Learning and Transfer Learning | §7 PPCA, otokodlayıcılar, VAE, otoregresif modeller, GAN, aktarım | `otokodlayici.py` |
| 21.8 Applications | §8 Görme, dil, pekiştirmeli öğrenme | — |

## Öğrenme hedefleri

1. Bir ileri beslemeli ağı hesap grafiği olarak yazmak; geri yayılımı zincir kuralıyla türetmek.
2. Aktivasyon fonksiyonlarını, softmax'ı ve çapraz entropi kaybını açıklamak.
3. Evrişim, adım, dolgu, alıcı alan ve havuzlamayı hesaplamak; parametre paylaşımının etkisini göstermek.
4. Kaybolan gradyanın nedenini ve artık bağlantılar, ReLU, toplu normalleştirme, LSTM gibi çarelerini açıklamak.
5. Ağırlık bozunumu ve dropout'un ne yaptığını açıklamak.
6. Doğrusal otokodlayıcı ile PCA arasındaki ilişkiyi göstermek; üretici modelleri (VAE, GAN, otoregresif) tanımak.

---

## Büyük resim

**Derin öğrenme:** Uzun hesap yolları olan, ayarlanabilir ağırlıklı devrelerle öğrenme. Bölüm 19'daki doğrusal ve lojistik regresyon tek katmanlıydı; girdiden çıktıya kısa yollar karmaşık etkileşimleri temsil edemez. Karar ağaçları uzun yollar kurabilir ama girdinin yalnızca küçük bir kısmına bakar. Derin ağlar ikisini birleştirir: **her** girdi değişkeni uzun yollar üzerinden çıktıyı etkileyebilir. Görme, konuşma, çeviri gibi yüksek boyutlu verilerde baskın yöntemdir.

---

## 1. Basit ileri beslemeli ağlar (`hesap_grafigi.py`)

**İleri beslemeli ağ:** Yönlü döngüsüz graf; bilgi girdiden çıktıya akar, iç durum yok. **Yinelemeli ağ** ise çıktılarını girdisine geri besler (§6).

**Birim:** aⱼ = gⱼ(Σᵢ wᵢ,ⱼ aᵢ) = gⱼ(inⱼ); w₀,ⱼ ağırlıklı, değeri +1 olan kukla girdi sabit terimi sağlar. Vektör biçiminde aⱼ = gⱼ(wᵀx).

**Doğrusal olmama şart:** Doğrusal birimlerin bileşimi yine doğrusaldır. **Evrensel yaklaşım teoremi:** İki katmanlı (ilki doğrusal olmayan, ikincisi doğrusal) bir ağ, her sürekli fonksiyona istenen doğrulukta yaklaşabilir; ama bunun için üstel büyüklükte olabilir (her yerde bir "tümsek").

| Aktivasyon | Formül | Not |
|---|---|---|
| Sigmoid (lojistik) | σ(x) = 1/(1 + e⁻ˣ) | Lojistik regresyondaki gibi |
| ReLU | max(0, x) | En yaygın |
| Softplus | log(1 + eˣ) | ReLU'nun pürüzsüz hâli; türevi sigmoid |
| tanh | (e²ˣ − 1)/(e²ˣ + 1) | Aralığı (−1, 1); tanh(x) = 2σ(2x) − 1 |

Hepsi tekdüze azalmayan, yani türevleri negatif değil.

**Şekil 21.3'teki ağ:** 2 girdi, 2 gizli birim (3, 4), 1 çıktı (5):

```text
ŷ = g5(w0,5 + w3,5 g3(w0,3 + w1,3 x1 + w2,3 x2) + w4,5 g4(w0,4 + w1,4 x1 + w2,4 x2))     (21.2)
h_w(x) = g⁽²⁾(W⁽²⁾ g⁽¹⁾(W⁽¹⁾ x))                                                       (21.3)
```

**Hesap grafiği (veri akış grafiği):** Her düğüm temel bir işlem; girdiler ve ayarlanabilir ağırlıklar ayrı düğümler. Her katmanın her birimi sonraki katmanın her birimine bağlıysa **tam bağlı**.

### 1.1 Gradyanlar ve öğrenme

L₂ kaybı (y − ŷ)² için zincir kuralı:

```text
∂L/∂w3,5 = −2(y − ŷ) g5'(in5) a3                                   (21.4)
∂L/∂w1,3 = −2(y − ŷ) g5'(in5) w3,5 g3'(in3) x1                     (21.5)
```

Δ₅ = 2(ŷ − y) g5'(in5) çıktıdaki "algılanan hata"dır; Δ₃ = Δ₅ w3,5 g3'(in3) bu hatanın gizli birime **geri yayılmış** payıdır. Gradyan = Δ × girdi. Kodumuz bu formüllerle hesaplanan gradyanları sonlu farklarla birebir doğrular.

**Kaybolan gradyan:** Geri yayılan sinyal her katmanda g'(in) ile çarpılır. Sigmoid'in türevi en çok 1/4; doyumda neredeyse 0. Derin ağda gradyan üstel küçülür (kodumuzda 20 sigmoid katmanda ~10⁻¹³). Ağırlıklar büyükse **patlayan gradyan** olur.

---

## 2. Derin öğrenme için hesap grafikleri

### 2.1 Girdi kodlama

Boolean: 0/1 (bazen −1/+1). Sayısal: olduğu gibi ya da ölçeklenerek. Kategorik (d değer): **one-hot** kodlama (d bit, biri 1). Görüntüler: piksel ızgarası, sıradan bir vektör gibi değil, komşuluğu koruyarak (§3).

### 2.2 Çıktı katmanları ve kayıp fonksiyonları

Olasılıksal yorum: Ağ P_w(y | x)'i tanımlar; ağırlıklar **negatif log olabilirliği** en küçükler:

```text
w* = argmin_w −Σⱼ log P_w(yⱼ | xⱼ)                       (21.6)
```

Derin öğrenmede bu **çapraz entropi kaybı** olarak anılır: H(P, Q) = −Σ P(z) log Q(z) = H(P) + D_KL(P ‖ Q). (Uzaklık değildir: H(P, P) = H(P) ≠ 0.) P sabitken çapraz entropiyi en küçüklemek KL ıraksamasını en küçüklemektir.

| Çıktı | Katman | Kayıp |
|---|---|---|
| Boolean | sigmoid | ikili çapraz entropi |
| Çok sınıflı | **softmax**: e^{inₖ} / Σ e^{inₖ'} | çapraz entropi |
| Sayısal | doğrusal (Gauss ortalaması) | kare hata (= sabit varyanslı Gauss'un negatif log olabilirliği) |
| Çok kipli sayısal | Gauss karışımı parametreleri | karışımın log olabilirliği |

Softmax farkları büyütür: ⟨5, 2, 0, −2⟩ → ⟨0.946, 0.047, 0.006, 0.001⟩. d = 2'de sigmoid'e indirgenir.

### 2.3 Gizli katmanlar

Gizli katmanlar girdinin **iç temsillerini** öğrenir; derin katmanlar giderek soyutlaşan özellikler (kenar → doku → nesne parçası). ReLU ve softplus kaybolan gradyanı azalttığı için yaygın. Aynı ağırlık sayısında derin ağlar çoğu zaman sığ ve geniş ağlardan daha iyi genelleştirir (kitaptaki Şekil 21.7'de 11 katmanlı ağ 3 katmanlıdan belirgin biçimde iyi).

---

## 3. Evrişimli ağlar (`cnn.py`)

Görüntüyü düz vektör saymak komşuluğu ve **uzamsal değişmezliği** (kedi görüntünün neresinde olursa olsun kedidir) kaybettirir. Çözüm: **yerel bağlantılar** ve **paylaşılan ağırlıklar**. Birçok yerel bölgede tekrarlanan ağırlık örüntüsü bir **çekirdektir**; uygulanmasına **evrişim** denir (sinyal işlemedeki adıyla çapraz ilinti).

```text
zᵢ = Σⱼ kⱼ x_{j+i−(l+1)/2}                                (21.8)
```

Kitaptaki Şekil 21.4: x = ⟨5, 6, 6, 2, 5, 6, 5⟩, çekirdek ⟨+1, −1, +1⟩ (koyu bir noktayı bulur), **adım** s = 2 → ⟨5, 9, 4⟩; en güçlü yanıt koyu piksel (2) üzerinde. Aynı işlem, çekirdeğin her satırda kaydırılarak yer aldığı bir matrisle çarpımdır (21.9).

- Adım s çıktıyı ~n/s'ye küçültür; **dolgu** ile kenarlarda da uygulanır. Çıktı boyutu ⌊(n + 2p − l)/s⌋ + 1.
- Bir katmanda d çekirdek → d **kanal** (özellik haritası).
- **Alıcı alan:** Bir birimi etkileyebilen girdi bölgesi. İlk katmanda l piksel; adım 1'de k. katmanda k(l − 1) + 1. Derin birimler büyük bölgeleri "görür".
- **Parametre paylaşımı:** 256 × 256 × 3'ten aynı boyutta 32 kanala tam bağlı katman ~4 × 10¹¹ ağırlık, 5 × 5 evrişim 2432.

### 3.1 Havuzlama

- **Ortalama havuzlama:** l girdinin ortalaması (1/l çekirdekli evrişim); adım l ile **alt örnekleme**, ölçek değişmezliği.
- **En büyük havuzlama:** En büyük değer; "bu bölgede özellik var mı?" (mantıksal VEYA gibi).
Sınıflandırmada son katman softmax; arada evrişim ve havuzlama katmanları boyutu küçültür; sonda bir iki tam bağlı katman.

### 3.2 Tensörler

Görüntü katmanları **tensörlerdir** (ör. genişlik × yükseklik × kanal; mini toplu ile bir boyut daha). Tensör işlemleri GPU/TPU'da verimli paralel hesaplanır.

### 3.3 Artık ağlar

Her katman temsili baştan kurmak yerine bir öncekini **düzeltsin**:

```text
z⁽ⁱ⁾ = g_r(z⁽ⁱ⁻¹⁾ + f(z⁽ⁱ⁻¹⁾))                            (21.10)
```

f "artık"tır (genelde bir doğrusal olmayan katman + bir doğrusal katman). ReLU'lu artık ağda ağırlıklar sıfırsa katman girdiyi aynen geçirir; bilgi ve gradyan derinlikte kaybolmaz. Yüzlerce katmanlı ağlar mümkün olur. Kodumuzda 30 katmanlı sigmoid ağda ilk katmanın gradyanı düz yapıda ~10⁻¹⁹, artık yapıda ~4.

---

## 4. Öğrenme algoritmaları (`mlp_egitim.py`)

**SGD:** w ← w − α ∇_w L(w). Mini toplu: Rastgele m örneğin gradyanı. Küçük m: ucuz adımlar ve yerel en küçüklerden kaçmaya yardım eden gürültü (benzetilmiş tavlama gibi). m genelde donanımın paralelliğini dolduracak biçimde seçilir.
- Azalan **öğrenme hızı** yakınsamaya yardım eder (çizelge deneme yanılmayla).
- **Momentum:** Geçmiş gradyanların yürüyen ortalaması; küçük mini toplu gürültüsünü dengeler.
- Sayısal sorunlar: taşma, alt taşma, yuvarlama.

**Hesap grafiğinde gradyan:** Geri yayılım, grafiği çıktıdan girdiye geri gezerek her düğümün gradyanını çocuklarının gradyanlarından hesaplar (bir düğüm birden çok yere bağlıysa gradyanlar toplanır). Otomatik türev alma; bütün modern çerçeveler bunu yapar. İleri geçişteki ara değerler saklanmalıdır (bellek maliyeti).

**Toplu normalleştirme:** Bir katmandaki değerleri mini toplu içinde standartlaştır:

```text
ẑᵢ = γ (zᵢ − μ) / √(ε + σ²) + β
```

γ ve β öğrenilir. Yakınsamayı hızlandırır; derin ağlarda değerlerin sönmesini ya da patlamasını önler; etkisi artık bağlantılara benzer. Önceki katmanın ağırlıklarının ölçeğine duyarsızdır (A9).

---

## 5. Genelleme

### 5.1 Mimari seçimi ve arama

Mimari, problemin yapısına uymalı: görüntüde evrişim, dizide RNN. Derinlik genişlikten genellikle daha değerlidir. **Çekişmeli örnekler:** Gözle fark edilmeyecek küçük girdi değişiklikleri sınıflandırmayı değiştirebilir; ağların girdi–çıktı eşlemeleri süreksiz olabilir.

**Sinir mimarisi araması (NAS):** Mimari uzayında arama (evrimsel algoritmalar, pekiştirmeli öğrenme, gradyan tabanlı yöntemler). Her adayı tam eğitmek pahalıdır; daha küçük veri, daha az tur ya da mimarinin değerini tahmin eden bir model kullanılır.

### 5.2 Ağırlık bozunumu

Kayba λ Σ W²ᵢⱼ ekle (λ ≈ 10⁻⁴ yaygın). Bölüm 19'daki L₂ düzenlileştirmenin karşılığı. Sigmoid ağlarda ağırlıkları doyumdan uzak tutar; ReLU ve artık ağlarda etkisi farklı ama yine yararlı. Bir yorum: Ağırlıklar üzerinde sıfır ortalamalı Gauss önseliyle **MAP öğrenme** (Bölüm 20).

### 5.3 Dropout

Her eğitim adımında birimlerin bir kısmını rastgele kapat: Gizli birimlerde tutma olasılığı p = 0.5, girdi birimlerinde p = 0.8 en etkili. Test zamanında dropout yok (ağırlıklar ölçeklenir; kodumuzda "ters dropout" ile eğitim sırasında 1/p ile ölçeklenir, beklenen değer korunur). Yorumlar:
- Paylaşılan ağırlıklı **çok büyük bir inceltilmiş ağ topluluğuna** yaklaşır (n birimde 2ⁿ alt ağ; torbalama gibi).
- Birimler başka birimlere aşırı güvenemez; her biri tek başına yararlı olmalı.
- Gürültüye ve hasara dayanıklı, çoklu açıklamalar öğrenilir (yüzde "burun birimi" kapansa bile yüz tanınmalı).

---

## 6. Yinelemeli sinir ağları (`rnn.py`)

Dizi verisi (dil, konuşma, zaman serisi) için: Gizli durum zₜ bir önceki durumu ve yeni girdiyi alır; **aynı ağırlıklar** her adımda kullanılır (zamanda değişmezlik). Bir RNN, Bölüm 14'teki HMM/DBN'lerin "öğrenilmiş geçiş modeli" gibidir; Markov varsayımı gizli durumun içinde.

```text
zₜ = g_z(W_zz zₜ₋₁ + W_xz xₜ)          ŷₜ = g_y(W_zy zₜ)
```

**Zamanda geri yayılım (BPTT):** Ağ zamanda açılır; gradyan her adımda W_zz ve g' ile çarpılır. W_zz'nin en büyük özdeğeri 1'den küçükse gradyan geçmişe doğru üstel küçülür, büyükse patlayabilir. Kodumuzda spektral yarıçap 0.5 iken 40 adım geriye gradyan ~10⁻¹⁴. Sonuç: Uzun vadeli bağımlılıklar zor öğrenilir.

**LSTM (uzun kısa süreli bellek):** Bir **bellek hücresi** c ve öğrenilen **kapılar**:
- **Unutma kapısı** f: Hücredeki bilginin ne kadarı tutulacak.
- **Girdi kapısı** i: Yeni bilginin ne kadarı eklenecek.
- **Çıktı kapısı** o: Hücrenin ne kadarı çıktıya gidecek.

cₜ = fₜ ⊙ cₜ₋₁ + iₜ ⊙ c̃ₜ. f ≈ 1 iken bilgi (ve gradyan) uzun süre kayıpsız korunur: ∂cₜ/∂cₜ₋ₖ = Π f. Kapılar, ne zaman hatırlayıp ne zaman unutacağını veriden öğrenir.

---

## 7. Denetimsiz öğrenme ve aktarım öğrenmesi (`otokodlayici.py`)

Etiketli veri pahalı, etiketsiz veri bol. Üç yaklaşım: **denetimsiz**, **aktarım**, **yarı denetimli** öğrenme.

**Denetimsiz öğrenmenin hedefleri:** Yeni temsiller (özellikler) öğrenmek ve üretici modeller kurmak (P(x) ya da P(x, z)).

- **Olasılıksal PCA (PPCA):** z ~ N(0, I), x = Wz + N(0, σ²I). Veri üretmek kolay; EM ile öğrenilir. Kodumuzda 10 boyutlu ama gerçekte 2 boyutlu veride kovaryansın iki büyük özdeğeri ortaya çıkar.
- **Otokodlayıcı:** Kodlayıcı f: x → z, kod çözücü g: z → x̂; x̂ ≈ x olacak biçimde eğitilir. z dar bir boğazsa veriyi sıkıştırmayı öğrenir. **Doğrusal otokodlayıcı PCA ile yakından ilişkilidir:** Öğrendiği alt uzay en büyük özdeğerlerin özvektörlerinin gerdiği alt uzaydır. Kodumuzda iki alt uzay arasındaki açılar 0°; yeniden kurma hatası atılan özdeğerlerin toplamına eşit.
- **Değişimsel otokodlayıcı (VAE):** Sonsalı bir **değişimsel sonsal** Q ile yaklaşıklar ve **kanıt alt sınırını (ELBO)** en büyükler: L = log P(x) − D_KL(Q ‖ P(z | x)). Kodlayıcı Q'yu, kod çözücü P(x | z)'yi tanımlar.
- **Derin otoregresif modeller:** Her xᵢ öncekilere koşullu; doğrusal–Gauss yerine derin ağ (ses üretimi gibi).
- **Üretici çekişmeli ağlar (GAN):** **Üretici** z'den x üretir, **ayırt edici** gerçek ile üretileni ayırmaya çalışır; ikisi birlikte eğitilir. Çok gerçekçi görüntüler üretebilir.
- **Denetimsiz çeviri:** Eşleşmemiş iki görüntü kümesi arasında dönüşüm.

**Aktarım öğrenmesi:** Bir görevde (ör. ImageNet sınıflandırma) eğitilmiş ağın erken katmanlarını başka bir görev için yeniden kullan; üst katmanları yeni veriyle **ince ayar** yap (erken katmanları dondurarak). Dilde büyük metinlerde önceden eğitilmiş modeller ve kelime gömmeleri (Bölüm 24). **Çok görevli öğrenme:** Bir ağı birden çok görevde birlikte eğitmek ortak temsiller öğretir.

---

## 8. Uygulamalar

- **Görme:** 2012 ImageNet yarışmasında (1.2 milyon görüntü, 1000 sınıf) AlexNet ilk 5 hata oranını %15.3'e indirdi (sonraki en iyi > %25). O zamandan beri ilk 5 hata %2'nin altına indi; eğitimli bir insanın hatası ~%5.
- **Doğal dil işleme:** Uçtan uca derin öğrenmeyle çeviri; kitaba göre Wu ve ark. (2016) çeviri hatalarını önceki yaklaşıma göre %60 azalttı (Bölüm 24).
- **Pekiştirmeli öğrenme:** Değer fonksiyonlarını ve politikaları derin ağlarla temsil etmek: DeepMind'ın Atari oynayan DQN'i, AlphaGo (Bölüm 22).

---

## Sık yapılan hatalar

| Yanılgı | Doğrusu |
|---|---|
| "Doğrusal birimlerden derin ağ kurmak gücü artırır." | Doğrusal katmanların bileşimi doğrusaldır; doğrusal olmama şarttır. |
| "Evrensel yaklaşım teoremi iki katmanın yeteceğini söyler." | Yeter ama üstel büyüklükte olabilir; derinlik çoğu zaman çok daha verimlidir. |
| "Çapraz entropi bir uzaklıktır." | H(P, P) = H(P) ≠ 0; uzaklık olan KL ıraksamasıdır. |
| "Evrişim her piksel için ayrı ağırlık öğrenir." | Aynı çekirdek her yerde paylaşılır; parametre sayısı küçüktür. |
| "Derin ağlar doğal olarak eğitilir." | Kaybolan/patlayan gradyan: ReLU, artık bağlantılar, toplu normalleştirme, iyi başlangıç gerekir. |
| "Dropout test zamanında da açıktır." | Yalnızca eğitimde; testte ölçek düzeltilir. |
| "RNN istediği kadar geçmişi hatırlar." | BPTT gradyanı üstel küçülür; uzun bağımlılıklar için LSTM gibi kapılı birimler. |
| "Otokodlayıcı PCA'dan bambaşka bir şeydir." | Doğrusal otokodlayıcı PCA'nın alt uzayını öğrenir; derin otokodlayıcılar doğrusal olmayan genellemesidir. |

## Kendini yokla

1. Şekil 21.3'teki ağ için ŷ'yi ağırlıklar ve girdiler cinsinden yaz. ∂L/∂w1,3'ü türet.
2. Softmax neden çok sınıflı çıktılar için uygundur? d = 2'de neye indirgenir?
3. Çapraz entropiyi en küçüklemek neden en büyük olabilirliğe denktir?
4. x = ⟨5, 6, 6, 2, 5, 6, 5⟩ ve çekirdek ⟨+1, −1, +1⟩ ile adım 2'de evrişim nedir?
5. Alıcı alan derinlikle nasıl büyür? Havuzlama buna nasıl katkı yapar?
6. Artık bağlantı kaybolan gradyanı nasıl önler?
7. Toplu normalleştirme ne yapar?
8. Dropout neden bir topluluk yöntemi gibi düşünülebilir?
9. BPTT'de gradyan neden üstel küçülür? LSTM bunu nasıl çözer?
10. Doğrusal otokodlayıcı ile PCA arasındaki ilişki nedir?

## Kod rehberi

```bash
python ornekler/hesap_grafigi.py  # aktivasyonlar, Şekil 21.3 ağı, geri yayılım = sayısal gradyan, softmax, kaybolan gradyan
python ornekler/cnn.py            # Şekil 21.4 evrişimi (5, 9, 4), matris biçimi, alıcı alan, havuzlama, artık katman
python ornekler/mlp_egitim.py     # numpy MLP: XOR, ağırlık bozunumu, dropout, toplu normalleştirme, artık bağlantı
python ornekler/rnn.py            # BPTT'de kaybolan gradyan, hatırlama görevi, LSTM bellek çarpanı
python ornekler/otokodlayici.py   # PPCA verisi, doğrusal otokodlayıcı = PCA alt uzayı
python cozumler/alistirma_kod.py  # A2–A10
```

## Terimler

| Türkçe | İngilizce | Kısa açıklama |
|---|---|---|
| derin öğrenme | deep learning | Uzun hesap yollu devrelerle öğrenme |
| ileri beslemeli / yinelemeli ağ | feedforward / recurrent network | Döngüsüz / geri beslemeli |
| birim | unit | Ağırlıklı toplam + aktivasyon |
| aktivasyon fonksiyonu | activation function | Doğrusal olmayan g |
| sigmoid / ReLU / softplus / tanh | sigmoid / ReLU / softplus / tanh | Yaygın aktivasyonlar |
| evrensel yaklaşım teoremi | universal approximation theorem | İki katman her sürekli fonksiyona yaklaşır |
| hesap (veri akış) grafiği | computation (dataflow) graph | İşlemlerin grafı |
| tam bağlı | fully connected | Her birim sonraki her birime bağlı |
| çıktı / gizli katman | output / hidden layer | Son / ara katmanlar |
| geri yayılım | back-propagation | Hatanın geri dağıtılması |
| kaybolan / patlayan gradyan | vanishing / exploding gradient | Derinlikte üstel küçülme / büyüme |
| one-hot kodlama | one-hot encoding | Tek biti 1 olan vektör |
| negatif log olabilirlik | negative log likelihood | Olasılıksal kayıp |
| çapraz entropi | cross-entropy | H(P, Q) |
| Kullback–Leibler ıraksaması | Kullback–Leibler divergence | D_KL(P ‖ Q) |
| softmax | softmax | Olasılık vektörü üreten katman |
| evrişimli sinir ağı | convolutional neural network (CNN) | Yerel, paylaşılan ağırlıklı ağ |
| çekirdek / evrişim | kernel / convolution | Paylaşılan ağırlık örüntüsü / uygulanması |
| adım / dolgu | stride / padding | Çekirdek kaydırma aralığı / kenar ekleme |
| alıcı alan | receptive field | Birimi etkileyen girdi bölgesi |
| havuzlama (ortalama / en büyük) | pooling (average / max) | Alt örnekleme |
| alt örnekleme | downsampling | Boyutu küçültme |
| tensör | tensor | Çok boyutlu dizi |
| artık ağ | residual network | Katman girdiyi düzeltir: z + f(z) |
| stokastik gradyan inişi | stochastic gradient descent | Mini toplu gradyanla adım |
| momentum | momentum | Gradyanların yürüyen ortalaması |
| toplu normalleştirme | batch normalization | Mini toplu içinde standartlaştırma |
| sinir mimarisi araması | neural architecture search | Mimari uzayında arama |
| çekişmeli örnek | adversarial example | Sınıflandırmayı bozan küçük değişiklik |
| ağırlık bozunumu | weight decay | λ Σ W² cezası |
| dropout | dropout | Eğitimde rastgele birim kapatma |
| zamanda geri yayılım | back-propagation through time | RNN'yi zamanda açarak eğitme |
| uzun kısa süreli bellek | long short-term memory (LSTM) | Kapılı bellek hücresi |
| unutma / girdi / çıktı kapısı | forget / input / output gate | LSTM kapıları |
| aktarım öğrenmesi | transfer learning | Bir görevden diğerine bilgi aktarmak |
| ince ayar | fine-tuning | Önceden eğitilmiş ağı yeni veriyle ayarlamak |
| çok görevli öğrenme | multitask learning | Birden çok görevde birlikte eğitim |
| yarı denetimli öğrenme | semisupervised learning | Az etiketli + çok etiketsiz veri |
| olasılıksal PCA | probabilistic PCA (PPCA) | Doğrusal–Gauss gizli değişken modeli |
| otokodlayıcı | autoencoder | Kodlayıcı + kod çözücü |
| değişimsel otokodlayıcı | variational autoencoder (VAE) | ELBO ile eğitilen üretici model |
| kanıt alt sınırı | evidence lower bound (ELBO) | log P(x)'in alt sınırı |
| otoregresif model | autoregressive model | Her öğe öncekilere koşullu |
| üretici çekişmeli ağ | generative adversarial network (GAN) | Üretici ile ayırt edicinin oyunu |
