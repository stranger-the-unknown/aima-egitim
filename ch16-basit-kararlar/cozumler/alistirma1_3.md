# A1–A3 çözümleri

## A1 — Kestirme mi, ana yol mu?

1. `P(RESULT(kestirme) = zamanında) = Σ_s P(s) P(zamanında | s, kestirme) = 0.6 × 0.8 + 0.4 × 0.3 = 0.48 + 0.12 = 0.60`.
   - EU(kestirme) = 0.60 × 10 + 0.40 × 0 = **6**
   - EU(ana yol) = 1 × 5 = **5**
   - MEU kestirmeyi seçer.
2. p = P(kaza yok) için EU(kestirme) = 10 (0.8p + 0.3(1 − p)) = 10 (0.3 + 0.5p). Bu 5'ten büyükse kestirme: 0.3 + 0.5p > 0.5 ⇔ **p > 0.4**. P(kaza yok) 0.4'ün altına düşerse ana yol seçilir.

## A2 — Hangi aksiyom?

1. **Sıralanabilirlik:** Ajan iki seçenek arasında ya birini tercih etmeli ya da eşit görmeli.
2. **Tekdüzelik:** Daha çok sevdiği sonucu daha yüksek olasılıkla veren piyangoyu tercih etmeli.
3. **Ayrıştırılabilirlik:** İç içe piyango tek piyangoya indirgenir (0.5 + 0.5 × 0.5 = 0.75); "kumarın keyfi" bu aksiyomun dışında kalır. (Kitap: Keyif önemliyse "kumar oynadım" bilgisi durumun parçası yapılır.)
4. **İkame edilebilirlik:** Eşit görülen sonuçlar piyangoda birbirinin yerine konabilmeli.
5. **Geçişlilik:** Para pompası, A ≻ B ≻ C ≻ A gibi döngüsel tercihlerin sonucudur.

## A3 — Fayda ölçeği

1. EU(L) = 0.5 × 0 + 0.5 × 9 = **4.5** > U(b) = 4 → piyango seçilir.
2. - U′ = 2U + 3: EU′(L) = 0.5 × 3 + 0.5 × 21 = 12 > U′(b) = 11 → yine piyango. Pozitif afin dönüşüm her EU'yu aynı biçimde (2 × EU + 3) değiştirir, sıralama korunur.
   - U″ = √U: EU″(L) = 0.5 × 0 + 0.5 × 3 = 1.5 < U″(b) = 2 → **karar değişir**, kesin b seçilir.
   - √ tekdüze artan olduğu için sonuçların **sıralamasını** korur; belirsizlik olmasaydı karar değişmezdi. Ama piyangolar arasındaki tercih, faydaların **oranlarına** bağlıdır. √ eğriyi içbükey yaparak ajanı riskten kaçınan hâle getirdi.
