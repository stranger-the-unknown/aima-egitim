# Bölüm 15 — Olasılıksal programlama

> **Kitapta:** AIMA 4. baskı, Bölüm 15 *"Probabilistic Programming"*.
> Önce kitabı oku, sonra bu notlarla pekiştir. Metin özgündür; kitaptan alıntı yoktur.

## Bu bölümün haritası

| Kitap alt bölümü | Bu nottaki karşılığı | Kod |
|---|---|---|
| 15.1 Relational Probability Models | §1 Tipler, bağımlılık ifadeleri, temellendirme; beceri derecelendirme | `rpm_oneriler.py`, `beceri_derecelendirme.py` |
| 15.2 Open-Universe Probability Models | §2 Sayı ifadeleri, köken fonksiyonları, kimlik belirsizliği | `acik_evren.py` |
| 15.3 Keeping Track of a Complex World | §3 Çok hedefli izleme, veri ilişkilendirme | `cozumler/alistirma_kod.py` (A9) |
| 15.4 Programs as Probability Models | §4 Üretimsel programlar, bozulmuş metni okumak | `metin_okuma.py`, `basit_uretimsel_model.py`, `reddetme_ornekleme.py` |

## Öğrenme hedefleri

1. Bayes ağlarının neden "önermesel" kaldığını ve birinci dereceden olasılık modellerinin neden gerektiğini açıklamak.
2. İlişkisel bir olasılık modeli (RPM) yazmak ve onu Bayes ağına temellendirmek.
3. Açık evren modellerinde nesne sayısı ve kimlik belirsizliğini modellemek.
4. Veri ilişkilendirme probleminin neden zor olduğunu göstermek.
5. Bir programı olasılık modeli olarak görmek ve gözlemlerden onun rastgele seçimlerini çıkarmak.

---

## Neden olasılıksal programlama?

Bölüm 13'teki Bayes ağları **önermesel mantık** gibidir: Değişkenler sabittir, nesneler ve ilişkiler yoktur. Bir kitap satış sitesinin milyonlarca müşterisi ve kitabı için her birine ayrı düğüm yazmak mümkün değildir. Birinci dereceden mantığın (Bölüm 8) ifade gücünü olasılıkla birleştirmek gerekir.

Kitaptaki ayrım:
- **Kapalı evren** (veritabanı anlamı): Her sabit farklı bir nesnedir, başka nesne yoktur. → **RPM**
- **Açık evren**: Nesne sayısı bilinmez, iki isim aynı nesneyi gösterebilir. → **OUPM**

---

## 1. İlişkisel olasılık modelleri (`rpm_oneriler.py`)

**Kitap önerisi örneği.** Müşteri c, kitap b'ye 1–5 puan verir. Puan, müşterinin **dürüstlüğüne** ve **nezaketine**, kitabın **kalitesine** bağlıdır.

**Tip imzaları:**
```text
Honest : Customer → {true, false}
Kindness : Customer → {1..5}
Quality : Book → {1..5}
Recommendation : Customer × Book → {1..5}
```

**Bağımlılık ifadeleri:**
```text
Honest(c)            ~ ⟨0.99, 0.01⟩
Kindness(c)          ~ ⟨0.1, 0.1, 0.2, 0.3, 0.3⟩
Quality(b)           ~ ⟨0.05, 0.2, 0.4, 0.2, 0.15⟩
Recommendation(c, b) ~ RecCPT(Honest(c), Kindness(c), Quality(b))     (2 × 5 × 5 = 50 satır)
```

**Temellendirme (açma):** C müşteri ve B kitap için Bayes ağı kurulur: 2C + B + BC düğüm. Birinci dereceden mantıktaki önermeselleştirmenin tam karşılığı. Büyük alanlarda çok büyük olabilir.

**Bağlama özgü bağımsızlık:** Dürüst olmayan müşteri kitaba bakmaz:
```text
Recommendation(c, b) ~ if Honest(c) then HonestRecCPT(Kindness(c), Quality(b))
                       else ⟨0.4, 0.1, 0.0, 0.1, 0.4⟩
```

