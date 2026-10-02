# Çözümler — A3, A4, A5, A6, A8

## A3 — Türkiye haritası

1. **3 renkle çözüm yok**, 4 renkle var (ör. Marmara K, Ege Y, Akdeniz K, İç Anadolu M, Karadeniz Y, Doğu Anadolu S, Güneydoğu Y).
2. **Elle kanıt:** İç Anadolu (İ), Akdeniz (A) ve Doğu Anadolu (D) karşılıklı komşudur, bu yüzden 3 farklı renk alırlar; bunlara 1, 2, 3 diyelim.
   - Güneydoğu, A (2) ve D'ye (3) komşudur → **1**.
   - Karadeniz, İ (1) ve D'ye (3) komşudur → **2**.
   - Marmara, İ (1) ve Karadeniz'e (2) komşudur → **3**.
   - Ege; Marmara (3), İ (1) ve A'ya (2) komşudur → **renk kalmadı**. ∎

   Kanıtın kilit bağı **Akdeniz–Doğu Anadolu** komşuluğudur (Kahramanmaraş–Malatya). Bu kenar olmasaydı harita 3 renkle boyanabilirdi. Deponun ilk sürümü tam da bu kenarı atlamış ve gerçekte olmayan bir İç Anadolu–Güneydoğu kenarı eklemişti; bu yüzden 3 renkle "çözüm" buluyordu.
3. 3 renkle, "çözüm yok" sonucuna en az atamayla **MRV** (ileri kontrollü ya da kontrolsüz) ulaştı: 27 atama (sıralı düzende 33). Harita küçük olduğu için fark küçük. Asıl etki büyük problemlerde görülür (bkz. N-vezir tablosu).

## A4 — N-vezir CSP

1. **Değişken:** her sütun. **Alan:** vezirin satırı (0 … n − 1). **Kısıt:** her sütun çifti için farklı satır ve farklı çapraz (|rᵢ − rⱼ| ≠ |i − j|).
2. **MRV.** n = 20'de sıralı düzen (ileri kontrolle bile) 145.151 atama yaparken MRV + ileri kontrol 145 atamada bitiriyor. İleri kontrol tek başına yalnızca ~%25 kazandırıyor. Çünkü asıl kazanç, "seçeneği en az kalan sütunu önce ele al" kuralının çıkmazları erken yakalamasından geliyor. İleri kontrol ise MRV'nin ihtiyaç duyduğu bilgiyi (kalan değer sayılarını) ucuza sağlıyor.
3. Geri izleme **sistematik ve tamdır**: Çözüm varsa bulur, yoksa (n = 2, 3) bunu kanıtlar. Tepe tırmanma ve min-çatışma ise yereldir: Çok hızlı olabilirler ama çözüm bulacaklarını garanti etmezler ve çözüm olmadığını asla kanıtlayamazlar.

## A5 — İleri kontrol ile AC-3

İleri kontrol yalnızca **atanan değişkenin doğrudan komşularına** bakar ve silme işlemini zincirleme yaymaz. Senaryo: A–B–C zinciri, üçü de {1, 2} alanlı ve kısıtlar "komşular farklı". Ayrıca bir de A–C kenarı var (üçgen). A = 1 atanınca ileri kontrol B'den ve C'den 1'i siler: B = {2}, C = {2}. İkisi de tek değere düştü ve B–C komşu olduğu için çelişkili, ama ileri kontrol bunu görmez. AC-3 ise (B, C) yayını da kontrol eder, B'nin 2'sinin C'de destekçisi olmadığını görür ve B'nin alanını boşaltır: Tutarsızlık **hemen** yakalanır. MAC da aynı şeyi arama sırasında yapar.

## A6 — Elle AC-3

1. İleri kontrolle: WA = kırmızı → NT {Y, M}, SA {Y, M}. Q = yeşil → NT **{M}**, SA **{M}**, NSW {K, M}.
2. AC-3 (başlangıçta tüm yaylar kuyrukta):
   - (SA, NT): SA'nın mavisinin NT'de destekçisi yok (NT yalnızca mavi) → **SA = ∅** → tutarsız.
   - Yayların işlenme sırasına göre önce NT'nin boşalması da mümkündür. Her durumda sonuç aynıdır: **tutarsız**.
   - Kodla doğrulama (`kisit.ac3`): `False`, SA = [].
3. MAC bu çelişkiyi **Q = yeşil** atamasında yakalar ve hemen geri döner. İleri kontrol ise NT = mavi atar, SA'yı atamaya çalışınca başarısız olur ve geri döner. Burada tasarruf en az bir-iki atamadır. Büyük problemlerde ise erken yakalanan her çelişki, altındaki bütün alt ağacı budadığı için kazanç üstel olabilir.

## A8 — Kriptaritmetik

1. **7 çözüm** (734 + 734 = 1468, 765 + 765 = 1530, 836 + 836 = 1672, 846 + 846 = 1692, 867 + 867 = 1734, 928 + 928 = 1856, 938 + 938 = 1876). F, binler basamağının eldesidir. İki üç basamaklı sayının toplamı 1998'i geçemez, yani elde en fazla 1'dir. Baştaki harf 0 olamayacağı için **F = 1**.
2. MONEY'nin en soldaki M'si, iki dört basamaklı sayının toplamının eldesidir. En fazla 9999 + 9999 = 19998 olduğu için M ≤ 1, baştaki harf olduğu için de M ≠ 0 → **M = 1**. Bu tek bir sütun kısıtıdır (C₄ = M), arama gerektirmez. İyi bir kısıt yayıcı bunu en başta bulur.
3. TWO + TWO = FOUR için sütun sütun arama 1.002 kısmi atama dener; kaba kuvvet ise 151.200 permütasyonu. Bu yaklaşık **150 kat** daha azdır. SEND + MORE = MONEY'de oran 6.878'e karşı 1.814.400, yani ~264 kat. Kısıtları **erken** (her sütun dolunca) kontrol etmek, geri izlemeyi kaba kuvvetten ayıran şeydir.
