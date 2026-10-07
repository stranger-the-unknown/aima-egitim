# Bölüm 24 — Doğal dil işleme için derin öğrenme

> **Kitapta:** AIMA 4. baskı, Bölüm 24 *"Deep Learning for Natural Language Processing"*.
> Önce kitabı oku, sonra bu notlarla pekiştir. Metin özgündür; kitaptan alıntı yoktur.
> Kodlar yalnızca numpy kullanır; büyük modeller yerine mekanizmalar gösterilir.

## Bu bölümün haritası

| Kitap alt bölümü | Bu nottaki karşılığı | Kod |
|---|---|---|
| 24.1 Word Embeddings | §1 One-hot'tan yoğun vektörlere, benzetmeler | `gomme.py` |
| 24.2 Recurrent Neural Networks for NLP | §2 RNN dil modelleri, sınıflandırma, LSTM | (Bölüm 21 `rnn.py`) |
| 24.3 Sequence-to-Sequence Models | §3 Dizi-dizi, dikkat, kod çözme | `dikkat.py`, `kod_cozme.py` |
| 24.4 The Transformer Architecture | §4 Öz-dikkat, çok başlı dikkat, konum gömmesi | `dikkat.py` |
| 24.5 Pretraining and Transfer Learning | §5 Önceden eğitilmiş gömmeler, bağlamsal temsiller, maskeli dil modelleri | `gomme.py`, `cozumler/alistirma_kod.py` (A9) |
| 24.6 State of the art | §6 Günümüz modelleri ve sınırları | — |

## Öğrenme hedefleri

1. One-hot gösterimin sorununu ve sözcük gömmelerinin nasıl öğrenildiğini açıklamak.
2. Gömmelerle benzerlik ve benzetme (analoji) hesaplamak.
3. RNN tabanlı dizi-dizi modellerinin sınırlarını ve dikkatin bunları nasıl giderdiğini açıklamak.
4. Öz-dikkati (Q, K, V, √d ölçekleme), çok başlı dikkati, konum gömmesini ve maskeyi hesaplamak.
5. Açgözlü ve ışın araması ile kod çözmeyi karşılaştırmak.
6. Önceden eğitme ve aktarım öğrenmesini (gömmeler, bağlamsal temsiller, maskeli dil modelleri) açıklamak.

---

## 1. Sözcük gömmeleri (`gomme.py`)

**One-hot** vektörler sözcükler arasında hiçbir benzerlik taşımaz: Her sözcük çifti eşit uzaklıktadır (kosinüs 0). Firth'in ilkesi: Bir sözcüğü birlikte bulunduğu sözcüklerden tanırsın. Ham n-gram sayımları çok büyük (100 000 sözcükte 10²⁵ farklı 5-gram); bunun yerine **sözcük gömmesi**: düşük boyutlu (ör. 100–300) yoğun vektör. Boyutların tek tek anlamı yoktur; ama benzer sözcükler yakın düşer (kitaptaki Şekil 24.1'de ülke, akrabalık, ulaşım kümeleri).

- **Öğrenme:** Gömmeler, sözcüğü bağlamından tahmin etme görevinde (ya da birlikte geçme sayımlarından) öğrenilir. Kodumuz küçük bir Türkçe derlemde birlikte geçme sayımlarını PPMI ile ağırlıklandırıp SVD ile 4 boyuta indirir: "kedi"nin en yakın komşusu "köpek" (0.98), "araba"nınki "otobüs".
- **Benzetmeler:** Vektör farkları ilişkileri yakalar: Atina − Yunanistan ≈ Oslo − Norveç. "Atina Yunanistan'a neyse Oslo neye?" sorusu Yunanistan − Atina + Oslo'ya en yakın sözcükle yanıtlanır (Norveç). Kodumuz bunu başkent ilişkisinin ortak bir yön olduğu yapay gömmelerle gösterir. Gömmeler bu tür soruları her zaman doğru yanıtlamaz ve eğitim verisindeki önyargıları da öğrenebilir.
- **Hazır gömmeler:** word2vec, GloVe, FastText (157 dilde). Kullanmak çok zaman kazandırır.

Gömmelerle bir görev çözmek: POS etiketlemede her sözcüğün gömmesi (ve komşularınınki) bir ileri beslemeli ağa girer; one-hot'a göre çok daha iyi genelleştirir (görülmemiş ama benzer sözcükler).

---

## 2. NLP için yinelemeli ağlar

