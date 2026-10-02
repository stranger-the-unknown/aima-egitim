# Bölüm 17 — Quiz

Cevaplara bakmadan önce kendin yanıtla. Cevaplar dosyanın sonunda.

---

**S1.** Stokastik bir ortamda bir MDP'nin çözümü neden bir eylem dizisi değil de politikadır?

**S2.** 4 × 3 dünyada (4. baskı, γ = 1, r = −0.04) bir uç duruma girişin ödülü ne zaman sayılır?

A) Her adımda uç durumda kalırken tekrar tekrar
B) Uç duruma giren geçişte bir kez; uç durumun faydası 0
C) Hem girişte hem de uç durumun faydası olarak
D) Hiç sayılmaz; yalnızca −0.04 ödülleri sayılır

**S3.** Sonlu ufuklu bir problemde en iyi politika neden durağan olmayabilir?

**S4.** γ = 0.9 indirim çarpanı hangi faiz oranına denktir?

A) %9
B) %10
C) %11.1
D) %90

**S5.** Bellman denklemini yaz ve neden doğrusal olmadığını söyle.

**S6.** Değer yinelemesinin yakınsamasını garanti eden özellik nedir?

A) Bellman güncellemesinin γ çarpanlı bir büzülme olması
B) Durum sayısının sonlu olması
C) Ödüllerin negatif olması
D) Politikanın uygun olması

**S7.** Politika yinelemesinde politika değerlendirme adımı neden değer yinelemesinden daha kolaydır?

**S8.** Hangi ödül dönüşümü en iyi politikayı **değiştirebilir**?

A) R′ = 3R + 2
B) R′ = R + γΦ(s′) − Φ(s), uçlarda Φ = 0
C) Hedefe yaklaşan her geçişe +bonus, uzaklaşanlara ceza yok
D) R′ = R / 10

**S9.** Gittins indeksi nedir ve neden kullanışlıdır?

**S10.** Bernoulli haydudunda (3, 2) durumunun Gittins indeksi, tahmini daha yüksek olan (7, 4) durumununkinden neden büyüktür?

A) Hesap hatası
B) Az denenmiş kolun keşif bonusu daha büyüktür
C) (3, 2) daha çok başarı içerir
D) γ = 0.9 olduğu için

**S11.** POMDP'de en iyi eylem neye bağlıdır?

A) Gerçek fiziksel duruma
B) En olası duruma
C) Son algıya
D) İnanç durumuna (durumlar üzerindeki dağılıma)

**S12.** POMDP'de U(b) neden parçalı doğrusal ve dışbükeydir? İki durumlu dünyada derinlik 8 için kaç baskın olmayan plan kalır?

---

## Cevaplar

**S1.** Eylemler beklenen sonucu her zaman vermez; ajan planlamadığı durumlara düşebilir. Politika her olası durum için bir eylem verdiği için sonuç ne olursa olsun ajan ne yapacağını bilir. (4 × 3 dünyada en iyi dizi bile yalnızca 0.32776 olasılıkla başarılı.)

**S2.** **B.** 4. baskıda ödül R(s, a, s′) geçişe aittir. Uç durum emicidir ve faydası 0'dır. C, bu deponun eski kodundaki çift sayım hatasıdır.

**S3.** En iyi eylem kalan zamana bağlıdır: (3,1)'de az zaman kalınca riskli kısa yol (Yukarı), zaman bolken güvenli uzun yol (Sol) en iyidir.

**S4.** **C.** (1/γ) − 1 = 1/0.9 − 1 ≈ 0.111.

**S5.** U(s) = max_a Σ_s′ P(s′ | s, a)[R(s, a, s′) + γ U(s′)]. max işlemi doğrusal değildir; bu yüzden n denklem doğrusal cebirle doğrudan çözülemez, yinelemeli çözülür.

**S6.** **A.** ‖BU − BU′‖ ≤ γ‖U − U′‖: Tek bir sabit nokta vardır ve hata her adımda en az γ katına iner.

**S7.** Politika sabit olduğu için max kalkar; denklemler doğrusaldır ve O(n³)'te tam çözülür (ya da birkaç basit güncellemeyle yaklaşık çözülür).

**S8.** **C.** Potansiyele dayanmayan bir bonus döngüleri ödüllendirebilir ve ajan hedefe hiç varmayabilir. A ve D pozitif afin dönüşümler, B şekillendirme teoremidir.

**S9.** Bir kolun, sabit λ veren bir kola karşı kayıtsız kalınan λ değeri: birim indirimli zamandaki en büyük fayda. Yalnızca kolun kendisine bağlıdır; "en yüksek indeksli kolu çek" politikası en iyidir ve her karar O(1)'de güncellenir.

**S10.** **B.** (3, 2) daha az denenmiştir; değeri hakkında öğrenilecek daha çok şey vardır. Gittins indeksi tahmine ek olarak bu bilginin değerini içerir.

**S11.** **D.** Ajan gerçek durumu bilmez; en iyi politika π*(b) inanç durumunun fonksiyonudur. B yaygın bir yanılgıdır: Bilgi toplamanın değerini görmez.

**S12.** Sabit bir koşullu planın beklenen faydası b · α_p, b'de doğrusaldır. En iyi politika her b'de en iyi planı seçer: U(b) = max_p b · α_p, doğruların maksimumu, yani parçalı doğrusal ve dışbükey. Derinlik 8'de **144** baskın olmayan plan kalır (budamasız 2²⁵⁵).
