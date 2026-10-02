# Bölüm 21 — Alıştırmalar

Sorular özgündür. Çözümler `cozumler/` klasöründe; önce kendin dene.

Zorluk: ★ kolay · ★★ orta · ★★★ zor

---

## A1 — Aktivasyonların türevleri ★

1. σ'(x) = σ(x)(1 − σ(x)) olduğunu göster. σ'(x)'in en büyük değeri nedir, nerede?
2. softplus(x) = log(1 + eˣ)'in türevinin σ(x) olduğunu göster.
3. tanh(x) = 2σ(2x) − 1 eşitliğini doğrula.

## A2 — Şekil 21.3'ü elle hesapla (kod) ★

Ağırlıklar: w0,3 = 0, w1,3 = 1, w2,3 = 1; w0,4 = 0, w1,4 = −1, w2,4 = 1; w0,5 = 0, w3,5 = 1, w4,5 = 1; bütün birimler sigmoid. Girdi x = (1, 1), hedef y = 1.
1. in3, a3, in4, a4, in5, ŷ değerlerini hesapla.
2. L₂ kaybı için ∂L/∂w3,5 ve ∂L/∂w1,3'ü (21.4) ve (21.5) ile hesapla.

## A3 — Softmax (kod) ★★

1. Softmax'ın bütün girdilere aynı sabiti eklemeye karşı değişmez olduğunu göster.
2. Girdiler bir T "sıcaklığına" bölünürse (z/T) T = 0.5 ve T = 5 için ⟨5, 2, 0, −2⟩'nin softmax'ı ne olur? T → 0 ve T → ∞ uçlarını yorumla.

## A4 — Evrişim (kod) ★★

x = ⟨5, 6, 6, 2, 5, 6, 5⟩, çekirdek ⟨+1, −1, +1⟩.
1. Adım 1, dolgu yokken çıktıyı elle hesapla. Adım 2'de neden ⟨5, 9, 4⟩ çıkar?
2. Bir sıfır dolguyla çıktı neden girdiyle aynı boyda olur?
3. Çekirdek 3, adım 1 iken 1., 2., 3., 4. katmanların alıcı alanı kaç pikseldir?

## A5 — Boyut ve parametre hesabı (kod) ★★

1. Çıktı boyutu ⌊(n + 2p − l)/s⌋ + 1 formülüyle: n = 224, l = 7, s = 2, p = 3; n = 32, l = 5, s = 1, p = 0; n = 32, l = 3, s = 1, p = 1.
2. 32 × 32 × 3 görüntüden 32 × 32 × 16'lık katmana tam bağlı ve 3 × 3 evrişimli katmanın ağırlık sayılarını karşılaştır.

## A6 — Sigmoid ve ReLU derinlikte (kod) ★★

Genişliği 64 olan, 2, 10, 20, 50 katmanlı rastgele ağlarda ilk katmana ulaşan gradyanın normunu sigmoid (Xavier başlangıcı) ve ReLU (He başlangıcı) için karşılaştır. Farkı açıkla.

## A7 — İki gizli birimle XOR ★★

Basamak aktivasyonlu (z ≥ 0 ise 1) ve iki gizli birimli bir ağın XOR'u hesapladığı ağırlıkları bul. Gizli birimler neyi hesaplıyor?

## A8 — Dropout'ta beklenen değer (kod) ★★

Ters dropout'ta eğitim sırasında tutulan birimler 1/p ile çarpılır.
1. Bir birimin beklenen çıktısının dropout'suzla aynı olduğunu göster; benzetimle doğrula.
2. 100 gizli birimli bir katmanda dropout kaç farklı "inceltilmiş ağ" tanımlar?

## A9 — Toplu normalleştirme (kod) ★★★

Bir katmanın ağırlıkları 10 ile çarpılırsa, ardından gelen toplu normalleştirmenin çıktısı nasıl değişir? Neden? Bu özellik öğrenmeyi nasıl kolaylaştırır?

## A10 — Otokodlayıcı ve özdeğerler (kod) ★★★

PPCA'dan üretilmiş 10 boyutlu veride (gerçekte 2 gizli boyut) m = 1, 2, 3 için doğrusal otokodlayıcı eğit.
1. Yeniden kurma hatası ile kovaryansın atılan özdeğerlerinin toplamını karşılaştır.
2. m = 3'te neden küçük bir fark kalıyor?
