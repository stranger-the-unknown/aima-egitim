# Çözümler — A3, A4, A5

## A3 — 8-vezir deneyi

1. `--deney 2000` çıktısı (tohum 1):

   | | Başarı | Adım (başarı / takılma) | Kitap |
   |---|---|---|---|
   | Yana hamle yok | %15 | 4,1 / 3,1 | %14 · 4 / 3 |
   | 100 yana hamle | %95 | 19,5 / 63,6 | %94 · 21 / 64 |

   Farklar örneklem gürültüsünden kaynaklanır. 2000 denemede %14 civarındaki bir oranın standart hatası ~%0,8'dir.

2. Beklenen toplam adım = (başarılı bir denemenin maliyeti) + (1 − p)/p × (başarısız bir denemenin maliyeti):
   - Yana hamle yok: 4 + (0,86/0,14) × 3 ≈ **22 adım** (yaklaşık 7 deneme).
   - 100 yana hamle: 21 + (0,06/0,94) × 64 ≈ **25 adım** (yaklaşık 1,06 deneme).

   Yana hamle bir denemeyi uzatır ama deneme sayısını çok azaltır. İkisi de 8-vezir için birkaç düzine adımda çözüm demektir.
3. h, birbirini tehdit eden (aynı satırda veya çaprazda) vezir çiftlerinin sayısıdır. Sütunlar zaten farklı olduğu için h = 0 ise hiçbir vezir diğerini tehdit etmiyordur. Bu da tam olarak 8-vezir probleminin çözümüdür.

## A4 — Benzetilmiş tavlama

1. Kötüleşen adım e^(ΔE/T) olasılıkla kabul edilir. ΔE = −2 için:
   - T = 10 → e^(−0,2) ≈ **0,82** (neredeyse her zaman kabul)
   - T = 0,1 → e^(−20) ≈ **2 × 10⁻⁹** (pratikte hiç)

   Yüksek sıcaklıkta arama "gevşektir" ve kötü turlara geçerek başka bölgeleri keşfeder.
2. `--soguma 0.5` ile T yalnızca 15 adımda 10'dan 0,001'in altına düşer ve arama biter. Bulunan tur **21,384**, optimum 17,699. Çok hızlı soğuma, tavlamayı birkaç adımlık rastgele bir tepe tırmanmaya çevirir. Metallerde de hızlı soğutma kırılgan ve düzensiz bir yapı bırakır.
3. 30 şehirde ortalama fark ≈ **7,6** birim (438,6'ya karşı 431,0). Farkı artırmak için soğumayı yavaşlatmak (`soguma` 1'e daha yakın) ve adım sınırını büyütmek gerekir. Böylece yüksek sıcaklıkta daha uzun keşif yapılır. Başlangıç sıcaklığı, tipik ΔE değerleriyle aynı büyüklükte seçilmelidir.

## A5 — Çevrimiçi arama ve inanç

1. **Çevrimiçi.** Harita bilinmiyor; SONUÇ(s, a)'yı öğrenmenin tek yolu a'yı s'de denemek.
2. Robotun **olabileceği kareler** kümesi (ve bu karelerdeki duvar yapıları hakkında öğrendikleri). Her algı, algılanan duvar düzenine uymayan kareleri inançtan çıkarır. Bu, robotik konum belirlemenin (Bölüm 26) mantıksal hâlidir.
3. Geri dönüşsüz eylemler varsa ortam artık **güvenle keşfedilebilir** değildir. Hiçbir çevrimiçi algoritma rekabet oranını sınırlayamaz; düşman bir ortam, robotun seçtiği her yolu çukura çevirebilir. Pratikte ya ek bilgi (ör. "çukurların kenarı algılanabilir") ya da riskten kaçınan bir keşif politikası gerekir.
