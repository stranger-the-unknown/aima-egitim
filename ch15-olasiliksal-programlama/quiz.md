# Bölüm 15 — Quiz

Cevaplara bakmadan önce kendin yanıtla. Cevaplar dosyanın sonunda.

---

**S1.** Bayes ağları neden "önermesel" sayılır? Bu hangi sorunlara yol açar?

**S2.** RPM ile OUPM arasındaki fark nedir?

A) RPM'de nesne sayısı belirsizdir, OUPM'de bilinir
B) RPM kapalı evren (veritabanı anlamı) varsayar; OUPM'de nesne sayısı ve kimlikleri belirsiz olabilir
C) İkisi aynı şeydir
D) OUPM yalnızca sürekli değişkenlerle çalışır

**S3.** C müşteri ve B kitaplı kitap önerisi modeli temellendirilince kaç düğüm oluşur?

A) C + B
B) C · B
C) 2C + B + BC
D) 2^C · 5^B

**S4.** Kitaptaki beceri modelinde Win(i, j, g) nasıl tanımlanır?

**S5.** Recommendation(c, b) için "if Honest(c) then … else ⟨0.4, 0.1, 0.0, 0.1, 0.4⟩" yazmak hangi kavrama örnektir?

A) Bağlama özgü bağımsızlık
B) Gürültülü-VEYA
C) Markov örtüsü
D) Veri ilişkilendirme

**S6.** Köken fonksiyonu (örneğin Owner) ne işe yarar?

**S7.** Bir sistemde en fazla 3 müşteri olabiliyor ve 4 giriş kimliği görüldü. Ne sonuç çıkar?

**S8.** Poisson(λ) dağılımının standart sapması nedir?

A) λ
B) λ²
C) 1/λ
D) √λ

**S9.** Veri ilişkilendirme problemini tanımla. Gerçek sistemlerde onu zorlaştıran iki etken nedir?

**S10.** En yakın komşu filtresinin zayıflığı nedir?

A) Çok yavaştır
B) Tek bir eşleşmeye bağlanır; yakın hedeflerde ve kargaşada hata yapar ve hatasını fark etmez
C) Yalnızca tek hedefli izlemede çalışır
D) Olasılık kullanır

**S11.** Üretimsel bir programın "yürütme izi" nedir? Olasılığı nasıl hesaplanır?

**S12.** Kitaptaki metin okuma örneğinde ikili harf modeli neden bağımsız harf modelinden daha iyi sonuç verebilir? Her zaman daha iyi midir?

---

## Cevaplar

1. Değişkenleri sabit ve adlandırılmış önermeler gibidir; nesneler, ilişkiler ve niceleyiciler yoktur. Çok sayıda benzer nesnesi olan alanlarda her nesne için ayrı düğüm ve CPT yazmak gerekir; nesne sayısı ya da kimliği belirsizse hiç temsil edilemez.
2. **B.**
3. **C.** Her müşteri için Honest ve Kindness (2C), her kitap için Quality (B), her çift için Recommendation (BC).
4. Win(i, j, g) = Performance(i, g) > Performance(j, g); performanslar Skill etrafında Gauss dağılır.
5. **A.** Dürüst olmayanlarda öneri, nezaket ve kaliteden bağımsızdır.
6. Nesnenin nereden geldiğini (hangi nesnenin onu ürettiğini) kaydeder. Örneğin her giriş kimliği onu açan müşteriyi bilir. Böylece her olası dünya tek bir biçimde kurulabilir ve "bu kimlikler aynı kişiye mi ait?" sorusu sorulabilir.
7. En az bir müşteri birden çok kimlik açmıştır (sahtekârdır): P(en az bir sahtekâr) = 1. Kimlik sayısı kişi sayısıyla aynı değildir.
8. **D.** Ortalama λ, varyans λ.
9. Gözlemleri (radar işaretleri, kamera görüntüleri) onları üreten nesnelere eşlemek. Zorlaştıranlar: yanlış alarmlar (kargaşa), algılama hataları, nesnelerin sahneye girip çıkması, yakın nesneler. Hipotez sayısı üstel büyür.
10. **B.**
11. Programın bir çalıştırmasında yaptığı bütün rastgele seçimlerin değerleri. Olasılığı, her seçimin (önceki seçimler verildiğinde) olasılıklarının çarpımıdır: P(ω) = Π P(xᵢ | x₁, …, xᵢ₋₁). Bir olası dünyaya karşılık gelir.
12. Harf dizileri hakkında önsel bilgi taşır: Görüntü belirsizse gerçek kelimelerde sık görülen harf geçişlerini tercih eder. Her zaman değil: Okumayı sık dizilere doğru çekip yeni hatalar da yaratabilir; ortalamada, özellikle yüksek gürültüde, yardım eder.
