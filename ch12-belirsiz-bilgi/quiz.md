# Bölüm 12 — Quiz

Cevaplara bakmadan önce kendin yanıtla. Cevaplar dosyanın sonunda.

---

**S1.** Kitaba göre mantığın tıbbi tanıda başarısız olmasının üç nedeni nedir?

**S2.** İki adil zar atılıyor. P(Toplam = 11) kaçtır?

A) 1/36
B) 1/12
C) 1/6
D) 1/18

**S3.** Karar kuramı hangi iki kuramın birleşimidir? Rasyonel ajan hangi ilkeye göre seçim yapar?

**S4.** Diş hekimi tablosunda P(cavity) = 0.2 ve P(toothache) = 0.2 ise, P(cavity ∧ toothache) = 0.12 iken P(cavity ∨ toothache) nedir?

A) 0.28
B) 0.40
C) 0.32
D) 0.12

**S5.** Normalizasyon sabiti α ne işe yarar? Hangi olasılığı hesaplamaktan kurtarır?

**S6.** P(s | m) = 0.7, P(m) = 1/50000, P(s) = 0.01 ise P(m | s) kaçtır?

A) 0.7
B) 0.0014
C) 0.014
D) 0.00002

**S7.** Tanısal bilgi yerine nedensel bilgi saklamak neden daha sağlamdır? Bir örnekle açıkla.

**S8.** Toothache ve Catch için hangisi doğrudur?

A) Mutlak bağımsızdırlar
B) Hiçbir koşulda bağımsız değildirler
C) Cavity verildiğinde koşullu bağımsızdırlar, ama mutlak bağımsız değildirler
D) Weather verildiğinde koşullu bağımsızdırlar

**S9.** n belirtinin hepsi tek bir neden verildiğinde koşullu bağımsızsa (Boole değişkenler), temsil boyutu nasıl büyür?

A) O(2ⁿ)
B) O(n)
C) O(n²)
D) O(1)

**S10.** Naif Bayes metin sınıflandırmada, eğitimde hiç görülmemiş bir kelimeye 0 olasılık verilirse ne olur?

**S11.** de Finetti'nin argümanı ne gösterir?

**S12.** Kitaptaki Wumpus durumunda P(P₂,₂) ≈ 0.86 iken P(P₁,₃) ≈ 0.31'dir. Mantık ajanı ile olasılık ajanı arasındaki fark nedir? Hesap neden 4096 yerine 4 terimle yapılabilir?

---

## Cevaplar

1. **Tembellik** (bütün koşulları listelemek çok zahmetli), **kuramsal bilgisizlik** (alanın tam kuramı yok), **pratik bilgisizlik** (bu hasta için gerekli bütün testler yapılmamış).
2. **D.** (5, 6) ve (6, 5): 2/36 = 1/18.
3. Olasılık kuramı + fayda kuramı. **En yüksek beklenen fayda (MEU)** ilkesi: Olası sonuçların faydalarının olasılıkla ağırlıklı ortalaması en yüksek olan eylem seçilir.
4. **A.** Dahil etme–dışlama: 0.2 + 0.2 − 0.12 = 0.28.
5. Sorgu değişkeninin her değeri için ham değerleri hesaplayıp toplamı 1 yapar. Kanıtın olasılığını, P(e)'yi, ayrıca hesaplamaya gerek kalmaz.
6. **B.** 0.7 × (1/50000) / 0.01 = 0.0014.
7. Nedensel bilgi (P(belirti | hastalık)) hastalığın nasıl işlediğini yansıtır ve ortam değişince aynı kalır. Salgında P(m) artar. Tanısal P(m | s)'yi eski istatistikten öğrenmiş doktor onu güncelleyemez. Nedensel bilgiyi saklayan doktor ise Bayes kuralıyla yeni P(m | s)'yi hesaplar.
8. **C.** Sonda takılırsa çürük olasıdır, çürük de ağrıtır: Tek başlarına ilişkilidirler. Çürüğün durumu bilinince biri diğeri hakkında bilgi vermez.
9. **B.** Her belirti için 2 sayı, neden için 1 sayı: 2n + 1. Tam tablo ise 2ⁿ⁺¹ − 1.
10. O kategori için bütün çarpım 0 olur ve diğer bütün kanıtlar silinir. Belge, ne kadar güçlü kanıt olursa olsun o kategoriye atanamaz. Görülmemiş kelimelere küçük bir olasılık ayrılmalıdır (yumuşatma).
11. Olasılık aksiyomlarını çiğneyen inançlara sahip bir ajana karşı, her sonuçta kaybettiren bir bahis kombinasyonu kurulabilir. Yani rasyonel bir ajanın inançları aksiyomlara uymalıdır.
12. Mantık ajanı üç kare için de yalnızca "bilinmiyor" diyebilir ve rastgele seçer. Olasılık ajanı [2,2]'nin çok daha riskli olduğunu bilir ve ondan kaçınır. Gözlenen esintiler, bilinenler, sorgu ve **sınır** kareleri verildiğinde diğer karelerden koşullu bağımsızdır. Diğer 10 kare toplamdan çıkar; yalnızca 2 sınır karesinin 4 ataması kalır.