**RNN dil modeli:** Her adımda gizli durum zₜ önceki durumu ve yeni sözcüğün gömmesini alır; çıktı softmax ile sonraki sözcüğün dağılımı. n-gramlardan farklı olarak bağlam penceresi sabit değildir. Eğitim zamanda geri yayılımla (Bölüm 21).

- **Sınıflandırma:** Bütün dizinin özetiyle (son gizli durum ya da ortalama) duygu analizi gibi görevler. **Çift yönlü RNN:** Hem soldan hem sağdan bağlam (etiketleme görevlerinde yararlı).
- **LSTM:** Uzak bağımlılıklar için bellek hücresi ve kapılar (Bölüm 21): "The athletes who…" ile başlayan uzun bir cümlede fiilin çoğul olacağını hatırlamak gibi.

---

## 3. Dizi-dizi modelleri (`dikkat.py`, `kod_cozme.py`)

**Makine çevirisi:** Kaynak dizi → hedef dizi; uzunluklar ve sözcük eşleşmeleri bire bir değil ("caballo de mar" → "seahorse"). Temel model: Kaynağı bir RNN ile kodla, hedefi başka bir RNN ile üret. Üç kusuru:
1. **Yakın bağlam yanlılığı:** RNN geçmişi gizli duruma sıkıştırmak zorundadır; yakındaki sözcükler baskın olur.
2. **Sabit bağlam boyutu sınırı:** Bütün kaynak cümle tek bir sabit uzunluklu vektöre sığmalıdır.
3. **Yavaş, sıralı işleme:** Her adım bir öncekini bekler; paralelleştirmek zordur.

### 3.1 Dikkat

Hedef her adımda kaynağın **bütün** durumlarına bakar:

```text
rᵢⱼ = hᵢ₋₁ · sⱼ          (hedef durumu ile kaynak durumu arasındaki ham puan)
aᵢⱼ = softmax_j(rᵢⱼ)     (dikkat olasılıkları)
cᵢ = Σⱼ aᵢⱼ sⱼ           (bağlam vektörü)
```

Softmax'ın üç yararı: türevlenebilir (eğitilebilir), olasılıkların görselleştirilebilmesi (hangi kaynak sözcüğe bakıldığı), birden çok sözcüğe yumuşakça dağıtılabilmesi. Dikkat, sözcük hizalamasını (çeviride hangi sözcüğün hangisine karşılık geldiğini) etiketsiz veriden öğrenir.

### 3.2 Kod çözme

- **Açgözlü kod çözme:** Her adımda en olası sözcüğü seç. Hızlı ama bütün cümle için en iyiyi bulmayabilir.
- **Işın araması:** En iyi b hipotezi tut; her birini genişlet, b² aday arasından en iyi b'yi seç. Hipotezin puanı log-olasılıkların toplamı. Kitaptaki Şekil 24.8'de "La entrada" ile başlayan hipotez yalnızca düşük olasılıklı devamlar üretebildiği için ışından düşer. Günümüz sinirsel çeviri modelleri 4–8, eski istatistiksel modeller 100 ve üzeri ışın kullanır. Kodumuzda açgözlü kod çözücü "La entrada es" (log P −2.63) verir, b = 2 ile ışın araması "La puerta de entrada es roja" (log P −1.16) bulur.

---

## 4. Transformer mimarisi (`dikkat.py`)

### 4.1 Öz-dikkat

Bir dizi kendi kendine dikkat eder; her konum diğer bütün konumlara bakar. Doğrudan iç çarpım (xᵢ · xⱼ) her sözcüğün en çok kendine bakmasına yol açar; bu yüzden üç farklı izdüşüm:

```text
qᵢ = W_q xᵢ (sorgu)    kᵢ = W_k xᵢ (anahtar)    vᵢ = W_v xᵢ (değer)
rᵢⱼ = (qᵢ · kⱼ) / √d    aᵢⱼ = softmax_j(rᵢⱼ)    cᵢ = Σⱼ aᵢⱼ vⱼ
```

Kitap üç ayrıntıyı vurgular: (1) Öz-dikkat **asimetriktir**, rᵢⱼ ≠ rⱼᵢ. (2) √d çarpanı **sayısal kararlılık** için eklenmiştir. Bizim açıklamamız: Rastgele q ve k'nin iç çarpımının standart sapması √d'dir; büyük d'de softmax doyar, bölünce ~1 olur (kodumuzda d = 512 için 22.7 → 1.0). (3) Bütün sözcüklerin kodlaması matris işlemleriyle **aynı anda (paralel)** hesaplanır: RNN'nin sıralılık sorunu kalkar.

