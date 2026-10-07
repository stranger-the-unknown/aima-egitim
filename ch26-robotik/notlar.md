# Bölüm 26 — Robotik

> **Kitapta:** AIMA 4. baskı, Bölüm 26 *"Robotics"*.
> Önce kitabı oku, sonra bu notlarla pekiştir. Metin özgündür; kitaptan alıntı yoktur.
> Kodlar yalnızca numpy kullanır; dünyalar küçük ve yapaydır.

## Bu bölümün haritası

| Kitap alt bölümü | Bu nottaki karşılığı | Kod |
|---|---|---|
| 26.1 Robots | §1 Robot nedir, neden zor? | — |
| 26.2 Robot Hardware | §2 Robot türleri, algılayıcılar, eyleyiciler | — |
| 26.3 What kind of problem is robotics solving? | §3 MDP/POMDP/oyun, üç düzeyli hiyerarşi | — |
| 26.4 Robotic Perception | §4 Hareket/algılayıcı modeli, MCL, EKF, SLAM, öz-denetimli öğrenme | `lokalizasyon.py` |
| 26.5 Planning and Control | §5 C-uzayı, hareket planlama, yörünge izleme, en iyi denetim | `planlama.py`, `kontrol.py` |
| 26.6 Planning Uncertain Movements | §6 MPC, bilgi toplama, korumalı hareketler | — |
| 26.7 Reinforcement Learning in Robotics | §7 Modelden yararlanma, simülasyondan gerçeğe | — |
| 26.8 Humans and Robots | §8 Eşgüdüm, insan tahmini, tercih ve taklit öğrenmesi | `insan_robot.py` |
| 26.9 Alternative Robotic Frameworks | §9 Tepkisel denetçiler, kapsama mimarisi | `insan_robot.py` |
| 26.10 Application Domains | §10 Uygulamalar | — |

## Öğrenme hedefleri

1. Robotik probleminin neden sürekli, kısmen gözlenebilir, stokastik ve çok etmenli olduğunu açıklamak.
2. Hareket ve algılayıcı modelleriyle Monte Carlo lokalizasyonu ve EKF uygulamak.
3. Konfigürasyon uzayını, ileri/ters kinematiği ve C-uzayı engellerini hesaplamak.
4. Görünürlük çizgesi, hücre ayrıştırma, PRM, RRT ve yörünge optimizasyonunu karşılaştırmak.
5. P, PD, PID ve LQR denetçilerini benzetmek; kararlılığı yorumlamak.
6. İnsan davranışını amaç çıkarımıyla tahmin etmek; taklit öğrenmesinin sorunlarını açıklamak.

---

## 1. Robotlar

Robotlar fiziksel dünyayı **etkileyicilerle** (bacak, tekerlek, eklem, tutucu) değiştiren fiziksel etmenlerdir; **algılayıcılarla** (kamera, radar, lazer, mikrofon; jiroskop, gerinim ve tork algılayıcısı, ivmeölçer) çevrelerini ve kendi durumlarını algılarlar. Zorluklar:

- Ortam **kısmen gözlenebilir** ve **stokastik** (kamera köşeyi göremez, dişliler kayar); çevredeki insanlar öngörülemez.
- Durum ve eylem uzayları **sürekli** ve çoğu zaman **yüksek boyutlu** (robot kolunda 6–7 eklem, insan benzeri robotlarda yüzlerce).
- Gerçek dünya gerçek zamandan hızlı işlemez: Simülasyonda saatler süren milyonlarca deneme gerçekte yıllar alır ve zarar verebilecek denemeler yapılamaz. Simülasyonda öğreneni gerçeğe aktarmak (**sim-to-real**) etkin bir araştırma alanıdır.

---

## 2. Robot donanımı

