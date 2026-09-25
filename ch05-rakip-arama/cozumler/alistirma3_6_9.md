# Çözümler — A3, A4, A5, A6, A9

## A3 — İki optimal XOX ajanı

1. Oyun **berabere** biter. XOX'un minimax değeri 0'dır: Kusursuz oynayan iki oyuncudan hiçbiri kazanmayı zorlayamaz. Bu yüzden iki optimal ajanın berabere kalması beklenen sonuçtur.
2. İlk hamlede saf minimax **549.945** düğüm inceler (ağacın kök hariç tamamı), alfa-beta ise **30.709**. Yaklaşık **18 kat** daha az. Sonraki hamlelerde ağaç küçüldükçe oran da küçülür.

## A4 — Pozisyondan hamle

Tahta `X . O / . X . / O . .` (X: 0 ve 4, O: 2 ve 6).

1. X ve O ikişer taş oynamış, sıra **X**'te. Normal minimax **1. hücreyi**, `--hizli-kazan` **8. hücreyi** önerir.
2. 1. hücre yanlış değildir. X 1'e oynarsa hem 7'yi (1-4-7) hem 8'i (0-4-8) tehdit eder; O ikisini birden kapatamaz ve X bir sonraki hamlede kazanır. Minimax değeri iki hamle için de +1'dir. Saf minimax **ne zaman** kazanıldığını umursamaz ve eşitlik durumunda listede ilk bulduğu hamleyi seçer.
3. `--hizli-kazan` kazancı 1 + boş kare sayısıyla ölçekler: Erken kazanç daha çok puan getirir. Artık minimax değeri "kazanıyor muyum?" değil, "ne kadar çabuk kazanıyorum (ya da ne kadar geç kaybediyorum)?" sorusunun cevabıdır. Kazanma/kaybetme ayrımı değişmez, yalnızca kazanan hamleler arasındaki tercih değişir.

## A5 — Ufuk etkisi

Arama 4 katta kesilirse, 5. katta gerçekleşecek bir taş kaybı "görünmez". Daha kötüsü, program kaçınılmaz kaybı birkaç hamle **erteleyen** hamleler (anlamsız şahlar, feda edilen piyonlar) bulursa, bu hamleleri "kaybı önledim" diye seçer. Sonuç: kayıp yine gerçekleşir ve üstüne erteleme için verilen piyonlar da gider.

- **Sessizlik araması:** Kesme noktasında konum "hareketliyse" (ör. taş alışverişi sürüyorsa) aramayı yalnızca alma hamleleriyle uzatır, sakin bir konuma kadar devam eder. Değerlendirme böylece yalnızca güvenilir konumlara uygulanır.
- **Tekil genişletme:** Bir hamle açıkça diğerlerinden iyiyse (ör. tek kurtarıcı hamle), bu hamle kesme sınırının ötesinde de izlenir. Bu hamleler az olduğu için maliyet düşüktür.

Aynı olgunun XOX'taki küçük bir örneği A7'de: Tek derinlikte arayan O ajanı, rakibin çift tehdidini göremediği için kaybedebilir.

## A6 — Elle alfa-beta

1. B = min(5, 7, 3) = **3**, C = min(4, 8, 1) = **1**, D = min(6, 2, 9) = **2**, A = max = **3**.
2. Soldan sağa:
   - B: 5, 7, 3 → B = 3; kökte α = 3.
   - C: 4 (C ≤ 4, hâlâ > α), 8 (C ≤ 4), 1 (C = 1). C'nin **üç yaprağına da** bakılır; en küçük değer sonda geldiği için budama olmaz.
   - D: 6 (D ≤ 6), 2 → D ≤ 2 ≤ α = 3 → **9 budanır**.
   - 9 yapraktan 8'ine bakılır.
3. En iyi sıralama: Önce en iyi MIN düğümü (B), sonra diğer MIN düğümlerinde en küçük yaprak önce. Yani B: (5, 7, 3 herhangi bir sırayla), C: 1 önce, D: 2 önce. B'nin 3 yaprağının hepsine bakılmalı; C'de 1 görülünce C ≤ 1 < 3 olduğu için kalanlar, D'de de 2 görülünce kalanlar budanır. Toplam **3 + 1 + 1 = 5** yaprak. Knuth–Moore formülü (b = 3, d = 2): 3¹ + 3¹ − 1 = **5** ✓

## A9 — Beklenti-minimaks

1. a1 = 0,5·8 + 0,5·4 = **6**; a2 = (1/6)·30 + (5/6)·3 = 5 + 2,5 = **7,5** → **a2**.
2. 3v + 1: a1 = 0,5·25 + 0,5·13 = 19; a2 = (1/6)·91 + (5/6)·10 = 23,5 → yine **a2**. Pozitif doğrusal dönüşüm beklenen değerlerin sırasını korur, çünkü E[3v + 1] = 3E[v] + 1.
3. √v: a1 = 0,5·√8 + 0,5·√4 ≈ **2,414**; a2 = (1/6)·√30 + (5/6)·√3 ≈ **2,356** → **a1**. Karar değişti.

   Karekök **içbükey** bir dönüşümdür: Büyük değerleri "bastırır". a2'nin çekiciliği, düşük olasılıklı büyük kazançtan (30) geliyordu; karekök bu kazancı küçültünce güvenli a1 öne geçti. Bu dönüşüm **riskten kaçınan** bir oyuncuyu temsil eder. Bölüm 16'da paranın faydası konusunda tam olarak bu fikir işlenir. Ders: Şanslı oyunlarda EVAL'ın ölçeği bir "kişilik" seçimidir. Kazanma olasılığıyla doğrusal olmayan bir EVAL, farkında olmadan riskten kaçınan ya da risk seven bir oyuncu üretir.
