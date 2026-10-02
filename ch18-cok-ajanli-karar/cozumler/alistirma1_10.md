# A1–A10 çözümleri

Kodlu kısımlar: `python cozumler/alistirma_kod.py` (bölüm klasöründen).

---

## A1 — Tavuk oyunu

1. Baskın strateji yok: Karşı taraf kaçarsa dümdüz gitmek (+1 > 0), dümdüz giderse kaçmak (−1 > −10) iyidir. Saf Nash dengeleri: **(kaç, dümdüz)** ve **(dümdüz, kaç)**. Pareto en iyi: (kaç, kaç), (kaç, dümdüz), (dümdüz, kaç); yalnızca çarpışma Pareto en iyi değil.
2. Can'ın kaçma olasılığı q olsun. Ayşe kayıtsız: kaç → −(1 − q); dümdüz → q − 10(1 − q). Eşitlik: −1 + q = 11q − 10 ⇒ **q = 9/10**. Simetriden Ayşe de 9/10 kaçar. Çarpışma olasılığı (1/10)² = **1/100**. Karma dengede iki sürücü de −1/10 alır: (kaç, kaç)'tan kötü.

## A2 — Baskın denge ve serpiştirme

1. Baskın strateji, diğerlerinin **her** stratejisine en iyi tepkidir; özel olarak dengedeki stratejilerine de. O hâlde kimse tek başına sapıp kazanamaz: Nash dengesi. Tersi yanlış: Koordinasyon oyununun iki Nash dengesi var ama baskın strateji yok.
2. 2 + 3 = 5 yuvadan A'nın 2 eylemine yer seç: C(5, 2) = **10**. Genel: (n₁ + … + n_k)! / (n₁! ⋯ n_k!). İki eylemli iki plan için kitaptaki 6.
3. A fileye gider, B bekler: Kimse topa vurmaz. "Kendi tarafında kal" Plan 1'i eler (A sağ dip çizgiye geçiyor), ikisi de Plan 2'yi seçer.

## A3 — Üç parmaklı Morra

1. | | O: 1 | O: 2 | O: 3 |
   |---|---|---|---|
   | E: 1 | +2 | −3 | +4 |
   | E: 2 | −3 | +4 | −5 |
   | E: 3 | +4 | −5 | +6 |
2. Önce E açıklarsa: satır minimumları −3, −5, −5 → **−3**. Önce O açıklarsa: sütun maksimumları 4, 4, 6 → **+4**. −3 ≤ U ≤ 4.
3. LP: değer **0**; bir denge stratejisi (1/4, 1/2, 1/4) (simetrik matris, iki oyuncu için de). Kontrol: O'nun 1'ine karşı 2/4 − 3/2 + 4/4 = 0; 2'sine karşı −3/4 + 2 − 5/4 = 0; 3'üne karşı 1 − 5/2 + 3/2 = 0. Başka denge stratejileri de vardır; değer her zaman 0'dır.

## A4 — Ne zaman biteceği bilinmeyen oyun

1. Sus: −1 − δ − δ² − … = **−1/(1 − δ)**. Tanık ol: Bu tur 0, sonra karşı taraf sonsuza dek tanık olur, en iyi tepki de tanık: 0 + δ(−5)/(1 − δ) = **−5δ/(1 − δ)**.
2. −1/(1 − δ) ≥ −5δ/(1 − δ) ⇔ 1 ≤ 5δ ⇔ **δ ≥ 0.2**. (Kod: δ = 0.1'de denge değil, 0.2'de eşit, üstünde denge.)
3. Sabit 100 turda son tur bilindiği için geriye tümevarım her turu tanıklığa çözer. Belirsiz son "son turu" ortadan kaldırır: Her turda gelecekte cezalandırılma olasılığı vardır.

## A5 — Basit poker

1. kr: as varken bekle, papaz varken artır. fc: as varken çekil, papaz varken gör.
   - AA (1/6): Oyuncu 1 bekler, eşit kart → 0.
   - AK (1/3): Bekler, as papazı yener → +1.
   - KA (1/3): Artırır; oyuncu 2'de as → çekilir → +1.
   - KK (1/6): Artırır; oyuncu 2'de papaz → görür → eşit → 0.
   - Toplam: 1/3 + 1/3 = **2/3**.
2. Dengeler (rk, cf) ve (kk, cf), değer 0. cf: "As varsa gör (kaybetmezsin), papaz varsa çekil (görürsen ya berabere kalırsın ya kaybedersin)." Bu tepki karşısında oyuncu 1'in blöfü (papazla artırmak) ödüllendirilmez.
3. Yalnızca rr satırında oyuncu 2'nin en iyi tepkisi yine **cf**: −1/6. Oyuncu 1 0 yerine **−1/6** alır; artırmasından bilgi sızmasa bile esnekliğini kaybetmenin bedeli.

