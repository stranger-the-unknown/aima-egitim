# Bölüm 26 — Robotik

> AIMA 4. baskı, Bölüm 26 · *Robotics*

## Öğrenme hedefleri

1. Robotik probleminin neden sürekli, kısmen gözlenebilir, stokastik ve çok etmenli olduğunu açıklamak.
2. Hareket ve algılayıcı modelleriyle Monte Carlo lokalizasyonu ve EKF uygulamak.
3. Konfigürasyon uzayını, ileri/ters kinematiği ve C-uzayı engellerini hesaplamak.
4. Görünürlük çizgesi, hücre ayrıştırma, PRM, RRT ve yörünge optimizasyonunu karşılaştırmak.
5. P, PD, PID ve LQR denetçilerini benzetmek.
6. İnsan davranışını amaç çıkarımıyla tahmin etmek; taklit öğrenmesinin sorunlarını açıklamak.

## Çalışma sırası

1. Kitapta Bölüm 26'yı oku.
2. [`notlar.md`](notlar.md)
3. Örnekleri çalıştır (yalnızca numpy gerekir).
4. [`alistirmalar.md`](alistirmalar.md) → [`cozumler/`](cozumler/)
5. [`quiz.md`](quiz.md)

## Dosyalar

| Dosya | İçerik |
|---|---|
| `ornekler/robot_lokalizasyon.py` | Kinematik hareket modeli, işaret ve uzaklık taraması modelleri, ışın izleme, Monte Carlo lokalizasyonu (simetrik koridor), EKF, doğrusallaştırma |
| `ornekler/hareket_planlama.py` | C-uzayı engeli (Minkowski), iki eklemli kol kinematiği ve C-uzayı, ızgara araması, görünürlük çizgesi, k-PRM, çift yönlü RRT + kısaltma, yörünge optimizasyonu |
| `ornekler/kontrol.py` | P, PD, PID denetçileri, LQR (Riccati) |
| `ornekler/insan_robot.py` | Amaç çıkarımı (26.8–26.9), davranış klonlama ve DAGGER, bacak AFSM'si, üçlü yürüyüşte statik kararlılık |
| `alistirmalar.md` | 10 alıştırma |
| `cozumler/` | Tüm çözümler (A3, A4, A5, A7–A10 kod) |
| `quiz.md` | 12 soru + cevaplar |

## Kitapla doğrulama

`tests/test_ch26_robotik.py`:

| Değer | Kitap | Kod |
|---|---|---|
| Kinematik model | X̂ = X + (vΔt cos θ, vΔt sin θ, ωΔt) | ✔ |
| İşaret modeli | uzaklık √(Δx² + Δy²), yön arctan(Δy/Δx) − θ | ✔ |
| MCL | Simetrik ortamda iki tepeli, ayırt edici yer görülünce tek tepeli inanç (Şekil 26.7) | ✔ |
| EKF | İşaret görülünce belirsizlik azalır, sonra yeniden artar (Şekil 26.9) | ✔ |
| Doğrusallaştırma | Ortalama izdüşümü f(μ), kovaryans yanlış olabilir (Şekil 26.8) | ✔ |
| C-uzayı engeli | Dönmeyen üçgen + dikdörtgen → beş kenarlı çokgen (Şekil 26.11) | ✔ |
| Ters kinematik | φ(IK(x)) = x | ✔ |
| Görünürlük çizgesi | En kısa yol | ✔ diğer planlayıcılar daha uzun |
| J_eff | Engel yokken en iyi yol doğru parçası | ✔ |
| P denetçisi | Sürtünmesiz sistemde sonsuz salınım | ✔ |
| PD (K_P = 0.3, K_D = 0.8) | Salınımsız izleme; sistematik kuvvette kalıcı hata | ✔ |
| PID | Kalıcı hatayı giderir | ✔ |
| LQR | u = −Kx | ✔ çift integratörde K = [1, √2] |
| İnsan tahmini | P(u_H \| x, J_H) ∝ e^(−Q), b′ ∝ b P(u_H \| x, J_H) | ✔ |
| DAGGER | Öğrenilen politikanın durumlarında uzmandan etiket | ✔ |

Bizim seçimlerimiz: koridor haritası ve MCL'de "koridora paralel" önseli; iki dikdörtgenli dünya; nokta engelli yörünge optimizasyonunda yol integralindeki ‖dφ/ds‖ çarpanının atılması; şerit tutma örneği; bacak AFSM'sinde yükseklik artışı.
