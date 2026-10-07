# A1–A10 çözümleri

Kodlu kısımlar: `python cozumler/alistirma_kod.py` (bölüm klasöründen).

---

## A1 — Turing testi ve Çin odası

1. Program bir sorgulayıcıyla beş dakika yazışır; sorgulayıcı karşısındakinin program mı insan mı olduğunu tahmin eder; program sorgulayıcıyı %30 oranında kandırırsa geçer. Eugene Goostman eğitimsiz jürinin %33'ünü, dil hatalarını açıklayan bir kimlikle (İngilizcesi zayıf Ukraynalı çocuk) kandırdı. Bu, testin zekâdan çok sorgulayıcının saflığını ve koşulların (süre, jürinin uzmanlığı, kimlik bahanesi) etkisini ölçebileceğini gösterir; kitap da "belki de bir saflık testi" der. Turing'e göre asıl önemli olan, zekânın felsefi spekülasyon yerine açık uçlu bir davranış göreviyle ölçülmesiydi.
2. (i) Odadaki insan Çince anlamaz. (ii) Kural kitabı ve kâğıtlar da anlamaz. (iii) Başka bir şey olmadığına göre odada Çince anlama yoktur; bilgisayar da aynı işi yapar, öyleyse bilgisayar da anlamaz. "Sistem yanıtı" ve "hücreler de anlamaz" itirazları (iii)'e, yani "parçalar anlamıyorsa bütün de anlamaz" çıkarımına saldırır: Aynı çıkarım insan beynine uygulanırsa insanın da anlamadığı sonucuna varılır (Bisson'un "Etten Yapılmışlar" öyküsü). Searle'ün yanıtı biyolojik doğalcılıktır: nöronlarda olan "o şey" transistörlerde yoktur; ama bu "şey" tanımlanmamıştır.

## A2 — Gödel itirazı

