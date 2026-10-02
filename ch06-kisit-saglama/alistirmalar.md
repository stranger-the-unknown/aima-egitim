# Bölüm 6 — Alıştırmalar

Sorular özgündür. Çözümler `cozumler/` klasöründe; önce kendin dene.

Zorluk: ★ kolay · ★★ orta · ★★★ zor

---

## A1 — CSP modeli ★

Bir üniversitede üç ders (MAT, FİZ, YAZ) üç zaman dilimine (09:00, 11:00, 14:00) yerleştirilecek. Aynı saatte en fazla bir ders olabilir. MAT ile FİZ aynı hocayı paylaşıyor.

1. Değişkenleri, alanları ve kısıtları yaz.
2. Bu problem neden "yol arama"dan çok CSP'ye uyar?

## A2 — MRV ve derece ★

Türkiye haritasında (`ornekler/harita_boyama_csp.py`) İç Anadolu'nun 5, Güneydoğu'nun 2 komşusu var. Üç renk kullanılıyor. Bir noktada İç Anadolu'nun alanında 1 renk, Ege'nin alanında 3 renk kalmış.

1. MRV hangi değişkeni önce seçer? Neden?
2. Hiç atama yapılmamışken (bütün alanlar eşitken) derece sezgiseli hangi bölgeyi seçer?

## A3 — Türkiye haritası ★★

```bash
python ornekler/harita_boyama_csp.py
python ornekler/harita_boyama_csp.py --karsilastir
```

1. Üç renkle çözüm bulundu mu? Dört renkle?
2. Üç rengin yetmediğini aramaya başvurmadan, elle kanıtla.
3. `--karsilastir` çıktısında, 3 renkle "çözüm yok" sonucuna en az atamayla hangi ayar ulaştı?

## A4 — N-vezir CSP ★

```bash
python ornekler/n_vezir_csp.py --n 4
python ornekler/n_vezir_csp.py
```

1. Değişken, alan ve kısıt tanımını kendi cümlelerinle yaz.
2. Tablodaki hangi sezgisel en büyük farkı yaratıyor?
3. Bölüm 4'teki tepe tırmanmadan (ve bu bölümdeki min-çatışmadan) farkı nedir? "Garanti" açısından düşün.

## A5 — İleri kontrol ile AC-3 ★★

Bir değişkene değer verdin ve komşularının alanlarından uyumsuz değerleri sildin (ileri kontrol). Bu neden tam yay tutarlılığı (AC-3) kadar güçlü değildir? A–B–C zinciriyle somut bir senaryo kur.

## A6 — Elle AC-3 ★★

Avustralya haritasında WA = kırmızı ve Q = yeşil atanmış olsun; diğer alanlar {K, Y, M}.

1. Bu iki atamadan sonra, ileri kontrolle NT, SA ve NSW'nin alanları ne olur?
2. Şimdi AC-3'ü çalıştır. Kuyruktan hangi yaylar çıkınca hangi değerler silinir? Sonuç nedir?
3. Bu, geri izleme aramasında kaç atama tasarrufu sağlar?

## A7 — En küçük döngü kesme kümesi (kod) ★★★

Türkiye haritasının kısıt grafı için:

1. Tek bir değişken çıkarılınca graf ağaç olur mu? Her bölge için kontrol et.
2. Grafı ağaca çeviren **en küçük** kesme kümesini bul.
3. `kisit.kesme_kumesi_coz` ile haritayı 4 renkle çöz. Kesme kümesinin kaç ataması denendi?

## A8 — Kriptaritmetik ★

```bash
python ornekler/kriptaritmetik.py
python ornekler/kriptaritmetik.py --bulmaca "SEND+MORE=MONEY"
```

1. TWO + TWO = FOUR'un kaç çözümü var? F neden her çözümde 1?
2. SEND + MORE = MONEY'de M neden 1 olmak zorunda? Bunu aramasız, yalnızca bir sütun kısıtıyla göster.
3. Sütun sütun arama, kaba kuvvete göre kaç kat az kısmi atama deniyor?

## A9 — Min-çatışmada gürültü (kod) ★★

`ornekler/min_catisma_vezir.py` içindeki `min_catisma` fonksiyonunu gürültü = 0; 0,05; 0,3 ile n = 8 ve n = 1000 için 20'şer tohumla çalıştır (en fazla 10.000 adım).

1. Her ayar için başarı oranını ve ortalama adım sayısını tablo yap.
2. Gürültü 0 iken n = 8 neden bazen hiç bitmiyor, n = 1000 ise neden sorun çıkmıyor?
3. Çok fazla gürültünün bedeli nedir?

## A10 — Değer simetrisi (kod) ★★

Avustralya haritasının 18 çözümü var.

1. NT < SA < WA (renklerin alfabetik sırası: kırmızı < mavi < yeşil gibi bir sabit sıra) **simetri kırıcı** kısıtını ekle. Kaç çözüm kalır?
2. Bu sayı neden 18 / 3! = 3'tür?
3. Simetri kırmanın geri izleme aramasındaki etkisini ölç (tüm çözümleri sayarken yapılan atama sayısı).
