# Bölüm 13 — Olasılıksal akıl yürütme (Bayes ağları)

> **Kitapta:** AIMA 4. baskı, Bölüm 13 *"Probabilistic Reasoning"*.
> Önce kitabı oku, sonra bu notlarla pekiştir. Metin özgündür; kitaptan alıntı yoktur.

## Bu bölümün haritası

| Kitap alt bölümü | Bu nottaki karşılığı | Kod |
|---|---|---|
| 13.1 Representing Knowledge in an Uncertain Domain | §1 Bayes ağı nedir; hırsız alarmı | `hirsiz_alarmi.py`, `bayes_agi.py` |
| 13.2 The Semantics of Bayesian Networks | §2 Ortak dağılım, düğüm sırası, koşullu bağımsızlık, verimli CPT'ler, sürekli değişkenler | `hirsiz_alarmi.py`, `yerel_dagilimlar.py` |
| 13.3 Exact Inference in Bayesian Networks | §3 Numaralandırma, değişken eleme, karmaşıklık | `bayes_agi.py`, `hirsiz_alarmi.py` |
| 13.4 Approximate Inference for Bayesian Networks | §4 Doğrudan, ret, olabilirlik ağırlıklandırma, Gibbs | `ornekleme.py` |
| 13.5 Causal Networks | §5 do-işleci, arka kapı ölçütü | `nedensel.py` |

## Öğrenme hedefleri

1. Bir alanı Bayes ağı olarak modellemek ve ağın tam ortak dağılımı nasıl tanımladığını açıklamak.
2. Düğüm sırasının ağın büyüklüğünü neden değiştirdiğini göstermek.
3. Ağdan koşullu bağımsızlıkları okumak (ebeveynler, Markov örtüsü, d-ayrım).
4. Numaralandırma ve değişken elemeyle kesin çıkarım yapmak; karmaşıklığı tartışmak.
5. Örnekleme yöntemlerini uygulamak ve gözlem ile müdahale arasındaki farkı açıklamak.

---

## 1. Bayes ağı

Bölüm 12'nin iki dersi: Tam ortak tablo üstel büyür; bağımsızlık ve koşullu bağımsızlık tabloyu küçültür. **Bayes ağı** bu bağımsızlıkları bir grafikle ifade eder:

1. Her düğüm bir rastgele değişkendir.
2. Yönlü bağlar döngüsüzdür (**DAG**). X → Y ise X, Y'nin **ebeveynidir**.
3. Her düğümün bir **koşullu olasılık tablosu (CPT)** vardır: P(Xᵢ | Ebeveynler(Xᵢ)).

Okun sezgisel anlamı: X'in Y üzerinde **doğrudan etkisi** var. Nedenler genellikle etkilerin ebeveyni olur. Bir uzmanın hangi doğrudan etkilerin olduğunu söylemesi, olasılıkları vermesinden çok daha kolaydır.

**Hırsız alarmı** (Judea Pearl): Alarm hırsızlığa karşı güvenilir ama küçük depremlerde de çalar. Komşular John ve Mary alarmı duyunca arar. John telefon zilini alarmla karıştırabilir, Mary yüksek sesle müzik dinler ve bazen alarmı kaçırır.

| Düğüm | CPT |
|---|---|
| Burglary | P(b) = 0.001 |
| Earthquake | P(e) = 0.002 |
| Alarm | P(a \| b, e) = 0.95; P(a \| b, ¬e) = 0.94; P(a \| ¬b, e) = 0.29; P(a \| ¬b, ¬e) = 0.001 |
| JohnCalls | P(j \| a) = 0.90; P(j \| ¬a) = 0.05 |
| MaryCalls | P(m \| a) = 0.70; P(m \| ¬a) = 0.01 |

