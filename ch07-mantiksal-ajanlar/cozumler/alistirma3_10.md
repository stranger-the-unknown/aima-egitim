# Çözümler — A3–A10

Kodla doğrulanabilen kısımlar: `alistirma4_9_kod.py`.

## A3 — "Bilinmiyor" yanıtı

1. KB = {Yağmur ⇒ IslakZemin, Bulut ∨ Yağmur, Yağmur}. KB'nin doğru olduğu modellerde Yağmur = D ve IslakZemin = D olmak zorundadır. Bulut ∨ Yağmur zaten Yağmur sayesinde doğrudur, bu yüzden Bulut'a hiçbir kısıt kalmaz. İki model vardır: (Bulut = D) ve (Bulut = Y). Bulut birinde doğru, birinde yanlıştır. Ne Bulut ne de ¬Bulut gerektirilir: **bilinmiyor**.
2. **"Bulut"** eklenirse "evet" olur. **"Yagmur => ~Bulut"** (ya da doğrudan "~Bulut") eklenirse "hayır" olur.
3. P = Y, Q = D modelinde P ⇒ Q doğrudur (öncül yanlış), Q ⇒ P ise yanlıştır (öncül doğru, sonuç yanlış). Tek bir model eşdeğerliği bozmaya yeter.

## A4 — CNF dönüşümü

1. ⇒ eliminasyonu: ¬(A ∨ B) ∨ (C ∧ ¬D)
2. De Morgan: (¬A ∧ ¬B) ∨ (C ∧ ¬D)
3. Dağılma: (¬A ∨ C) ∧ (¬A ∨ ¬D) ∧ (¬B ∨ C) ∧ (¬B ∨ ¬D)

`onerme.cnf` aynı dört tümceyi verir: (C ∨ ¬A) ∧ (¬A ∨ ¬D) ∧ (C ∨ ¬B) ∧ (¬B ∨ ¬D).

## A5 — Model sayısı

1. 2⁵ = **32** model.
2. R1–R5'te 7 sembol var (B11, B21, P11, P12, P21, P22, P31): 2⁷ = **128** model. KB bunların **3**'ünde doğrudur.
3. 16 kare × 4 sembol = **64** sembol → 2⁶⁴ ≈ 1,8 × 10¹⁹ model. Saniyede bir milyar model denense bile ~585 yıl sürer. Doğruluk tablosu küçük KB'ler dışında kullanışsızdır. DPLL ise aynı soruya birkaç düzine çağrıyla karar verir (bkz. A8).

## A6 — Elle çözümleme

Gereken tümceler: R3'ün CNF'sinden (P11 ∨ P22 ∨ P31 ∨ ¬B21), R1'den ¬P11, R5'ten B21. Sorgunun değili ¬(P22 ∨ P31), yani iki birim tümce: ¬P22 ve ¬P31.

| Adım | Tümceler | Çözümleyici |
|---|---|---|
| 1 | (P11 ∨ P22 ∨ P31 ∨ ¬B21) + (¬P22) | P11 ∨ P31 ∨ ¬B21 |
| 2 | (P11 ∨ P31 ∨ ¬B21) + (¬P11) | P31 ∨ ¬B21 |
| 3 | (P31 ∨ ¬B21) + (¬P31) | ¬B21 |
| 4 | (¬B21) + (B21) | **□** |

Boş tümce türetildiği için KB ⊨ P22 ∨ P31. Kod aynı dört adımlık kanıtı buluyor. Ama arama sırasında 185 çözümleyici üretiyor: Çözümleme hangi tümcelerin önemli olduğunu önceden bilmez.

## A7 — İleri ve geri zincirleme

| KB | İleri zincirleme (çıkarılan sembol) | Geri zincirleme (bakılan alt hedef) |
|---|---|---|
| Özgün | 6 | 14 |
| + 10 ilgisiz kural | 10 | 14 |

