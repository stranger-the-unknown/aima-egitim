# Bölüm 14 — Zaman içinde olasılıksal akıl yürütme

> **Kitapta:** AIMA 4. baskı, Bölüm 14 *"Probabilistic Reasoning over Time"*.
> Önce kitabı oku, sonra bu notlarla pekiştir. Metin özgündür; kitaptan alıntı yoktur.

## Bu bölümün haritası

| Kitap alt bölümü | Bu nottaki karşılığı | Kod |
|---|---|---|
| 14.1 Time and Uncertainty | §1 Durumlar, gözlemler, geçiş ve algılayıcı modelleri | `zamansal.py` |
| 14.2 Inference in Temporal Models | §2 Filtreleme, tahmin, yumuşatma, en olası dizi | `semsiye.py` |
| 14.3 Hidden Markov Models | §3 Matris algoritmaları, konumlandırma | `zamansal.py`, `lokalizasyon.py` |
| 14.4 Kalman Filters | §4 Gauss güncellemesi, tek boyut, genel durum, sınırlar | `kalman.py` |
| 14.5 Dynamic Bayesian Networks | §5 DBN kurmak, algılayıcı arızaları, parçacık filtresi | `pil_sensoru.py`, `parcacik_filtresi.py` |

## Öğrenme hedefleri

1. Zamanla değişen bir dünyayı durum ve gözlem değişkenleriyle, geçiş ve algılayıcı modelleriyle kurmak.
2. Filtreleme, tahmin, yumuşatma ve en olası dizi görevlerini ayırt edip hesaplamak.
3. HMM'lerin matris algoritmalarını uygulamak (ileri–geri, Viterbi).
4. Kalman filtresinin güncellemesini yorumlamak; ne zaman yetersiz kaldığını bilmek.
5. DBN'lerin HMM'lerden neden daha tıkız olduğunu açıklamak ve parçacık filtresi uygulamak.

---

## 1. Zaman ve belirsizlik

Dünya, **zaman dilimlerinden** oluşan bir dizi olarak görülür. Her dilimde:
- **Durum değişkenleri X_t:** Gözlenemeyen (Yağmur_t).
- **Kanıt değişkenleri E_t:** Gözlenen (Şemsiye_t).

**Şemsiye dünyası:** Yeraltındaki bir güvenlik görevlisi dışarıyı göremez. Her sabah müdürün şemsiyeyle gelip gelmediğini görür ve yağmuru tahmin eder.

İki model gerekir:
- **Geçiş modeli P(X_t | X_{0:t−1}).** **Markov varsayımı:** Şimdiki durum yalnızca sonlu sayıda önceki duruma bağlıdır. **Birinci dereceden:** P(X_t | X_{t−1}). Ayrıca **durağan süreç** varsayılır: Geçiş kuralları zamanla değişmez.
- **Algılayıcı modeli P(E_t | X_t)** (**algılayıcı Markov varsayımı**): Gözlem yalnızca o anki duruma bağlıdır.

| Şemsiye dünyası | |
|---|---|
| P(R_t \| R_{t−1}) | 0.7 (dün yağmur) / 0.3 (dün kuru) |
| P(U_t \| R_t) | 0.9 (yağmur) / 0.2 (kuru) |
| P(R_0) | ⟨0.5, 0.5⟩ |

Tam ortak dağılım: **P(X_{0:t}, E_{1:t}) = P(X_0) Π P(X_i | X_{i−1}) P(E_i | X_i)**.

Birinci dereceden Markov varsayımı yetersizse iki yol var: Daha yüksek dereceli bir süreç kullanmak ya da **durum değişkenlerini zenginleştirmek** (Mevsim, Sıcaklık, Nem eklemek; bir robotta konuma hız ve pil düzeyi eklemek).

---

## 2. Zamansal modellerde çıkarım (`semsiye.py`)

