# Bölüm 12 — Belirsizliği nicelendirme

> **Kitapta:** AIMA 4. baskı, Bölüm 12 *"Quantifying Uncertainty"*.
> Önce kitabı oku, sonra bu notlarla pekiştir. Metin özgündür; kitaptan alıntı yoktur.

## Bu bölümün haritası

| Kitap alt bölümü | Bu nottaki karşılığı | Kod |
|---|---|---|
| 12.1 Acting under Uncertainty | §1 Neden mantık yetmez; karar kuramı | `cozumler/alistirma_kod.py` (havalimanı) |
| 12.2 Basic Probability Notation | §2 Olası dünyalar, önsel/koşullu olasılık, aksiyomlar, de Finetti | `olasilik.py`, `hollanda_kitabi.py` |
| 12.3 Inference Using Full Joint Distributions | §3 Marjinalleştirme, koşullama, normalizasyon | `dis_hekimi.py` |
| 12.4 Independence | §4 Mutlak bağımsızlık | `dis_hekimi.py` |
| 12.5 Bayes' Rule and Its Use | §5 Bayes kuralı, kanıtları birleştirme, koşullu bağımsızlık | `bayes_kurali.py` |
| 12.6 Naive Bayes Models | §6 Naif Bayes, metin sınıflandırma | `naive_bayes_mini.py` |
| 12.7 The Wumpus World Revisited | §7 Çukur olasılıkları | `wumpus_olasilik.py` |

## Öğrenme hedefleri

1. Mantığın belirsiz alanlarda neden yetersiz kaldığını ve karar kuramının ne eklediğini açıklamak.
2. Olası dünyalar, önsel ve koşullu olasılık, çarpım kuralı ve aksiyomlarla rahatça çalışmak.
3. Tam ortak dağılımdan marjinalleştirme ve normalizasyonla her sorguyu yanıtlamak.
4. Mutlak ve koşullu bağımsızlığın temsili nasıl küçülttüğünü göstermek.
5. Bayes kuralını ve naif Bayes modelini uygulamak; Wumpus dünyasında olasılıkla karar vermek.

---

## 1. Belirsizlik altında eylem

Diş hekimi örneği: "Toothache ⇒ Cavity" kuralı yanlıştır (ağrının başka nedenleri de var). "Cavity ⇒ Toothache" de yanlıştır (her çürük ağrıtmaz). Kuralı düzeltmek için sonsuz bir koşul listesi gerekir. Kitap, mantığın başarısızlığını üç nedene bağlar:

| Neden | Anlamı |
|---|---|
| **Tembellik** | İstisnasız bir kural için bütün koşulları listelemek çok zahmetli. |
| **Kuramsal bilgisizlik** | Alanın tam bir kuramı yok (tıp her şeyi bilmiyor). |
| **Pratik bilgisizlik** | Kurallar bilinse bile, bu hasta için gerekli testlerin hepsi yapılmamış. |

Ajanın bilgisi ancak bir **inanç derecesi** verebilir. Olasılık, bu inancı özetler: "Ağrısı olan hastaların %80'inde çürük var" gibi. Olasılıklar **ajanın bilgi durumuna** görelidir: Yeni kanıt geldikçe değişir. Bu bir çelişki değildir, farklı bilgi durumları hakkında farklı iddialardır.

**Karar kuramı = olasılık kuramı + fayda kuramı.** Havalimanına 90 dakika önce çıkmak (A90) uçağı %97 olasılıkla yakalatıyorsa bu rasyonel mi? Belki A180 daha güvenli. Ama 24 saat önce çıkmak (A1440) katlanılmaz bir bekleme demek. Doğru seçim, her sonucun **faydasını** olasılığıyla tartıp **beklenen faydası en yüksek** (MEU) eylemi seçmektir.

---

## 2. Temel gösterim

- **Örnek uzay Ω:** Olası dünyaların kümesi (birbirini dışlayan ve kapsayan). İki zar için 36 dünya.
- **Olasılık modeli:** Her dünyaya 0 ≤ P(ω) ≤ 1, toplam 1.
- **Önerme (olay):** Bir dünyalar kümesi. **P(φ) = Σ_{ω ∈ φ} P(ω).** Adil zarlarla P(Toplam = 11) = 2/36 = 1/18.
- **Önsel (koşulsuz) olasılık:** Başka bilgi yokken P(a).
- **Koşullu (sonsal) olasılık:** P(a | b) = P(a ∧ b) / P(b). Birinci zar 5 gösteriyorsa P(çift | Zar1 = 5) = 1/6.
- **Çarpım kuralı:** P(a ∧ b) = P(a | b) P(b).
- **Rastgele değişken:** Değer alanı olan bir fonksiyon (Weather ∈ {güneşli, yağmurlu, bulutlu, karlı}). **P(Weather)** kalın P ile tüm dağılımı gösterir: ⟨0.6, 0.1, 0.29, 0.01⟩.
- Sürekli değişkenler için **olasılık yoğunluk fonksiyonu** kullanılır (bir noktanın olasılığı 0'dır; yoğunluk 1'den büyük olabilir).