**Çok başlı dikkat:** cᵢ bütün cümle üzerinden bir ortalama olduğu için önemli bilgi "ortalamada kaybolabilir". Kitap çözümü şöyle anlatır: m parçaya bölüp her parçaya kendi ağırlıklarıyla dikkat uygulamak ve sonuçları **toplamak yerine birleştirmek** (önemli bir parça öne çıkabilsin diye). Uygulamada (Vaswani vd., 2017) bölünen şey vektör boyutlarıdır: Her başın kendi (W_q, W_k, W_v) kümesi vardır; kodumuzda iki baş d/2 boyutlu çıktı üretir, birleştirilip doğrusal bir katmandan geçirilir.

### 4.2 Öz-dikkatten transformer'a

Transformer katmanı (Şekil 24.9): önce öz-dikkat, sonra her konuma ayrı ayrı aynı ağırlıklarla uygulanan ileri beslemeli katmanlar (ilkinden sonra genellikle ReLU) ve kaybolan gradyana karşı iki artık bağlantı. Uygulamada genellikle altı ya da daha çok katman yığılır; i. katmanın çıktısı i + 1. katmanın girdisidir.

- **Konum gömmesi:** Öz-dikkat sıraya duyarsızdır: Girdinin yerini değiştirmek çıktıların yerini aynı biçimde değiştirir (kodumuz doğrular). Kitaptaki çözüm: En çok n uzunluklu girdi için n yeni gömme vektörü **öğrenilir** (her konuma bir tane); ilk katmanın girdisi sözcük gömmesi + konum gömmesidir. Kodumuz öğrenme yapmadığı için özgün transformer makalesindeki sabit sin/cos kodlamasını kullanır (bizim seçimimiz); bu kodlamada iki konum vektörünün iç çarpımı yalnızca aralarındaki uzaklığa bağlıdır (A6).
- **Kodlayıcı–kod çözücü:** Kod çözücüde öz-dikkat **maskelenir** (i. konum yalnızca ≤ i konumlara bakar) ve kodlayıcı çıktısına dikkat eden bir katman eklenir.
- Transformer'lar POS etiketleme, çeviri, dil modelleme gibi görevlerde RNN'lerin yerini almıştır.

---

## 5. Önceden eğitme ve aktarım öğrenmesi