| Görev | Hesaplanan | Örnek |
|---|---|---|
| **Filtreleme** (durum kestirimi) | P(X_t \| e_{1:t}) | Bugün yağmur var mı? |
| **Tahmin** | P(X_{t+k} \| e_{1:t}) | Üç gün sonra yağmur? |
| **Yumuşatma** | P(X_k \| e_{1:t}), k < t | Dün yağmur yağmış mıydı (bugünü de bilerek)? |
| **En olası açıklama** | argmax_{x_{1:t}} P(x_{1:t} \| e_{1:t}) | Hangi yağmur dizisi en olası? |
| **Öğrenme** | Modelin kendisi | EM (Bölüm 20) |

### 2.1 Filtreleme ve tahmin

**İleri özyineleme:** f_{1:t+1} = α P(e_{t+1} | X_{t+1}) Σ_{x_t} P(X_{t+1} | x_t) f_{1:t}

Önce **tahmin** (geçiş modeliyle ileri taşı), sonra **güncelleme** (gözlemle çarp, normalize et). Her adım sabit zaman ve bellek ister.

Kitaptaki hesap:
- P(R_1 | u_1) = α ⟨0.9, 0.2⟩ ⟨0.5, 0.5⟩ = α ⟨0.45, 0.1⟩ ≈ **⟨0.818, 0.182⟩**
- P(R_2 | u_1) ≈ ⟨0.627, 0.373⟩ (tahmin), P(R_2 | u_1, u_2) ≈ **⟨0.883, 0.117⟩**

**Tahmin**, kanıt eklemeden ileri özyinelemedir. Tahmin ufku uzadıkça dağılım **durağan dağılıma** (burada ⟨0.5, 0.5⟩) yakınsar. Bunun süresine **karışma süresi** denir. Ötesinde tahmin bilgi taşımaz.

**Olabilirlik** P(e_{1:t}), normalize edilmemiş ileri mesajın toplamıdır. Farklı modelleri karşılaştırmak için kullanılır.

### 2.2 Yumuşatma

P(X_k | e_{1:t}) = α f_{1:k} × b_{k+1:t}

**Geri mesaj:** b_{k+1:t} = Σ_{x_{k+1}} P(e_{k+1} | x_{k+1}) b_{k+2:t}(x_{k+1}) P(x_{k+1} | X_k), b_{t+1:t} = 1.

Kitaptaki hesap: b_{2:2} = ⟨0.69, 0.41⟩ → P(R_1 | u_1, u_2) = α ⟨0.818, 0.182⟩ × ⟨0.69, 0.41⟩ ≈ **⟨0.883, 0.117⟩**. Ertesi günün şemsiyesi dünkü yağmuru daha olası kılar.

**İleri–geri algoritması** bütün dizi için yumuşatmayı O(t) zamanda yapar. Bellek O(|f| t). **Sabit gecikmeli yumuşatma** P(X_{t−d} | e_{1:t}), çevrimiçi kullanımda d adım geriden gelir.

### 2.3 En olası dizi: Viterbi

Tek tek en olası durumları birleştirmek en olası **diziyi** vermez. **Viterbi** algoritması, filtrelemedeki toplam yerine **maksimum** alır:

m_{1:t+1} = P(e_{t+1} | X_{t+1}) max_{x_t} (P(X_{t+1} | x_t) m_{1:t}(x_t))

Her durum için en iyi öncülü gösteren işaretçiler saklanır; sonda geriye izlenir. Şemsiye dizisi [u, u, ¬u, u, u] için: **yağmur, yağmur, kuru, yağmur, yağmur**. Mesajlar: ⟨.8182, .1818⟩, ⟨.5155, .0491⟩, ⟨.0361, .1237⟩, ⟨.0334, .0173⟩, ⟨.0210, .0024⟩. Uzun dizilerde sayılar çok küçüldüğü için pratikte logaritmalarla çalışılır.

---

## 3. Gizli Markov modelleri (`zamansal.py`, `lokalizasyon.py`)

**HMM:** Durumun **tek bir ayrık** rastgele değişken olduğu zamansal model. Birden çok değişken varsa hepsi tek bir "süper değişkende" birleştirilir.

