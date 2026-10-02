# Çözümler — A7, A8, A10 (kod)

## A7 — XOX değerlendirme fonksiyonu: `alistirma7_xox_degerlendirme.py`

1. Boş tahtada X'in hamlesinden sonra EVAL: **orta = 4** (4 hattın parçası), **köşe = 3**, **kenar = 2**. Fonksiyon, "hangi karenin kaç hatta yer aldığı" sezgisini doğrudan kodluyor.
2. Tam minimax'a karşı tek oyunda, derinlik 1, 2, 3 ve 4'ün hepsi berabere kalıyor. Ama bu zayıf bir sınav: İki ajan da deterministik olduğu için hep aynı oyun oynanıyor.
3. Daha güçlü sınav, rakibin **olası tüm hamle dizilerini** denemek:

   | Derinlik | X olarak | O olarak |
   |---|---|---|
   | 1 | asla kaybetmez | **kaybedebilir** |
   | 2 | asla | asla |
   | 3 | asla | **kaybedebilir** |
   | 4 | asla | asla |

   En sığ güvenli derinlik **2**'dir. Tek derinliklerde O'nun araması **kendi hamlesiyle** biter; rakibin cevabını görmez. X bir çatal (iki tehdit birden) kurarsa O bunu fark etmez. Bu, ufuk etkisinin XOX'taki küçük bir örneğidir. Çift derinlikte arama rakibin cevabıyla bittiği için tehdit görünür. Pratik oyun programları bu yüzden "tek–çift etkisine" dikkat eder ya da sessizlik araması kullanır.

## A8 — MCTS'te C ve yineleme: `alistirma8_mcts_c.py`

MCTS (X) tam minimax'a (O) karşı, 10 oyundaki kayıp sayısı:

| C | 50 | 200 | 1000 |
|---|---|---|---|
| 0,0 | 1 | 1 | 3 |
| 0,5 | 0 | 0 | 0 |
| 1,4 | 2 | 0 | 0 |
| 5,0 | 0 | 0 | 0 |

- **C = 0** saf sömürüdür. İlk benzetimler şanslı çıkan bir hamleye "kilitlenir" ve diğer hamleleri yeterince denemez. Yineleme sayısını artırmak sorunu çözmez (1000'de bile 3 kayıp), çünkü keşif yoktur.
- **Çok az yineleme** (50) her C için risklidir: İstatistikler gürültülüdür.
- **Büyük C** (5) keşfe ağırlık verir. XOX küçük olduğu için burada zarar görmedik. Büyük oyunlarda ise bütçenin çoğu kötü hamleleri tekrar tekrar denemeye gider ve iyi hamlenin alt ağacı derinleşemez.
- Sonuçlar tek bir tohumla alındı; tam bir karşılaştırma için birkaç tohumun ortalaması alınmalıdır.

## A10 — Dört-Bir-Arada öznitelikleri: `alistirma10_dortlu_oznitelik.py`

Derinlik 3, her ikili için 6 oyun:

| Eşleşme | Sonuç |
|---|---|
| özgün — merkez | 6 – 0 |
| özgün — tehdit | 6 – 0 |
| merkez — tehdit | 3 – 3 |

- Özgün fonksiyon (1/10/100 puanlı pencereler + merkez bonusu) her iki sade sürümü de her oyunda yeniyor.
- Tek başına "merkez" ya da tek başına "tehdit" yetersiz. Merkez, açılışta iyi bir yön verir ama taktik tehditleri görmez. Tehdit özniteliği ise tahtada 3'lü oluşana kadar hep 0 döner. Bu yüzden erken oyunda hiçbir yön göstermez.
- **Ağırlıklı doğrusal değerlendirme** fikri tam da bu: Farklı zaman ölçeklerinde bilgi veren öznitelikleri toplamak. Ağırlıklar (1, 10, 100, 3) elle seçildi. Bölüm 22'de bu ağırlıkların kendi kendine oynayarak nasıl **öğrenilebileceğini** göreceğiz.