`olasilik.py` bu kavramları doğrudan kodlar: `OrtakDagilim`, `P(olay, kanit)`, `kosullu`, `marjinal`, `bagimsiz_mi`.

### 2.1 Aksiyomlar ve neden onlara uymalıyız

Kolmogorov aksiyomlarından türeyenler:
- P(¬a) = 1 − P(a)
- **Dahil etme–dışlama:** P(a ∨ b) = P(a) + P(b) − P(a ∧ b)

**de Finetti'nin argümanı** (`hollanda_kitabi.py`): İnançların bahis oranları demektir. Aksiyomları çiğneyen bir ajana karşı, **her sonuçta** kaybettiren bir bahis kombinasyonu kurulabilir. Kitaptaki örnek: P(a) = 0.4, P(b) = 0.3, P(a ∧ b) = 0, P(a ∨ b) = 0.8 (0.7 olmalıydı). Karşı taraf a'ya 4$, b'ye 3$, ¬(a ∨ b)'ye 2$ yatırır. Ajan 1'in kazançları: −11, −1, −1, −1. Tutarlı inançlarda ise her adil bahsin beklenen değeri 0'dır, bu yüzden garanti kayıp kurulamaz.

"Bahse girmezsem?" itirazının yanıtı: Her eylem (hareketsizlik dahil) bir tür bahistir.

---

## 3. Tam ortak dağılımla çıkarım (`dis_hekimi.py`)

Kitaptaki tablo (Toothache, Catch, Cavity):

| | toothache, catch | toothache, ¬catch | ¬toothache, catch | ¬toothache, ¬catch |
|---|---|---|---|---|
| **cavity** | 0.108 | 0.012 | 0.072 | 0.008 |
| **¬cavity** | 0.016 | 0.064 | 0.144 | 0.576 |

- **Marjinalleştirme (toplamla çıkarma):** P(cavity) = 0.108 + 0.012 + 0.072 + 0.008 = **0.2**.
- P(cavity ∨ toothache) = **0.28**.
- **Koşullama:** P(cavity | toothache) = (0.108 + 0.012) / 0.2 = **0.6**.
- **Normalizasyon:** P(Cavity | toothache) = α ⟨0.12, 0.08⟩ = **⟨0.6, 0.4⟩**. P(toothache)'ı hesaplamaya gerek yok; α, toplamı 1 yapan sabittir.
- İki kanıtla: P(Cavity | toothache, catch) ≈ **⟨0.871, 0.129⟩**.

**Genel çıkarım formülü:** Sorgu X, kanıt e, gözlenmeyen değişkenler Y:

**P(X | e) = α Σ_y P(X, e, y)**

Her sorguyu yanıtlar, ama n Boole değişkeni için tablo 2ⁿ satırdır. Zaman ve bellek O(2ⁿ): Ölçeklenmez.

---

## 4. Bağımsızlık

Weather'ı eklersek tablo 8 × 4 = 32 satır olur. Ama diş sorunları havayı etkilemez:

P(Toothache, Catch, Cavity, Weather) = P(Toothache, Catch, Cavity) P(Weather)

32 sayı yerine 8 + 4 yeter. **Bağımsızlık:** P(a | b) = P(a) ya da P(b | a) = P(b) ya da P(a ∧ b) = P(a) P(b) (üçü denktir). n bağımsız yazı-tura: 2ⁿ yerine n sayı.

Sorun: Tam bağımsızlık nadirdir. Bir bağlantı (dolaylı bile olsa) varsa bağımsızlık bozulur.

---

## 5. Bayes kuralı (`bayes_kurali.py`)

**P(b | a) = P(a | b) P(b) / P(a)**

Genelde **nedensel** yönde (neden → belirti) bilgi vardır, **tanısal** yönde (belirti → neden) soru sorulur.

**Menenjit:** P(s | m) = 0.7, P(m) = 1/50000, P(s) = 0.01 → **P(m | s) = 0.0014.** Belirti güçlü olsa da hastalık çok nadir olduğu için sonsal küçük kalır.

**Neden nedensel bilgi saklanır?** Salgın çıkarsa P(m) artar. Tanısal P(m | s)'yi doğrudan istatistikten öğrenmiş bir doktor onu nasıl güncelleyeceğini bilemez. P(s | m) ise menenjitin nasıl işlediğini yansıtır, salgından etkilenmez. Bayes'le hesaplayan doktor, P(m | s)'nin P(m) ile orantılı arttığını görür.