**Matris biçimi:** T_{ij} = P(X_t = j | X_{t−1} = i); O_t = köşegeninde P(e_t | X_t = i) olan köşegen matris.
- İleri: **f_{1:t+1} = α O_{t+1} Tᵀ f_{1:t}**
- Geri: **b_{k+1:t} = T O_{k+1} b_{k+2:t}**

S durumlu bir HMM'de her adım O(S²).

**Konumlandırma örneği:** Robot bir labirentte rastgele dolaşır. Dört algılayıcısı (K, G, D, B) o yönde engel olup olmadığını söyler; her bit ε olasılıkla yanlıştır:

P(e_t | X_t = i) = (1 − ε)^{4 − d} ε^d  (d: uyuşmayan bit sayısı)

Kitaptaki labirentte 42 boş kare var. `lokalizasyon.py` benzer bir özgün labirentte (45 kare) aynı deneyi yapar: ε ≤ 0.1 iken robot birkaç adımda yerini bulur; ε = 0.2'de yavaşça öğrenir; ε = 0.4'te kaybolur. Viterbi yolu tüm geçmişi birlikte kestirdiği için yol hatası konum hatasından da küçük olabilir.

---

## 4. Kalman filtreleri (`kalman.py`)

Sürekli durum (konum, hız) ve Gauss gürültüsü. Anahtar özellik: **Doğrusal Gauss** geçiş ve algılayıcı modelleriyle, Gauss bir önsel hep Gauss bir sonsal verir. Filtreleme yalnızca **ortalama ve kovaryansı** güncellemekten ibarettir.

### 4.1 Tek boyutlu örnek

Rastgele yürüyüş: P(x_{t+1} | x_t) = N(x_t, σx²), P(z_t | x_t) = N(x_t, σz²).

- **μ_{t+1} = ((σ_t² + σx²) z_{t+1} + σz² μ_t) / (σ_t² + σx² + σz²)**
- **σ²_{t+1} = (σ_t² + σx²) σz² / (σ_t² + σx² + σz²)**

Kitaptaki şekil: μ₀ = 0, σ₀ = 1.5, σx = 2, σz = 1, z₁ = 2.5. Tahmin N(0, 6.25), güncelleme **N(2.155, 0.862)**.

Yorum:
- Yeni ortalama, **gözlem** ile **önceki ortalamanın** ağırlıklı ortalamasıdır. Gözlem güvenilirse (σz² küçük) ona, önceki kestirim güvenilirse ona yaklaşır.
- **Varyans güncellemesi gözlemden bağımsızdır.** Varyans dizisi önceden hesaplanabilir ve hızla bir sabite yakınsar (burada ≈ 0.828).

### 4.2 Genel durum

Geçiş x_{t+1} = F x_t + gürültü (Σx), algılayıcı z_t = H x_t + gürültü (Σz):
- **K_{t+1} = (F Σ_t Fᵀ + Σx) Hᵀ (H (F Σ_t Fᵀ + Σx) Hᵀ + Σz)⁻¹** (Kalman kazancı)
- **μ_{t+1} = F μ_t + K_{t+1} (z_{t+1} − H F μ_t)**
- **Σ_{t+1} = (I − K_{t+1} H)(F Σ_t Fᵀ + Σx)**

`kalman.py` konum–hız izlemesi yapar: Yalnızca konum ölçüldüğü hâlde hız da kestirilir.

### 4.3 Sınırlar

- **Genişletilmiş Kalman filtresi (EKF):** Doğrusal olmayan sistemleri, o anki kestirim çevresinde **yerel doğrusallaştırarak** ele alır.
- **Kitabın kuş örneği:** Bir kuş hızla ağaç gövdesine doğru uçuyor. Kalman filtresi tek bir Gauss tahmin eder ve ortalaması **gövdenin tam üstünde** olur. Gerçekçi bir model kuşun sağa ya da sola kaçacağını öngörür: iki tepeli bir dağılım. Böyle durumlarda **anahtarlamalı Kalman filtresi** (birden çok Kalman filtresinin ağırlıklı karışımı) ya da parçacık filtresi gerekir.

---

## 5. Dinamik Bayes ağları

