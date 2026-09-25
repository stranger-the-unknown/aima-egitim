# Bölüm 11 — Quiz

Cevaplara bakmadan önce kendin yanıtla. Cevaplar dosyanın sonunda.

---

**S1.** PDDL'de bir eylemin sonucu nasıl hesaplanır?

A) SONUÇ(s, a) = s ∪ EKLE(a)
B) SONUÇ(s, a) = (s ∪ EKLE(a)) − SİL(a)
C) SONUÇ(s, a) = (s − SİL(a)) ∪ EKLE(a)
D) SONUÇ(s, a) = EKLE(a)

**S2.** Bir eylemin etkisinde adı geçmeyen bir atom, eylemden sonra ne olur?

**S3.** Geri (regression) aramada bir eylemin **ilgili** olması için hangisi gerekir?

A) Önkoşullarının başlangıçta doğru olması
B) Hedefin bir atomunu eklemesi ve hiçbir hedef atomunu silmemesi
C) En az bir atom silmesi
D) Hedefin tüm atomlarını eklemesi

**S4.** Kitaptaki hava kargo örneğinde (10 havalimanı, her birinde 5 uçak, 20 kargo) ileri aramanın neden zor olduğunu bir cümleyle açıkla.

**S5.** Hedef alt hedeflere ayrıştırılıp her biri için en iyi plan bulunuyor. Hangi birleştirme her zaman **kabul edilebilir** bir sezgisel verir?

A) Alt plan maliyetlerinin toplamı
B) Alt plan maliyetlerinin toplamının iki katı
C) Alt planlar ortak eylem içerdiğinde maliyetlerin toplamı
D) Alt plan maliyetlerinin en büyüğü

**S6.** Sussman anomalisi neyi gösterir?

**S7.** "Önkoşulları yok say" sezgiselinin kesin değeri neden kolay hesaplanamaz? Pratikte ne yapılır, bunun bedeli nedir?

**S8.** Hiyerarşik planlamada **meleksi anlamda** kötümser betimleme hedefle kesişiyorsa ne söyleyebiliriz?

A) Plan kesinlikle işe yaramaz
B) Plan kesinlikle işe yarar (bir inceltme seçimiyle hedefe ulaşılır)
C) Plan ilkel eylemlere inceltilmeden değerlendirilemez
D) Plan yalnızca deterministik olmayan ortamlarda işe yarar

**S9.** Masa ve sandalyeyi, renklerini bilmediğimiz iki kutu boyadan biriyle aynı renge boyamak için algısız bir plan yaz.

**S10.** Kritik yol yönteminde bir eylemin bolluğu (slack) nasıl hesaplanır? Bolluğu 0 olan eylemler hakkında ne söylenir?

**S11.** Kitaptaki iki arabalık montajda kaynak kısıtları eklenince en kısa çizelge kaç dakika olur?

A) 115
B) 85
C) 100
D) 130

**S12.** PlanSAT ve Sınırlı PlanSAT (en fazla k adımlık plan var mı?) önermeselleştirilmiş klasik planlamada hangi karmaşıklık sınıfındadır?

---

## Cevaplar

1. **C.** Önce silme listesi çıkarılır, sonra ekleme listesi eklenir. (B yanlıştır: Bir eylem aynı atomu hem siliyor hem ekliyorsa sonuçta atom doğru olmalıdır.)
2. Olduğu gibi kalır. PDDL, etkide adı geçmeyen her şeyin değişmediğini varsayar. Bu, çerçeve problemini kendiliğinden çözer.
3. **B.** Ayrıca tutarlı olmalıdır: Hiçbir hedef atomunu bozmamalıdır.
4. Durum başına yaklaşık 2000 eylem uygulanabilir. Çözüm derinliği de büyük olduğu için ağaç astronomik boyuta ulaşır. İyi bir sezgisel olmadan ileri arama umutsuzdur.
5. **D.** Bütün hedefi sağlayan plan, her alt hedefi de sağlar; bu yüzden en az en pahalı alt plan kadar uzundur. Toplam ise ancak alt hedefler bağımsızsa kabul edilebilirdir. Alt planlar ortak eylem içeriyorsa toplam o eylemleri iki kez sayar ve fazla tahmin eder.
6. Alt hedeflerin birbirinden bağımsız olmadığını: On(A, B) ve On(B, C) hangi sırayla tek tek çözülürse çözülsün, biri diğerini bozar. Doğru plan, iki alt hedefin adımlarını birbirine serpiştirir.
7. Hedef atomlarını sağlayan en az eylem sayısını bulmak bir küme örtme problemidir ve NP-zordur. Pratikte açgözlü algoritma kullanılır: Sonuç en iyinin log n katı içinde kalır, ama sezgisel kabul edilebilirliğini kaybeder.
8. **B.** Kötümser betimleme, kesinlikle ulaşılabilir durumların alt yaklaşımıdır. Hedefle kesişiyorsa plan kesinlikle işe yarar.
9. `RemoveLid(Can1), Paint(Chair, Can1), Paint(Table, Can1)`. Hangi renk olduğunu bilmesek de ikisi aynı kutudan boyandığı için aynı renkte olurlar.
10. Bolluk = LS − ES (en geç başlama − en erken başlama). Bolluğu 0 olan eylemler kritik yoldadır. Birini geciktirmek tüm planı geciktirir.
11. **A.** Kaynaksız hâlde 85 dk, tek vinç ve tek teker istasyonuyla 115 dk.
12. Kitaba göre önermeselleştirilmiş problemler için hem PlanSAT hem Sınırlı PlanSAT **PSPACE** sınıfındadır. Bu, NP'den geniş (ve daha zor olabilecek) bir sınıftır. Pratikteki problemler ise çoğu zaman bu kadar kötü değildir.