**İlişkisel belirsizlik:** Müşteri, yazarın hayranıysa hep 5 verir: `if Fan(c, Author(b)) then Exactly(5)`. Author(b) bilinmiyorsa, bütün olası yazarların Fan(c, a) değişkenleri ebeveyn olur ve Author(b) bir **çoğullayıcı** (multiplexer) gibi hangisinin etkili olduğunu seçer.

Kodumuz HonestRecCPT için kendi varsayımımızı kullanır ve kesin çıkarım yapar: Üç dürüst görünen müşteri B1'e 4, 5, 4 verince E[Quality(B1)] 3.2'den 4.18'e çıkar. Dördüncü bir müşteri tam tersini söylerse (B1 → 1, B2 → 5) model onun dürüst olmadığına karar verir ve puanlarını görmezden gelir.

### 1.1 Oyuncu becerisini derecelendirme (`beceri_derecelendirme.py`)

Elo'ya Bayesçi bir alternatif:
```text
Skill(i)          ~ N(μ, σ²)
Performance(i, g) ~ N(Skill(i), β²)
Win(i, j, g)      = if Game(g, i, j) then Performance(i, g) > Performance(j, g)
```
Takım oyunlarında takım performansı, oyuncuların performanslarının toplamıdır. Takım bileşimleri değiştikçe bireysel beceriler bile öğrenilebilir. Microsoft'un **TrueSkill** sistemi bu modeli kullanır. Kodumuz olabilirlik ağırlıklandırmayla sonsal becerileri ve yeni maçların sonucunu hesaplar. Burak > Ceren > Deniz > Burak döngüsü ve üçünün de Ayşe'ye kaybetmesi, üçünü eşit gösterir.

### 1.2 RPM'lerde çıkarım

1. **Temellendir ve Bayes ağı algoritması uygula.** Yalnızca sorguyla ilgili değişkenler (sorgu ve kanıtın ataları) örneklenmeli; küçük bir parça çoğu zaman yeter.
2. **Tekrarlanan yapıyı kullan:** Açılmış ağdaki özdeş faktörler önbelleğe alınabilir (kitap büyük ağlarda üç büyüklük mertebesi hızlanmadan söz eder). Kodumuz da müşterilerin, kitap kaliteleri verildiğinde bağımsız olmasını kullanır.
3. **MCMC:** Her örnek tam bir dünya olduğu için ilişkisel yapı (Author(B2) kim?) her örnekte bellidir; ilişkisel belirsizlik ağı büyütmez.
4. **Kaldırılmış çıkarım (lifted inference):** Birinci dereceden çözümlemenin karşılığı; nesneleri tek tek temellendirmeden, gruplar hâlinde akıl yürütür.

---

## 2. Açık evren olasılık modelleri (`acik_evren.py`)

Gerçek dünyada kaç nesne olduğu ve hangi ismin hangi nesneyi gösterdiği bilinmez:
- Bir sitede bir müşteri birden çok giriş kimliği açabilir (**sybil**, sybil saldırısı).
- Bir makalenin farklı yazılmış atıfları aynı makaleyi gösterebilir.
- Radardaki iki işaret aynı uçağa ait olabilir.

**Sayı ifadeleri:**
```text
#Customer            ~ UniformInt(1, 3)
#Book                ~ UniformInt(2, 4)
#LoginID(Owner = c)  ~ if Honest(c) then Exactly(1) else UniformInt(2, 5)
```
**Owner** bir **köken fonksiyonudur**: Her giriş kimliği onu açan müşteriyi bilir. Olası bir dünya, bu sayı ifadelerinin ve temel rastgele değişkenlerin her birine değer verir.