> **PDF'teki baskı hatası:** Elimizdeki PDF'te Şekil 13.2'deki Alarm tablosu yanlış basılmış (MaryCalls'ın .70/.01 değerleri kopyalanmış). Hemen ardından gelen P(j, m, a, ¬b, ¬e) örneği de bu yüzden 0.01 ile hesaplanıp 0.00628 bulunmuş. Bölümün geri kalanı (Şekil 13.10 ve P(B | j, m) = 0.284) yukarıdaki standart değerleri kullanır. Biz bu değerleri kullanıyoruz; onlarla P(j, m, a, ¬b, ¬e) ≈ **0.000628** olur.

Ağda "Mary müzik dinliyor" ya da "telefon çaldı" gibi düğümler yok. Bu etkenler, Alarm → JohnCalls ve Alarm → MaryCalls bağlarındaki belirsizliğe gömülü. Bu, Bölüm 12'deki tembellik ve bilgisizliğin iş başında olmasıdır.

---

## 2. Ağın anlamı

### 2.1 Tam ortak dağılım

**P(x₁, …, xₙ) = Π P(xᵢ | ebeveynler(Xᵢ))**

Örnek: P(j, m, a, ¬b, ¬e) = P(j | a) P(m | a) P(a | ¬b, ¬e) P(¬b) P(¬e) = 0.90 × 0.70 × 0.001 × 0.999 × 0.998 ≈ 0.000628.

Bu, zincir kuralının (P(x₁, …, xₙ) = Π P(xᵢ | xᵢ₋₁, …, x₁)) ağın yapısıyla sadeleşmiş hâlidir: Her değişken, ebeveynleri verildiğinde **kendinden önceki** diğer değişkenlerden koşullu bağımsızdır.

### 2.2 Tıkızlık ve düğüm sırası

Her düğümün en fazla k ebeveyni varsa ağ n · 2ᵏ sayıyla tanımlanır; tam tablo ise 2ⁿ sayı ister. Kitaptaki hesap: n = 30, k = 5 → ağ 960 sayı, tam tablo bir milyardan fazla.

**Düğüm sırası önemlidir.** Ağı, değişkenleri bir sırayla ekleyip her birine öncüllerinden en küçük yeterli ebeveyn kümesini seçerek kurarız. `hirsiz_alarmi.py` bu kümeleri tam ortak dağılımdan **otomatik** bulur:

| Sıra | Parametre |
|---|---|
| B, E, A, J, M (nedenler önce) | **10** |
| M, J, A, B, E | **13** |
| M, J, E, B, A | **31** (tam tablo kadar!) |

Tanısal yönde (etkiden nedene) kurulan ağlar daha büyüktür ve istenen olasılıklar (P(Earthquake | Alarm, Burglary) gibi) tahmin etmesi zor sayılardır. Ders: **Nedenleri etkilerden önce ekle.**

### 2.3 Koşullu bağımsızlık ilişkileri

