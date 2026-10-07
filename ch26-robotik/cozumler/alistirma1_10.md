# A1–A10 çözümleri

Kodlu kısımlar: `python cozumler/alistirma_kod.py` (bölüm klasöründen).

---

## A1 — Hareket ve işaret modeli

1. x = 2 + 1 · cos 30° = **2.866**, y = 1 + 1 · sin 30° = **1.5**, θ = 0.524 + 0.2 = **0.724 rad** (≈ 41.5°). Gerçek robot için bu ortalamadır; dağılım N(X̂, Σx).
2. Uzaklık √(3² + 4²) = **5**; yön açısı arctan(4/3) − 0 = **53.1°**. Robot 90° dönmüş olsaydı uzaklık aynı, yön açısı 53.1° − 90° = **−36.9°** (işaret robotun sağında).

## A2 — Uzaklık taraması olabilirliği

1. log P(z | A) = −(0.1² + 0.1² + 0 + 0.2²) / (2 · 0.2²) = −0.06 / 0.08 = **−0.75**.
   log P(z | B) = −(1² + 1² + 0.5² + 0.5²) / 0.08 = −2.5 / 0.08 = **−31.25**.
   Oran e^30.5 ≈ **1.8 × 10¹³**: A pozu çok daha olası (Şekil 26.5b'deki karşılaştırma gibi).
2. Komşu ışınlar aynı haritada olmayan nesneye (yürüyen bir insan, açık bırakılmış bir kapı) çarparsa hataları ilişkilidir. Bağımsızlık varsayımı bu kanıtı çok kez sayar ve süzgeci aşırı emin yapar: Doğru pozun parçacıkları bile tek bir kötü taramayla silinebilir. Pratikte σ büyütülür, ışınlar seyreltilir ya da "beklenmeyen nesne" bileşenli karma modeller kullanılır (bizim notumuz).

## A3 — MCL'de tepe kaybı

| Ayar | 8. adımda iki tepe de yaşıyor | Sonda doğru konum |
|---|---|---|
| N = 1000, θ ∈ {0, π} | 4/8 | 7/8 |
| N = 5000, θ ∈ {0, π} | 8/8 | 8/8 |
| N = 5000, θ düzgün | 1/8 | 5/8 |

Simetrik koridorda iki tepenin ağırlıkları kuramda eşittir; ama yeniden örnekleme rastgeledir ve her tepedeki parçacık sayısı adım adım rastgele dalgalanır ("genetik sürüklenme"). Az parçacıkla bir tepe sıfıra düşebilir. Doğru tepe kaybolursa girinti görüldüğünde hiçbir parçacık gözleme uymaz ve süzgeç yanlış yerde kalır (parçacık yoksunluğu). Tamamen düzgün başlangıç yönünde parçacıkların çok azı doğru yönle başlar; 5000 parçacık bile yetmez. Çözümler: daha çok parçacık, daha iyi önsel, rastgele parçacık enjeksiyonu (bizim notumuz; kitapta yok).

## A4 — EKF ve doğrusallaştırma

1. İşaretle: 0.32, 0.43, 0.52 → **0.20**, 0.16, 0.17, 0.19 → 0.35, … 0.74. İşaretsiz: 0.32'den 1.15'e tekdüze artar. Hareket her adımda belirsizlik ekler; konumu bilinen bir işaretin gözlemi onu hızla azaltır (Şekil 26.9).
2. σ = 0.1: Taylor ortalama 1.909, gerçek 1.891; std 0.017'ye karşı 0.031. σ = 0.5: ortalama 1.909'a karşı 1.551, std 0.084'e karşı 0.489. σ = 1.0: 1.909'a karşı 1.122, std 0.168'e karşı 1.123. Belirsizlik, f'nin doğrusal sayılabileceği aralıktan küçükken EKF güvenilirdir; belirsizlik büyüdükçe hem ortalama hem kovaryans bozulur (burada std 3–7 kat küçük kestiriliyor, süzgeç aşırı emin olur).

## A5 — Konfigürasyon uzayı

1. Üçgen: köşeler (2, 2), (4, 1), (6, 1), (6, 3), (2, 3): **beş kenarlı**, alan **7**. Kare: (3, 1), (6, 1), (6, 3), (3, 3): 3 × 2 dikdörtgen, alan **6** (engelin her yönde robotun boyu kadar "şişirilmesi"; kare simetrik olduğundan köşe kesilmez). Üçgende eğik kenar bir köşeyi keser ve beşinci kenarı oluşturur.
2. Dönebilen üçgen **3** (x, y, θ); bir de ölçek **4**; iki eklemli kol **2**; altı bacaklı robot **18** (12 bacak + gövdenin 3B konumu ve yönelimi için 6; kitaptaki sayı).

## A6 — Ters kinematik

1. cos θ_d = (1² + 1² − 1 − 1) / 2 = 0 → θ_d = ±90°. θ_o = atan2(1, 1) − atan2(sin θ_d, 1 + cos θ_d) = 45° ∓ 45°. Çözümler **(0°, 90°)** ve **(90°, −90°)**. Doğrulama: (0°, 90°): dirsek (1, 0), el (1, 0) + (cos 90°, sin 90°) = (1, 1). (90°, −90°): dirsek (0, 1), el (0, 1) + (cos 0°, sin 0°) = (1, 1).
2. Ulaşılabilen küme: merkezi tabanda, yarıçapı L₁ + L₂ = 2 olan disk (L₁ ≠ L₂ ise |L₁ − L₂| ≤ r ≤ L₁ + L₂ halkası). (2, 0): kol tam uzanmış, **tek** çözüm (0°, 0°). (2.5, 0): **çözüm yok**. (0, 0): dirsek tamamen katlanmış (θ_d = 180°) ve θ_o herhangi bir değer: **sonsuz** çözüm (bizim modelimizde |θ_d| > 160° kendine çarpma sayıldığı için hiçbiri geçerli değil).

## A7 — Planlayıcıları karşılaştır

| Planlayıcı | Uzunluk |
|---|---|
| Görünürlük çizgesi | **13.71** |
| Izgara 0.25 m | 15.05 |
| Izgara + kısaltma | 14.23 |
| k-PRM (M = 30), 10 tohum ort. | 18.41 |
| Çift yönlü RRT, ort. | 20.18 |
| RRT + kısaltma, ort. | 16.45 |

Görünürlük çizgesi 2B çokgen engellerde en kısa yolu garanti eder (en kısa yol köşelerden geçen doğru parçalarından oluşur). Izgara yolu 45°'lik açılarla sınırlı olduğu için tırtıklıdır ve yalnızca tamamen serbest hücreleri kullandığı için engellerden biraz uzak durur. PRM ve RRT en iyi yolu aramaz, yalnızca bir yol bulur; kısaltma önemli ölçüde iyileştirir ama yine de en iyiye ulaşmaz. Üstünlükleri: Görünürlük çizgesi yüksek boyutta ve çokgen olmayan C-uzaylarında kullanılamaz; ızgara boyutla üstel büyür; PRM ve RRT ise yalnızca bir çarpışma denetleyicisine ihtiyaç duyar ve yüksek boyutlu C-uzaylarında çalışır. Ayrıca görünürlük yolu engellere sürtünür; belirsizlik varken bu risklidir.

## A8 — Yörünge optimizasyonu

1. F(s, τ, τ̇) = ½‖τ̇‖². ∂F/∂τ = 0, ∂F/∂τ̇ = τ̇, dolayısıyla ∇J = 0 − d/ds τ̇ = **−τ̈**. Gradyan sıfır → τ̈ = 0 → τ̇ sabit → τ(s) = a s + b; uç koşullar a = q_g − q_s, b = q_s verir: **doğru parçası**. Kodumuz kıvrık bir başlangıçtan (uzunluk 11.94) engelsiz gradyan inişiyle 10.00'a, yani doğru parçasına iner.
2. (en küçük uzaklık, uzunluk): λ = 20 → (0.39, 10.04); 200 → (1.12, 10.83); 1000 → (1.41, 11.43); 3000 → (1.47, 11.58). λ büyüdükçe engellerden uzaklaşmak, kısalığa göre daha önemli olur; ödünleşim.
3. Üstten başlangıç: (1.43, **10.62**): Düz çizgiden başlayan optimizasyonun bulduğu S biçimli yoldan (11.43) daha kısa ve neredeyse aynı açıklıklı bir yol. Gradyan inişi **yerel** en iyiyi bulur: Düz çizgi iki engelin arasından geçtiği için gradyan onu birinciden aşağı, ikinciden yukarı iter; daha iyi olan "ikisinin de üstünden" çözümüne hiç bakılmaz. Kitabın önerdiği gibi farklı başlangıçlar ya da benzetimli tavlama yardımcı olur.

## A9 — Denetçi kazançları

1. K_P = 0.3 için ζ = K_D / (2√0.3) = K_D / 1.095:

| K_D | ζ | Aşım | Oturma süresi |
|---|---|---|---|
| 0.1 | 0.09 (çok az sönümlü) | 0.75 | 60 s içinde oturmadı |
| 0.8 | 0.73 | 0.034 | 10.7 s |
| 3.0 | 2.74 (aşırı sönümlü) | yok | 38.1 s |

Az sönümde sistem uzun süre salınır; aşırı sönümde salınmaz ama hedefe çok yavaş yaklaşır. ζ ≈ 0.7 civarı hızlı ve az aşımlıdır; kitabın seçtiği kazançlar tam bu bölgededir.
2. R = 0.1 → K = (3.12, 2.50); R = 1 → (0.99, 1.41); R = 10 → (0.31, 0.79). (Sürekli zamanda K = (1/√R, √(2/√R)).) R kontrol çabasının maliyetidir: Küçük R güçlü torkları ucuz sayar ve sert, hızlı bir denetçi verir; büyük R enerjiyi korur, yumuşak ve yavaş denetçi verir. Her durumda sonuç bir PD denetçisidir.

## A10 — İnsan modeli

1. İki adım sonra P(pencere): β = 0.1 → 0.40; β = 1 → 0.87; β = 5 → ≈ 1.00. β, insanın ne kadar "akılcı" (en iyi eyleme ne kadar bağlı) varsayıldığıdır. Büyük β ile robot birkaç adımda emin olur; insan aslında daha gelişigüzel davranıyorsa (bir şeye bakmak için yoldan sapmak) robot yanlış amaca aşırı güvenir. Küçük β ile robot çok temkinli kalır, tahmini işe yaramaz hâle gelir. β da veriden kestirilebilir (bizim notumuz).
2. Gürültülü gösterimde durumlar y = 0 çevresinde dağılır; her biri uzman tarafından etiketlendiği için doğrusal regresyon eğimi doğru öğrenir: u = −0.50 y − 0.30, şeritten çıkma %0. Gösterimdeki küçük sapmalar, DAGGER'ın sağladığı "düzeltme örneklerinin" bir kısmını doğal olarak sağlar. Ama bu DAGGER'ı gereksiz kılmaz: Gösterim gürültüsü yalnızca uzmanın kendi hatalarının boyutundaki sapmaları kapsar; öğrenilen politikanın kendi hataları onu daha uzak ve farklı durumlara götürebilir (ve gerçek politikalar doğrusal değildir). DAGGER öğrenilen politikanın **kendi** ziyaret ettiği durum dağılımında veri toplar.
