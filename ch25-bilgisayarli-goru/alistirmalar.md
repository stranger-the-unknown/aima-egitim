# Bölüm 25 — Alıştırmalar

Sorular özgündür. Çözümler `cozumler/` klasöründe; önce kendin dene.

Zorluk: ★ kolay · ★★ orta · ★★★ zor

---

## A1 — Perspektif izdüşüm ★

Odak uzaklığı f = 50 mm olan bir iğne deliği kamera düşün.
1. 1.8 m boyundaki bir insan 10 m uzaktaysa görüntüsü kaç mm'dir? 0.18 m'lik bir oyuncak 1 m uzaktaysa?
2. Bu sonuç kitaptaki "oyuncak Godzilla mı gerçek canavar mı" belirsizliğini nasıl açıklar? Belirsizliği gidermek için hangi ek bilgiler kullanılabilir?
3. Görüntüdeki eksi işaretlerin anlamı nedir?

## A2 — Kaybolma noktaları (kod) ★★

f = 1 için şu yönlerdeki doğruların kaybolma noktalarını bul: (0, 0, 1), (1, 0, 1), (−1, 0, 1), (1, 0, 3), (0, 1, 1).
1. V = 0 olan bütün yönlerin (yere paralel doğruların) kaybolma noktaları nerede toplanır? Bu çizgiye ne denir?
2. W = 0 olan doğrular için ne olur?

## A3 — Lambert yasası ve renk ★

Albedosu ρ = 0.6 olan bir yüzey I₀ = 200 şiddetinde uzak bir nokta kaynakla aydınlatılıyor.
1. θ = 0°, 45°, 60°, 80° için parlaklığı hesapla. Parlaklık hangi açıda yarıya iner?
2. RGB albedoları (0.8, 0.4, 0.1) olan bir yüzey beyaz ışıkta (100, 100, 100) ve kırmızımsı ışıkta (100, 60, 40) hangi piksel değerlerini verir? İnsan gözü bu farkı nasıl karşılar?

## A4 — Stereo ile derinlik ★★

1. Kitaptaki insan değerleriyle (b = 6 cm, en küçük δθ = 5 açı saniyesi) Z = 100 cm ve Z = 30 cm için ayırt edilebilen derinlik farkını hesapla.
2. Taban uzunluğu 0.12 m, odak uzaklığı 700 piksel olan bir kamera çifti 7 piksel eşitsizlik ölçüyor. Nesne ne kadar uzakta? Ölçüm 1 piksel hatalıysa (6 ya da 8 piksel)?
3. Aynı soru 70 piksel eşitsizlik için. Derinlik hatası uzaklıkla nasıl büyüyor?

## A5 — Düzeltme ölçeği (kod) ★★

`ozellikler.py`'deki gürültülü basamak için düzeltmesiz türevle ve σ = 1, 2, 4 Gauss türeviyle kenar tepelerini bul. Sonra 2 piksel genişliğinde bir şerit (iki kenar) için aynı işlemi yap. Büyük σ'nın yararı ve zararı nedir?

## A6 — Doku histogramları (kod) ★★

8 kutulu yön histogramını dikey çizgiler, 90° döndürülmüş dikey çizgiler, 45° eğik çizgiler, benekler ve 0.3 ile çarpılıp 0.5 eklenmiş dikey çizgiler için hesapla. Kitaptaki iki istek (ışıkla değişmeme, döndürmeyle anlamlı değişme) karşılanıyor mu?

## A7 — Optik akış (kod) ★★

1. Rastgele dokulu bir görüntüyü (2, 1) kaydırıp SSD blok eşlemeyle akışı bul.
2. Dikey çizgili bir görüntüyü dikey yönde 3 piksel kaydır. SSD hangi adaylar için sıfırdır? Neden? (Bu durum kitaptaki beyaz duvar örneğinin bir uzantısıdır.)
3. Duvardan 0.5 m uzaktaki bir sinek duvara 0.25 m/s hızla yaklaşıyor. Çarpışma zamanı nedir? Sinek uzaklığı ve hızı ayrı ayrı bilmeden bunu nasıl kestirebilir?

## A8 — Normalleştirilmiş kesme (kod) ★★★

`iki_bolgeli()` görüntüsünde aydınlatma eğimi 0, 0.4, 0.8 için 5 farklı tohumla normalleştirilmiş kesmenin ve (gerçek etiketi bilerek seçilen) en iyi tek parlaklık eşiğinin doğruluğunu karşılaştır. Hangisi neden daha dayanıklı? Ncut bazen neden başarısız olur?

## A9 — Desenlerin deseni (kod) ★★

1. 3 × 3 çekirdekli, adım 1'li 1–5 katmanlı bir ağda bir çıktı birimi kaç × kaç pikselik bir pencereye bakar?
2. `tespit.py`'deki 2. katman artıya da L köşesine de yanıt veriyor. Merkezin iki yanında yatay, üstünde ve altında dikey yanıt isteyen bir 3. katman tasarla; yalnızca artıya yanıt verdiğini göster.

## A10 — Nesne tespiti (kod) ★★

1. A = (0, 0, 4, 4) ve B = (2, 2, 6, 6) kutularının IoU'sunu elle hesapla.
2. Beş kutu ve puanları: (0, 0, 10, 10) 0.95; (1, 1, 11, 11) 0.9; (20, 20, 30, 30) 0.8; (21, 19, 31, 29) 0.85; (50, 50, 60, 60) 0.4. IoU eşiği 0.5 ile NMS uygula.
3. Gerçek kutular (0, 0, 10, 10), (20, 20, 30, 30), (70, 70, 80, 80) ise kesinlik ve duyarlılık nedir? 0.5 altı puanları atınca?
4. 200 × 200 görüntüde kaç dikdörtgen pencere vardır? 1280 × 720 görüntüde Faster RCNN (adım 16, 9 kutu) kaç çapa kutusu değerlendirir?
