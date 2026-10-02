# A1–A10 çözümleri

Kodlu kısımlar: `python cozumler/alistirma_kod.py` (bölüm klasöründen).

---

## A1 — Aktivasyonların türevleri

1. σ(x) = (1 + e⁻ˣ)⁻¹ ⇒ σ'(x) = e⁻ˣ/(1 + e⁻ˣ)² = σ(x) · e⁻ˣ/(1 + e⁻ˣ) = σ(x)(1 − σ(x)). En büyük değer x = 0'da: 0.5 · 0.5 = **1/4**. Bu yüzden her sigmoid katmanı geri yayılan gradyanı en az 4 kat küçültür.
2. d/dx log(1 + eˣ) = eˣ/(1 + eˣ) = 1/(1 + e⁻ˣ) = σ(x).
3. 2σ(2x) − 1 = 2/(1 + e⁻²ˣ) − 1 = (1 − e⁻²ˣ)/(1 + e⁻²ˣ) = (eˣ − e⁻ˣ)/(eˣ + e⁻ˣ) = tanh(x).

## A2 — Şekil 21.3'ü elle hesapla

1. in3 = 0 + 1 + 1 = **2**, a3 = σ(2) = **0.8808**; in4 = 0 − 1 + 1 = **0**, a4 = **0.5**; in5 = 0.8808 + 0.5 = **1.3808**, ŷ = σ(1.3808) = **0.7991**.
2. g5'(in5) = 0.7991 · 0.2009 = 0.1605.
   - ∂L/∂w3,5 = −2(1 − 0.7991) · 0.1605 · 0.8808 ≈ **−0.0568**
   - ∂L/∂w1,3 = −2(1 − 0.7991) · 0.1605 · w3,5 · g3'(2) · x1 = −0.0645 · 1 · (0.8808 · 0.1192) · 1 ≈ **−0.0068**

   Gizli katmandaki ağırlığın gradyanı, araya bir sigmoid türevi (0.105) daha girdiği için çok daha küçük.

## A3 — Softmax

1. e^{zₖ + c} / Σ e^{zₖ' + c} = eᶜ e^{zₖ} / (eᶜ Σ e^{zₖ'}) = softmax(z)ₖ. (Sayısal kararlılık için uygulamalarda max(z) çıkarılır.)
2. - T = 1: ⟨0.946, 0.047, 0.006, 0.001⟩
   - T = 0.5: ⟨0.9975, 0.0025, 0, 0⟩, daha keskin
   - T = 5: ⟨0.462, 0.254, 0.170, 0.114⟩, daha düz

   T → 0: en büyük girdiye 1, diğerlerine 0 (argmax). T → ∞: düzgün dağılım. Sıcaklık, belirsizlik/keşif düzeyini ayarlamak için kullanılır.

## A4 — Evrişim

1. Adım 1, dolgu yok: ⟨5−6+6, 6−6+2, 6−2+5, 2−5+6, 5−6+5⟩ = **⟨5, 2, 9, 3, 4⟩**. Adım 2 bunların 1., 3. ve 5.'sini alır: ⟨5, 9, 4⟩. En büyük yanıt (9) koyu pikselin (2) üzerinde.
2. Her uca bir sıfır eklenince 9 değer, çekirdek 3 → 9 − 3 + 1 = 7 çıktı: ⟨1, 5, 2, 9, 3, 4, 1⟩.
3. **3, 5, 7, 9** piksel: Her katman alanı l − 1 = 2 piksel büyütür.

## A5 — Boyut ve parametre hesabı

1. (224 + 6 − 7)/2 + 1 = **112** (aşağı yuvarlanır); (32 − 5)/1 + 1 = **28**; (32 + 2 − 3)/1 + 1 = **32** ("aynı" dolgu).
2. Tam bağlı: (32·32·3) · (32·32·16) = **50 331 648** ağırlık. Evrişim: 3·3·3·16 + 16 sabit = **448**. Yaklaşık 10⁵ kat az; üstelik aynı özellik görüntünün her yerinde aranır.

## A6 — Sigmoid ve ReLU derinlikte

| katman | sigmoid | ReLU |
|---|---|---|
| 2 | 5.1e−1 | 1.2e+1 |
| 10 | 3.5e−6 | 9.0e+0 |
| 20 | 1.3e−12 | 1.9e+1 |
| 50 | 2.7e−31 | 1.7e+1 |

Sigmoid'in türevi ≤ 1/4 olduğundan her katman gradyanı küçültür. ReLU'nun türevi etkin birimlerde 1'dir; He başlangıcı (varyans 2/n) etkin birimlerin yarı yarıya olmasını telafi eder, gradyan normu derinlikte yaklaşık korunur.

## A7 — İki gizli birimle XOR

h1 = [x1 + x2 − 0.5 ≥ 0] (**VEYA**), h2 = [x1 + x2 − 1.5 ≥ 0] (**VE**), y = [h1 − h2 − 0.5 ≥ 0]. XOR = VEYA ama VE değil:

| x1 x2 | h1 | h2 | y |
|---|---|---|---|
| 0 0 | 0 | 0 | 0 |
| 0 1 | 1 | 0 | 1 |
| 1 0 | 1 | 0 | 1 |
| 1 1 | 1 | 1 | 0 |

Gizli katman girdiyi, çıktının doğrusal ayırabileceği yeni bir temsile çevirir.

## A8 — Dropout'ta beklenen değer

1. Birim p olasılıkla h/p, 1 − p olasılıkla 0 verir: E = p · h/p = h. Benzetimde ⟨0.300, 1.204, 1.996⟩ ≈ ⟨0.3, 1.2, 2.0⟩. Böylece test zamanında hiçbir ölçekleme gerekmez.
2. Her birim açık ya da kapalı: 2¹⁰⁰ ≈ **1.27 × 10³⁰** alt ağ; hepsi ağırlıkları paylaşır.

## A9 — Toplu normalleştirme

Çıktı **değişmez** (kod: en büyük fark ~10⁻⁶). z = XW yerine 10XW gelirse ortalama ve standart sapma da 10 kat büyür; (z − μ)/σ aynı kalır (ε'dan kaynaklanan çok küçük fark hariç). Ağırlıkların ölçeği katmanın çıktısını etkilemediği için büyük ya da küçük ağırlıklar sonraki katmanları doyuma itmez; daha büyük öğrenme hızları kullanılabilir ve eğitim daha kararlı olur.

## A10 — Otokodlayıcı ve özdeğerler

| m | yeniden kurma hatası | atılan özdeğerlerin toplamı |
|---|---|---|
| 1 | 7.055 | 7.055 |
| 2 | 0.718 | 0.718 |
| 3 | 0.631 | 0.615 |

1. m bileşenli en iyi doğrusal sıkıştırmanın hatası, atılan özdeğerlerin toplamıdır (PCA'nın en iyilik özelliği); otokodlayıcı bu en iyiye ulaşır. m = 2'de hata gürültü düzeyine iner: Veri gerçekten 2 boyutlu.
2. Üçüncü ve sonraki özdeğerler neredeyse eşit (~0.09–0.10): Hangi gürültü yönünün seçileceği belirsizdir ve gradyan inişi bu yönde çok yavaş ilerler. Daha çok adımla fark kapanır; ama gürültüyü modellemenin bir yararı da yoktur.