Kodumuzdaki kesin hesap: 4 giriş kimliği görülürse, en fazla 3 müşteri olabildiğinden **en az biri kesinlikle sahtekârdır** (P = 1). Sonsal: P(#Customer = 1, 2, 3) ≈ 0.17, 0.34, 0.50. 3 kimlik görülürse en olası açıklama üç dürüst müşteridir (0.99).

**Poisson dağılımı** nesne sayıları için yaygındır: Ortalama λ, standart sapma √λ. Büyük λ'da göreli belirsizlik çok küçüktür (λ = 10⁶ için %0.1). "Bir milyon civarı" gibi kaba bilgiler için kitap büyüklük mertebesi dağılımlarını önerir.

### 2.1 Kitaptaki uygulamalar

- **Atıf eşleştirme:** Farklı yazılmış atıf dizgelerinin hangi makaleye ait olduğunu bulmak. Model, atıf metninin yazarlardan ve başlıktan (hatalarla) nasıl üretildiğini tanımlar. Kitaptaki çarpıcı örnek: 2002'de CiteSeer, Russell ve Norvig'e ait 120'den fazla farklı kitap listelemişti. OUPM çıkarımı CiteSeer'e göre 2–3 kat daha az hata yapar. Bir makaleye ne kadar çok atıf varsa her biri o kadar doğru çözümlenir (**toplu, bilgiye dayalı belirsizlik giderme**).
- **Nükleer deneme yasağı denetimi (NET-VISA):** Klasik otomatik sistemin algılama hatası oranı yaklaşık %30'dur. NET-VISA jeofiziği doğrudan modeller: Sismik olayların sayısı Poisson, her istasyondaki algılamalar olaylardan ya da gürültüden üretilir. Algılama hatalarını önemli ölçüde azaltır.

---

## 3. Karmaşık bir dünyayı izlemek

**Çok hedefli izleme:** Radar ekranında her adımda birkaç işaret (blip) görünür, ama hangisinin hangi uçağa ait olduğu bilinmez. **Veri ilişkilendirme** problemi: Gözlemleri nesnelere eşlemek.

Gerçek sistemlerde ayrıca:
- **Yanlış alarmlar** (kargaşa): Hiçbir nesneye ait olmayan işaretler. `#Blip(Time = t) ~ Poisson(λf)`.
- **Algılama hataları:** Nesne işaret üretmeyebilir.
- Nesneler sahneye girer ve çıkar.

n nesne ve T adım için olası eşleşme sayısı (n!)^T gibi üstel büyür. Yaklaşımlar:
- **En yakın komşu filtresi:** Her adımda tahmin edilen konuma en yakın gözlemi seç. Hızlı ama yakın hedeflerde hata yapar.
- **Macar algoritması:** Her adımda toplam uyuşmazlığı en küçük eşleşmeyi bulur; ama tek bir en iyi eşleşmeye bağlanır.
- **MCMC / parçacık filtresi:** Eşleşme hipotezleri üzerinde olasılık dağılımı tutar.

**Trafik gözetimi:** Otoyol kameralarında aynı aracın farklı kameralardaki görüntülerini eşlemek; seyahat sürelerini buradan çıkarmak.

---

## 4. Programlar olasılık modeli olarak (`metin_okuma.py`)

**Üretimsel program:** Her rastgele seçimi bir rastgele değişken tanımlayan, çalıştırılabilir bir program. Bir çalıştırmanın **yürütme izi** (execution trace) bir olası dünyadır; olasılığı, yaptığı rastgele seçimlerin olasılıklarının çarpımıdır. Pek çok olasılıksal programlama dili **hesaplama açısından evrenseldir**: Durmaları koşuluyla olasılıksal bir Turing makinesinin örnekleyebildiği her dağılımı temsil edebilirler.

**Bozulmuş metni okumak:** Program (1) bir harf dizisi üretir, (2) onu gürültülü ve bulanık bir görüntüye çizer. Çıkarım: Görüntüden harfleri bulmak. Kitap MCMC kullanır ve iki model karşılaştırır: Harfler bağımsız ya da bir **ikili harf (bigram) Markov modeliyle**. Çok gürültülü görüntülerde Markov modelinin sonuçları olası harf dizileri hakkındaki önsel bilgiyi yansıtır.

Kodumuzdaki küçük sürüm: 17 harf için 5×3 piksellik şekiller, her piksel p olasılıkla ters. Harf sınırları bilindiği için kesin çıkarım yapılabilir (Markov modelinde Viterbi, Bölüm 14):

| p | bağımsız | ikili harf |
|---|---|---|
| 0.05 | %91 | %94 |
| 0.25 | %48 | %53 |
| 0.35 | %26 | %34 |

Önsel bilgi ortalamada yardım eder, ama bazen okumayı sık görülen harf dizilerine çekip yeni hata yaratır.

**Çıkarım yöntemleri:** Reddetme örneklemesi (`reddetme_ornekleme.py`), olabilirlik ağırlıklandırma, MCMC. Genel amaçlı çıkarım motoru yazmak zordur; verimli olmak için programın yapısını (hangi seçimin hangisine bağlı olduğunu) kullanmak gerekir.

---

## Sık yapılan hatalar

| Yanılgı | Doğrusu |
|---|---|
| "Bayes ağları her alanı rahatça modeller." | Nesne ve ilişki sayısı büyükse önermesel gösterim patlar; RPM/OUPM gerekir. |
| "Temellendirme her zaman bütün ağı kurmayı gerektirir." | Yalnızca sorgu ve kanıtla ilgili parça yeter. |
| "Her isim farklı bir nesnedir." | Açık evrende iki isim aynı nesneyi gösterebilir (sybil, atıflar). |
| "Veri ilişkilendirmede en yakın komşu yeterlidir." | Yakın hedeflerde ve kargaşada hatalı; hipotezler üzerinde dağılım gerekir. |
| "Olasılıksal program, sıradan bir simülasyondur." | Simülasyon ileri çalışır; olasılıksal programlama gözlemden geriye, rastgele seçimleri çıkarır. |

## Kendini yokla

1. RPM ile OUPM arasındaki temel fark nedir?
2. 3 müşteri ve 4 kitap için temellendirilmiş ağda kaç düğüm olur?
3. Köken fonksiyonu ne işe yarar?
4. İki hedef ve 10 adım için kaç veri ilişkilendirme hipotezi vardır?
5. Bir programın "yürütme izi" ile Bayes ağındaki "olası dünya" arasındaki ilişki nedir?

## Kod rehberi

```bash
python ornekler/rpm_oneriler.py            # kitap önerisi RPM'i: temellendirme, kesin çıkarım
python ornekler/beceri_derecelendirme.py   # TrueSkill benzeri beceri modeli
python ornekler/acik_evren.py              # sayı ifadeleri, sybil çıkarımı, Poisson
python ornekler/metin_okuma.py             # bozulmuş metni okumak: bağımsız vs ikili harf modeli
python ornekler/basit_uretimsel_model.py   # özgün hileli zar modeli
python ornekler/reddetme_ornekleme.py      # aynı modelde reddetme örneklemesi
```

## Terimler

| Türkçe | İngilizce | Kısa açıklama |
|---|---|---|
| olasılıksal programlama dili | probabilistic programming language (PPL) | Olasılık modellerini program olarak yazma dili |
| ilişkisel olasılık modeli | relational probability model (RPM) | Kapalı evrende nesneler ve ilişkilerle olasılık |
| tip imzası | type signature | Fonksiyon argümanlarının ve değerinin tipleri |
| bağımlılık ifadesi | dependency statement | Bir fonksiyonun koşullu dağılımı |
| temellendirme / açma | grounding / unrolling | RPM'den Bayes ağı kurma |
| ilişkisel belirsizlik | relational uncertainty | Hangi nesnenin ilişkili olduğunun bilinmemesi |
| çoğullayıcı | multiplexer | Bir ebeveynin hangi diğer ebeveynin etkili olacağını seçmesi |
| kaldırılmış çıkarım | lifted inference | Nesneleri gruplar hâlinde ele alan çıkarım |
| açık evren olasılık modeli | open-universe probability model (OUPM) | Nesne sayısı ve kimliği belirsiz modeller |
| sayı ifadesi | number statement | Bir tipteki nesne sayısının dağılımı |
| köken fonksiyonu | origin function | Nesnenin nereden geldiğini söyleyen fonksiyon |
| kimlik belirsizliği | identity uncertainty | İki ismin aynı nesne olup olmadığı |
| sybil saldırısı | sybil attack | Sahte kimliklerle itibar sistemini yanıltma |
| atıf eşleştirme | citation matching | Atıf dizgelerini makalelere bağlama |
| veri ilişkilendirme | data association | Gözlemleri nesnelere eşleme |
| yanlış alarm / kargaşa | false alarm / clutter | Nesneden gelmeyen gözlem |
| algılama hatası | detection failure | Nesnenin gözlem üretmemesi |
| en yakın komşu filtresi | nearest-neighbor filter | Açgözlü veri ilişkilendirme |
| üretimsel program | generative program | Rastgele seçimler yapan, model tanımlayan program |
| yürütme izi | execution trace | Bir çalıştırmadaki rastgele seçimlerin değerleri |
