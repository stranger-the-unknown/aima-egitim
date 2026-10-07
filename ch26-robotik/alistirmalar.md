# Bölüm 26 — Alıştırmalar

Sorular özgündür. Çözümler `cozumler/` klasöründe; önce kendin dene.

Zorluk: ★ kolay · ★★ orta · ★★★ zor

---

## A1 — Hareket ve işaret modeli ★

1. Robot (x, y, θ) = (2, 1, 30°) pozunda; v = 1 m/s, ω = 0.2 rad/s, Δt = 1 s. Kinematik modelle X̂ₜ₊₁'i hesapla.
2. Robot (0, 0, 0°)'da, işaret (3, 4)'te. Beklenen uzaklık ve yön açısı nedir? Robot 90° dönmüş olsaydı?

## A2 — Uzaklık taraması olabilirliği ★★

Dört ışınlık ölçüm z = (2.0, 1.0, 3.0, 1.0); σ = 0.2. A pozundan beklenen tarama (2.1, 0.9, 3.0, 1.2), B pozundan (1.0, 2.0, 3.5, 0.5).
1. İki pozun log-olabilirliklerini (sabit hariç) ve olabilirlik oranını hesapla.
2. Işın hatalarının bağımsız olduğu varsayımı ne zaman bozulur, sonucu ne olur?

## A3 — MCL'de tepe kaybı (kod) ★★

`mcl_deneyi()`'ni 8 tohumla (a) 1000 parçacık, (b) 5000 parçacık, (c) 5000 parçacık ve tamamen düzgün başlangıç yönüyle çalıştır. 8. adımda iki tepe de yaşıyor mu? Sonunda doğru konum bulunuyor mu? Sonuçları açıkla.

## A4 — EKF ve doğrusallaştırma (kod) ★★

1. `ekf_deneyi()`'ni işaretle ve işaret hiç görünmezken (gorus = 0) karşılaştır.
2. `dogrusallastirma()` ile σ = 0.1, 0.5, 1.0 için Taylor yaklaşımının ortalama ve standart sapma hatalarını karşılaştır. EKF ne zaman güvenilirdir?

## A5 — Konfigürasyon uzayı (kod) ★★

1. `UCGEN` robotunun ve (4, 2)–(6, 3) dikdörtgeninin C-uzayı engelinin köşelerini ve alanını bul. Robot 1 × 1'lik bir kare olsaydı?
2. Şu robotların C-uzayı kaç boyutludur: dönebilen üçgen, dönebilen ve büyüyüp küçülebilen üçgen, iki eklemli kol, her bacağında iki motor olan altı bacaklı robot (gövdenin konumu ve yönelimi dahil)?

## A6 — Ters kinematik ★

L₁ = L₂ = 1 olan iki eklemli kol için:
1. El (1, 1)'e ulaşmalı. Bütün (θ_omuz, θ_dirsek) çözümlerini bul ve ileri kinematikle doğrula.
2. Kolun ulaşabildiği noktalar kümesi nedir? (2, 0), (2.5, 0) ve (0, 0) için kaç çözüm vardır?

## A7 — Planlayıcıları karşılaştır (kod) ★★

İki dikdörtgenli dünyada görünürlük çizgesi, 0.25 m'lik ızgara (yalnızca tamamen serbest hücreler), ızgara + kısaltma, k-PRM (M = 30) ve çift yönlü RRT (kısaltmalı ve kısaltmasız) yol uzunluklarını karşılaştır. Hangisi neden en kısa? Diğerlerinin üstünlükleri ne?

## A8 — Yörünge optimizasyonu (kod) ★★★

1. Euler–Lagrange denklemini kullanarak J_eff = ∫ ½‖τ̇‖² ds'nin gradyanının −τ̈ olduğunu ve engel yokken en iyi yolun doğru parçası olduğunu göster.
2. λ = 20, 200, 1000, 3000 için engellere en küçük uzaklığı ve yol uzunluğunu karşılaştır.
3. Optimizasyonu iki engelin de üstünden geçen kavisli bir yoldan başlat. Ne buldun? Neden?

## A9 — Denetçi kazançları (kod) ★★

1. K_P = 0.3 iken K_D = 0.1, 0.8, 3.0 için aşımı ve %2 bandına oturma süresini bul. Sönüm oranı ζ = K_D / (2√K_P) ile yorumla.
2. LQR'de Q = diag(1, 0) sabitken R = 0.1, 1, 10 için K'yi hesapla. R'nin anlamı nedir?

## A10 — İnsan modeli (kod) ★★★

1. Amaç çıkarımını β = 0.1, 1, 5 ile tekrarla (P(u | x, J) ∝ exp(−βQ)). İki adım sonra P(pencere) nasıl değişiyor? β'nın anlamı nedir; yanlış β seçmenin riskleri neler?
2. Davranış klonlamayı, uzmanın gürültülü bir ortamda sürdüğü (σ = 0.05) gösterimlerle tekrarla. Sonuç neden değişti? Bu DAGGER'ı gereksiz kılar mı?
