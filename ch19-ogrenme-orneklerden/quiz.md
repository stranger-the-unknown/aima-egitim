# Bölüm 19 — Quiz

Cevaplara bakmadan önce kendin yanıtla. Cevaplar dosyanın sonunda.

---

**S1.** Yarın sıcaklığın kaç derece olacağını tahmin etmek hangi tür öğrenme problemidir?

A) Sınıflandırma
B) Kümeleme
C) Regresyon
D) Pekiştirmeli öğrenme

**S2.** Restoran verisinde neden Patrons köke gider? Kazanç(Patrons) ve Kazanç(Type) yaklaşık kaçtır?

**S3.** LEARN-DECISION-TREE'de bir dalda hiç örnek kalmazsa ne döndürülür?

A) Rastgele bir sınıf
B) Ebeveyn düğümdeki örneklerin çoğunluk sınıfı
C) Her zaman "No"
D) Algoritma başarısız olur

**S4.** Erken durdurma neden XOR gibi fonksiyonlarda sorun çıkarır?

**S5.** Hiperparametreleri seçmek için hangi küme kullanılmalıdır?

A) Eğitim kümesi
B) Test kümesi
C) Doğrulama kümesi (ya da çapraz doğrulama)
D) Fark etmez

**S6.** PAC sınırı N ≥ (1/ε)(ln(1/δ) + ln|H|) neden bütün Boolean fonksiyonları için umutsuzdur?

**S7.** Toplu gradyan inişi ile stokastik gradyan inişi arasındaki fark nedir?

**S8.** Hangisi seyrek (çok ağırlığı tam sıfır olan) modeller üretmeye yatkındır?

A) L₂ düzenlileştirme
B) L₁ düzenlileştirme
C) Düzenlileştirmesiz en küçük kareler
D) Lojistik regresyon

**S9.** Algılayıcı öğrenme kuralı hangi durumda yakınsar?

**S10.** k = 10 ve N = 10⁶ için 200 boyutta komşuluğun kenarı birim küpün kenarının yaklaşık ne kadarıdır?

A) %0.3
B) %2
C) %50
D) %94

**S11.** Çekirdek hilesi neyi mümkün kılar?

**S12.** Bağımsız 5 sınıflandırıcı her biri %75 doğruysa çoğunluk oyu yaklaşık yüzde kaç doğrudur? Gerçekte neden daha azdır?

---

## Cevaplar

**S1.** **C.** Çıktı bir sayı: regresyon.

**S2.** Patrons iki değerde (None, Some) örnekleri tamamen saf ayırır; Type ise her değerde yarı yarıya bırakır. Kazanç(Patrons) ≈ 0.541 bit, Kazanç(Type) = 0.

**S3.** **B.** O nitelik değeri birleşimi hiç görülmemiştir; en iyi tahmin, bir üst düğümdeki örneklerin çoğunluğudur.

**S4.** XOR'da tek başına hiçbir nitelik bilgi kazancı sağlamaz (her dal yarı yarıya). Erken durdurma burada durur; ama iki niteliği birlikte test eden ağaç fonksiyonu tam öğrenir. Önce kurup sonra budamak bu durumu yakalar.

**S5.** **C.** Test kümesi yalnızca en sonda, bir kez kullanılmalıdır; yoksa test hatası iyimser olur.

**S6.** |H| = 2^(2ⁿ) olduğundan ln|H| ∝ 2ⁿ: Gereken örnek sayısı olası girdi sayısı kadar büyür. Hipotez uzayı her örnek kümesini her biçimde sınıflandırabildiği için görülmemiş örnekler hakkında bir şey söylemez.

**S7.** Toplu: Her adımda bütün örneklerin gradyanı (bir adım = bir tur). Stokastik: Her adımda bir örnek ya da mini toplu; adımlar ucuz ama gürültülü, yakınsaması azalan öğrenme hızı ister.

**S8.** **B.** L₁'in elmas biçimli kısıt bölgesi eksenlerde köşelidir; en iyi nokta sık sık bir eksene, yani bazı ağırlıkların sıfır olduğu yere düşer.

**S9.** Veri doğrusal ayrılabilirse (sabit öğrenme hızıyla bile) sonlu adımda bir ayırıcı bulur. Ayrılabilir değilse salınır.

**S10.** **D.** ℓ = (10/10⁶)^(1/200) ≈ 0.94: "Yerel" komşuluk neredeyse bütün küptür.

**S11.** Veriyi yüksek (hatta sonsuz) boyutlu bir özellik uzayına gömüp orada doğrusal ayırıcı bulmayı, özellikleri hiç hesaplamadan: Yalnızca iç çarpımlar gerekir ve onlar bir çekirdek fonksiyonuyla (ör. (x · z)²) girdi uzayında hesaplanır.

**S12.** Yaklaşık **%89** (en az 3'ünün doğru olma olasılığı). Gerçekte sınıflandırıcılar aynı veriyi ve varsayımları paylaşır; hataları ilişkilidir, bu yüzden kazanç daha küçüktür.
