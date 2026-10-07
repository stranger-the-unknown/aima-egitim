# A1–A10 çözümleri

Kodlu kısımlar: `python cozumler/alistirma_kod.py` (bölüm klasöründen).

---

## A1 — One-hot'tan gömmeye

1. **100 000** boyutlu; tek biti 1. İki farklı sözcüğün one-hot vektörleri diktir: kosinüs benzerliği **0**. "kedi"–"köpek" ile "kedi"–"otobüs" aynı uzaklıkta; model bir sözcük için öğrendiğini benzer sözcüğe aktaramaz.
2. 100 000 × 300 = **30 milyon** sayı.
3. 100 000⁵ = **10²⁵** farklı 5-gram (kitaptaki sayı); vektörler çok seyrek olurdu.

## A2 — Benzetmeyi elle çöz

1. Yunanistan − Atina + Oslo = (1, 1) − (1, 3) + (4, 3) = **(4, 1) = Norveç**. "Başkentten ülkeye" yönü (0, −2)'dir; her başkentte aynıdır.
2. Atina − Yunanistan + İtalya = (1, 3) − (1, 1) + (7, 1) = **(7, 3) = Roma**.
3. İlişki vektörü küçük olduğunda b − a + c çoğunlukla c'nin kendisine (ya da a, b'ye) çok yakın düşer; aday listesinden çıkarılmazlarsa cevap sıklıkla "Oslo" olur. `benzetme()` fonksiyonu bu yüzden üç sözcüğü dışarıda bırakır. Gerçek gömmelerde ilişkiler bu kadar düzgün değildir; benzetme her zaman doğru çıkmaz.

## A3 — Pencere boyutu

| Pencere | "kedi"nin en yakın üç komşusu |
|---|---|
| 1 | köpek, içti, fare |
| 2 | köpek, süt, içti |
| 4 | köpek, kovaladı, içti |

"köpek" her pencerede ilk sırada: İkisi de aynı bağlamlarda (süt içti, mama yedi, evde uyudu) geçiyor. Pencere büyüdükçe cümledeki uzak sözcükler de bağlama girer ("kovaladı"). Genel eğilim (bizim gözlemimiz değil, literatürdeki bulgu): Küçük pencere aynı yerde kullanılabilen, **işlevce** benzer sözcükleri; büyük pencere aynı **konuda** geçen sözcükleri yakın getirir. Derlemimiz çok küçük olduğundan bu farklar gürültülüdür; eğilimi göstermek için büyük bir derlem gerekir.

## A4 — RNN dil modelinin parametreleri

1. Gömme tablosu 10 000 × 100 = 1 000 000; W_x,z 100 × 200 = 20 000; W_z,z 200 × 200 = 40 000; W_z,y 200 × 10 000 = 2 000 000. Toplam **3 060 000**. Parametrelerin çoğu sözlükle ilgili iki matristedir.
2. **Değişmez.** Aynı ağırlıklar her adımda kullanılır (kitaptaki O(1)).
3. 10 000³ = **10¹²** olasılık. Karşılaştırma: n-gram modeli her olası bağlam için ayrı sayım tutar (O(vⁿ)); n sözcüklük pencereli ileri beslemeli ağ her konum için ayrı ağırlık tutar (O(n)) ve bir sözcük hakkında öğrendiğini her konumda yeniden öğrenmek zorundadır; RNN ağırlıkları zaman adımları arasında paylaştığı için parametre sayısı cümle uzunluğundan bağımsızdır.

## A5 — Dikkati elle hesapla

1. r = (2, 0, 2). a = (e², 1, e²) / (2e² + 1) = **(0.468, 0.063, 0.468)**. c = 0.468 · (1, 0) + 0.063 · (0, 1) + 0.468 · (1, 1) = **(0.937, 0.532)**.
2. Bütün puanlar 0 → olasılıklar eşit (1/3); c = (2/3, 2/3), yani kaynak durumlarının düz ortalaması.
3. r = (20, 0, 20) → a ≈ (0.5, 10⁻⁹, 0.5): Softmax neredeyse "katı" bir seçime dönüşür; ikinci duruma bakılmaz ve gradyanlar çok küçülür. Öz-dikkatte d boyutlu rastgele vektörlerin iç çarpımları d büyüdükçe büyür; √d'ye bölmek puanları makul bir aralıkta tutar (kitap: sayısal kararlılık).

## A6 — Konum kodlaması

| Konumlar | İç çarpım |
|---|---|
| 10 · 10 | 16.000 |
| 10 · 11 | 15.314 |
| 10 · 12 | 13.730 |
| 10 · 15 | 11.777 |
| 10 · 30 | 10.471 |
| 30 · 35 | **11.777** |

