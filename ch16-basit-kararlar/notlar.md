# Bölüm 16 — Basit kararlar almak

> **Kitapta:** AIMA 4. baskı, Bölüm 16 *"Making Simple Decisions"*.
> Önce kitabı oku, sonra bu notlarla pekiştir. Metin özgündür; kitaptan alıntı yoktur.

## Bu bölümün haritası

| Kitap alt bölümü | Bu nottaki karşılığı | Kod |
|---|---|---|
| 16.1 Combining Beliefs and Desires under Uncertainty | §1 Beklenen fayda ve MEU ilkesi | `fayda_kurami.py` |
| 16.2 The Basis of Utility Theory | §2 Altı aksiyom, fayda fonksiyonunun varlığı, afin dönüşüm | `fayda_kurami.py` (para pompası) |
| 16.3 Utility Functions | §3 Fayda ölçekleri, paranın faydası, iyileştiricinin laneti, insan yargısı | `fayda_kurami.py`, `iyimserlik_laneti.py` |
| 16.4 Multiattribute Utility Functions | §4 Baskınlık, tercih bağımsızlığı, toplamsal değer fonksiyonu | `karar_agi.py` |
| 16.5 Decision Networks | §5 Karar ağları ve değerlendirilmeleri | `karar_agi.py` |
| 16.6 The Value of Information | §6 VPI, özellikleri, bilgi toplayan ajan, hazine avı, sağlam kararlar | `bilgi_degeri.py`, `cozumler/alistirma_kod.py` (A7, A9) |
| 16.7 Unknown Preferences | §7 Kendi tercihinden emin olmamak, kapatma düğmesi oyunu | `bilinmeyen_tercihler.py` |

## Öğrenme hedefleri

1. Beklenen faydayı hesaplamak ve MEU ilkesiyle eylem seçmek.
2. Fayda kuramının altı aksiyomunu ve birinin çiğnenmesinin neden akıl dışı davranışa yol açtığını açıklamak.
3. Paranın faydasını, risk tutumlarını, kesinlik eşdeğerini ve sigorta primini yorumlamak.
4. İyileştiricinin lanetini ve insan kararlarındaki bilinen sapmaları (Allais, Ellsberg, çerçeveleme, çıpalama) tanımak.
5. Çok nitelikli kararlarda baskınlığı ve toplamsal değer fonksiyonunu kullanmak.
6. Bir karar ağını kurmak ve değerlendirmek.
7. Mükemmel bilginin değerini (VPI) hesaplamak ve bilgi toplamayı ona göre yönlendirmek.
8. Tercih belirsizliğinin makineyi neden insana danışmaya yönelttiğini açıklamak.

---

## Büyük resim

Bölüm 12–15 ajanın neye **inanması** gerektiğini anlattı. Bu bölüm ajanın ne **istediğini** ekler:

> olasılık kuramı (inanç) + fayda kuramı (istek) = **karar kuramı** (ne yapmalı)

Burada kararlar **tek seferliktir** (epizodik): Eylemi seç, sonucu gör, bitti. Ardışık kararlar Bölüm 17'nin konusu.

---

## 1. Beklenen fayda ve MEU

Ajan mevcut durumdan emin değildir (P(s)) ve eylemlerinin sonucundan da emin değildir (P(s′ | s, a)). Bir eylemin sonucunun dağılımı:

```text
P(RESULT(a) = s′) = Σ_s P(s) P(s′ | s, a)
```

**Fayda fonksiyonu** U(s), bir durumun ne kadar istendiğini tek bir sayıyla söyler. **Beklenen fayda:**

```text
EU(a) = Σ_s′ P(RESULT(a) = s′) U(s′)
```

**MEU ilkesi:** Rasyonel ajan EU'yu en büyük yapan eylemi seçer: `eylem = argmax_a EU(a)`.

MEU ilkesi yapay zekâ problemini çözmez, yalnızca tanımlar: P(s)'yi bulmak algı, öğrenme ve çıkarım ister; U(s′)'yü bilmek de arama ya da planlama gerektirebilir.

**Başarım ölçütüyle ilişkisi (Bölüm 2):** Başarım ölçütü bütün bir geçmişi **sonradan** puanlar. Fayda fonksiyonu ise **bir sonraki durumu** puanlar, bu yüzden adım adım eylem seçmek için kullanılabilir. Fayda fonksiyonu başarım ölçütünü doğru yansıtıyorsa MEU ajanı ortalamada en yüksek puanı alır.

---

## 2. Fayda kuramının temeli

