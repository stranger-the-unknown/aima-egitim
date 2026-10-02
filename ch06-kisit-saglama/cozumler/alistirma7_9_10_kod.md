# Çözümler — A7, A9, A10 (kod: `alistirma7_9_10_kod.py`)

## A7 — En küçük döngü kesme kümesi

1. **Hiçbir tek bölge** çıkarıldığında graf ağaç olmuyor. Örneğin İç Anadolu çıkarılınca Akdeniz–Güneydoğu–Doğu Anadolu üçgeni kalıyor.
2. En küçük kesme kümesinin boyutu **2**. Kod ilk olarak **{Akdeniz, İç Anadolu}** kümesini buluyor. Geriye Ege–Marmara–Karadeniz–Doğu Anadolu–Güneydoğu yolu kalır; bu bir ağaçtır. ({İç Anadolu, Doğu Anadolu} de iş görür.)
3. 4 renkle kesme kümesi koşullandırması çözüm buluyor. 3 renkle ise kesme kümesinin her tutarlı ataması (3 × 2 = 6 atama) için kalan ağaç çözülemiyor, sonuç `None`. Bu, 3 rengin yetmediğinin **ikinci bir kanıtıdır**.

   Süre O(d^c · (n − c)·d²): d = 4, c = 2, n = 7 → en fazla 16 atama × 5 düğümlük ağaç.

## A9 — Min-çatışmada gürültü

| Gürültü | n | Başarı (20 tohum) | Ort. adım |
|---|---|---|---|
| 0 | 8 | 17/20 | 51,6 |
| 0 | 1000 | 20/20 | 54,1 |
| 0,05 | 8 | 20/20 | 75,2 |
| 0,05 | 1000 | 20/20 | 55,7 |
| 0,3 | 8 | 20/20 | 86,5 |
| 0,3 | 1000 | **16/20** | 4.169,9 |

- **Gürültü 0, n = 8:** Küçük tahtada, çatışan her vezirin en iyi satırının zaten bulunduğu satır olduğu yerel minimumlar vardır. Algoritma "hareket ediyormuş gibi" yapıp aynı yerde kalır ve sonsuza kadar döner (20'de 3). n = 1000'de çözümler çok yoğun ve seçenek çok fazla olduğu için böyle bir tuzağa düşmek pratikte imkânsızdır.
- **Az gürültü (%5)** tuzakları kırar, bedeli de küçüktür.
- **Çok gürültü (%30)** büyük tahtada felakettir. Her adımın %30'u rastgele bir satıra gider ve bu çoğu zaman *yeni* çatışmalar yaratır. Algoritma çözüme yaklaştığı hızla uzaklaşır. Bu, keşif–sömürü ödünleşiminin bir başka yüzüdür (Bölüm 4'teki tavlamada sıcaklığın çok yüksek kalması gibi).

## A10 — Değer simetrisi

| | Çözüm | Tümünü bulmak için atama |
|---|---|---|
| Simetri kırılmadan | 18 | 51 |
| NT < SA < WA ile | **3** | 11 |

- WA, NT ve SA karşılıklı komşudur, yani üç farklı renk alırlar. 3 rengin 3! = 6 permütasyonundan yalnızca **biri** NT < SA < WA sırasını sağlar. Anakara çözümleri 6'dan 1'e iner; Tazmanya'nın 3 seçeneği bağımsız olduğu için toplam 1 × 3 = **3** çözüm kalır (18 / 3! = 3).
- Tüm çözümleri sayarken atama sayısı 51'den 11'e düşüyor. Simetrik dallar hiç açılmıyor. Çok simetrik problemlerde (ör. d renk ile büyük bir harita) bu kazanç d! katına kadar çıkabilir.