1. Yalnızca **uzaklığa** bağlıdır: 10·15 ile 30·35 aynı. Her frekans ω için vektörde (sin ωt, cos ωt) çifti vardır; iki konumun katkısı sin ωt sin ωt' + cos ωt cos ωt' = cos(ω(t − t')). d = 32'de 16 çift vardır, bu yüzden aynı konumda iç çarpım 16'dır. Uzaklık arttıkça değer (kesin tekdüze olmasa da) genel olarak azalır.
2. Öğrenilen konum gömmeleri yalnızca eğitimde görülen en çok n konum için vardır; daha uzun bir girdinin fazladan konumları için vektör yoktur. Ayrıca her konum vektörü ayrı ayrı öğrenilir; seyrek görülen (uzak) konumlar için az veri olur. Sin/cos kodlaması herhangi bir uzunluk için hesaplanabilir ve öğrenilecek parametre içermez.

## A7 — Öz-dikkatin yapısı

1. W_q = W_k = W olsaydı rᵢⱼ = (W xᵢ) · (W xⱼ) / √d = rⱼᵢ, yani simetrik olurdu. Ama ilişkiler simetrik değildir: Fiil öznesine bakmalıdır, özne fiile aynı ölçüde bakmak zorunda değildir. Ayrı W_q ve W_k bu asimetriyi öğrenebilir; ayrıca doğrudan xᵢ · xᵢ'nin her zaman büyük olması sorununu (her sözcüğün kendine bakması) giderir.
2. n² puan. 512² = 262 144, 1024² = 1 048 576: **4 kat**. Hesap ve bellek uzunluğun karesiyle büyür.
3. RNN'de **n** sıralı adım (her gizli durum bir öncekini bekler). Öz-dikkatte bir katmanın bütün konumları tek matris çarpımıyla **aynı anda** hesaplanır; sıralı adım sayısı katman sayısına bağlıdır, n'ye değil.

## A8 — Işın genişliği

1. Açgözlü: La (0.9), entrada (0.5 > 0.45), es (0.4), `</s>` (0.4). P = 0.9 · 0.5 · 0.4 · 0.4 = 0.072 → **log P = −2.631**.
2. La puerta de entrada es roja `</s>`: 0.9 · 0.45 · 0.9 · 0.95 · 0.95 · 0.95 · 1 = 0.3125 → **log P = −1.163**. Açgözlünün bulduğundan 4 kattan fazla olası.
3. b = 2 (olasılıklar):

| Adım | Işın |
|---|---|
| 1 | La (0.9), El (0.1) |
| 2 | La entrada (0.45), La puerta (0.405) |
| 3 | La puerta de (0.365), La entrada es (0.18) |
| 4 | La puerta de entrada (0.346), La entrada es `</s>` (0.072, bitti) |
| 5–7 | La puerta de entrada es → … roja → `</s>` (0.3125, bitti) |

"La entrada" 3. adımda geçici olarak ikinci sırada kalır, 4. adımda yalnızca bitmiş "La entrada es `</s>`" olarak yaşar; devamları ("roja", "rojo") 0.054 ile "La puerta de entrada"nın çok gerisindedir. Kodumuzda bitmiş hipotezler de ışında yer kaplar (uygulama seçimimiz).

4. b = 1: "La entrada es `</s>`" (−2.631), açgözlüyle aynı. b = 2 ve b = 3: "La puerta de entrada es roja `</s>`" (−1.163). Bu modelde b = 2 yeterli; kitaba göre günümüz sinirsel çeviri modelleri 4–8, eski istatistiksel modeller 100 ve üzeri ışın kullanır.

## A9 — Maskeli dil modeli

1. Derlemde "kedi"den sonra beş farklı sözcük birer kez geliyor: **süt, fare, kovaladı, mama, evde**. Soldan sağa bir model bunlar arasında ayrım yapamaz.
2. "kedi _ içti" kalıbına yalnızca **süt** uyar. Sağdaki bağlam seçenekleri daraltır; maskeli dil modelleri (BERT, RoBERTa) bu yüzden çift yönlü bağlam kullanır.
3. Gizlenen sözcük metnin kendisinde zaten vardır: Cümle kendi etiketini sağlar. Aynı cümle farklı sözcükler gizlenerek defalarca kullanılabilir; bu sayede çok büyük etiketsiz metinlerle eğitim yapılabilir.

## A10 — Aktarım öğrenmesi tasarla

1. (a) Sıfırdan RNN 2 000 örnekle hem dili hem görevi öğrenmek zorunda; aşırı uyum riski yüksek, görülmemiş sözcüklerde zayıf. (b) Hazır gömmeler (FastText'in Türkçe dahil 157 dilde gömmeleri var) sözcük benzerliğini getirir; az veriyle makul sonuç. Ama statik gömmeler bağlamı bilmez. (c) Önceden eğitilmiş transformer bağlamsal temsiller üretir; küçük bir öğrenme oranıyla ince ayar genellikle en iyi sonucu verir; hesap maliyeti en yüksektir.
2. Olumsuzlama ("hiç de … değil") ve "kötü"nün anlamını tersine çeviren bağlam ancak cümlenin bütününe bakan bağlamsal bir modelde yakalanır; sözcük torbası ya da ortalama gömme "kötü"yü görüp olumsuz der. Transformer (c) en başarılısı olur; (a) bu kalıbı 2 000 örnekten öğrenebilecek kadar görmeyebilir.
3. Bir kök onlarca biçimde görülür (ev, evde, evlerimizden…); her biçimi ayrı sözcük sayan bir sözlük çok büyür ve çoğu biçim nadiren görülür. Alt sözcük birimleri (FastText'in karakter n-gramları ya da transformer'ların alt sözcük sözlükleri) bu sorunu hafifletir.
4. (i) **Alan uyumsuzluğu:** Genel metinle eğitilmiş model ürün yorumu diline (argo, yazım hataları) uymayabilir. (ii) **Önyargı:** Eğitim metnindeki önyargılar sınıflandırıcıya taşınabilir (ör. belli marka ya da gruplarla ilgili yorumlarda sistematik hata). Değerlendirme: Etiketli verinin bir kısmını hiç dokunmadan test kümesi olarak ayır, farklı ürün türlerinde ve olumsuzlama gibi zor örneklerde hata oranlarını ayrı ayrı ölç.