## A6 — Ataş oyununun dili

1. 1 + 1'in Harriet'e getirisi 1 + orta (Robbie orta + orta ile cevap verirse), 2 ataşınki 92θ, 2 zımbanınki 92(1 − θ). 1 + 1 ⇔ θ ∈ [1 − (1 + orta)/92, (1 + orta)/92].
   - 50 + 50: [41/92, 51/92] = **[0.446, 0.554]** (kitap).
   - 45 + 45: (1 + 45)/92 = 1/2 → aralık tek bir nokta: Pratikte **hiç**.
   - 40 + 40: 41/92 < 1/2 → aralık **boş**.
2. Robbie için orta + orta, hiçbir θ'da max(90θ, 90(1 − θ)) ≥ 45'ten iyi değilse (orta ≤ 45) gereksizdir. Harriet'in "kararsızım" sinyalinin anlamı kalmaz ve dil iki kelimeye iner: ataş / zımba. Robbie yine θ'nın hangi yarıda olduğunu öğrenir ve elindeki seçeneklerle en iyisini yapar; bu durumda bir şey kaybedilmez. 50 + 50 ise θ yarıya yakınken 90'lık seçeneklerden daha iyidir; onu kullanabilmek için üçüncü bir "kelime" gerekir. Dengedeki dil, Robbie'nin elindeki seçeneklere göre biçimlenir.

## A7 — Eldiven oyunu

1. ν = 1: {1, 2}, {1, 3}, {1, 2, 3}; diğer bütün koalisyonlar 0. Süperadditif.
2. Altı sıralamada oyuncu 1'in marjinal katkısı: ilk sıradaysa 0, değilse 1 → 4/6 = **2/3**. Oyuncu 2 ve 3: her biri **1/6**.
3. Çekirdek: x₁ + x₂ ≥ 1 ve x₁ + x₃ ≥ 1 ve toplam 1 ⇒ x₃ ≤ 0 ve x₂ ≤ 0 ⇒ **yalnızca (1, 0, 0)**. Shapley çekirdekte **değil**: Oyuncu 1, 2 ve 3'ten birini her zaman diğerine karşı kullanabilir (sağ eldiven bolluğu). Çekirdek pazar gücünü yansıtır; Shapley ise "katkıya göre adalet"i.

## A8 — VCG

1. Kazananlar 30 ve 25. 30 olmasaydı 25 ve 10 kazanırdı; diğerlerinin toplamı 25 yerine 35 → vergi **10**. Aynısı 25 için: **10**.
2. Kod, her teklifçi için 0–40 arası her teklifi dener: Hiçbiri net faydayı dürüst teklifin üstüne çıkarmaz. Kazananlar için vergi kendi tekliflerine bağlı değildir; kaybedenler 10'un üstüne teklif verirse değerlerinden fazla öderler.
3. Tek mal için VCG tam olarak Vickrey açık artırmasıdır: Kazanan, olmasaydı kazanacak olanın değerini, yani ikinci en yüksek teklifi öder. k özdeş malda herkes (k + 1). en yüksek teklifi öder.

## A9 — Hangi kural, hangi kazanan?

1. Çoğulluk: A (4 birinci tercih). Anında ikinci tur: C elenir (2), oyları B'ye gider → B 5 – A 4 → **B**. Borda: A 17, B 17, **C 20**. Condorcet: C, A'yı 5–4 ve B'yi 6–3 yener → **C**. Dört kural, üç farklı kazanan.
2. Evet. C'ciler (C ≻ B ≻ A) çoğullukta B'ye oy verirse B 5 oyla kazanır; onlar için A'dan iyidir. Bu, **Gibbard–Satterthwaite** teoreminin bir örneğidir: Çoğulluk manipüle edilebilir.

## A10 — Sabır

1. γ₁ = 0.9, γ₂ = 0.8:
   - 1 tur: A1 hepsini alır → **1**.
   - 2 tur: A2 ikinci turda hepsini alacak (değeri 0.8) → A1 (0.2, 0.8) önerir → **0.2**.
   - 3 tur: Üçüncü turda A1 hepsini alır; ikinci turda A2, A1'e 0.9 vermek zorunda, kendine 0.1 kalır; ilk turda A1, A2'ye 0.8 × 0.1 = 0.08 verir → **0.92**.
   - Tur sayısı arttıkça pay salınarak **(1 − γ₂)/(1 − γ₁γ₂) = 0.2/0.28 ≈ 0.714**'e yakınsar.
2. (1 − γ)/(1 − γ²) = **1/(1 + γ)**. γ = 0.5'te 2/3, γ = 0.9'da 0.526, γ → 1 iken **1/2**: İlk teklif verme üstünlüğü, oyuncular sabırlandıkça kaybolur.
