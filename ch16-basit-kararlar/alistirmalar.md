# Bölüm 16 — Alıştırmalar

Sorular özgündür. Çözümler `cozumler/` klasöründe; önce kendin dene.

Zorluk: ★ kolay · ★★ orta · ★★★ zor

---

## A1 — Kestirme mi, ana yol mu? ★

Bir kurye iki yoldan birini seçecek. Kestirme yolda kaza olup olmadığını bilmiyor: P(kaza yok) = 0.6.
- **Kestirme:** Kaza yoksa 0.8, kaza varsa 0.3 olasılıkla zamanında varır.
- **Ana yol:** Kesin olarak biraz geç kalır.

Fayda: zamanında = 10, biraz geç = 5, çok geç = 0. Kestirmede zamanında varamazsa çok geç kalır.

1. P(RESULT(kestirme) = zamanında)'yı ve iki yolun EU'sunu hesapla. MEU hangisini seçer?
2. P(kaza yok) hangi değerin altına düşerse karar değişir?

## A2 — Hangi aksiyom? ★

Her davranış hangi aksiyomu çiğner?
1. "Bu iki tatil paketini karşılaştıramam; ikisini de seçmem, ikisine de eşit demem."
2. A ≻ B olduğu hâlde [0.6, A; 0.4, B] yerine [0.4, A; 0.6, B] seçiyor.
3. [0.5, A; 0.5, [0.5, A; 0.5, B]] ile [0.75, A; 0.25, B] arasında fark görüyor, çünkü "iki kez zar atmak daha heyecanlı".
4. A ∼ B olduğu hâlde [0.3, A; 0.7, C] ≻ [0.3, B; 0.7, C].
5. Takas zincirinde her seferinde 1 kuruş ödeyip başladığı yere dönüyor.

## A3 — Fayda ölçeği ★

Üç sonuç için U(a) = 0, U(b) = 4, U(c) = 9. Piyango L = [0.5, a; 0.5, c], kesin seçenek b.
1. MEU'ya göre hangisi seçilir?
2. U′ = 2U + 3 ile ve U″ = √U ile tekrar hesapla. Hangisi kararı değiştirir? Neden?

## A4 — Paranın faydası ve hayatın fiyatı (kod) ★★

1. Bay Beard için yarı yarıya 0 $ / 800 000 $ piyangosunun EMV'sini, kesinlik eşdeğerini ve sigorta primini hesapla. Aynı soruyu 0 / 1000 $ için yanıtla. Farkı açıkla.
2. Bay Beard'ın fayda fonksiyonu verilen aralıkta herhangi bir yerde risk arayan davranış gösterir mi?
3. Kitaptaki araba örneğini kullanarak bir mikromortun kaç dolar edildiğini hesapla.

## A5 — Allais'i kurtarmak (kod) ★★

1. Allais'teki B ≻ A tercihi için kişi ne kadar EMV'den vazgeçiyor?
2. A'yı seçip kaybeden kişi, para dışında bir de "pişmanlık" yaşasın: Faydası 0 değil −r olsun (U(0 $) = 0, U(4000 $) = 1 ölçeğinde). C ve D'de pişmanlık yok (kesin bir şeyden vazgeçilmiyor). Hangi r ve U(3000 $) değerleri B ≻ A ve C ≻ D'yi birlikte açıklar?

## A6 — İyileştiricinin laneti ve büzme (kod) ★★

20 seçenek var; gerçek değerleri V ~ N(0, 1). Yarısının tahmin hatası σe = 3 (gürültülü), yarısınınki σe = 0.5.
1. "Saf" seçici en büyük tahmini seçer. Seçilen seçeneğin tahmini ve gerçek değeri ortalamada kaçtır? Seçtiği seçeneklerin yüzde kaçı gürültülü gruptan?
2. Bayesçi seçici her tahmini E[V | tahmin] = tahmin / (1 + σe²) ile düzeltip (büzüp) seçer. Aynı soruları yanıtla.
3. Bütün seçeneklerin σe'si aynı olsaydı büzme seçimi değiştirir miydi?

## A7 — Havalimanı karar ağında bilgi ve duyarlılık (kod) ★★

`ornekler/karar_agi.py`'deki ağı kullan.
1. Hava trafiğini önceden öğrenmenin değeri (VPI) nedir? Neden?
2. Ölüm ağırlığı (w_ölüm, varsayılan 5) hangi değeri geçince en iyi yer değişir? Bu, kararın sağlamlığı hakkında ne söyler?
3. P(trafik yoğun) [0, 1] aralığında herhangi bir değer olabilirse sağlam (minimaks) karar nedir?

## A8 — Petrol ve VPI'nin özellikleri ★★

1. 4 blokluk petrol örneğinde jeoloğun blok 3 hakkındaki kesin bilgisinin değerini adım adım hesapla.
2. VPI'nin neden asla negatif olamayacağını açıkla. Tek bir kötü haber kararı kötüleştirmez mi?
3. Bir hastaya aynı kan testini iki kez yapmanın değeri neden ilk testin değerinin iki katı değildir?

## A9 — Hazine avı (kod) ★★★

Dört yer var. Hazine olma olasılıkları P = [0.3, 0.6, 0.15, 0.4], bakma maliyetleri C = [3, 10, 1, 2]. Hazine bulununca aramayı bırakırsın; hazinenin bir yerde olduğu garanti değil.
1. `C(xy) = C(x) + F(x) C(y)` kuralıyla [4, 3, 1, 2] sırasının beklenen maliyetini elle hesapla.
2. "P/C'ye göre", "en olası önce" ve "en ucuz önce" sıralarını karşılaştır. Kaba kuvvetle (bütün 24 sıra) en iyisini bul.
3. Komşu iki yerin yer değiştirmesinin etkisinin neden geri kalan sıradan bağımsız olduğunu açıkla.

## A10 — Hata yapan Harriet (kod) ★★★

Kapatma düğmesi oyununda u ~ U[−40, 60]. Harriet ε olasılıkla yanlış karar verir: İyi bir eylemi durdurur ya da kötü bir eyleme izin verir.
1. "Bekle" seçeneğinin değerini ε cinsinden yaz.
2. Robbie hangi ε değerinden sonra Harriet'e danışmayı bırakıp eylemi hemen yapar?
3. Bu sonuç güvenli yapay zekâ için ne anlama gelir?