**Piyango:** Olası sonuçlar ve olasılıkları: `L = [p₁, S₁; p₂, S₂; …]`. Belirsiz bir eylemin sonucu bir piyangodur.

Tercih gösterimi: `A ≻ B` (A tercih edilir), `A ∼ B` (fark yok), `A ≿ B` (A tercih edilir ya da fark yok).

### 2.1 Altı aksiyom

| Aksiyom | Kısaca |
|---|---|
| **Sıralanabilirlik** (orderability) | İki piyango arasında ajan ya birini tercih eder ya da ikisini eşit görür; kararsız kalamaz. |
| **Geçişlilik** (transitivity) | A ≻ B ve B ≻ C ise A ≻ C. |
| **Süreklilik** (continuity) | A ≻ B ≻ C ise B ile [p, A; 1−p, C] arasında ajanın kayıtsız kaldığı bir p vardır. |
| **İkame edilebilirlik** (substitutability) | A ∼ B ise bir piyangoda A yerine B koymak tercihi değiştirmez. |
| **Tekdüzelik** (monotonicity) | A ≻ B ise, A'yı daha yüksek olasılıkla veren piyango tercih edilir. |
| **Ayrıştırılabilirlik** (decomposability) | İç içe piyangolar olasılık kurallarıyla tek piyangoya indirgenebilir ("kumarın kendisinden zevk alma" yok). |

**Neden gerekli?** Bir aksiyomu çiğneyen ajan sömürülebilir. Örnek, **para pompası**: Tercihleri A ≻ B ≻ C ≻ A (geçişsiz) olan ajan, elindekini daha çok sevdiğiyle değiştirmek için her seferinde 1 kuruş öder; üç takastan sonra başladığı yere döner, parası azalmıştır ve bu sonsuza dek sürebilir (`fayda_kurami.py`).

### 2.2 Tercihlerden faydaya

von Neumann ve Morgenstern (1944): Tercihler aksiyomlara uyuyorsa

1. Bir U fonksiyonu **vardır**: `U(A) > U(B) ⇔ A ≻ B` ve `U(A) = U(B) ⇔ A ∼ B`.
2. Bir piyangonun faydası, sonuçların faydalarının **beklenen değeridir**: `U([p₁, S₁; …; pₙ, Sₙ]) = Σ pᵢ U(Sᵢ)`.

Yani tutarlı tercihleri olan ajan, **sanki** beklenen faydayı en büyüklüyormuş gibi davranır. Bu, ajanın içinde açıkça bir U hesapladığı anlamına gelmez (bir tablo da aynı davranışı üretebilir).

**Tek değil:** `U′(S) = a U(S) + b` (a > 0, **pozitif afin dönüşüm**) aynı davranışı verir. Belirsizlik yoksa yalnızca sıralama önemlidir; buna **değer fonksiyonu** ya da **sıralı (ordinal) fayda** denir. Belirsizlik varsa sayıların oranları önemlidir: Örneğin U yerine U² kullanmak kararları değiştirebilir (A3).

---

## 3. Fayda fonksiyonları

### 3.1 Fayda ölçekleri ve ölçme

**Tercih çıkarma** (preference elicitation): İnsana seçimler sunup tercihlerinden fayda fonksiyonunu bulmak.

**Normalleştirilmiş fayda:** En kötü sonuç u⊥ = 0, en iyi sonuç u⊤ = 1. Bir S sonucunun faydası, **standart piyango** [p, u⊤; 1−p, u⊥] ile karşılaştırılarak ölçülür: Ajanın kayıtsız kaldığı p, U(S)'dir. Kitaptaki örnek: İngiltere taraftarı için "yarı finalde elenmek" ile "%30 kupayı kazanmak, %70 elemelerde kalmak" eşitse U(yarı final) = 0.3.

**Hayatın değeri:** Hayat söz konusu olunca da değiş tokuşlar sürekli yapılır (uçak bakım aralıkları, araba güvenliği). Kitaptaki kavramlar:

- **İstatistiksel yaşam değeri:** ABD kurumlarında 2019'da kabaca 10 milyon $.
- **Mikromort:** Milyonda bir ölüm riski. İngiltere'de 230 mil araba yolculuğu ≈ 1 mikromort; arabanın ömrü 92 000 mil ≈ **400 mikromort**. İnsanlar bu riski yarıya indiren daha güvenli bir arabaya yaklaşık 12 000 $ fazla ödüyor → 12 000 / 200 = **60 $ / mikromort**. (Yalnızca küçük riskler için geçerli.)
- **QALY** (kaliteye göre düzeltilmiş yaşam yılı): Böbrek hastaları ortalamada diyalizle 2 yıl ile tam sağlıkla 1 yıl arasında kayıtsız.