- İleri zincirleme veri güdümlüdür: A doğru olduğu için A ⇒ X1 ⇒ X2 ⇒ … zincirini de ateşler. Burada Q bulununca durduğu için dört ilgisiz sembol çıkardı. Sorgu hiç bulunmasaydı on ilgisiz sembolün hepsini çıkarırdı.
- Geri zincirleme hedeften başladığı için ilgisiz kurallara hiç dokunmaz; iş aynı kalır.
- **İleri zincirleme şu durumlarda tercih edilir:** Belirli bir sorgu yoksa, yeni algılar geldikçe tüm sonuçlar güncel tutulmak isteniyorsa (ör. ajan her algıdan sonra "hangi kareler güvenli?" diye merak ediyorsa) ya da birçok sorgu aynı ara sonuçlara dayanıyorsa.

## A8 — Doğruluk tablosu ve DPLL

1. **64** sembol (16 kare × P, W, B, S). Doğruluk tablosu 2⁶⁴ ≈ 1,8 × 10¹⁹ model dener.
2. DPLL, KB ⊨ W13'e (yani KB ∧ ¬W13'ün karşılanamaz olduğuna) **21** çağrıda karar veriyor.
3. Birim tümce ve saf sembol sezgiselleri kapatılınca **179** çağrı. Birim yayılım burada çok güçlüdür: Algılar birim tümcedir (¬B11, S12 …) ve biconditional kurallar üzerinden zincirleme olarak birçok sembolü hemen belirler.

## A9 — WalkSAT'ta p

| p | Başarı (20) | Medyan çevirme |
|---|---|---|
| 0,0 | 2 | 5.000 (sınır) |
| 0,2 | 18 | 160 |
| 0,5 | 20 | 72 |
| 0,8 | 20 | 135 |
| 1,0 | 20 | 586 |

- **p = 0** (hep açgözlü): Yerel minimumlarda takılır. Yanlış tümce sayısını azaltmayan bir hamle hiç yapılmaz; aynı birkaç sembolü ileri geri çevirir.
- **p = 1** (hep rastgele): Rastgele yürüyüştür. Sonunda bulur ama yavaştır.
- **p ≈ 0,5** iyi bir dengedir. Bu, Bölüm 4'teki tavlama ve Bölüm 6'daki min-çatışma gürültüsüyle aynı keşif–sömürü ödünleşimidir.

## A10 — Ardıl durum aksiyomları

1. HaveArrow^{t+1} ⇔ (HaveArrow^t ∧ ¬Shoot^t)

   Oku olan ve atmayan ajan onu tutmaya devam eder. Oku geri kazandıran bir eylem yoktur, bu yüzden "doğru yapan eylem" kısmı boştur.
2. Yardımcı ifade: VurulurW^t ⇔ Shoot^t ∧ HaveArrow^t ∧ (wumpus ajanın baktığı doğrultuda). Buna göre:

   WumpusAlive^{t+1} ⇔ (WumpusAlive^t ∧ ¬VurulurW^t)

   Wumpus'u diriltecek bir eylem olmadığı için yine yalnızca "değişmezlik" kısmı vardır.
3. L^{t+1}_{1,1} ⇔ (L^t_{1,1} ∧ (¬Forward^t ∨ Bump^{t+1})) ∨ (L^t_{2,1} ∧ FacingWest^t ∧ Forward^t) ∨ (L^t_{1,2} ∧ FacingSouth^t ∧ Forward^t)

   Ajan [1,1]'de kalır, eğer oradaysa ve ya ileri gitmediyse ya da duvara çarptıysa; ya da [1,1]'e komşu bir kareden ona doğru ilerlediyse. [1,1]'de doğuya bakarken ileri giderse (çarpma yoksa) L^{t+1}_{1,1} yanlış olur, L^{t+1}_{2,1} doğru.
4. Etki + çerçeve aksiyomlarıyla her (eylem, akışkan) çifti için bir aksiyom gerekir: **O(m·n)**. Ardıl durum aksiyomlarıyla her akışkan için bir tane: **O(n)** (her biri, o akışkanı etkileyen eylemleri listeler). Çoğu eylem çoğu akışkanı etkilemediği için toplam boyut çok daha küçüktür.
