# Bölüm 6 — Quiz

Cevaplar dosyanın sonunda.

---

**S1.** Bir CSP'nin üç bileşeni nedir? "Çözüm" nasıl tanımlanır?

**S2.** Avustralya haritası 3 renkle kaç farklı şekilde boyanabilir? Neden?

**S3.** Yay tutarlılığını tanımla. Yay tutarlı bir CSP'nin çözümü olmak zorunda mı?

**S4.** AC-3'ün en kötü durum karmaşıklığı nedir?

**S5.** MRV, derece ve LCV sezgisellerini birer cümleyle tanımla.

**S6.** WA = kırmızı, Q = yeşil, V = mavi atamalarından sonra ileri kontrol neyi fark eder?

**S7.** MAC, ileri kontrolden neden daha güçlüdür? Kitaptaki örnekte hangi anda fark ortaya çıkar?

**S8.** Min-çatışma bir milyon vezirde ortalama kaç adımda çözüme ulaşır? Neden bu kadar hızlıdır?

**S9.** Ağaç yapılı bir CSP hangi karmaşıklıkta çözülür? Nasıl?

**S10.** Döngü kesme kümesi nedir? Avustralya için bir örnek ver.

**S11.** Türkiye'nin 7 coğrafi bölgesi kaç renkle boyanabilir?

**S12.** Değer simetrisi nedir? Nasıl kırılır?

---

## Cevaplar

1. Değişkenler, alanlar, kısıtlar. Çözüm: tam (her değişken atanmış) ve tutarlı (hiçbir kısıt ihlal edilmemiş) atama.
2. **18.** SA, WA, NT, Q, NSW ve V'nin renklendirilmesi 3! = 6 yolla yapılabilir (SA'nın rengi seçilince çevresindeki halka iki renkle dönüşümlü boyanır). Tazmanya bağımsızdır ve 3 seçeneği vardır: 6 × 3 = 18.
3. Her Xᵢ değerinin, her (Xᵢ, Xⱼ) kısıtı için Xⱼ'de bir destekçisi olması. Hayır, olmak zorunda değil: İki renkli üçgen yay tutarlıdır ama çözümü yoktur.
4. **O(c·d³)**, c: ikili kısıt sayısı, d: en büyük alan.
5. MRV: yasal değeri en az olan değişken önce. Derece: atanmamış komşusu en çok olan değişken önce. LCV: komşuların alanlarından en az değer silen değer önce.
6. SA'nın alanının **boşaldığını**. Bu yüzden hemen geri döner.
7. MAC, silme işlemlerini zincirleme yayar (AC-3). İleri kontrol yalnızca atanan değişkenin komşularına bakar. Q = yeşil atandığında NT ve SA'nın ikisinde de yalnız mavi kalır ve ikisi komşudur. MAC bunu o anda yakalar, ileri kontrol yakalayamaz.
8. **~50 adım.** Açgözlü bir başlangıçtan sonra yalnızca birkaç çatışma kalır ve çözümler durum uzayında yoğun dağılmıştır. Adım sayısı n'den neredeyse bağımsızdır.
9. **O(n·d²).** Topolojik sırada sondan başa yönlü yay tutarlılığı sağlanır, sonra baştan sona her değişkene ebeveyniyle uyumlu bir değer verilir; geri dönüş gerekmez.
10. Çıkarılınca kısıt grafını ağaca çeviren değişken kümesi. Avustralya'da **{SA}**.
11. **4.** 3 renk yetmez: İç Anadolu–Akdeniz–Doğu Anadolu üçgeninden başlayan zincirleme bir kısıt Ege'de çelişkiye yol açar.
12. Değer isimlerini permüte etmek, bir çözümden başka bir çözüm üretir (d renk için d! kat). Simetri kırıcı bir kısıtla (ör. NT < SA < WA) her simetri sınıfından yalnızca bir temsilci bırakılır.
