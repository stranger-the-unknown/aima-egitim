# Bölüm 6 — Quiz (5 soru)

Cevaplar dosyanın sonunda.

---

**S1.** CSP’nin üç temel bileşeni nedir?

**S2.** Backtracking’te “geri dönüş” ne zaman olur?

**S3.** MRV neyi seçer? LCV neyi tercih eder?

**S4.** İleriye kontrol (forward checking) ne yapar?

**S5.** Yay tutarlılığı (arc consistency) bir kenar \((X_i,X_j)\) için ne ister?

---

## Cevaplar

**S1.** Değişkenler, domainler, kısıtlar.

**S2.** Mevcut değişken için hiçbir tutarlı değer kalmayınca bir önceki atamaya dönülür.

**S3.** MRV: kalan değeri en az olan değişken. LCV: komşuları en az kısıtlayan değer.

**S4.** Yeni atamadan etkilenen atanmamış komşuların domainlerini küçültür; boşalırsa hemen başarısız sayar.

**S5.** \(X_i\)’nin her değeri için \(X_j\)’de en az bir uyumlu değer bulunmasını.
