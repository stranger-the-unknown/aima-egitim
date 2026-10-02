# Bölüm 21 — Quiz

Cevaplara bakmadan önce kendin yanıtla. Cevaplar dosyanın sonunda.

---

**S1.** Bir ağdaki bütün aktivasyon fonksiyonları doğrusal olsaydı ne olurdu?

**S2.** Aşağıdakilerden hangisinin türevi sigmoid fonksiyonudur?

A) ReLU
B) tanh
C) Softplus
D) Softmax

**S3.** Evrensel yaklaşım teoremi ne söyler? Neden yine de derin ağlar kullanılır?

**S4.** Softmax girdisi ⟨5, 2, 0, −2⟩ ise en büyük çıktı yaklaşık kaçtır?

A) 0.50
B) 0.71
C) 0.95
D) 1.00

**S5.** Çapraz entropi kaybını en küçüklemek hangi ilkeye denktir?

**S6.** x = ⟨5, 6, 6, 2, 5, 6, 5⟩, çekirdek ⟨+1, −1, +1⟩, adım 2 için evrişim çıktısı nedir?

A) ⟨5, 2, 9, 3, 4⟩
B) ⟨5, 9, 4⟩
C) ⟨6, 2, 6⟩
D) ⟨1, 9, 1⟩

**S7.** Alıcı alan nedir ve derinlikle nasıl değişir?

**S8.** Kaybolan gradyan problemine çare **olmayan** hangisidir?

A) Artık bağlantılar
B) ReLU aktivasyonu
C) Daha çok sigmoid katmanı eklemek
D) Toplu normalleştirme

**S9.** Dropout'un üç yorumunu söyle.

**S10.** Temel bir RNN uzun vadeli bağımlılıkları neden zor öğrenir? LSTM'in unutma kapısı bunu nasıl çözer?

**S11.** Doğrusal bir otokodlayıcının öğrendiği alt uzay nedir?

A) Rastgele bir alt uzay
B) Kovaryansın en büyük özdeğerlerinin özvektörlerinin gerdiği alt uzay
C) Kovaryansın en küçük özdeğerlerinin özvektörlerinin gerdiği alt uzay
D) Girdi uzayının tamamı

**S12.** Aktarım öğrenmesi nedir? Bir görüntü sınıflandırıcıyı az veriyle yeni bir göreve nasıl uyarlarsın?

---

## Cevaplar

**S1.** Doğrusal fonksiyonların bileşimi doğrusaldır: Ağ ne kadar derin olursa olsun tek bir doğrusal fonksiyon temsil ederdi (XOR'u bile öğrenemezdi).

**S2.** **C.** d/dx log(1 + eˣ) = σ(x).

**S3.** Bir doğrusal olmayan ve bir doğrusal katmandan oluşan ağ her sürekli fonksiyona istenen doğrulukta yaklaşabilir. Ama gereken birim sayısı üstel olabilir; derin ağlar aynı fonksiyonları çok daha az parametreyle temsil eder ve pratikte daha iyi genelleştirir.

**S4.** **C.** ⟨0.946, 0.047, 0.006, 0.001⟩.

**S5.** En büyük olabilirliğe (negatif log olabilirliği en küçüklemeye); P sabitken KL ıraksamasını en küçüklemeye.

**S6.** **B.** A adım 1'deki çıktıdır.

**S7.** Bir birimin değerini etkileyebilen girdi bölgesi. İlk katmanda çekirdek boyu kadar; her katmanda (adım 1'de) l − 1 piksel büyür; adım ve havuzlamayla çok daha hızlı büyür.

**S8.** **C.** Her sigmoid katmanı gradyanı en az 4 kat küçültür; daha çok sigmoid sorunu ağırlaştırır.

**S9.** (1) Ağırlık paylaşan çok sayıda inceltilmiş ağın topluluğu (torbalamaya benzer); (2) birimlerin birbirine aşırı uyumunu engeller, her birim tek başına yararlı olmalı; (3) gürültü ve hasara dayanıklı, çoklu açıklamalar öğrenmeye zorlar.

**S10.** BPTT'de gradyan her adımda W_zz ve g' ile çarpılır; özdeğerler 1'den küçükse geçmişe doğru üstel küçülür. LSTM'de bellek hücresi cₜ = fₜ cₜ₋₁ + iₜ c̃ₜ; f ≈ 1 iken bilgi ve gradyan çarpanı Π f ≈ 1 kalır.

**S11.** **B.** PCA'nın alt uzayı; yeniden kurma hatası atılan özdeğerlerin toplamıdır.

**S12.** Bir görevde öğrenilen temsilleri başka bir göreve aktarmak. Önceden (ör. ImageNet'te) eğitilmiş ağın erken katmanlarını dondur, son katmanları yeni sınıflar için değiştir ve az sayıdaki yeni veriyle ince ayar yap.