İlginç bir nokta: Hayata değer biçmeyi reddetmek, onu **daha düşük** değerlemeye yol açabilir (kitaptaki asbest örneği).

### 3.2 Paranın faydası (`fayda_kurami.py`)

İnsanlar daha çok parayı daha aza tercih eder (**tekdüze tercih**), ama paranın faydası doğrusal değildir.

**Yarışma örneği (kitap):** 1 000 000 $'ı al ya da yazı-tura at: tura → 0 $, yazı → 2 500 000 $.
- **Beklenen parasal değer** (EMV): 0.5 × 0 + 0.5 × 2 500 000 = **1 250 000 $** > 1 000 000 $.
- Ama faydalar U(şimdiki) = 5, U(+1M) = 8, U(+2.5M) = 9 ise: EU(kumar) = 0.5 × 5 + 0.5 × 9 = **7** < EU(al) = **8**. Parayı almak rasyoneldir. İlk milyonun faydası ikincisinden çok daha büyüktür.

**Bay Beard'ın fayda fonksiyonu** (Grayson, 1960; kitaptaki eğri): `U(S_{k+n}) = −263.31 + 22.09 log(n + 150 000)`, −150 000 ≤ n ≤ 800 000 $ aralığında.

**Risk tutumları:**

| Eğri | Tutum | Davranış |
|---|---|---|
| İçbükey (concave) | **riskten kaçınan** | U(L) < U(S_EMV(L)): kumarın kendisinden çok onun EMV'sini kesin almayı tercih eder |
| Doğrusal | **risk-nötr** | Yalnızca EMV'ye bakar |
| Dışbükey (convex) | **risk arayan** | Kitap: büyük borç içindeki "çaresiz" bölgede görülür |

**Kesinlik eşdeğeri:** Ajanın piyango yerine kabul edeceği kesin tutar. Kitap: İnsanların çoğu yarı yarıya 1000 $ / 0 $ piyango yerine ~400 $ kabul eder. EMV 500 $, kesinlik eşdeğeri 400 $.
**Sigorta primi** = EMV − kesinlik eşdeğeri = 100 $. Riskten kaçınma sigorta sektörünün temelidir.

Küçük tutarlarda (servete göre) fayda eğrisi neredeyse doğrusaldır, bu yüzden ajan risk-nötr davranır. Bay Beard için 0/1000 $ piyangosunun primi yalnızca ~1 $; 0/800 000 $ piyangosunun primi ~172 500 $.

### 3.3 Beklenen fayda ve karar sonrası hayal kırıklığı (`iyimserlik_laneti.py`)