- **Türler:** **manipülatörler** (robot kolları; fabrikada büyük yük taşıyanlar ya da tekerlekli sandalyeye takılan daha güvenli kollar), **mobil robotlar** (tekerlek, bacak, pervane; İHA'lar, otonom sualtı araçları, otonom arabalar, Mars gezginleri), **bacaklı robotlar** (engebeli arazi; denetimi daha zor). Ayrıca protezler, dış iskeletler, sürüler, akıllı ortamlar.
- **Algılayıcılar:** **Edilgin** (kamera) ve **etkin** (sonar; daha çok bilgi ama daha çok güç ve girişim riski). **Uzaklık bulucular:** sonar (sualtında tercih edilir), stereo görme, yapılandırılmış ışık (Kinect), uçuş süresi kameraları (saniyede 60 kareye kadar), **taramalı lidar** (100 m'de santimetre doğruluk; parlak gün ışığında daha iyi), radar (kilometrelerce, sisi deler), dokunsal algılayıcılar. **Konum algılayıcıları:** GPS (31 GPS ve 24 GLONASS uydusu; birkaç metre; diferansiyel GPS ideal koşullarda milimetre), iç mekânda işaretçiler ve kablosuz sinyaller, sualtında sonar işaretçileri. **Öz algı (proprioceptive):** mil kodlayıcıları (eklem açısı; tekerlekte **odometri** — kayma yüzünden yalnızca kısa mesafede doğru), atalet algılayıcıları, **kuvvet** ve **tork** algılayıcıları (saniyede yüzlerce ölçüm; ampulü kırmadan vidalamak).
- **Eyleyiciler:** elektrikli (dönme hareketi), hidrolik, pnömatik. **Döner** ve **prizmatik** eklemler (tek eksenli); küresel, silindirik, düzlemsel eklemler (çok eksenli). **Tutucular:** paralel çeneli (iki parmak, tek eyleyici), üç parmaklı, insan benzeri eller (Shadow Dexterous Hand: 20 eyleyici).

---

## 3. Robotik hangi problemi çözüyor?

Robot tek başına ve ortamını biliyorsa **MDP**, bilgi eksikse **POMDP**, insanların arasında hareket ediyorsa çoğu zaman **oyun** (dar koridorda insanla hem iş birliği hem biraz rekabet). Ödül çoğu zaman robotun değil, hizmet ettiği insanındır; tasarımcının yazdığı ödül yalnızca bir vekildir.

Ham algılayıcı girdileri ile motor akımları arasındaki uçurumu kapatmak için problem parçalanır:

- **Algıyı eylemden ayırmak:** Algının çıktısını kullanıp ileride yeni bilgi gelmeyecekmiş gibi davranmak (POMDP'nin bilgi toplama eylemlerinden vazgeçmek).
- **Üç düzeyli hiyerarşi:** **görev planlama** (kapıya git, aç, asansöre bin…), **hareket planlama** (bir noktadan diğerine yol), **denetim** (eyleyicilerle yolu izleme). Ayrıca **tercih öğrenme** (kullanıcının amacı) ve **insan tahmini**.
- Parçalamak karmaşıklığı azaltır ama parçaların birbirine yardım etme fırsatını kaybettirir; bu yüzden yeniden bütünleştirme eğilimi var (planlama + denetim, görev + hareket planlama, algı + tahmin + eylem).

---

## 4. Robot algısı (`lokalizasyon.py`)

İyi bir iç temsil: (1) iyi karar için yeterli bilgi içerir, (2) verimli güncellenebilir, (3) doğal (değişkenleri fiziksel durum değişkenlerine karşılık gelir). Süzme denklemi, eylemlerle koşullanan ve sürekli değişkenler için integralle:

```text
P(Xₜ₊₁ | z₁:ₜ₊₁, a₁:ₜ) = α P(zₜ₊₁ | Xₜ₊₁) ∫ P(Xₜ₊₁ | xₜ, aₜ) P(xₜ | z₁:ₜ, a₁:ₜ₋₁) dxₜ      (26.1)
```

P(Xₜ₊₁ | xₜ, aₜ) **hareket modeli**, P(zₜ₊₁ | Xₜ₊₁) **algılayıcı modeli**.

### 4.1 Lokalizasyon

- **Poz** Xₜ = (x, y, θ). Kinematik yaklaşımda eylem = öteleme hızı v ve dönme hızı ω:
  X̂ₜ₊₁ = Xₜ + (vΔt cos θ, vΔt sin θ, ωΔt); gürültüyle P(Xₜ₊₁ | Xₜ, v, ω) = N(X̂ₜ₊₁, Σx).
- **İşaret noktası modeli:** konumu bilinen işarete uzaklık ve yön açısı, N(ẑ, Σz). Kodumuzda (0, 0, 0°)'dan (3, 4)'teki işaret: 5, 53.1°.
- **Uzaklık taraması modeli:** M ışın, bağımsız Gauss hata: P(z | x) = α Π exp(−(zⱼ − ẑⱼ)²/2σ²). İşaret tanımaya gerek yoktur (özelliksiz bir duvar karşısında bile çalışır); tanınabilir işaretler varsa anında lokalizasyon sağlayabilir.
- **Monte Carlo lokalizasyonu (MCL):** parçacık süzgecinin robot sürümü (Şekil 26.6): her parçacığı hareket modelinden örnekle; her ışın için **ışın izleme** ile beklenen uzaklığı hesapla, ağırlıklandır; ağırlıkla yeniden örnekle. Kodumuzda 20 m'lik simetrik bir koridorun bir ucunda girinti var: Robot girintiyi görene dek parçacıklar iki tepeye (gerçek poz ve 180° döndürülmüş ayna poz) bölünür, girinti görülünce %100 gerçek poza toplanır (Şekil 26.7'nin küçük bir benzeri). Yeniden örnekleme rastgele olduğundan az parçacıkla tepelerden biri erken kaybolabilir (A3: 1000 parçacıkta 8 denemenin 4'ünde).
- **Genişletilmiş Kalman süzgeci (EKF):** İnanç tek bir Gauss (μ, Σ). Gauss yalnızca doğrusal f ve h altında kapalıdır; EKF f ve h'yi μ çevresinde **birinci derece Taylor açılımıyla doğrusallaştırır**. Ortalamanın izdüşümü doğrudur ama kovaryans yanlış olabilir (Şekil 26.8; kodumuzda f(x) = x + sin 2x, σ = 0.5 için Taylor std 0.08, gerçek std 0.49). Robot ilerledikçe belirsizlik büyür, işaret görülünce küçülür, işaret kaybolunca yeniden büyür (Şekil 26.9; kodumuzda 0.52 → 0.20 → 0.74). EKF işaretler kolay tanınıyorsa iyi çalışır; yoksa inanç çok tepeli olur (**veri ilişkilendirme** sorunu).

### 4.2 SLAM ve diğer algılar

- Harita yoksa robot hem haritayı kurmalı hem kendini bu haritada konumlandırmalıdır: **eşzamanlı lokalizasyon ve haritalama (SLAM)**. EKF ile: işaret konumlarını durum vektörüne ekle; güncelleme ikinci dereceden ölçeklenir, birkaç yüz işarete kadar uygundur. Daha zengin haritalar için çizge gevşetme yöntemleri ve EM.
- Sıcaklık, koku, ses gibi büyüklükler de dinamik Bayes ağlarıyla kestirilebilir; ya da robot olasılık dağılımları üzerinden akıl yürütmeden tepkisel programlanabilir (§9).
- **Öğrenme:** yüksek boyutlu algılayıcı akışlarını **düşük boyutlu gömmelere** indirmek; algılayıcı ve hareket modellerini veriden öğrenmek. **Uyarlanır algı:** "Sürülebilir yüzey" örneği: Lazer, aracın hemen önündeki düz bölgeyi olumlu örnek olarak etiketler; bir Gauss karışımı modeli bu bölgenin renk ve dokusunu öğrenip bütün görüntüye uygular. Robotun kendi etiketli verisini toplaması: **öz-denetimli öğrenme**.

---

## 5. Planlama ve denetim (`planlama.py`, `kontrol.py`)

**Yol** uzayda bir nokta dizisidir; bulmak **hareket planlama**dır. **Yörünge** zamanı da olan yoldur; izlemek **yörünge izleme denetimi**dir.

### 5.1 Konfigürasyon uzayı

- **İş uzayı**nda robot ve engeller nokta kümeleridir. **C-uzayı**nda robotun bütün noktaları tek bir noktayla (konfigürasyon q) temsil edilir. Dönmeyen üçgen: (x, y); dönebilen: (x, y, θ); bir de esneyebilen: (x, y, θ, s).
- **C-uzayı engeli:** C_obs = {q : A(q) ∩ O ≠ ∅}; **serbest uzay** C_free = C − C_obs. Kodumuzda dönmeyen dik üçgen ve dikdörtgen engel için C_obs, engelle robotun ters çevrilmiş biçiminin Minkowski toplamıdır: beş kenarlı bir çokgen (Şekil 26.11'deki gibi); ızgarada çarpışma denetleyicisiyle %100 uyumlu.
- **Serbestlik derecesi (DOF):** İki eklemli kolun C-uzayı (θ_omuz, θ_dirsek). **İleri kinematik** φ_b : C → W; **ters kinematik** IK_b(x) = {q : φ_b(q) = x}. Kodumuzda (0.866, 1.5) için iki çözüm: (30°, 60°) ve (90°, −60°) (dirsek yukarı/aşağı); erişilemeyen noktada çözüm yok.
- Basit bir iş uzayı engeli C-uzayında çok karmaşık, hatta iç bükey bir biçim alır (Şekil 26.12). Bu yüzden C-uzayı açıkça kurulmaz; bir **çarpışma denetleyicisi** γ(q) ile yoklanır (konfigürasyonu kinematikle iş uzayına taşı, çarpışmaya bak).

### 5.2 Hareket planlama

**Piyano taşıyıcı problemi:** W, O, robot (C, A(q)), q_s, q_g verildiğinde C_free içinde sürekli bir yol τ(t), τ(0) = q_s, τ(1) = q_g. Yollar uzayı sonsuz boyutludur.

| Yöntem | Fikir | Özellik |
|---|---|---|
| **Görünürlük çizgesi** | Çokgen köşeleri + q_s, q_g; birbirini "gören" köşeler arasında kenar; çizgede arama | 2B çokgen engellerde en kısa yolu garanti eder; yol engellere sürtünür |
| **Voronoi diyagramı** | Engellere eşit uzaklıktaki noktalar; q_s ve q_g en yakın noktaya bağlanır | Koridorun ortasından gider; açık alanda gereksiz dolambaç (200 m'lik alanda 100 m) |
| **Hücre ayrıştırma** | Serbest uzayı hücrelere böl (düzenli ızgara); değer fonksiyonu = hedefe en kısa yol (değer yinelemesi ya da A*) | Boyutun laneti; tırtıklı yollar; karışık hücreler (sağlam mı, tam mı ikilemi); hybrid A* sürekli durumu saklayarak düzgün yörünge üretir |
| **PRM** | Rastgele M kilometre taşı (reddetme örneklemesi), basit planlayıcıyla k en yakın komşuya bağla, ara; yol yoksa M taş daha | Olasılıksal olarak tam; yüksek boyutta iyi; çok sorgulu planlama |
| **RRT (çift yönlü)** | Başlangıç ve hedeften iki ağaç; rastgele taş iki ağaca bağlanınca çözüm; yoksa en yakın düğümden δ uzat | Tek sorgu için popüler; yollar en iyi değil, kısaltma (short-cutting) ile iyileştirilir; RRT* asimptotik olarak en iyi |
| **Yörünge optimizasyonu** | Basit ama uygulanamaz bir yoldan (düz çizgi) başla, J = J_obs + λ J_eff'i gradyan inişiyle küçült | Yerel en iyi; benzetimli tavlama gibi keşif yardımcı olur |

Kodumuzdaki iki dikdörtgenli dünyada: görünürlük çizgesi 13.72 (en iyi), 0.25 m ızgara 15.05, k-PRM ortalama ~18.4, RRT ~20.2 → kısaltma sonrası ~16.5 (A7). İki eklemli kolda C-uzayında düz çizgi engele çarpar; ızgara araması dirseği 45° bükerek engelin altından geçen bir yol bulur.

**Yörünge optimizasyonunun matematiği:** J_eff = ∫ ½‖τ̇‖² ds. Euler–Lagrange denklemi ∇J = ∂F/∂τ − d/dt ∂F/∂τ̇ verir; J_eff için ∇J = −τ̈. Gradyanı sıfırlamak τ̈ = 0, yani τ(s) = a s + b: **Engel yoksa en iyi yol doğru parçasıdır.** J_obs, işaretli uzaklık alanından türetilen bir c maliyetinin robotun bütün noktaları üzerinden **yol integrali**dir (‖dφ/ds‖ çarpanı yeniden zamanlamaya karşı değişmezlik sağlar). Kodumuzda düz çizgi iki nokta engelin 0.22 yakınından geçer; optimizasyon yolu birinci engelin altından, ikincinin üstünden geçen bir S'ye büker (en küçük uzaklık 1.41). Başka bir başlangıçtan başka bir yerel en iyiye varılır (A8).

### 5.3 Yörünge izleme denetimi

- **Açık döngü:** **Dinamik model** q̈ = f(q, q̇, u); **ters dinamik** u = f⁻¹(q, q̇, q̈). Önce yol **yeniden zamanlanır** (ξ(t), [0, T]), sonra u(t) = f⁻¹(ξ, ξ̇, ξ̈). Model kusurlu olduğunda (kütle, eylemsizlik, **yapışma sürtünmesi**) hatalar birikir.
- **Kapalı döngü:** **P denetçisi** u = K_P(ξ − q). Sürtünme yokken bir yay yasasıdır: sonsuza dek salınır; K_P'yi küçültmek salınımı yavaşlatır ama gidermez (kodumuzda K_P = 1 ve 0.1'de son 10 s'de q'nun aralığı ~2). **Kararlı:** küçük bozulmalar sınırlı hata verir. **Kesin kararlı:** bozulmadan sonra yola döner ve kalır. P kararlı ama kesin kararlı değildir.
- **PD denetçisi:** u = K_P(ξ − q) + K_D(ξ̇ − q̇) (26.4). Türev terimi sönümler (kitapta ve kodumuzda K_P = 0.3, K_D = 0.8: aşım %3, salınım yok). Sistematik bir dış kuvvet varsa (eğimli yol, aşınma) kalıcı hata bırakır (kodumuzda d / K_P = 0.167).
- **PID denetçisi:** + K_I ∫(ξ − q) (26.5); uzun süreli sapmaları düzeltir (kalıcı hata 0) ama salınım tehlikesi getirir. Sezgi: oransal — uzaktaysan daha çok uğraş; türev — hata artıyorsa daha da çok; integral — uzun süredir ilerlemiyorsan daha çok.
- **Hesaplanmış tork denetimi:** u = f⁻¹(ξ, ξ̇, ξ̈) (ileri besleme) + m(ξ)[K_P(ξ − q) + K_D(ξ̇ − q̇)] (geri besleme); m eylemsizlik matrisi.
- **Plan mı politika mı?** Denetim yasaları politikadır ama genellikle en iyi değildir: Dinamiği hesaba katmadan planlamak ve sapınca hep eski plana dönmek iki kayıp kaynağıdır.

### 5.4 En iyi denetim

Torklar üzerinden doğrudan optimize et: min ∫ J(x(t), u(t)) dt, ẋ = f(x, u), x(0) = x_s, x(T) = x_g (26.7). Çoklu atış ve doğrudan eşleme (collocation) gibi yöntemler küresel en iyiyi bulmaz ama insansı robotları yürütür, arabaları sürer.

**LQR:** J karesel, f doğrusal (ẋ = Ax + Bu, maliyet ∫ xᵀQx + uᵀRu, Q ve R pozitif tanımlı) ise sonsuz ufukta en iyi değer fonksiyonu karesel, en iyi politika doğrusaldır: u = −Kx; K **cebirsel Riccati denkleminden** bulunur (yerel optimizasyon, değer ya da politika yinelemesi gerekmez). Kodumuzda çift integratör, Q = diag(1, 0), R = 1 için K → [1, √2]: LQR'nin en iyi politikası bir PD denetçisidir. **Yinelemeli LQR (ILQR):** çözüm çevresinde dinamiği doğrusal, maliyeti karesel yaklaştırıp LQR'yi tekrar tekrar çözer.

---

## 6. Belirsiz hareketleri planlamak

- Günümüz robotlarının çoğu **en olası durumu** seçip deterministik planlayıcı kullanır.
- **Çevrim içi yeniden planlama** ve **model öngörülü denetim (MPC):** kısa ufukla planla, ilk eylemi uygula, her adımda yeniden planla; sonuçta bir politika elde edilir.
- **Bilgi toplama:** Kestirimi denetimden ayırmak her adımda bir MDP çözmek demektir; POMDP'nin aksine **bilginin değerini** hesaba katmaz (yolun dışındaki bir işarete yaklaşmak gibi eylemler hiç seçilmez). Çözümler: **korumalı hareketler** (hareket komutu + algılayıcıya dayalı bitiş koşulu; Şekil 26.23–26.25'te hız belirsizliği konisine rağmen deliğe giren iki adımlık strateji), **kıyı navigasyonu** sezgiseli (bilinen işaretlere yakın kal), beklenen bilgi kazancını maliyete eklemek.

---

## 7. Robotikte pekiştirmeli öğrenme

Sürekli uzaylar (ayrıklaştırma ya da fonksiyon yaklaşımı) ve asıl zorluk: **gerçek dünyadaki örnek karmaşıklığı** ve güvenlik.

- **Modelden yararlanmak:** parametreli fizik denklemleri + parametre uydurma (model tabanlı RL), hata terimi öğrenme, yerel doğrusal modeller (hokkabazlık); **simülasyondan gerçeğe** aktarım: modele gürültü eklemek, **alan rastgeleleştirme** (sürtünme, sönüm, görsel öznitelikleri değiştirerek, Şekil 26.26); Dyna gibi melez yöntemler; uçtan uca öğrenme (piksellerden torklara). Belirsizlikli model **güvenli keşif** için kısıtlar koyabilir.
- **Başka bilgiler:** parametreli **hareket ilkelleri** ("topu (x, y)'deki oyuncuya pasla"; hızlı ama davranış uzayını kısıtlar), meta-öğrenme / aktarım öğrenmesi, insanlar.

---

## 8. İnsanlar ve robotlar (`insan_robot.py`)

### 8.1 Eşgüdüm

İnsan ve robotun ortak durumu x = (x_R, x_H), eylemleri u_R, u_H, maliyetleri J_R(x, u_R, u_H), J_H(x, u_H, u_R). Zorluklar: amaçlar karşılıklı bilinmez (**eksik bilgili oyun**), uzaylar süreklidir, insanlar oyunun çözümünü hesaplayamaz ("senin benim senin … düşündüğümü düşündüğünü…").

- **İnsan eylemini tahmin:** Robot, insanın robotu yok saydığını ve amacına göre **gürültülü olarak akılcı** davrandığını varsayar: P(u_H | x, J_H) ∝ e^(−Q(x, u_H; J_H)) (26.8). Her gözlenen eylem inancı günceller: b′(J_H) ∝ b(J_H) P(u_H | x, J_H) (26.9). Kodumuzda kuzeydoğuya yürüyen insan için P(pencere) 0.33 → 0.66 → 0.87 → … → 1.00; koridor olasılığı hemen düşer (Şekil 26.27'nin benzeri). Sonra P(u_H | x) amaçlar üzerinden marjinalleştirilir ve problem bir MDP'ye indirgenir.
- Tahmini eylemden ayırmak, robotun **insanları etkileyebileceğini** görmesini engeller; birlikte düşünen otonom araç şeride kararlıca girerek arkadaki sürücünün yavaşlayacağını hesaba katar (Şekil 26.28).
- **İnsanın robotu tahmini:** Robot, amacının kolayca çıkarılabileceği biçimde davranabilir. Aynı takımdaysalar (J_H = J_R) **ortak etmen** için plan yapılır; insan plandan sapınca MPC ile yeniden planlanır (waffle yaparken un dolabına yönelen insanı görüp robotun unu değil waffle makinesini alması).
- **Kara kutu insan:** İnsan politikası π_H dinamiği "karıştıran" bilinmeyen bir parçadır; veriden π_H uydurmak ya da modelsiz RL.

### 8.2 İnsanların istediğini yapmayı öğrenmek

- **Tercih öğrenme (maliyet öğrenme):** Gösterimleri, gürültülü akılcı bir insanın bir J'yi optimize etmesinin kanıtı olarak kullan; çıkarılan J'yi robot kendisi optimize etsin (Şekil 26.29: toprak yolda kalmayı tercih). Dil, eleştiri, karşılaştırma ve fiziksel düzeltme (Şekil 26.30) da girdi olabilir.
- **Taklit öğrenmesi / davranış klonlama:** D = {(xᵢ, uᵢ)} üzerinde gözetimli öğrenme ile π : x ↦ u. Sorun **genelleme**: ALVINN'de küçük hatalar aracı gösterilmemiş durumlara götürür, orada daha büyük hatalar yapılır. Kodumuzda gösterim tam şerit ortasında ve gürültüsüz olduğu için klonlanan politika düzeltmeyi hiç öğrenmez (eğim 0) ve araç %62 olasılıkla şeritten çıkar.
- **DAGGER (veri birleştirme):** Öğrenilen politikayla veri topla, uzmana etiketlet, bütün verilerle yeni politika eğit; tekrarla. Kodumuzda tek turda eğim −0.5'i bulur, şeritten çıkma %0. Ayrıca gösterimlerden dinamik model öğrenip en iyi denetim (uzman düzeyinde helikopter manevraları) ve **çekişmeli** eğitim.
- **Öğretme arayüzleri:** İnsan kendi bedeniyle gösterirse **karşılık sorunu** (beş parmaklı kavrayışı iki parmaklı tutucuya aktarmak); robotun kolunu tutarak öğretmek (**kinestetik öğretme**) zor; ara çözümler: anahtar kareler, görsel programlama.

---

## 9. Alternatif çerçeveler: tepkisel denetim (`insan_robot.py`)

- **Tepkisel denetçi:** Dünyayı modelleyip planlamak yerine doğrudan politika (refleks etmen). Altı bacaklı Genghis'te 12 serbestlik derecesiyle (bacak başına iki) yol planlamak zor; bunun yerine bir **yürüyüş** seç: sağ ön, sağ arka ve sol orta bacakları ileri götür (diğer üçü yerde), sonra öbür üçünü. Kodumuzda her iki fazda yerdeki üç ayak gövde merkezini içeren bir üçgen oluşturur (statik kararlı); yalnızca sol ayaklar yerde kalsa kararlılık bozulur.
- **Bacak AFSM'si (Şekil 26.32b):** İleri salınımda takılırsa geri çek, daha yükseğe kaldır, yeniden dene. Kodumuzda 2.5 yüksekliğindeki engel için 3, 4.2 için 5 deneme.
- **Kapsama mimarisi** (Brooks, 1986): Sonlu durum makinelerini saatlerle **artırılmış sonlu durum makineleri (AFSM)** olarak birleştirip aşağıdan yukarı karmaşık davranış kurmak (bacaklar → bacak eşgüdümü → çarpışmadan kaçınma). Yol planlamayla aynı davranış 18 boyutlu C-uzayı (12 bacak + 6 gövde konumu/yönelimi) gerektirirdi.
- **Sorunları:** ham algılayıcı girdisine dayanır (zaman içinde bütünleştirme gerekirse başarısız), amaç değiştirmek zordur (bok böceği gibi), gerçek dünyadaki politika açıkça kodlanamayacak kadar karmaşık olabilir (şerit değiştirme pazarlığı).

---

## 10. Uygulamalar

Evde bakım (tekerlekli sandalye kolları, beyin–makine arayüzüyle kendini besleyen felçli hastalar, protez ve dış iskeletler), kişisel robotlar (robot süpürge), sağlık (Da Vinci cerrahi robotu), hizmet (otel ve hastane teslimat robotları, uzaktan katılım robotları), otonom arabalar (her yıl trafik kazalarında milyondan fazla ölüm; 2005 DARPA Grand Challenge: Stanley 200 km'lik çöl parkurunu yedi saatten kısa sürede bitirdi; 2007 Urban Challenge: BOSS; 2009 Google projesi → Waymo, 2018'de sürücüsüz testler), eğlence (Disney animatronikleri 1963'ten beri), keşif ve tehlikeli ortamlar (Mars, batık gemiler, terk edilmiş maden, aktif yanardağ, Three Mile Island, Çernobil, Fukuşima, Dünya Ticaret Merkezi), endüstri (robotların çoğu fabrikalarda, en çok otomobil fabrikalarında; işçilerin yerinden edilmesi Bölüm 27'de).

---

## Sık yapılan hatalar

| Yanılgı | Doğrusu |
|---|---|
| "Odometri robotun konumunu verir." | Tekerlekler kayar; yalnızca kısa mesafede doğrudur, süzme gerekir. |
| "Parçacık süzgeci her zaman doğru tepeyi korur." | Yeniden örnekleme rastgele olduğu için az parçacıkla tepeler kaybolabilir. |
| "EKF her zaman doğru kovaryans verir." | Doğrusallaştırma doğrusal olmayan f, h'de kovaryansı bozar. |
| "İş uzayındaki basit engel C-uzayında da basittir." | Çoğu zaman karmaşık ve iç bükeydir; çarpışma denetleyicisiyle yoklanır. |
| "PRM tamdır." | Olasılıksal olarak tamdır: yol varsa sonunda bulur. |
| "K_P'yi küçültmek P denetçisinin salınımını giderir." | Yalnızca yavaşlatır; sönüm için türev terimi gerekir. |
| "PD her hatayı sıfırlar." | Sistematik dış kuvvette kalıcı hata kalır; integral terimi gerekir. |
| "Uzmanı taklit eden politika uzman kadar iyidir." | Gösterilmemiş durumlara kayınca hatalar birikir (DAGGER). |

## Kendini yokla

1. Robotikte öğrenme neden simülasyondakinden zordur?
2. Etkin ve edilgin algılayıcıların artı ve eksileri nedir?
3. Süzme denklemi (26.1) Bölüm 14'tekinden hangi iki bakımdan farklıdır?
4. MCL'nin bir adımı nasıl işler? Simetrik bir koridorda inanç neden iki tepelidir?
5. EKF doğrusallaştırması neyi doğru, neyi yanlış izdüşürür?
6. C_obs nasıl tanımlanır? Dönmeyen üçgenin C-uzayı neden 2, dönebilenin 3 boyutludur?
7. Görünürlük çizgesi ile Voronoi diyagramının yolları nasıl farklıdır?
8. PRM ile RRT hangi tür sorgular için tercih edilir?
9. Engel yokken J_eff'in en iyi yolu neden doğru parçasıdır?
10. P, PD ve PID denetçilerinin davranışlarını karşılaştır.
11. LQR'yi bu kadar kullanışlı kılan nedir?
12. DAGGER davranış klonlamanın hangi sorununu çözer?

## Kod rehberi

```bash
python ornekler/lokalizasyon.py    # hareket/algılayıcı modelleri, MCL (simetrik koridor), EKF, doğrusallaştırma
python ornekler/planlama.py        # C-uzayı engeli, kinematik, kol C-uzayında ızgara arama, görünürlük, PRM, RRT, yörünge optimizasyonu
python ornekler/kontrol.py         # P, PD, PID, LQR
python ornekler/insan_robot.py     # amaç çıkarımı, davranış klonlama ve DAGGER, bacak AFSM'si, statik kararlılık
python cozumler/alistirma_kod.py   # A3, A4, A5, A7, A8, A9, A10
```

## Terimler

| Türkçe | İngilizce | Kısa açıklama |
|---|---|---|
| etkileyici | effector | Bacak, tekerlek, eklem, tutucu |
| eyleyici | actuator | Hareketi başlatan mekanizma (motor, hidrolik…) |
| manipülatör | manipulator | Robot kolu |
| mobil robot | mobile robot | Tekerlek, bacak, pervaneyle hareket eden robot |
| simülasyondan gerçeğe | sim-to-real | Simülasyonda öğreneni gerçeğe aktarma |
| uzaklık bulucu | range finder | Sonar, lidar, uçuş süresi kamerası |
| öz algı algılayıcısı | proprioceptive sensor | Robotun kendi hareketini ölçen algılayıcı |
| odometri | odometry | Tekerlek dönüşünden yol ölçümü |
| döner / prizmatik eklem | revolute / prismatic joint | Dönen / kayan eklem |
| görev / hareket planlama | task / motion planning | Üst düzey adımlar / noktadan noktaya yol |
| hareket modeli | motion model | P(Xₜ₊₁ \| xₜ, aₜ) |
| poz | pose | (x, y, θ) |
| işaret noktası | landmark | Konumu bilinen, tanınabilir özellik |
| Monte Carlo lokalizasyonu | Monte Carlo localization (MCL) | Robot için parçacık süzgeci |
| doğrusallaştırma | linearization | Birinci derece Taylor yaklaşımı |
| genişletilmiş Kalman süzgeci | extended Kalman filter (EKF) | Doğrusallaştırılmış Kalman süzgeci |
| eşzamanlı lokalizasyon ve haritalama | SLAM | Harita kurarken konumlanma |
| öz-denetimli öğrenme | self-supervised learning | Robotun kendi etiketlerini üretmesi |
| yol / yörünge | path / trajectory | Noktalar dizisi / zamanlı yol |
| konfigürasyon uzayı | configuration space (C-space) | Robotun bütün durumlarını bir noktayla temsil |
| serbestlik derecesi | degrees of freedom (DOF) | Bağımsız hareket eksenleri |
| ileri / ters kinematik | forward / inverse kinematics | q → konum / konum → q |
| çarpışma denetleyicisi | collision checker | γ(q) ∈ {0, 1} |
| görünürlük çizgesi | visibility graph | Birbirini gören köşeler çizgesi |
| Voronoi diyagramı | Voronoi diagram | Engellere eşit uzaklıktaki noktalar |
| hücre ayrıştırma | cell decomposition | Serbest uzayı hücrelere bölme |
| olasılıksal yol haritası | probabilistic roadmap (PRM) | Rastgele kilometre taşları çizgesi |
| hızla keşfeden rastgele ağaç | rapidly exploring random tree (RRT) | Rastgele büyüyen arama ağacı |
| yörünge optimizasyonu | trajectory optimization | Yolu maliyet fonksiyonelini küçülterek bulma |
| işaretli uzaklık alanı | signed distance field | Engelin içinde negatif uzaklık |
| ters dinamik | inverse dynamics | İstenen ivme için tork |
| P / PD / PID denetçisi | P / PD / PID controller | Oransal / türevli / integralli geri besleme |
| kesin kararlı | strictly stable | Bozulmadan sonra yola dönen |
| hesaplanmış tork denetimi | computed torque control | İleri besleme + geri besleme |
| doğrusal karesel düzenleyici | linear quadratic regulator (LQR) | u = −Kx, Riccati denklemi |
| model öngörülü denetim | model predictive control (MPC) | Kısa ufuk, her adımda yeniden planlama |
| korumalı hareket | guarded movement | Komut + algılayıcıya dayalı bitiş koşulu |
| alan rastgeleleştirme | domain randomization | Farklı benzetim parametreleriyle eğitme |
| hareket ilkeli | motion primitive | Parametreli beceri |
| tercih öğrenme | preference learning | Kullanıcının maliyet fonksiyonunu öğrenme |
| davranış klonlama | behavioral cloning | Gösterimlerden gözetimli politika öğrenme |
| karşılık sorunu | correspondence problem | İnsan hareketini robota aktarma |
| kinestetik öğretme | kinesthetic teaching | Robotun kolunu tutarak öğretme |
| kapsama mimarisi | subsumption architecture | AFSM'lerden tepkisel denetçi kurma |
| yürüyüş | gait | Bacakların hareket düzeni |