Lucas: Aritmetik yapabilen her biçimsel sistemin içinde kanıtlayamadığı ama (sistem tutarlıysa) doğru olan bir Gödel cümlesi vardır; makineler biçimsel sistemdir, insanlar bu sınıra tabi değildir; öyleyse insan zihni makineden üstündür. Yanıtlar:
1. Kendine özgü sınır herkes için kurulabilir: "Lucas bu cümlenin doğru olduğunu tutarlı biçimde ileri süremez" cümlesi doğrudur ama Lucas onu ileri süremez. Bu Lucas'ı küçültmez; makineyi de küçültmemeli.
2. Teorem matematik içindir: Kanıtlanamayanı kimse kanıtlayamaz. İnsanların "kendi tutarlılığını varsayabildiği" iddiası temelsizdir: İnsanlar tutarsızdır, dikkatli matematikte bile (Kempe'nin hatalı dört renk ispatı 11 yıl kabul gördü).
3. Teorem aritmetik yapabilen (sonsuz) biçimsel sistemler içindir; gerçek bilgisayarlar ve beyinler sonludur, büyük bir önermeler mantığı sistemi olarak betimlenebilir ve teoreme tabi değildir. Ayrıca bilgisayarlar da "fikir değiştirebilir" (yeni kanıtla, öğrenmeyle).
En güçlü yanıt bir görüş meselesidir; çoğu kişi ikinciyi seçer, çünkü Lucas'ın argümanı insanların tutarlı olduğu varsayımına dayanır ve bu varsayım deneysel olarak yanlıştır.

## A3 — Yeniden tanımlama

| n (bir posta kodunda) | Tek başına (gözlenen) | e^(−n/K) | Doğum yılıyla k |
|---|---|---|---|
| 1 000 | 0.98 | 0.983 | 1 |
| 10 000 | 0.84 | 0.843 | 45 |
| 100 000 | 0.18 | 0.180 | 562 |

K = 365 · 80 · 2 = 58 400 olası (doğum günü, cinsiyet) çifti. Bir kişinin çiftini başka hiç kimsenin paylaşmama olasılığı (1 − 1/K)^(n−1) ≈ e^(−n/K). Kalabalık posta kodunda aynı çifti paylaşan başka biri bulunma olasılığı yüksektir. Ama doğum yılına genelleştirmek bile küçük bir posta kodunda yetmeyebilir (n = 1 000'de k = 1: bir yılda tek kişi doğmuş olabilir; kitaptaki "94720'de 90–100 yaşında tek kişi" örneği). Ayrıca gerçek nüfus düzgün dağılmaz; uç değerler daha da kolay tanınır.

## A4 — Fark saldırısı ve diferansiyel mahremiyet

1. 13 × 81 199 − 12 × 81 234 = 1 055 587 − 974 808 = **$80 779**.
2. | ε | Saldırı başarısı | e^ε/(1 + e^ε) |
   |---|---|---|
   | 0.1 | 0.513 | 0.525 |
   | 0.5 | 0.561 | 0.622 |
   | 1 | 0.620 | 0.731 |
   | 2 | 0.724 | 0.881 |
   | 5 | 0.908 | 0.993 |

   Sınır: Kişinin hasta olup olmaması yalnızca ikinci sorgunun sonucunu etkiler. ε-DP'ye göre herhangi bir y için P(y | hasta) / P(y | sağlıklı) ≤ e^ε. Önsel 1/2 iken sonsal olasılık en çok e^ε / (1 + e^ε) olur; hiçbir saldırgan bundan daha sık doğru tahmin edemez. Kodumuzdaki saldırgan (fark > 0.5 ise "hasta") en iyi saldırgan değildir, bu yüzden sınırın altında kalır. Küçük ε güçlü mahremiyet ama gürültülü yanıt demektir (ε = 0.1'de std ≈ 14): mahremiyet ile doğruluk arasında ödünleşim.

## A5 — Güvenli toplama

İlk üç kullanıcının gerçek toplamı (2.006, −3.339); maskeli toplamları (−1860.7, −865.8). Dördüncü kullanıcının maskeleri eksik kaldığı için diğer üçünün maskeleri birbirini götürmez ve sonuç anlamsızdır. Kitabın sözünü ettiği gereksinim: Protokol kullanıcıların yanıt vermemesine **dayanıklı** olmalıdır (gerçek protokoller maskeleri gizli paylaşımla yeniden kurabilir; ayrıntı kitapta yok). Tam katılımda toplam doğru çıkar.

## A6 — Kalibrasyon ve fırsat eşitliği

| Taban oranlar | Yanlış pozitif (A, B) | Yanlış negatif (A, B) | Puan 0.6–0.7'de gerçek oran (A, B) |
|---|---|---|---|
| (0.3, 0.3) | (0.095, 0.096) | (0.615, 0.613) | (0.639, 0.641) |
| (0.3, 0.5) | (0.095, 0.319) | (0.616, 0.314) | (0.644, 0.645) |
| (0.2, 0.6) | (0.039, 0.461) | (0.758, 0.188) | (0.645, 0.654) |

Puan her durumda kalibredir. Taban oranlar eşitken hata oranları da eşittir. Taban oranlar ayrıştıkça, aynı kalibre puan ve aynı eşik riskli grupta çok daha fazla yanlış pozitif, az riskli grupta çok daha fazla yanlış negatif üretir. Kleinberg vd.: Taban oranlar farklıysa (ve tahmin kusursuz değilse) kalibrasyon ile hata oranı eşitliği birlikte sağlanamaz; birini düzeltmek (örneğin grup eşikleri) ötekini bozar. COMPAS'ta kalibrasyon sağlanmış (%60 / %61), bu yüzden suç işlemeyenlerden "yüksek riskli" sayılanlar siyahlarda %45, beyazlarda %23: Hangi ölçütün seçileceği teknik değil, değer yargısıdır (kitap eşit etkiyi bir seçenek olarak önerir).

## A7 — Vekil değişkenler

| P(z = 1 \| B) | Onay A | Onay B |
|---|---|---|
| 0.5 (vekil bilgisiz) | 0.311 | 0.311 |
| 0.8 | 0.386 | 0.249 |
| 0.95 | 0.464 | 0.186 |

Model geçmişteki yanlı etiketleri en iyi açıklayan bilgiyi arar; grup sütunu yoksa onunla ilişkili posta kodunu kullanır. Vekil ne kadar güçlüyse ayrımcılık o kadar geri gelir; 0.95'te neredeyse grup sütunu varmış gibi. Sakınca: Grup bilgisi silinince fırsat ya da sonuç eşitliğini **denetlemek de imkânsızlaşır** (kitap). Asıl sorun etiketlerin yanlı olmasıdır; vekili de silmek (yalnızca x) onay oranlarını eşitler ama yanlı etiketlerle eğitilmiş bir modelin hâlâ yanlış şeyi öğrenmesi mümkündür.

## A8 — Örneklem boyu dengesizliği

| Azınlık payı | Çoğunluk hatası | Azınlık hatası |
|---|---|---|
| %1 | 0.0025 | 0.260 |
| %5 | 0.0033 | 0.290 |
| %20 | 0.0156 | 0.207 |
| %50 | 0.0834 | 0.086 |

Azınlık küçükken model neredeyse yalnızca çoğunluğa uyar. Önlemler: (1) azınlıktan fazla örnekleme ya da yeniden ağırlıklandırma (SMOTE, ADASYN): hatayı dengeler ama burada ikisini de kötüleştirir (~0.08), çünkü tek bir doğru iki zıt ilişkiye uyamaz; (2) daha uygun model (gruba özgü eğim): ikisini de çözer — kitaptaki "kısıtlı bir model iki sınıfa birden uyamayabilir" uyarısının ilacı; (3) alt gruplar için ayrı ölçütler izlemek ve azınlık kullanıcı deneyimini test etmek: sorunu ilk fark ettiren budur (ortalama hata %5 azınlıkta yalnızca 0.017'dir ve sorunu gizler).

## A9 — Düşük etki ve şartname oyunu

1. Vazodan geçen yol 6 adım + λ, dolambaç 8 adım: **λ > 2** olunca robot dolaşır (λ = 1.5 → vazo kırılır, 2.5 → dokunulmaz). Zayıflık: Bütün değişiklikleri eşit sayar. Değerli vazo ile değersiz bir toz zerresi aynı cezayı alır; ya da önemli bir değişiklik (kedinin mama kabını devirmek) hiç sayılmayabilir. Kitabın dediği gibi zorluk "etkiyi ölçmek"tir: açık programlama, zamanla öğrenme ve sıkı testlerin birleşimi gerekir.
2. γ = 0: temizle ×3, sonra bekle. γ = 0.95: temizle ×3, dök, temizle ×3, dök… Kiri dökmenin anlık ödülü sıfırdır; yalnızca gelecekteki temizleme ödülünü önemseyen etmen bu "boşluğu" keşfeder. Daha yetenekli (daha iyi planlayan, daha uzağı gören) etmenler şartnamenin boşluklarını daha iyi bulur; bu yüzden kitap "yeterince zeki bir robot başka bir şey yapmanın yolunu bulur" der ve kurallar yerine doğru amacı (değer hizalama) vurgular.

## A10 — Sor mu, uygula mı?

1. Uygula: 10p − 100(1 − p). Sor (kusursuz insan): −1 + 10p (felaket planlar reddedilir). Uygula ≥ sor ⇔ −100(1 − p) ≥ −1 ⇔ 1 − p ≤ 0.01 ⇔ **p ≥ 0.99**.
2. İnsan q olasılıkla doğru yanıt verirse sor = −1 + 10pq − 100(1 − p)(1 − q). Uygula ≥ sor ⇔ 10p(1 − q) − 100q(1 − p) ≥ −1. q = 0.95 → **p ≥ 0.984**; q = 0.80 → **p ≥ 0.963**. İnsan ne kadar hatalıysa sormanın değeri o kadar azalır: Felaket bir planı onaylama olasılığı (1 − q) varken sormak riski sıfırlamaz. Kitabın uyarısı tam budur: İnsanlar uzun vadeli sonuçları öngöremeden izin verebilir; robot bu kusurları hesaba katmalı, yalnızca "izin alındı" diye güvende sayılmamalıdır.
3. 1993'te 30 yıl kaldı; 2017'de 2045 − 2017 = 28 yıl kaldı. 24 yılda 2 yıl yaklaşıldı: yılda 1/12 yıl. Kalan 28 yıl ÷ (1/12) = **336 yıl**.