Etiketli veri pahalı, etiketsiz metin bol (kitaba göre web'e her gün 100 milyardan fazla sözcük ekleniyor). Önce büyük etiketsiz metinde genel bir dil modeli eğit, sonra küçük etiketli veriyle **ince ayar** yap.

- **Önceden eğitilmiş gömmeler:** GloVe, sözcüklerin birlikte geçme olasılıklarının oranlarından gömme öğrenir; milyarlarca sözcükle birkaç saatte eğitilebilir. Alana özgü gömmeler: Kitaptaki örnekte 3.3 milyon malzeme bilimi özetinden öğrenilen gömmeler, henüz keşfedilmemiş malzeme özelliklerini öngörebildi.
- **Bağlamsal temsiller:** Aynı sözcüğün farklı anlamları ("rose" çiçek / yükseldi) tek bir statik vektörle temsil edilemez. Bütün cümleye bakan (çift yönlü) bir RNN ya da transformer, sözcüğün bağlama göre değişen temsilini üretir.
- **Maskeli dil modeli (MLM):** Girdideki bazı sözcükleri gizle ("The river [masked] five feet"), modelden onları tahmin etmesini iste. Etiket verisi gerekmez: Cümle kendi etiketini sağlar; aynı cümle farklı sözcükleri gizleyerek defalarca kullanılabilir. Çift yönlü bağlam tahmini çok kolaylaştırır (A9: "kedi [MASK] içti"de sağdaki "içti" seçenekleri daraltır). BERT ve RoBERTa bu tür modellerdir.

---

## 6. Günümüz durumu

- **ARISTO**, 8. sınıf çoktan seçmeli fen sınavında %91.6 başarı gösterdi; en etkili bileşeni RoBERTa'dır (tek başına %88.2).
- **GPT-2** (1.5 milyar parametreli, transformer benzeri dil modeli) birkaç sözcüklük bir başlangıçtan oldukça ikna edici metin üretebilir.
- Büyük önceden eğitilmiş modeller ince ayarla birçok görevde en iyi sonuçları verir; ama metni gerçekten "anlayıp anlamadıkları", tutarlılık, olgusal doğruluk ve önyargı açık sorulardır.

---

## Sık yapılan hatalar

| Yanılgı | Doğrusu |
|---|---|
| "One-hot vektörler benzer sözcükleri yakın tutar." | Her çift eşit uzaklıktadır; benzerlik için gömme gerekir. |
| "Gömmenin her boyutu bir anlam taşır." | Boyutlar tek tek yorumlanamaz; anlam göreli konumlardadır. |
| "Sabit bir vektör bütün cümleyi taşıyabilir." | Dizi-dizi modellerinin darboğazı budur; dikkat bütün kaynak durumlarına bakar. |
| "Öz-dikkat sözcük sırasını bilir." | Sıraya duyarsızdır; konum gömmesi eklenmelidir. |
| "Açgözlü kod çözme en olası cümleyi bulur." | Yalnızca her adımda en iyi sözcüğü bulur; ışın araması daha iyi cümleler bulabilir. |
| "√d ile bölmek yalnızca bir süs." | Kitaba göre sayısal kararlılık için eklenir: Büyük boyutta softmax'ın doymasını önler. |
| "Maskeli dil modeli etiketli veri ister." | Cümle kendi etiketini sağlar; etiketsiz metin yeter. |

## Kendini yokla

1. One-hot gösterim neden sözcük benzerliğini yakalayamaz?
2. Gömmelerle "Atina Yunanistan'a neyse Oslo neye?" sorusu nasıl yanıtlanır?
3. RNN tabanlı dizi-dizi modellerinin üç kusuru nedir?
4. Dikkatte rᵢⱼ, aᵢⱼ ve cᵢ nasıl hesaplanır?
5. Öz-dikkatte sorgu, anahtar ve değer neden ayrı izdüşümlerdir? √d neden?
6. Öz-dikkat neden konum gömmesine ihtiyaç duyar?
7. Kod çözücüde maske ne işe yarar?
8. Açgözlü kod çözme ile ışın araması arasındaki fark nedir?
9. Bağlamsal temsil statik gömmeden neden daha iyidir?
10. Maskeli dil modeli nasıl eğitilir?

## Kod rehberi

```bash
python ornekler/gomme.py         # one-hot vs gömme, PPMI + SVD, kosinüs benzerliği, benzetmeler
python ornekler/dikkat.py        # dizi-dizi dikkati, öz-dikkat, maske, çok başlı dikkat, sin/cos konum kodlaması, √d
python ornekler/kod_cozme.py     # açgözlü kod çözme ve ışın araması
python cozumler/alistirma_kod.py # A3, A5, A6, A8, A9
```

## Terimler

| Türkçe | İngilizce | Kısa açıklama |
|---|---|---|
| sözcük gömmesi | word embedding | Sözcüğün yoğun, düşük boyutlu vektörü |
| one-hot vektör | one-hot vector | Tek biti 1 olan vektör |
| kosinüs benzerliği | cosine similarity | Vektörler arası açı ölçüsü |
| noktasal karşılıklı bilgi | pointwise mutual information (PMI) | log P(w, c)/(P(w)P(c)) |
| benzetme | analogy | b − a + c ≈ ? |
| GloVe / word2vec / FastText | GloVe / word2vec / FastText | Hazır gömme modelleri |
| yinelemeli dil modeli | recurrent language model | RNN ile sonraki sözcük tahmini |
| çift yönlü RNN | bidirectional RNN | İki yönden bağlam |
| dizi-dizi modeli | sequence-to-sequence model | Kodlayıcı–kod çözücü |
| makine çevirisi | machine translation | Diller arası çeviri |
| yakın bağlam yanlılığı | nearby context bias | RNN'nin yakını kayırması |
| dikkat | attention | Kaynak durumlarına ağırlıklı bakış |
| bağlam vektörü | context vector | Σ aᵢⱼ sⱼ |
| açgözlü kod çözme | greedy decoding | Her adımda en olası sözcük |
| ışın araması | beam search | En iyi b hipotezi tutma |
| transformer | transformer | Öz-dikkat tabanlı mimari |
| öz-dikkat | self-attention | Dizinin kendine dikkati |
| sorgu / anahtar / değer | query / key / value | q, k, v izdüşümleri |
| çok başlı dikkat | multiheaded attention | Paralel dikkat kümeleri |
| konum gömmesi | positional embedding | Her konuma eklenen (öğrenilen ya da sin/cos) vektör |
| maskeli öz-dikkat | masked self-attention | Geleceğe bakmayı engelleme |
| önceden eğitme | pretraining | Büyük etiketsiz veride eğitim |
| ince ayar | fine-tuning | Küçük etiketli veriyle uyarlama |
| bağlamsal temsil | contextual representation | Bağlama göre değişen sözcük vektörü |
| maskeli dil modeli | masked language model (MLM) | Gizlenen sözcükleri tahmin |
