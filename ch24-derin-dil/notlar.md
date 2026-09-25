# Bölüm 24 — Derin öğrenme ile doğal dil: Özgün Notlar

> Bu notlar kitabın metninin kopyası değildir. Anlatım özgün Türkçe öğretim dilindedir.
> Amaç: gömü, dizi modeli ve dikkat dilini kurmak; ağır framework şart değil.

---

## 1. Kelime gömüleri (embeddings) — sezgi

One-hot: her sözcük kendi boyutunda 1; “kedi” ile “köpek” kosinüsü 0.
**Gömü:** her sözcük için küçük yoğun vektör (ör. 2–300 boyut). Benzer anlamda / benzer bağlamda kullanılan sözcükler uzayda yakın olur.

Klasik sezgi (dağılımsal hipotez): *anlam ≈ kullanım komşuluğu*.
Word2Vec (skip-gram / CBOW), GloVe sayım–bağlamdan öğrenir; modern sistemlerde bağlama duyarlı gömü (transformer) hâkim.

`embedding_benzerlik.py` elle seçilmiş 2B vektörlerle Türkçe sözcük kosinüs demosu verir (eğitim yok; sezgi).

---

## 2. Dizi modelleri: RNN ve LSTM (yüksek seviye)

Metin sıradır. Basit tekrarlayan ağ (RNN):

```text
h_t = f(W_h h_{t-1} + W_x x_t + b)
```

Her adımda gizli durum `h_t` “şimdiye kadarki özet”i taşır.  
Sorun: uzun bağımlılıklarda gradyan kaybolur / patlar; pratikte kısa bellek.

**LSTM / GRU:** kapılar (unut, yaz, oku) ile belleği seçici tutar. Detay formüller bu pakette yok; sezgi yeter: *kapılı bellek → daha uzun bağlam*.

Bugün birçok görevde LSTM yerine transformer tercih edilir; RNN fikri hâlâ “sıra + durum” öğretisi için değerlidir.

---

## 3. Dikkat (attention) — iskelet

Bağlam vektörü: sorgu **Q**, anahtar **K**, değer **V**.

```text
skorlar = Q Kᵀ / √d     (isteğe bağlı ölçek)
α = softmax(skorlar)    (satır satır, toplam 1)
çıktı = α V
```

“Hangi anahtarlara ne kadar bakayım?” → ağırlıklı ortalama.
Self-attention: aynı dizinin her konumu diğerlerine bakar.

`dikkat_skoru.py` 2–3 konumluk minik Q,K ile softmaks skorlarını basar.

---

## 4. Transformer — kabataslak

Bir katman (encoder tarzı iskelet):

1. Multi-head self-attention
2. Artık bağlantı + katman norm (yüksek seviye: “eski + yeni”)
3. Konum-bağımsız feed-forward (MLP)
4. Yine artık + norm

Konum bilgisi ayrı kodlanır (sinüzoidal / öğrenilen).  
Decoder’da maskeli dikkat (geleceğe bakmama) + çapraz dikkat eklenir — çeviri / üretim için.

Bu bölümde katman kodlamıyoruz; fikir: **paralel dikkat + MLP yığını = modern dil omurgası**.

---

## 5. Aktarım öğrenmesi (transfer learning)

Büyük derlemde (veya çok görevde) önceden eğit → hedef göreve az etiketle uyarla (fine-tune) veya dondurulmuş gömü / özellik kullan.

Kazanç: az veri, daha iyi genelleme, yeniden sıfırdan eğitmemek.
Risk: alan kayması (domain shift), hesap maliyeti, önyargı aktarımı.

Eğitim demosunda ağır model yok; kavram: *genel dil bilgisi → özel görev*.

---

## 6. Ajan bakışı

1. Önce gömü + benzerlik sezgisi (Ch23 BoW’dan sıçrama).
2. RNN’i “bellekli sıra” olarak tut; LSTM’i “kapı” diye etiketle.
3. Dikkat skorunu elle sayı ile gör.
4. Transformer’ı blok diyagramı olarak çiz; sonra kütüphane.

Özet: **gömü = yoğun anlam; RNN = sırayla durum; dikkat = soft seçim; transformer = dikkat + MLP; aktarım = önce genel, sonra özel.** Kitabı yasal nüshadan oku.
