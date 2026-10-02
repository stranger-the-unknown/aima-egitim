# Bölüm 4 — Quiz

Cevaplar dosyanın sonunda.

---

**S1.** Yerel arama hangi tür problemlerde tercih edilir? Temel avantajı nedir?

**S2.** 8-vezirde en dik tırmanış yüzde kaç başarılıdır? 100 yana hamle izniyle bu oran kaça çıkar?

**S3.** Başarı olasılığı p olan bir yerel arama için yeniden başlatmalı sürümün beklenen deneme sayısı nedir?

**S4.** Benzetilmiş tavlamada kötüleşen bir adımın kabul olasılığı nedir? T azaldıkça ne olur?

**S5.** k ışınlı yerel arama, k bağımsız yeniden başlatmadan nasıl ayrılır?

**S6.** Genetik algoritmada çaprazlama hangi durumda gerçekten faydalıdır?

**S7.** Havalimanı probleminde gradyan neden yalnızca "yerel olarak" doğrudur?

**S8.** AND-OR arama ağacında VEYA ve VE düğümleri kimin seçimini temsil eder?

**S9.** Algısız süpürge dünyasında [Sağ, Süpür, Sol, Süpür] planı hangi inanç dizisini üretir?

**S10.** Kısmi gözlemde inanç güncellemenin iki adımı nelerdir?

**S11.** Çevrimiçi aramada "güvenle keşfedilebilir" ortam ne demektir? Neden önemlidir?

**S12.** LRTA*'ta denenmemiş bir eylemin maliyeti nasıl tahmin edilir, neden?

---

## Cevaplar

1. Yolun değil **son durumun** önemli olduğu eniyileme problemlerinde. Avantajı: sabit bellek, çok büyük veya sürekli uzaylarda da çalışması.
2. **%14** (kitap; bizim deneyde %15). Yana hamleyle **%94**.
3. **1/p.** 8-vezirde yana hamle olmadan yaklaşık 7 deneme.
4. **e^(ΔE/T)** (ΔE < 0). T azaldıkça kötü adımların kabul olasılığı sıfıra yaklaşır; algoritma tepe tırmanmaya dönüşür.
5. Işınlar bilgi paylaşır: Bir sonraki k durum, *tüm* ışınların komşuları arasından en iyi k olarak seçilir. İyi bir bölge bulan ışın diğerlerini oraya çeker.
6. Temsilde, birbirinden bağımsız olarak iyi olabilen **yapı taşları** (schema) varsa. Çaprazlama iyi parçaları birleştirebilir.
7. Gradyan formülü, her havalimanına en yakın il kümelerine (Cᵢ) bağlıdır. Havalimanları çok hareket edince kümeler değişir ve formül de değişir.
8. VEYA: **ajanın** seçimi (bir eylem yeter). VE: **ortamın** seçimi (her olası sonuç için plan gerekir).
9. {1,…,8} → {2, 4, 6, 8} → {4, 8} → {3, 7} → {7}
10. **TAHMİN** (eylemin olası sonuçlarının birleşimi) ve **GÜNCELLEME** (gözlenen algıyla tutarlı olmayan durumları atma).
11. Her erişilebilir durumdan bir hedefe ulaşılabilen ortam. Geri dönüşsüz eylemler (çıkmazlar) varsa hiçbir çevrimiçi algoritmanın rekabet oranı sınırlı olamaz.
12. Doğrudan hedefe h(s) maliyetle gittiği varsayılır (**belirsizlik karşısında iyimserlik**). Bu, ajanı bilinmeyen yolları denemeye teşvik eder.