**DBN:** Her zaman dilimi, birden çok durum ve kanıt değişkeni içeren bir Bayes ağıdır; dilimler aynı yapıyla tekrarlanır. Her HMM bir DBN'dir (tek değişkenli) ve her ayrık DBN bir HMM'ye çevrilebilir (değişkenler birleştirilerek). Fark **tıkızlıktır**: n değişkenli, her biri d değerli bir sistemin HMM geçiş matrisi O(d^{2n}) boyutludur; ebeveyn sayısı k ile sınırlıysa DBN O(n d^k). Kitaptaki 42 kareli kirli süpürge dünyası: ~5 × 10²⁹ sayı yerine birkaç bin. Her Kalman filtresi, doğrusal Gauss koşullu dağılımlı bir DBN'dir; ama her DBN bir Kalman filtresi değildir (DBN çok tepeli dağılımları, "anahtarım cebimde ya da masada" gibi durumları, temsil edebilir).

### 5.1 Algılayıcı arızalarını modellemek (`pil_sensoru.py`)

Robotun pil ölçeri bazen saçmalar. Kitaptaki üç aşama:

| Model | Kısa aksaklık (…5555 00 5555…) | Kalıcı bozulma (…5555 000000…) |
|---|---|---|
| Yalnızca Gauss hatası | Tek bir 0'da "pil bitti" der | Pilin bittiğine inanır |
| **Geçici arıza modeli** (P(BMeter = 0 \| Battery) ≥ 0.03) | Atlatır | Sonunda pilin bittiğine karar verir (**aşırı karamsar**) |
| **Kalıcı arıza modeli** (BMBroken değişkeni, **süreklilik bağıyla**) | Atlatır; P(bozuk) kısa süre yükselip düşer | P(bozuk) → 1; pil tahminini korur |

Ders: Gerçek sistemlerde algılayıcı arızaları olasılıksal modelin **içine** yazılmalıdır.

### 5.2 DBN'de çıkarım

- **Kesin çıkarım:** DBN'yi gözlem sayısı kadar dilime **açıp** Bölüm 13'ün algoritmalarını uygulamak mümkündür. Değişken elemeyle filtreleme, bellek açısından sabit kalır, ama durum değişkenlerinin sayısında üsteldir: Değişkenler zamanla birbirine bağlanır ve faktörler büyür.
- **Olabilirlik ağırlıklandırma** zaman içinde kötüleşir: Örnekler kanıttan habersiz üretilir ve ağırlıklar hızla küçülür.

### 5.3 Parçacık filtresi (`parcacik_filtresi.py`)

N örnekten (parçacık) oluşan bir nüfus tutulur:
1. Her parçacığı geçiş modeliyle **ileri taşı**.
2. Her parçacığı gözlemin olabilirliğiyle **ağırlıklandır**.
3. Ağırlıklara göre N parçacığı **yeniden örnekle**.

Parçacıkların dağılımı, filtrelenmiş dağılımın tutarlı bir tahminidir. Yeniden örnekleme, nüfusu durum uzayının olası bölgelerinde tutar. Yeniden örnekleme olmayan sürümde (**SIS**, ardışık önem örneklemesi) ağırlıklar birkaç parçacıkta toplanır ve hata zamanla büyür. Kod bunu ölçer: N = 1000 için yeniden örneklemeli hata 0.007, SIS hatası 0.19.

Zayıflık: Gerçek durum, geçiş modeline göre olası olmayan bir yere giderse parçacıklar onu kaçırabilir. Durum uzayı çok boyutluysa gerekli parçacık sayısı üstel artabilir.

---

## Sık yapılan hatalar

