# Bölüm 26 — Quiz

Cevaplara bakmadan önce kendin yanıtla. Cevaplar dosyanın sonunda.

---

**S1.** Robotikte öğrenmeyi simülasyondakinden zorlaştıran iki etken nedir?

**S2.** Hangisi öz algı (proprioceptive) algılayıcısıdır?

A) Lidar
B) GPS
C) Mil kodlayıcısı
D) Kamera

**S3.** Robot süzme denklemi (26.1) Bölüm 14'teki süzme denkleminden hangi iki bakımdan farklıdır?

**S4.** Monte Carlo lokalizasyonunun bir güncelleme adımında hangisi **yapılmaz**?

A) Her parçacık hareket modelinden örneklenir
B) Her ışın için beklenen uzaklık ışın izlemeyle hesaplanır
C) Parçacıklar ağırlıklarıyla yeniden örneklenir
D) Hareket ve algılayıcı modelleri doğrusallaştırılır

**S5.** EKF neden doğrusallaştırma yapar? Bunun bedeli nedir?

**S6.** C-uzayı engelinin tanımı nedir? Bir çarpışma denetleyicisi neden C-uzayını açıkça kurmaktan daha kullanışlıdır?

**S7.** Hangi planlayıcı 2B çokgen engellerde en kısa yolu garanti eder?

A) Görünürlük çizgesi
B) Voronoi diyagramı
C) PRM
D) RRT

**S8.** PRM'nin "olasılıksal olarak tam" olması ne demektir?

**S9.** Sürtünmesiz bir sistemde P denetçisi neden sonsuza dek salınır? Hangi terim bunu düzeltir?

**S10.** Eğimli bir yolda giden araçta PD denetçisi kalıcı hata bırakıyor. Çözüm nedir?

A) K_D'yi artırmak
B) İntegral terimi eklemek
C) K_P'yi sıfırlamak
D) Denetimi açık döngüye çevirmek

**S11.** Robot, insanın amacını nasıl tahmin eder (26.8–26.9)?

**S12.** Davranış klonlamanın temel sorunu nedir, DAGGER bunu nasıl çözer?

---

## Cevaplar

**S1.** Gerçek dünya gerçek zamandan hızlı işlemez (milyonlarca deneme yıllar alır) ve zarar verebilecek denemeler yapılamaz. Ayrıca durum ve eylem uzayları sürekli ve yüksek boyutludur.

**S2.** **C.** Mil kodlayıcıları robotun kendi eklem açısını ve tekerlek dönüşünü ölçer.

**S3.** Eylemlerle de koşullanır ve sürekli değişkenler için toplam yerine integral kullanır.

**S4.** **D.** Doğrusallaştırma EKF'ye özgüdür; MCL doğrusal olmayan modelleri doğrudan örnekler.

**S5.** Gauss inanç yalnızca doğrusal hareket ve ölçüm modellerinde Gauss kalır. Taylor açılımı ortalamanın izdüşümünü doğru verir ama kovaryansı bozabilir; belirsizlik büyükse ya da işaretler tanınamıyorsa (çok tepeli inanç) EKF başarısız olur.

**S6.** C_obs = {q ∈ C : A(q) ∩ O ≠ ∅}. Basit iş uzayı engelleri bile C-uzayında karmaşık, iç bükey biçimler alır; bir konfigürasyonun çarpışıp çarpışmadığını (kinematikle iş uzayına taşıyarak) denetlemek bütün C_obs'u kurmaktan çok daha kolaydır.

**S7.** **A.** Voronoi engellerden uzak durur; PRM ve RRT en iyi yolu aramaz.

**S8.** Yol varsa, yeterince kilometre taşı örneklendikçe sonunda bulunur; ama sınırlı sayıda örnekle başarısız olabilir.

**S9.** Denetçi bir yay gibi davranır: Hedefe geri itilen sistemin hızı oradayken sıfır değildir ve sönüm olmadığı için enerji korunur. Türev (D) terimi sönüm ekler.

**S10.** **B.** Uzun süreli hatanın integrali giderek artan bir düzeltme üretir.

**S11.** İnsanın amacına göre gürültülü olarak en iyi davrandığını varsayar: P(u_H | x, J_H) ∝ exp(−Q(x, u_H; J_H)). Gözlenen her eylemle amaç inancını Bayes kuralıyla günceller: b′(J_H) ∝ b(J_H) P(u_H | x, J_H). Sonra amaçlar üzerinden marjinalleştirerek gelecek eylemleri tahmin eder.

**S12.** Politika yalnızca uzmanın ziyaret ettiği durumlardan öğrenir; küçük hatalar onu hiç görmediği durumlara götürür ve orada hatalar büyür (ALVINN). DAGGER, öğrenilen politikanın ziyaret ettiği durumlar için uzmandan etiket toplar ve bütün veriyle yeniden eğitir.