- **Torun olmayanlar özelliği:** Her değişken, ebeveynleri verildiğinde torunu olmayan bütün değişkenlerden koşullu bağımsızdır. (JohnCalls, Alarm verildiğinde Burglary, Earthquake ve MaryCalls'tan bağımsız.)
- **Markov örtüsü:** Her değişken, **ebeveynleri, çocukları ve çocuklarının diğer ebeveynleri** verildiğinde ağdaki bütün diğer değişkenlerden bağımsızdır. Burglary'nin Markov örtüsü {Alarm, Earthquake}.
- **d-ayrım:** X ve Y kümeleri Z verildiğinde koşullu bağımsız mı?
  1. Yalnızca X, Y, Z ve onların atalarını içeren alt grafiği al.
  2. Ortak çocuğu olan her ebeveyn çiftini birleştir (**ahlaki grafik**).
  3. Okları yönsüz yap.
  4. Z, X ile Y arasındaki bütün yolları kesiyorsa X ⊥ Y | Z.

  Hırsız ağında: Burglary ⊥ Earthquake (koşulsuz). Ama Alarm verildiğinde bağımsız değiller (ahlaki grafikte birleşirler). JohnCalls ⊥ MaryCalls | Alarm.

### 2.4 Koşullu dağılımları verimli temsil etmek (`yerel_dagilimlar.py`)

k ebeveynli bir CPT 2ᵏ satır ister. Çoğu ilişki bir **kalıba** uyar:

- **Deterministik düğüm:** Değeri ebeveynlerinden kesin belirlenir. Örnek: KuzeyAmerikalı = Kanadalı ∨ ABDli ∨ Meksikalı; en iyi fiyat = bayilerdeki fiyatların en küçüğü.
- **Bağlama özgü bağımsızlık (CSI):** Kaza olmadıysa hasar, arabanın sağlamlığından bağımsızdır. "if Kaza = false then d₁ else d₂(Sağlamlık)".
- **Gürültülü-VEYA:** Her neden etkiyi bağımsız olarak, belli bir olasılıkla **engellenerek** üretir. Kitaptaki ateş örneği: q_cold = 0.6, q_flu = 0.2, q_malaria = 0.1.
  P(¬fever | cold, flu, ¬malaria) = 0.6 × 0.2 = 0.12 → P(fever) = 0.88. k neden için 2ᵏ yerine **k** parametre. Listede olmayan nedenler için bir **sızıntı** düğümü eklenebilir.

### 2.5 Sürekli değişkenler

- **Ayrıklaştırma:** Aralıklara bölmek; doğruluk kaybı ve büyük tablolar.
- **Parametrik dağılımlar:** Normal (Gauss) dağılım gibi.
- **Karma (hibrit) ağlar:** Hem ayrık hem sürekli değişkenler.
  - Sürekli çocuk, sürekli ebeveyn: **doğrusal Gauss** P(c | h) = N(a·h + b, σ²). Tamamı doğrusal Gauss olan bir ağın ortak dağılımı çok değişkenli Gauss'tur.
  - Ayrık çocuk, sürekli ebeveyn: **probit** (Φ((−c + μ)/σ)) ya da **expit / ters logit**. Kitaptaki "maliyet c ise ürünü alır mı?" örneği: μ = 6, σ = 1. İki eğri benzer, ama expit'in kuyrukları çok daha uzundur.

---

## 3. Kesin çıkarım

Sorgu: **P(X | e)**. Gizli değişkenler Y üzerinden toplanır: P(X | e) = α Σ_y P(X, e, y).

### 3.1 Numaralandırma

P(b | j, m) = α P(b) Σ_e P(e) Σ_a P(a | b, e) P(j | a) P(m | a)

Toplamları olabildiğince içeri almak O(n 2ⁿ)'yi O(2ⁿ)'ye indirir. ENUMERATION-ASK bunu derinlik öncelikli yapar: Bellek doğrusal, zaman O(2ⁿ).

Sonuç: P(B | j, m) = α ⟨0.00059224, 0.0014919⟩ ≈ **⟨0.284, 0.716⟩**. İki komşu da arasa bile hırsızlık olasılığı ancak %28'dir, çünkü önsel çok küçük (0.001) ve komşuların yanlış alarm oranları küçük de olsa sıfır değildir.

### 3.2 Değişken eleme

Numaralandırma ağacında P(j | a) P(m | a) gibi alt ifadeler **tekrar tekrar** hesaplanır. Değişken eleme hesabı bir kez yapıp saklar (dinamik programlama):

- **Faktör:** CPT'nin kanıtla kısıtlanmış hâli, bir tablo.
- **Noktasal çarpım:** f(A, B) × g(B, C) = h(A, B, C).
- **Toplayarak çıkarma:** Σ_a h(A, B, C) → yeni faktör (B, C).

`bayes_agi.py` bu işlemleri `Faktor` sınıfıyla yapar. Hırsız sorgusunda çarpma sayısı: numaralandırma 30, eleme 22. Büyük ağlarda fark üstel olabilir.

**İlgisiz değişkenler:** Sorgunun ya da kanıtın **atası olmayan** her değişken hesaptan çıkarılabilir (toplamı 1'dir). P(JohnCalls | burglary) sorusunda MaryCalls ilgisizdir.

**Eleme sırası** önemlidir: En iyi sırayı bulmak zordur, ama en az yeni faktör boyutu üreten değişkeni önce elemek gibi açgözlü sezgiseller iyi çalışır.

### 3.3 Kesin çıkarımın karmaşıklığı

- **Tekil bağlı ağlar (çok ağaçlar, polytree):** Herhangi iki düğüm arasında (yönsüz) en fazla bir yol. Kesin çıkarım ağın boyutunda **doğrusaldır**. Hırsız ağı böyledir.
- **Çoklu bağlı ağlar:** En kötü durumda üstel. Bayes ağında çıkarım **NP-zordur**: 3-SAT problemi bir Bayes ağına kodlanabilir (kök değişkenler 0.5 olasılıklı, cümle düğümleri deterministik VEYA, S hepsinin VE'si; P(S) > 0 ⇔ cümle karşılanabilir). Hatta #P-zordur: P(S) · 2ⁿ, karşılayan atama sayısını verir.
- **Kümeleme (birleşim ağacı) algoritmaları:** Düğümleri birleştirip ağı bir çok ağaca çevirir; birçok sorguyu birlikte verimli yanıtlar.

---

## 4. Yaklaşık çıkarım (`ornekleme.py`)

Kitabın yağmurlama ağı: Cloudy → Sprinkler, Cloudy → Rain, (Sprinkler, Rain) → WetGrass.

| Yöntem | Fikir | Zayıflık |
|---|---|---|
| **Doğrudan (önsel) örnekleme** | Değişkenleri topolojik sırayla, ebeveynlere koşullu örnekle. S_PS(t, f, t, t) = 0.5 × 0.9 × 0.8 × 0.9 = 0.324 | Kanıt kullanılmaz |
| **Ret örneklemesi** | Kanıtla uyuşmayan örnekleri at, kalanları say. P(Rain \| Sprinkler) → ⟨0.3, 0.7⟩ | Kanıt olasılığı küçükse örneklerin çoğu boşa gider (üstel) |
| **Olabilirlik ağırlıklandırma** (önem örneklemesi) | Kanıt değişkenlerini sabitle, örneği kanıtın olabilirliğiyle ağırlıklandır: w = Π P(eᵢ \| ebeveynler) | Kanıt aşağıda (yapraklarda) ise örnekler kanıttan habersiz üretilir; ağırlıklar çok küçülür |
| **Gibbs örneklemesi** (MCMC) | Kanıt sabit; her adımda bir gizli değişkeni **Markov örtüsü** verildiğinde yeniden örnekle | Başlangıçtan uzaklaşmak (ısınma) zaman alabilir; deterministik ilişkilerde takılabilir |

- Tüm bu yöntemler **tutarlıdır**: N → ∞ iken tahmin kesin değere yakınsar.
- Gibbs örneklemesi, durağan dağılımı P(gizli | e) olan bir Markov zinciri kurar. **Metropolis–Hastings** daha genel bir MCMC yöntemidir: Bir öneri dağılımından aday üretir ve belli bir olasılıkla kabul eder.
- **Derlenmiş yaklaşık çıkarım:** Aynı ağda çok sorgu yapılacaksa örnekleme kodu ağa özel üretilip derlenir; yorumlamaya göre çok daha hızlıdır.

---

## 5. Nedensel ağlar (`nedensel.py`)

Fire → Smoke ağı ile Smoke → Fire ağı aynı ortak dağılımı temsil edebilir. Fark ne? **Nedensel ağ**, okların "doğa, ebeveynlerin değerine bakarak çocuğun değerini belirler" anlamına geldiği ağdır. Böyle bir ağ **müdahalelerin** etkisini de öngörür.

**do-işleci:** do(X = x), X'i dışarıdan zorla x yapmak demektir. Bunun etkisi, X'e gelen bütün okları silen **sakatlanmış ağda** X = x ile koşullamaya denktir:

P(diğerleri | do(X = x)) = Π_{i ≠ X} P(xᵢ | ebeveynler(Xᵢ)), X = x yerine konarak.

Yağmurlama ağında:
- **Gözlem:** P(Rain | Sprinkler = true) = **0.3**. Yağmurlamanın açık olduğunu görmek, havanın bulutsuz olduğuna işarettir.
- **Müdahale:** P(Rain | do(Sprinkler = true)) = **0.5** = P(Rain). Yağmurlamayı açmak havayı değiştirmez.

**Arka kapı ölçütü:** Müdahalenin etkisini hesaplamak için her CPT'yi bilmek gerekmez. Sprinkler'dan WetGrass'a doğrudan yolun yanında Cloudy ve Rain üzerinden bir "arka kapı" yolu vardır. Bu kapıyı kapatan bir Z kümesi bulmak yeter. Kitabın teknik tanımı: Y, X ve Z verildiğinde Ebeveynler(X)'ten koşullu bağımsız olmalı (d-ayrımla kontrol edilir). O zaman:

**P(y | do(x)) = Σ_z P(y | x, z) P(z)**

Yani müdahalenin etkisi **deney yapmadan**, gözlemsel verilerden hesaplanabilir. Yağmurlama ağında Z = {Cloudy} de Z = {Rain} de kapıyı kapatır. İkisi de P(WetGrass | do(Sprinkler = true)) = 0.945 verir, sakatlanmış ağla aynı. Gözlemsel P(WetGrass | Sprinkler = true) ise 0.927'dir. Kitabın vurgusu: Bu, "nedensel bilgi yalnızca rastgele kontrollü deneyden gelir" dogmasına karşı güçlü bir araçtır.

---

## Sık yapılan hatalar

| Yanılgı | Doğrusu |
|---|---|
| "Ok, nedensellik demektir." | Sıradan Bayes ağında ok yalnızca olasılıksal bağımlılık yapısını verir. Nedensel anlam ek bir varsayımdır (§5). |
| "Bağ yoksa değişkenler bağımsızdır." | Bağ yokluğu koşullu bağımsızlık demektir. Burglary ve Earthquake bağımsız, ama Alarm verildiğinde bağımlı. |
| "Düğüm sırası farketmez, her sıra aynı ağı verir." | Hırsız ağında 10, 13 ya da 31 parametre. |
| "Değişken eleme her zaman polinomdur." | Çok ağaçlarda doğrusal; genelde NP-zor. |
| "Ret örneklemesi kanıt ne olursa olsun iyi çalışır." | Kanıt olasılığı küçüldükçe kabul edilen örnek sayısı çöker. |
| "P(y \| x) ile P(y \| do(x)) aynıdır." | Gözlem ve müdahale farklıdır: 0.3'e karşı 0.5. |

## Kendini yokla

1. Hırsız ağının parametre sayısı neden 10? Tam ortak tablo kaç sayı ister?
2. Burglary'nin Markov örtüsü nedir? Neden JohnCalls örtüde değil?
3. P(Burglary | alarm) ≈ 0.37 iken P(Burglary | alarm, earthquake) ≈ 0.003. Bu olgunun adı nedir?
4. Olabilirlik ağırlıklandırmada kanıt ağın köklerinde mi, yapraklarında mı olursa daha iyi çalışır?
5. P(Cloudy | Sprinkler = true) ve P(Cloudy | do(Sprinkler = true)) neden farklı?

## Kod rehberi

```bash
python ornekler/bayes_agi.py          # kütüphane: diş hekimi ağı, numaralandırma = eleme
python ornekler/hirsiz_alarmi.py      # 0.000628, P(B|j,m) = 0.284, düğüm sırası 10/13/31
python ornekler/yerel_dagilimlar.py   # gürültülü-VEYA ateş tablosu, probit / expit
python ornekler/ornekleme.py          # önsel, ret, olabilirlik ağırlıklandırma, Gibbs
python ornekler/nedensel.py           # gözlem vs do(), arka kapı ayarlaması
python ornekler/bayes_agi_kucuk.py    # özgün ofis alarmı ağı (numaralandırma)
python ornekler/cpt_goster.py         # CPT'leri okunaklı yazdırma
```

## Terimler

| Türkçe | İngilizce | Kısa açıklama |
|---|---|---|
| Bayes ağı | Bayesian network (belief network) | CPT'li yönlü döngüsüz grafik |
| yönlü döngüsüz grafik | directed acyclic graph (DAG) | Döngüsü olmayan yönlü grafik |
| koşullu olasılık tablosu | conditional probability table (CPT) | P(X \| ebeveynler) |
| koşullama durumu | conditioning case | Ebeveyn değerlerinin bir kombinasyonu |
| topolojik sıra | topological ordering | Ebeveynlerin çocuklardan önce geldiği sıra |
| Markov örtüsü | Markov blanket | Ebeveynler, çocuklar, çocukların diğer ebeveynleri |
| d-ayrım | d-separation | Grafikten koşullu bağımsızlık okuma |
| ahlaki grafik | moral graph | Ortak çocuklu ebeveynleri birleştirilmiş grafik |
| deterministik düğüm | deterministic node | Değeri ebeveynlerce kesin belirlenen düğüm |
| bağlama özgü bağımsızlık | context-specific independence (CSI) | Bazı ebeveyn değerlerinde bağımsızlık |
| gürültülü-VEYA | noisy-OR | k parametreli VEYA benzeri CPT |
| sızıntı düğümü | leak node | Listelenmeyen nedenleri temsil eder |
| karma ağ | hybrid Bayesian network | Ayrık + sürekli değişkenler |
| doğrusal Gauss | linear–Gaussian | Ortalaması ebeveynlerin doğrusal fonksiyonu olan normal dağılım |
| probit / expit (ters logit) | probit / expit (inverse logit) | Sürekli ebeveynli ayrık çocuk modelleri |
| numaralandırma ile çıkarım | inference by enumeration | Toplam–çarpım ağacı |
| değişken eleme | variable elimination | Faktörlerle dinamik programlama |
| faktör / noktasal çarpım | factor / pointwise product | Değişken elemenin yapı taşları |
| tekil bağlı ağ / çok ağaç | singly connected network / polytree | Doğrusal zamanlı kesin çıkarım |
| kümeleme / birleşim ağacı | clustering / join tree | Çoklu bağlı ağları çok ağaca çevirme |
| doğrudan örnekleme | direct (prior) sampling | Topolojik sırayla örnekleme |
| ret örneklemesi | rejection sampling | Kanıtla uyuşmayanları atma |
| olabilirlik ağırlıklandırma | likelihood weighting | Kanıtı sabitleyip ağırlıklandırma |
| önem örneklemesi | importance sampling | Başka dağılımdan örnekleyip ağırlıklandırma |
| Markov zinciri Monte Carlo | Markov chain Monte Carlo (MCMC) | Önceki örneği rastgele değiştirerek örnekleme |
| Gibbs örneklemesi | Gibbs sampling | Markov örtüsüne koşullu MCMC |
| açıklayıp götürme | explaining away | Bir nedeni öğrenmenin diğerini zayıflatması |
| nedensel ağ | causal network | Okları nedensel mekanizma olan ağ |
| müdahale / do-işleci | intervention / do-operator | Değişkeni dışarıdan sabitleme |
| arka kapı ölçütü | back-door criterion | Müdahaleyi gözlemsel veriden hesaplama koşulu |