| Yanılgı | Doğrusu |
|---|---|
| "Filtreleme ve yumuşatma aynı sonucu verir." | Yumuşatma gelecekteki kanıtı da kullanır: 1. gün 0.818 → 0.883. |
| "Her adımın en olası durumlarını birleştirmek en olası diziyi verir." | En olası dizi için Viterbi gerekir; tek tek en olası durumlar tutarsız bir dizi oluşturabilir. |
| "Uzun vadeli tahmin, son gözlemi yansıtır." | Karışma süresinden sonra tahmin durağan dağılıma yakınsar. |
| "Kalman filtresi her sistemi izleyebilir." | Yalnızca doğrusal Gauss (ya da yerel olarak öyle) sistemler; kuş–ağaç örneği. |
| "Kalman varyansı gözlemlere bağlıdır." | Güncellenen varyans gözlemden bağımsızdır; önceden hesaplanabilir. |
| "DBN, HMM'den daha güçlü bir modeldir." | Aynı dağılımları temsil ederler; DBN daha tıkızdır. |

## Kendini yokla

1. Filtrelemede "tahmin" ve "güncelleme" adımlarını şemsiye örneğiyle anlat.
2. Neden P(R_1 | u_1, u_2) > P(R_1 | u_1)?
3. Viterbi ile ileri algoritma arasındaki tek fark nedir?
4. Kalman güncellemesinde σz → ∞ olursa μ_{t+1} ne olur? σz → 0 olursa?
5. Parçacık filtresinde yeniden örnekleme adımı neden gerekli?

## Kod rehberi

```bash
python ornekler/zamansal.py            # kütüphane: HMM (ileri, geri, ileri–geri, Viterbi, olabilirlik)
python ornekler/semsiye.py             # 0.818, 0.883, b = ⟨0.69, 0.41⟩, Viterbi mesajları
python ornekler/lokalizasyon.py        # labirentte konumlandırma, ε'nin etkisi
python ornekler/kalman.py              # N(2.155, 0.862); konum–hız izleme
python ornekler/pil_sensoru.py         # geçici ve kalıcı arıza modelleri
python ornekler/parcacik_filtresi.py   # parçacık filtresi ve SIS karşılaştırması
```

## Terimler

| Türkçe | İngilizce | Kısa açıklama |
|---|---|---|
| zaman dilimi | time slice | Bir andaki değişkenler kümesi |
| geçiş modeli | transition model | P(X_t \| X_{t−1}) |
| algılayıcı modeli | sensor (observation) model | P(E_t \| X_t) |
| Markov varsayımı / süreci | Markov assumption / process | Şimdiki durum sınırlı geçmişe bağlı |
| durağan süreç | stationary process | Kuralları zamanla değişmeyen süreç |
| filtreleme / durum kestirimi | filtering / state estimation | P(X_t \| e_{1:t}) |
| tahmin | prediction | P(X_{t+k} \| e_{1:t}) |
| yumuşatma | smoothing | P(X_k \| e_{1:t}), k < t |
| en olası açıklama | most likely explanation | En olası durum dizisi |
| ileri–geri algoritması | forward–backward algorithm | Yumuşatma için iki yönlü mesajlar |
| sabit gecikmeli yumuşatma | fixed-lag smoothing | d adım geriden yumuşatma |
| durağan dağılım / karışma süresi | stationary distribution / mixing time | Uzun vadeli dağılım / ona yakınsama süresi |
| Viterbi algoritması | Viterbi algorithm | En olası diziyi dinamik programlamayla bulma |
| gizli Markov modeli | hidden Markov model (HMM) | Tek ayrık durum değişkenli zamansal model |
| konumlandırma | localization | Robotun yerini kestirmek |
| Kalman filtresi / kazancı | Kalman filter / gain | Doğrusal Gauss filtreleme / güncelleme ağırlığı |
| genişletilmiş / anahtarlamalı Kalman filtresi | extended / switching Kalman filter | Doğrusal olmayan / çok kipli sistemler için |
| dinamik Bayes ağı | dynamic Bayesian network (DBN) | Dilimlerden oluşan Bayes ağı |
| geçici / kalıcı arıza modeli | transient / persistent failure model | Algılayıcı arızalarını modelleme |
| süreklilik bağı | persistence arc | Bir değişkenin kendi önceki değerine bağı |
| parçacık filtresi | particle filtering | Örneklerle filtreleme, yeniden örneklemeli |
| ardışık önem örneklemesi | sequential importance sampling (SIS) | Yeniden örneklemesiz ağırlıklı örnekleme |
