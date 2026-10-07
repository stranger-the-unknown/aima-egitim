# Bölüm 24 — Quiz

Cevaplara bakmadan önce kendin yanıtla. Cevaplar dosyanın sonunda.

---

**S1.** İki farklı sözcüğün one-hot vektörleri arasındaki kosinüs benzerliği nedir?

A) 1
B) −1
C) 0
D) Sözcüklerin anlamına bağlıdır

**S2.** "Atina Yunanistan'a neyse Oslo neye?" sorusu sözcük gömmeleriyle nasıl yanıtlanır?

**S3.** Bir RNN dil modelinin parametre sayısı cümle uzunluğu n ile nasıl değişir?

A) O(1)
B) O(n)
C) O(n²)
D) O(vⁿ)

**S4.** RNN tabanlı temel dizi-dizi modelinin kitapta sayılan üç kusuru nedir?

**S5.** Dikkat mekanizmasında bağlam vektörü cᵢ nedir?

A) Son kaynak durumu
B) Kaynak durumlarının dikkat olasılıklarıyla ağırlıklı toplamı
C) Hedef durumlarının ortalaması
D) En yüksek puanlı kaynak durumu

**S6.** Açgözlü kod çözme ile ışın araması arasındaki fark nedir? Işın genişliği 1 olursa ne olur?

**S7.** Öz-dikkatte puan neden doğrudan xᵢ · xⱼ ile değil, sorgu ve anahtar izdüşümleriyle hesaplanır?

**S8.** Hangisi öz-dikkat için **yanlıştır**?

A) rᵢⱼ ile rⱼᵢ farklı olabilir
B) √d çarpanı sayısal kararlılık için eklenir
C) Cümlenin bütün konumları paralel hesaplanabilir
D) Sözcüklerin sırasını kendiliğinden bilir

**S9.** Kitaptaki transformer sözcük sırası bilgisini nasıl ekler?

**S10.** Transformer kod çözücüsü kodlayıcıdan hangi iki bakımdan farklıdır?

**S11.** Maskeli dil modeli eğitimi için hangisi doğrudur?

A) Her cümle elle etiketlenmelidir
B) Yalnızca soldaki bağlam kullanılabilir
C) Yalnızca sözcük gömmelerini öğrenir, bağlamı öğrenmez
D) Gizlenen sözcük metnin kendisinden gelir; etiketsiz metin yeter

**S12.** "rose" sözcüğü için statik bir sözcük gömmesi ile bağlamsal bir temsil arasındaki fark nedir?

---

## Cevaplar

**S1.** **C.** One-hot vektörler diktir; her sözcük çifti eşit uzaklıktadır, benzerlik bilgisi taşımaz.

**S2.** Yunanistan − Atina + Oslo vektörünü hesapla; soruda geçen sözcükler dışında bu vektöre (kosinüs ile) en yakın sözcüğü bul: Norveç.

**S3.** **A.** Ağırlıklar her zaman adımında paylaşılır. İleri beslemeli pencereli ağ O(n), n-gram modeli O(vⁿ).

**S4.** (1) Yakın bağlam yanlılığı: geçmiş gizli duruma sıkıştırılır, yakın sözcükler baskın olur. (2) Sabit bağlam boyutu: bütün kaynak cümle tek sabit uzunluklu vektöre sığmalıdır. (3) Yavaş, sıralı işleme: adımlar paralelleştirilemez.

**S5.** **B.** cᵢ = Σⱼ aᵢⱼ sⱼ; aᵢⱼ = softmax(hᵢ₋₁ · sⱼ).

**S6.** Açgözlü her adımda en olası tek sözcüğü seçer; ışın araması en iyi b hipotezi birlikte genişletir ve kısa vadede ikinci görünen ama sonunda daha olası çıkan cümleleri bulabilir. b = 1 açgözlü kod çözmedir.

**S7.** Bir vektörün kendisiyle iç çarpımı hep büyüktür; her sözcük en çok kendine bakardı. Ayrı W_q, W_k, W_v izdüşümleri hem bu sorunu giderir hem de asimetrik ilişkileri öğrenmeyi sağlar.

**S8.** **D.** Öz-dikkat sıraya duyarsızdır; girdinin yerini değiştirmek çıktıların yerini aynı biçimde değiştirir.

**S9.** Konum gömmesi: En çok n uzunluklu girdi için n vektör öğrenilir; ilk katmanın girdisi sözcük gömmesi + o konumun gömmesidir. (Özgün makaledeki sin/cos kodlaması bir alternatiftir.)

**S10.** (1) Öz-dikkati maskelenir: Her sözcük yalnızca kendinden önceki sözcüklere bakabilir (metin soldan sağa üretilir). (2) Her katmanda kodlayıcının çıktısına dikkat eden ikinci bir dikkat modülü vardır.

**S11.** **D.** Cümle kendi etiketini sağlar; çift yönlü bağlam kullanılır.

**S12.** Statik gömme "rose" için tek bir vektör verir; çiçek anlamı ile "yükseldi" anlamı karışır. Bağlamsal temsil (çift yönlü RNN ya da transformer) sözcüğün vektörünü cümlenin geri kalanına göre üretir; iki anlam farklı vektörler alır.
