# Bölüm 14 — Quiz

Cevaplara bakmadan önce kendin yanıtla. Cevaplar dosyanın sonunda.

---

**S1.** Birinci dereceden Markov varsayımı ve algılayıcı Markov varsayımı ne söyler?

**S2.** Şemsiye dünyasında P(R_1 | u_1) nedir?

A) ⟨0.5, 0.5⟩
B) ⟨0.9, 0.1⟩
C) ⟨0.818, 0.182⟩
D) ⟨0.883, 0.117⟩

**S3.** Filtrelemenin bir adımı hangi iki alt adımdan oluşur?

**S4.** Uzun vadeli tahminde (gözlem eklemeden) dağılıma ne olur?

A) Son gözleme göre sabit kalır
B) Durağan dağılıma yakınsar
C) Sürekli dalgalanır
D) Sıfıra gider

**S5.** P(R_1 | u_1, u_2) neden P(R_1 | u_1)'den büyüktür? Hangi algoritma bunu hesaplar?

**S6.** Viterbi algoritması ileri (filtreleme) algoritmasından hangi işlemle ayrılır?

A) Toplam yerine maksimum alır
B) Çarpım yerine toplam alır
C) Geri mesaj kullanır
D) Normalizasyon yapmaz, başka farkı yoktur

**S7.** S durumlu bir HMM'de bir filtreleme adımının zaman karmaşıklığı nedir?

**S8.** Kitaptaki tek boyutlu Kalman örneğinde (μ₀ = 0, σ₀ = 1.5, σx = 2, σz = 1, z₁ = 2.5) güncellenmiş dağılım yaklaşık nedir?

A) N(2.5, 1.0)
B) N(1.25, 3.25)
C) N(0.0, 6.25)
D) N(2.155, 0.862)

**S9.** Kalman güncellemesinde varyans dizisi hakkında şaşırtıcı olan nedir?

**S10.** Kitaptaki kuş–ağaç örneği Kalman filtresinin hangi sınırını gösterir? Çözüm önerileri nelerdir?

**S11.** DBN ile HMM arasındaki ilişki nedir? DBN neden tercih edilir?

**S12.** Parçacık filtresinde yeniden örnekleme adımı olmasaydı ne olurdu?

---

## Cevaplar

1. Birinci dereceden Markov: Şimdiki durum, geçmiş verildiğinde yalnızca bir önceki duruma bağlıdır: P(X_t | X_{0:t−1}) = P(X_t | X_{t−1}). Algılayıcı Markov: Gözlem yalnızca o anki duruma bağlıdır: P(E_t | X_{0:t}, E_{1:t−1}) = P(E_t | X_t).
2. **C.** α ⟨0.9 × 0.5, 0.2 × 0.5⟩ = α ⟨0.45, 0.1⟩.
3. **Tahmin:** Önceki dağılımı geçiş modeliyle ileri taşı. **Güncelleme:** Yeni gözlemin olabilirliğiyle çarp ve normalize et.
4. **B.** Karışma süresinden sonra tahmin, başlangıçtaki bilgiden bağımsız hâle gelir (şemsiye dünyasında ⟨0.5, 0.5⟩).
5. 2. gündeki şemsiye, hava ardışık günlerde benzer olma eğiliminde olduğu için 1. günde de yağmur yağdığını daha olası kılar (0.818 → 0.883). Yumuşatma: ileri–geri algoritması.
6. **A.** Aynı özyineleme, toplam yerine maksimumla; en iyi öncülleri gösteren işaretçiler de saklanır.
7. O(S²): Her yeni durum için bütün eski durumlar üzerinden toplam alınır.
8. **D.** Tahmin N(0, 6.25); güncelleme μ = 6.25 × 2.5 / 7.25 ≈ 2.155, σ² = 6.25 / 7.25 ≈ 0.862.
9. Gözlemlerden bağımsızdır: Önceden hesaplanabilir ve hızla sabit bir değere yakınsar.
10. Kalman filtresi tek bir Gauss (tek tepe) tahmin eder. Ağaca doğru uçan kuş için ortalama gövdenin üstüne düşer, oysa kuş ya sağa ya sola kaçacaktır (iki tepe). Çözümler: anahtarlamalı Kalman filtresi (birkaç Kalman filtresinin karışımı), parçacık filtresi. (Hafif doğrusal olmayanlık için genişletilmiş Kalman filtresi.)
11. Her HMM bir DBN'dir; her ayrık DBN, değişkenleri birleştirerek bir HMM'ye çevrilebilir. DBN, durumu değişkenlere ayırıp seyrekliği kullandığı için çok daha tıkızdır: O(d^{2n}) yerine O(n d^k) parametre.
12. Ağırlıklar zamanla birkaç parçacıkta toplanır (diğerlerinin ağırlığı sıfıra yaklaşır). Tahmin, pratikte çok az örneğe dayanır ve hata büyür. Bu, ardışık önem örneklemesidir (SIS).