EU tahminleri hatalıdır. Tahminler yansız olsa bile, **en yüksek tahmini seçmek** seçilen seçeneğin tahminini sistematik olarak şişirir: **İyileştiricinin laneti** (optimizer's curse).

k seçeneğin hepsinin gerçek değeri 0, tahmin hatası N(0, 1) olsun. En büyük tahminin yoğunluğu `k f(x) F(x)^{k−1}`:

| k | ortalama "hayal kırıklığı" |
|---|---|
| 3 | ~0.85 σ (kitap) |
| 30 | ~2 σ (kitap) |

**Gerçek hayatta:** Binlerce aday ilaç arasından seçilmiş, 10 hastanın 9'unu iyileştiren bir ilaç, 1000 hastanın 800'ünü iyileştiren bir ilaçtan muhtemelen **daha kötüdür**. Seçim süreci yanlılık yaratır.

**Çare:** Tahminleri olduğu gibi kullanmak yerine, tahminin ve hatanın olasılık modelini kurup **Bayesçi** olarak düzeltmek (önsele doğru "büzmek"). Gürültüsü farklı seçenekler varsa büzme seçimi de değiştirir (A6).

### 3.4 İnsan yargısı ve akıl dışılık

Karar kuramı **normatiftir** (nasıl davranılmalı); insanların gerçekte nasıl davrandığını anlatan kuram **betimseldir**. Kitaptaki sapmalar:

**Allais paradoksu:**

| Piyango | Ödül |
|---|---|
| A | %80 olasılıkla 4000 $ |
| B | kesin 3000 $ |
| C | %20 olasılıkla 4000 $ |
| D | %25 olasılıkla 3000 $ |

Çoğu kişi B ≻ A ve C ≻ D seçer. U(0 $) = 0 alınırsa B ≻ A ⇒ U(3000) > 0.8 U(4000), ama C ≻ D ⇒ 0.2 U(4000) > 0.25 U(3000) ⇒ U(3000) < 0.8 U(4000). **Hiçbir fayda fonksiyonu** iki tercihi birden açıklayamaz.
- Açıklama: **kesinlik etkisi** (kesin kazanca çekim). Olası nedenler: hesap yükünden kaçınmak, verilen olasılıklara güvenmemek, **pişmanlık**. B'yi bırakıp A'yı seçen ve kaybeden kişi kendini aptal gibi hisseder; bu duyguyu da sonuca katarsak tercihler tutarlı olur (A5). İnsanlar bunun için 200 $ EMV'den vazgeçmeye razıdır.

**Ellsberg paradoksu:** Torbada 1/3 kırmızı, 2/3 siyah ya da sarı top var (oran bilinmiyor). A: kırmızıya 100 $, B: siyaha 100 $; C: kırmızı ya da sarıya 100 $, D: siyah ya da sarıya 100 $. Çoğu kişi A ≻ B ve D ≻ C seçer. A ≻ B "siyah < 1/3" demektir, D ≻ C ise "siyah > 1/3". Hiçbir dünya buna uymaz. Açıklama: **belirsizlikten kaçınma** (ambiguity aversion): İnsanlar bilinen olasılığı tercih eder.

**Çerçeveleme etkisi:** "%90 hayatta kalma" diye anlatılan bir ameliyat, "%10 ölüm" diye anlatılandan yaklaşık iki kat daha çok beğenilir. Hastalarda, işletme öğrencilerinde ve deneyimli doktorlarda benzer.

**Çıpalama etkisi:** Restoran kimsenin almayacağı 200 $'lık bir şarap koyar; bu, bütün şarapların değer tahminini yukarı çeker ve 55 $'lık şarap ucuz görünür.

**Evrimsel psikoloji itirazı:** Beynimiz olasılığı sayılarla anlatılan sözel problemleri çözmek için evrilmedi. Aynı problem "100 ameliyattan 10'unda hasta ölüyor" gibi canlandırmayla sunulunca insanlar rasyonele çok daha yakın davranıyor.

---

## 4. Çok nitelikli fayda fonksiyonları (`karar_agi.py`)

Kitaptaki örnek: **havalimanı yeri** seçimi. Nitelikler: Güvenlik, Sessizlik, Tutumluluk (hepsi "büyük iyi" olacak biçimde yazılır).

### 4.1 Baskınlık

- **Katı baskınlık:** S1 her nitelikte S2'den iyi ya da eşitse (en az birinde daha iyi) S2 elenir. Belirsizlik olsa da, S1'in **her olası sonucu** S2'nin her olası sonucundan iyiyse işe yarar.
- **Stokastik baskınlık:** Kitaptaki sayılar: S1'in maliyeti U[2.8, 4.8], S2'nin U[3.0, 5.2] milyar $. Tutumluluk = −maliyet için S1'in birikimli dağılımı her noktada S2'ninkinin iyi tarafında. Sonuç: **Her tekdüze artan** fayda fonksiyonu için S1 en az S2 kadar iyidir. Fayda fonksiyonunu bilmeden karar verilebilir.

Tanım (büyük iyi): A1, A2'yi stokastik olarak baskılar ⇔ her x için `∫_{−∞}^{x} p₁(x′) dx′ ≤ ∫_{−∞}^{x} p₂(x′) dx′`.

Stokastik baskınlık çoğu zaman nitel akıl yürütmeyle de kurulabilir: "inşaat maliyeti şehre uzaklıkla artar" gibi.

### 4.2 Tercih yapısı

n nitelik ve her biri d değer alırsa en kötü durumda U için **dⁿ** değer gerekir. Amaç, Bayes ağlarındaki gibi bir **ayrıştırma** bulmak: `U(x₁, …, xₙ) = F[f₁(x₁), …, fₙ(xₙ)]`.

**Belirsizlik yokken:** X₁ ve X₂, X₃'ten **tercih bakımından bağımsızdır**, eğer ⟨x₁, x₂, x₃⟩ ile ⟨x′₁, x′₂, x₃⟩ arasındaki tercih x₃'e bağlı değilse. Her alt küme bu özelliği taşıyorsa **karşılıklı tercih bağımsızlığı (MPI)** vardır. Debreu (1960): MPI varsa

```text
V(x₁, …, xₙ) = Σᵢ Vᵢ(xᵢ)       (toplamsal değer fonksiyonu)
```

n boyutlu bir fonksiyon yerine n tane tek boyutlu fonksiyon ölçmek yeter. MPI'nin bozulduğu kitaptaki örnek: Ortaçağ pazarında av köpekleri, tavuklar ve kafesler. Yeterli kafes yoksa köpekler tavukları yer; köpek–tavuk değiş tokuşu kafes sayısına bağlıdır.

**Belirsizlik varken:** **Fayda bağımsızlığı** aynı fikri piyangolara taşır; karşılıklı fayda bağımsızlığı (MUI) **çarpımsal fayda fonksiyonunu** verir (Keeney, 1974): n nitelik için n tek nitelikli fayda ve n sabit yeter.

---

## 5. Karar ağları (`karar_agi.py`)

**Karar ağı** (etki diyagramı, influence diagram) = Bayes ağı + eylemler + fayda. Üç düğüm türü:

| Düğüm | Çizim | Anlamı |
|---|---|---|
| **Şans düğümü** | oval | Rastgele değişken (Bayes ağındaki gibi) |
| **Karar düğümü** | dikdörtgen | Ajanın seçimi |
| **Fayda düğümü** | elmas | Ebeveynlerine bağlı fayda fonksiyonu |

Kitaptaki havalimanı ağında karar düğümü Airport Site; şans düğümleri Air Traffic, Litigation, Construction ve bunlara bağlı sonuçlar Safety, Quietness, Frugality; fayda düğümü bu üç sonuca bağlıdır.

**Eylem–fayda biçimi:** Sonuç düğümleri ağdan atılıp fayda düğümü doğrudan karara ve şans düğümlerine bağlanabilir. Bu düğüm artık durumun değil, **eylemin** beklenen faydasını verir; Bölüm 17 ve 22'deki **Q-fonksiyonunun** ilk biçimidir. Daha az esnektir (sonuçlar değişirse yeniden hesaplanmalı).

**Değerlendirme algoritması:**

1. Kanıt değişkenlerini şu anki duruma göre ayarla.
2. Karar düğümünün her olası değeri için: (a) karar düğümünü o değere ayarla, (b) fayda düğümünün ebeveynlerinin sonsal olasılıklarını standart bir Bayes ağı çıkarımıyla hesapla, (c) eylemin beklenen faydasını hesapla.
3. En yüksek beklenen faydalı eylemi döndür.

Kodumuzdaki havalimanı ağının yapısı kitaptaki gibidir, ama **sayılar bizim varsayımımızdır** (kitap ağın olasılıklarını vermez). Varsayılan ağırlıklarla S1 seçilir; ölüme verilen ağırlık 5'ten yalnızca ~5.26'ya çıkınca karar S3'e döner (A7). Bu tür kırılganlık, §6.6'daki duyarlılık analizinin konusudur.

---

## 6. Bilginin değeri (`bilgi_degeri.py`)

Gerçek kararlarda bütün bilgi elde değildir. Bilgi almak (test, soru, araştırma) bir **eylemdir** ve bir maliyeti vardır. Ne zaman değer?

### 6.1 Basit örnek: petrol (kitap)

n blok var; yalnızca birinde C $ kâr getirecek petrol var. Her bloğun fiyatı C/n $. Şirket risk-nötr ise hiçbir blok almamakla rastgele bir blok almak aynıdır (beklenen kâr 0).

Bir jeolog blok 3 hakkında kesin bilgi satıyor. Bu bilgi ne kadar eder?
- 1/n olasılıkla "petrol var" der: Şirket blok 3'ü alır, kâr C − C/n = (n−1)C/n.
- (n−1)/n olasılıkla "yok" der: Petrol kalan n−1 bloktan birindedir. Şirket başka bir blok alır; beklenen kâr C/(n−1) − C/n = C/(n(n−1)).
- Beklenen kâr: (1/n) · (n−1)C/n + ((n−1)/n) · C/(n(n−1)) = **C/n**.

Bilgi, tam bloğun fiyatı kadar eder. Kod bunu tam kesirlerle doğrular.

### 6.2 Genel formül (mükemmel bilgi)

Şu anki kanıt e, en iyi eylem α. E_j'nin değeri öğrenilirse:

```text
EU(α | e)        = max_a Σ_s′ P(RESULT(a) = s′ | e) U(s′)
VPI_e(E_j)       = [ Σ_k P(E_j = e_jk | e) · EU(α_{e_jk} | e, E_j = e_jk) ]  −  EU(α | e)
```

E_j'nin değeri önceden bilinmediği için **olası bütün değerlerinin ortalaması** alınır.

**Bilgi ne zaman değerlidir?** İki eylem A1 ve A2 düşün:
- (a) A1 açıkça daha iyi ve belirsizlik az → bilgi kararı değiştirmez → VPI ≈ 0.
- (b) A1 ile A2 başa baş ama belirsizlik az → seçim fark etmez → VPI küçük.
- (c) Başa baş ve belirsizlik çok → bilgi kararı değiştirebilir ve bu önemli olabilir → VPI büyük.

Kısaca: **Bilgi, kararı değiştirebildiği ölçüde değerlidir.** Kodumuzdaki havalimanı ağında hava trafiğini öğrenmenin değeri 0'dır: Her iki durumda da S1 seçilir (A7).

### 6.3 VPI'nin özellikleri

| Özellik | Anlamı |
|---|---|
| **Negatif değil:** VPI ≥ 0 | Beklenen değer olarak bilgi zarar vermez (tek bir gözlem kötü haber olabilir, ama ortalama ≥ 0). |
| **Toplamsal değil:** VPI(E_j, E_k) ≠ VPI(E_j) + VPI(E_k) | Aynı testi iki kez yapmak iki kat bilgi vermez. |
| **Sıradan bağımsız** | Gözlemler hangi sırayla yapılırsa yapılsın, toplam değer aynıdır. |

Hepsi kodda örnekle gösterilir (`tibbi()`: aynı test iki kez yapılınca VPI 5.60 + 5.60 değil, 5.66).

### 6.4 Bilgi toplayan ajan

Kitaptaki **miyop** ajan: Her adımda VPI(E_j) / C(E_j) oranı en büyük gözlemi seç; VPI(E_j) > C(E_j) ise iste, değilse gerçek eylemi yap.

**Miyop**, çünkü her gözlemin değerini tek başına hesaplar. Açgözlü aramaya benzer ve pratikte çoğu zaman iyi çalışır (tanı testi seçiminde uzman doktorları geçtiği gösterilmiştir). Ama tek başına işe yaramayan, birlikte çok değerli olan iki gözlemi kaçırabilir.

### 6.5 Miyop olmayan bilgi toplama: hazine avı

En iyi gözlem dizisini bulmak genelde çok zordur (karar ağı çok ağaç olsa bile). Kolay bir özel durum, **hazine avı** (en az maliyetli test dizisi): n yer; i'de hazine olma olasılığı P(i) (bağımsız), bakma maliyeti C(i). Hazine bulununca durulur.

`C(xy) = C(x) + F(x) C(y)` (F = başarısızlık olasılığı) kullanılarak, komşu iki öğenin yer değiştirmesinin etkisinin bağlamdan bağımsız olduğu gösterilir. Sonuç: **En iyi sıra, yerleri P(i)/C(i) oranına göre büyükten küçüğe dizer.** A9'da kaba kuvvetle doğrulanır.

### 6.6 Duyarlılık analizi ve sağlam kararlar

Modeldeki olasılıklar öğrenilmiş ya da tahmin edilmiştir, kesin değildir.
- **Duyarlılık analizi:** Parametreler oynatılınca karar değişiyor mu? Değişmiyorsa karar güvenilirdir (fayda tahmini yanlış olsa bile). Küçük bir oynamayla değişiyorsa modeli iyileştirmeye değer.
- **Sağlam (minimaks) karar:** `a* = argmax_a min_θ EU(a; θ)`: En kötü parametrelerde en iyi olan eylem. Çoğu zaman güvenilir; bazen fazla temkinli (kitaptaki örnek: herkesin cani gibi araba sürdüğünü varsayan otonom araba garajdan hiç çıkmaz).
- **Bayesçi seçenek:** Parametre belirsizliğini bir önsel dağılımla (hiperparametreler) modelle; çoğu zaman pratikte daha iyi.
- **Yapısal belirsizlik** (ağda eksik değişken, yanlış bağımsızlık) için iyi bir yöntem henüz yok; bir fikir, model topluluğu kullanmak.

---

## 7. Bilinmeyen tercihler (`bilinmeyen_tercihler.py`)

### 7.1 Kendi tercihinden emin olmamak

Kitaptaki **durian dondurması**: Dondurmacıda iki çeşit kalmış, ikisi de 2 $. Vanilya senin için 3 $ değerinde (net +1 $). Durianı hiç denemedin: %50 bayılırsın (100 $ değerinde, net +98 $), %50 nefret edersin (−80 $, net −82 $).

```text
EU(vanilya) = +1 $      EU(durian) = 0.5 × 98 + 0.5 × (−82) = +8 $
```

Daha fazla bilgi alınamıyorsa (dükkân tattırmıyorsa) belirsiz faydayı beklenen değeriyle değiştirmek yeter. Ama inanç değişebiliyorsa (küçük bir tadım, akrabaların hepsinin durian sevdiğini öğrenmek) belirsizliği fayda fonksiyonundan **yeni bir rastgele değişkene** (LikesDurian, önseli 0.5) taşırız. Fayda fonksiyonu yine kesin olur ve bilinen tercihler için kurulan bütün araçlar kullanılabilir. Belirsizlik ortadan kalkmaz; yalnızca "dünyaya" taşınır.

### 7.2 İnsana saygı: kapatma düğmesi oyunu

**Robbie** (robot) **Harriet** (insan) için çalışır. Robbie bir eylemin (pahalı bir otel ayarlamak) Harriet'e faydası u'yu bilmez: u ~ U[−40, 60]. Robbie'nin seçenekleri:

| Seçenek | Robbie için değer |
|---|---|
| Hemen yap | E[u] = **+10** |
| Kendini kapat | **0** |
| Bekle, Harriet'e açıkla; Harriet isterse kapatsın | Harriet u < 0 ise kapatır: E[max(u, 0)] = 0.6 × 30 = **+18** |

Beklemek en iyisidir. Genel olarak `E[max(u, 0)] ≥ max(E[u], 0)`; fark, Harriet'in kararının Robbie için **bilgi değeridir**.

Sonuçlar:
- Robbie Harriet'in tercihlerinden **emin değilse**, ona danışmak ve kendini kapatmasına izin vermek için bir nedeni vardır.
- Robbie **emin olduğu anda** (σ → 0) bu teşvik kaybolur. Sabit ve kesin bir amaç verilen bir makine kendini kapatmaya direnebilir; tercih belirsizliği güvenli yapay zekâ için önemlidir.
- Harriet hata yapabiliyorsa Robbie ona daha az saygı gösterir: U[−40, 60] için hata olasılığı ε ≈ 0.31'i aşınca Robbie hemen yapmayı tercih eder (A10).

Bu oyun bir **yardım oyununun** (assistance game) basit hâlidir (Bölüm 18'de genelleşir).

---

## Sık yapılan hatalar

| Yanılgı | Doğrusu |
|---|---|
| "Rasyonel ajan beklenen parayı (EMV) en büyükler." | Beklenen **faydayı** en büyükler; paranın faydası doğrusal değildir. |
| "Faydanın sayısal değerleri anlamlıdır." | Yalnızca pozitif afin dönüşüme kadar; belirsizlik yoksa yalnızca sıralama önemli. |
| "En yüksek tahmini seçmek yansız bir tahmin verir." | İyileştiricinin laneti: Seçilenin tahmini sistematik olarak şişkindir. |
| "Bilgi her zaman değerlidir." | Kararı değiştiremeyecek bilginin değeri 0'dır; VPI asla negatif değildir ama sıfır olabilir. |
| "İki testin değeri, değerlerinin toplamıdır." | VPI toplamsal değildir; özellikle testler aynı şeyi ölçüyorsa. |
| "Miyop ajan her zaman en iyi test dizisini bulur." | Tek tek değersiz, birlikte değerli gözlemleri kaçırabilir. |
| "Allais'teki insanlar düpedüz akıl dışı." | Pişmanlık gibi duygular sonuca katılırsa tercihler tutarlı olabilir. |
| "Amacından emin bir makine daha güvenlidir." | Kapatma düğmesi oyunu tersini gösterir: Belirsizlik, insana danışma isteği doğurur. |

## Kendini yokla

1. EU(a) formülünü P(s) ve P(s′ | s, a) cinsinden yaz.
2. Geçişsiz tercihleri olan bir ajan nasıl sömürülür?
3. U yerine 3U + 7 kullanmak kararları değiştirir mi? Peki U² kullanmak?
4. Kesinlik eşdeğeri ile sigorta primi arasındaki ilişki nedir?
5. Allais paradoksunda neden hiçbir fayda fonksiyonu iki tercihi birden açıklayamaz?
6. Stokastik baskınlık fayda fonksiyonunu bilmeden karar vermeyi nasıl sağlar?
7. MPI neyi garanti eder? Köpek–tavuk–kafes örneğinde neden bozulur?
8. Karar ağı nasıl değerlendirilir?
9. Petrol örneğinde VPI neden C/n çıkar?
10. Kapatma düğmesi oyununda Robbie neden beklemeyi seçer? Hangi durumda bu teşvik kaybolur?

## Kod rehberi

```bash
python ornekler/fayda_kurami.py         # yarışma kumarı, Bay Beard, Allais, Ellsberg, para pompası
python ornekler/iyimserlik_laneti.py    # iyileştiricinin laneti, ilaç denemesi
python ornekler/karar_agi.py            # stokastik baskınlık, havalimanı karar ağı, eylem-fayda tablosu
python ornekler/bilgi_degeri.py         # petrol VPI = C/n, VPI özellikleri, miyop ajan
python ornekler/bilinmeyen_tercihler.py # durian dondurması, kapatma düğmesi oyunu
python cozumler/alistirma_kod.py        # A4–A7, A9, A10
```

## Terimler

| Türkçe | İngilizce | Kısa açıklama |
|---|---|---|
| karar kuramı | decision theory | Olasılık + fayda: ne yapılmalı |
| fayda fonksiyonu | utility function | Bir durumun istenirliğini veren sayı |
| beklenen fayda | expected utility (EU) | Sonuçların faydalarının olasılıkla ağırlıklı ortalaması |
| en büyük beklenen fayda ilkesi | maximum expected utility (MEU) | En yüksek EU'lu eylemi seç |
| piyango | lottery | Olasılıklı sonuçlar kümesi |
| sıralanabilirlik / geçişlilik / süreklilik | orderability / transitivity / continuity | Fayda aksiyomları |
| ikame edilebilirlik / tekdüzelik / ayrıştırılabilirlik | substitutability / monotonicity / decomposability | Fayda aksiyomları |
| pozitif afin dönüşüm | positive affine transformation | aU + b (a > 0): davranışı değiştirmez |
| değer fonksiyonu / sıralı fayda | value function / ordinal utility | Yalnızca sıralamanın önemli olduğu fayda |
| tercih çıkarma | preference elicitation | Seçimlerden fayda fonksiyonunu bulmak |
| normalleştirilmiş fayda | normalized utility | En kötü 0, en iyi 1 |
| standart piyango | standard lottery | [p, u⊤; 1−p, u⊥] |
| mikromort | micromort | Milyonda bir ölüm riski |
| kaliteye göre düzeltilmiş yaşam yılı | quality-adjusted life year (QALY) | Sağlık kararlarında fayda birimi |
| beklenen parasal değer | expected monetary value (EMV) | Paranın beklenen değeri |
| riskten kaçınan / risk-nötr / risk arayan | risk-averse / risk-neutral / risk-seeking | İçbükey / doğrusal / dışbükey fayda |
| kesinlik eşdeğeri | certainty equivalent | Piyango yerine kabul edilen kesin tutar |
| sigorta primi | insurance premium | EMV − kesinlik eşdeğeri |
| iyileştiricinin laneti | optimizer's curse | Seçilen seçeneğin tahmininin şişkinliği |
| normatif / betimsel kuram | normative / descriptive theory | Nasıl olmalı / nasıl oluyor |
| kesinlik etkisi | certainty effect | Kesin kazanca aşırı çekim |
| belirsizlikten kaçınma | ambiguity aversion | Bilinen olasılığı tercih etme |
| çerçeveleme etkisi | framing effect | Anlatım biçiminin seçimi değiştirmesi |
| çıpalama etkisi | anchoring effect | Göreli karşılaştırmanın değer yargısını kaydırması |
| katı / stokastik baskınlık | strict / stochastic dominance | Fayda bilinmeden eleme |
| tercih bağımsızlığı | preference independence | Bir niteliğin diğerlerinin değiş tokuşunu etkilememesi |
| karşılıklı tercih bağımsızlığı | mutual preferential independence (MPI) | Toplamsal değer fonksiyonunu sağlar |
| toplamsal değer fonksiyonu | additive value function | V = Σ Vᵢ(xᵢ) |
| fayda bağımsızlığı | utility independence | Tercih bağımsızlığının piyango hâli |
| çarpımsal fayda fonksiyonu | multiplicative utility function | MUI'nin verdiği biçim |
| karar ağı / etki diyagramı | decision network / influence diagram | Şans + karar + fayda düğümleri |
| eylem–fayda fonksiyonu | action-utility function | Q-fonksiyonunun öncülü |
| mükemmel bilginin değeri | value of perfect information (VPI) | Bilgiyle beklenen fayda artışı |
| miyop bilgi toplama | myopic information gathering | Gözlemleri tek tek değerlendirme |
| hazine avı | treasure hunt | En az maliyetli test dizisi problemi |
| duyarlılık analizi | sensitivity analysis | Parametre değişince sonucun değişimi |
| sağlam (minimaks) karar | robust (minimax) decision | En kötü durumda en iyi |
| kapatma düğmesi oyunu | off-switch game | Robotun insana kapatma izni vermesi |
| yardım oyunu | assistance game | İnsanın tercihlerini bilmeyen robotla oyun |