**Normalizasyonla:** P(M | s) = α ⟨P(s | m) P(m), P(s | ¬m) P(¬m)⟩. P(s) yerine P(s | ¬m) tahmin edilmelidir.

### 5.1 Kanıtları birleştirme ve koşullu bağımsızlık

İki kanıt: P(Cavity | toothache ∧ catch) = α P(toothache ∧ catch | Cavity) P(Cavity). n kanıt için 2ⁿ kombinasyon gerekir: yine ölçeklenmez.

Toothache ve Catch bağımsız değildir (sonda takılıyorsa çürük olasıdır, çürük de ağrıtır). Ama **Cavity biliniyorsa** bağımsızdırlar: Ağrı sinirlere, sondanın takılması hekimin becerisine bağlıdır. **Koşullu bağımsızlık:**

**P(X, Y | Z) = P(X | Z) P(Y | Z)**

Böylece P(Cavity | toothache, catch) = α P(toothache | Cavity) P(catch | Cavity) P(Cavity) = α ⟨0.6 · 0.9 · 0.2, 0.1 · 0.2 · 0.8⟩ ≈ ⟨0.871, 0.129⟩. Tablo 7 bağımsız sayı yerine 2 + 2 + 1 = 5 sayıyla ifade edilir. n belirtide O(2ⁿ) yerine **O(n)**. Kitabın vurgusu: Büyük olasılık alanlarını koşullu bağımsızlıkla zayıf bağlı parçalara ayırmak, yakın dönem yapay zekânın en önemli gelişmelerinden biridir.

---

## 6. Naif Bayes modelleri

Tek bir neden, birbirinden koşullu bağımsız birçok etki:

**P(Neden, Etki₁, …, Etkiₙ) = P(Neden) Π P(Etkiᵢ | Neden)**

"Naif", çünkü etkiler gerçekte tam bağımsız olmasa da bu varsayım yapılır. Pratikte çoğu zaman şaşırtıcı iyi çalışır.

Çıkarım: **P(Neden | e) = α P(Neden) Π_j P(e_j | Neden).** Gözlenmeyen etkiler hesaptan tamamen çıkar (toplamları 1'dir). Süre, gözlenen etki sayısıyla doğrusaldır.

**Metin sınıflandırma:** Neden = Kategori (haber, spor, ekonomi, hava, eğlence). Etkiler = HasWordᵢ (belgede i. kelime var mı). P(Kategori) = kategorideki belgelerin oranı. P(HasWordᵢ | Kategori) = o kategoride i. kelimeyi içeren belgelerin oranı.

**Dikkat:** Eğitimde hiç görülmemiş bir kelimeye 0 olasılık verilirse bütün çarpım 0 olur ve diğer kanıtların hepsi silinir. Görülmemiş kelimeler için küçük bir pay ayrılmalıdır (`naive_bayes_mini.py` Laplace yumuşatması kullanır; ayrıntısı Bölüm 20'de).

`naive_bayes_mini.py`, kitaptaki HasWord (var/yok) modelinden biraz farklıdır: Kelime **sayılarını** kullanır (çok terimli naif Bayes). Fikir aynıdır.

---

## 7. Wumpus dünyasına dönüş (`wumpus_olasilik.py`)

Ajan [1,1]'de esinti yok, [1,2] ve [2,1]'de esinti algıladı. [1,3], [2,2], [3,1]'in her biri çukur olabilir. Mantık "bilinmiyor" der ve ajan rastgele seçmek zorunda kalır.

Olasılık modeli: Her karede bağımsız 0.2 olasılıkla çukur. P(b | çukurlar) ya 1 ya 0'dır (esintiler çukurlarla tutarlı mı?).

- **Saf yöntem:** Sorgu dışındaki 12 bilinmeyen kare: 2¹² = 4096 terim.
- **Akıllı yöntem:** Bilinmeyenleri **sınır** (ziyaret edilen karelere komşu) ve **diğer** diye ayır. Gözlenen esintiler, bilinenler, sorgu ve sınır verildiğinde diğer karelerden koşullu bağımsızdır. Diğer kareler toplamdan tamamen çıkar:

**P(P₁,₃ | known, b) = α P(P₁,₃) Σ_sınır P(b | known, P₁,₃, sınır) P(sınır)**

Sınırda 2 kare → 4 terim. Sonuç:
- P(P₁,₃) = α ⟨0.2 (0.04 + 0.16 + 0.16), 0.8 (0.04 + 0.16)⟩ ≈ **⟨0.31, 0.69⟩**; simetriyle [3,1] de 0.31.
- P(P₂,₂) ≈ **0.86.** Ajan [2,2]'den kesinlikle kaçınmalı.

Kodumuz iki yöntemi de çalıştırıp aynı sonucu verdiklerini gösterir. Ek senaryoda **açıklayıp götürme** görülür: [1,3] boş ve esintisiz çıkarsa [2,2] kesin çukur olur ve [3,1] önsele (0.2) döner, çünkü [2,1]'deki esinti artık açıklanmıştır.

---

## Sık yapılan hatalar

| Yanılgı | Doğrusu |
|---|---|
| "P(a \| b) ile P(b \| a) yaklaşık aynıdır." | Menenjit: P(s \| m) = 0.7, P(m \| s) = 0.0014. Önsel çok önemlidir. |
| "Olasılık, olayın 'gerçek' özelliğidir; kanıtla değişmez." | Bu bölümde olasılık ajanın inanç derecesidir; kanıtla güncellenir. |
| "Koşullu bağımsızlık, mutlak bağımsızlık demektir." | Toothache ve Catch, Cavity verildiğinde bağımsız, ama tek başlarına bağımlıdır. |
| "Normalizasyon bir hile; P(e) bilinmeden sonuç yanlış olur." | α, toplamı 1 yapan sabittir; sonuç aynıdır. |
| "Görülmemiş kelimenin olasılığı 0'dır." | 0 bütün kanıtı siler; yumuşatma gerekir. |
| "İnançlar biraz tutarsız olsa ne olur?" | de Finetti: Garanti kaybettiren bahisler kurulabilir. |

## Kendini yokla

1. P(a ∨ b)'yi dahil etme–dışlama ile yaz. Neden P(a ∧ b) çıkarılır?
2. Tam ortak dağılım tablosundan P(¬cavity | toothache)'ı hesapla.
3. Bir salgında P(m) 10 katına çıkarsa P(m | s) ne olur?
4. 20 belirtili bir naif Bayes modelinde kaç bağımsız sayı gerekir? Tam tabloda kaç?
5. Wumpus örneğinde neden [4,4]'teki çukur [1,3] hakkındaki inancı etkilemez?

## Kod rehberi

```bash
python ornekler/olasilik.py          # kütüphane: iki zar, P(Toplam=11) = 1/18
python ornekler/dis_hekimi.py        # tam ortak dağılım, normalizasyon, bağımsızlık
python ornekler/bayes_kurali.py      # menenjit 0.0014, kanıtları birleştirme, nadir hastalık
python ornekler/hollanda_kitabi.py   # de Finetti: −11, −1, −1, −1
python ornekler/naive_bayes_mini.py  # metin sınıflandırma (spam / normal)
python ornekler/wumpus_olasilik.py   # çukur olasılıkları 0.31 / 0.86
```

## Terimler

| Türkçe | İngilizce | Kısa açıklama |
|---|---|---|
| inanç derecesi | degree of belief | Ajanın bir önermeye güveni |
| tembellik / kuramsal / pratik bilgisizlik | laziness / theoretical / practical ignorance | Mantığın belirsiz alanlarda başarısız olma nedenleri |
| karar kuramı | decision theory | Olasılık + fayda kuramı |
| en yüksek beklenen fayda | maximum expected utility (MEU) | Rasyonel eylem seçimi ilkesi |
| örnek uzay / olası dünya | sample space / possible world | Birbirini dışlayan tam durumlar |
| önsel / sonsal olasılık | prior / posterior probability | Kanıttan önce / sonra inanç |
| koşullu olasılık | conditional probability | P(a \| b) = P(a ∧ b) / P(b) |
| çarpım kuralı | product rule | P(a ∧ b) = P(a \| b) P(b) |
| olasılık dağılımı | probability distribution | Bir değişkenin tüm değerlerinin olasılıkları |
| olasılık yoğunluk fonksiyonu | probability density function | Sürekli değişkenler için |
| tam ortak dağılım | full joint distribution | Tüm değişkenlerin tüm değer kombinasyonları |
| dahil etme–dışlama | inclusion–exclusion | P(a ∨ b) = P(a) + P(b) − P(a ∧ b) |
| marjinalleştirme | marginalization (summing out) | Bir değişkeni toplamla çıkarma |
| normalizasyon | normalization | Toplamı 1 yapan α sabiti |
| (mutlak) bağımsızlık | (absolute) independence | P(a ∧ b) = P(a) P(b) |
| koşullu bağımsızlık | conditional independence | P(X, Y \| Z) = P(X \| Z) P(Y \| Z) |
| Bayes kuralı | Bayes' rule | P(b \| a) = P(a \| b) P(b) / P(a) |
| nedensel / tanısal | causal / diagnostic | Neden → belirti / belirti → neden yönü |
| naif Bayes | naive Bayes | Koşullu bağımsız etkilerle tek neden |
| metin sınıflandırma | text classification | Belgeyi kategoriye atama |
| sınır | frontier | Ziyaret edilen karelere komşu bilinmeyen kareler |
