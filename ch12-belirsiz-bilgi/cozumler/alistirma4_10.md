# A4–A10 çözümleri

Kodlu kısımlar: `python cozumler/alistirma_kod.py` (bölüm klasöründen).

---

## A4 — Diş hekimi tablosu

1. P(toothache) = 0.108 + 0.012 + 0.016 + 0.064 = **0.2**
2. P(catch) = 0.108 + 0.072 + 0.016 + 0.144 = 0.34. P(cavity ∧ catch) = 0.108 + 0.072 = 0.18.
   P(Cavity | catch) = ⟨0.18, 0.16⟩ / 0.34 ≈ **⟨0.529, 0.471⟩**
3. P(toothache | cavity) = (0.108 + 0.012) / 0.2 = **0.6**
4. P(toothache ∨ catch) = 1 − P(¬toothache, ¬catch) = 1 − (0.008 + 0.576) = 0.416.
   P(cavity ∧ (toothache ∨ catch)) = 0.2 − 0.008 = 0.192. Sonuç: 0.192 / 0.416 ≈ **0.462**

## A5 — Kendi Hollanda kitabın

1. Dahil etme–dışlama: P(a ∨ b) = 0.5 + 0.5 − 0.4 = **0.6** olmalıydı. Ajan a ∨ b'yi 0.1 düşük değerlendiriyor.
2. Ajan 1, her bileti kendi inancı olan fiyattan almaya ya da satmaya razıdır. Ajan 2:
   - a ∨ b biletini **alır** (0.5 öder),
   - a biletini ve b biletini **satar** (0.5 + 0.5 alır),
   - a ∧ b biletini **alır** (0.4 öder).
   
   Peşin para: −0.5 + 1.0 − 0.4 = **+0.1**. Biletlerin ödemesi: 1[a ∨ b] − 1[a] − 1[b] + 1[a ∧ b] = 0 **her sonuçta**. Ajan 2 hep 0.1 kazanır, Ajan 1 hep 0.1 kaybeder. Kod dört sonucun hepsinde −0.10$ gösterir.

## A6 — Salgın

1. P(s) = P(s | m) P(m) + P(s | ¬m) P(¬m) ⇒ P(s | ¬m) = (0.01 − 0.7/50000) / (1 − 1/50000) ≈ **0.009986**
2. P(m) = 1/5000. Yeni P(s) = 0.7/5000 + 0.009986 · (1 − 1/5000) ≈ **0.010124**. P(m | s) = 0.00014 / 0.010124 ≈ **0.0138**.
3. Tam 10 kat değil (0.014 olurdu), çünkü P(s) de biraz arttı: Menenjitliler de boyun sertliği yaşar. Ama boyun sertliğinin çoğu başka nedenlerden geldiği için artış küçüktür ve P(m | s) yaklaşık olarak P(m) ile orantılı artar. Kitabın vurguladığı nokta: Nedensel P(s | m) ve P(s | ¬m) değişmedi. Onları saklayan doktor, tanısal olasılığı yeniden hesaplayabilir.

## A7 — Naif Bayes ile haber sınıflandırma

1. spor: 0.4 · 0.5 · 0.6 · (1 − 0.01) = 0.1188; ekonomi: 0.6 · 0.02 · 0.05 · (1 − 0.4) = 0.00036.
   Normalize: **spor ≈ 0.997**, ekonomi ≈ 0.003.
2. "borsa" çarpanı yok: spor 0.12, ekonomi 0.0006 → **spor ≈ 0.995**. Gözlenmeyen bir kelime için iki durum da (var/yok) mümkündür; P(var | c) + P(yok | c) = 1 olduğu için toplamı 1'dir ve çarpımdan çıkar. Sonuç biraz değişti, çünkü "borsa geçmiyor" bilgisi de spor lehine küçük bir kanıttı.
3. P(gol | ekonomi) = 0 ise ekonomi için bütün çarpım 0 olur. "borsa" ne kadar güçlü bir ekonomi kanıtı olursa olsun belge **spor** sınıflanır (spor = 1.0). Tek bir görülmemiş kelime diğer bütün kanıtları siler. Çözüm: **yumuşatma** (Laplace gibi). Görülmemiş olaylara küçük bir olasılık ayrılır.

## A8 — Havalimanı

Beklenen fayda = P(yetişme) · değer − (çıkış süresi − 55) · 1.

| Plan | Değer 1000 | Değer 10 000 |
|---|---|---|
| A60 | 695 | 6995 |
| A90 | **935** | 9665 |
| A120 | 925 | 9835 |
| A180 | 874 | **9865** |
| A1440 | −385 | 8614 |

1. **A90.**
2. **A180.**
3. Rasyonel seçim hem **olasılıklara** hem **faydalara** bağlıdır. Olasılıklar aynı kalsa da uçuşun önemi değişince en iyi eylem değişir. Karar kuramı = olasılık + fayda. A1440 neredeyse kesin yetiştirir ama beklemenin maliyeti yüzünden hiçbir durumda en iyi değildir.

## A9 — Wumpus'ta önselin etkisi

| p | P(P₁,₃) | P(P₂,₂) |
|---|---|---|
| 0.01 | 0.020 | 0.990 |
| 0.2 | 0.310 | 0.862 |
| 0.5 | 0.600 | 0.800 |

1. İki esintiyi de açıklamanın en "ucuz" yolu [2,2]'de tek bir çukurdur (olasılık ∝ p). [2,2] boşsa hem [1,3] hem [3,1]'de çukur gerekir (∝ p²). p küçüldükçe p² ≪ p olur: Tek çukurlu açıklama ezici basar. P(P₂,₂) ≈ 1/(1 + p) → 1 ve P(P₁,₃) ≈ 2p → 0.
2. p = 0.5'te her yapılandırma eşit olasılıklı. Esintilerle tutarlı sınır modellerini saymak yeter: [1,3] çukurken 3 tutarlı model, boşken 2 (ama önsel eşit) → 0.6. [2,2] çukurken 4 model, boşken 1 → 0.8.
3. Esintiler yalnızca komşu karelerdeki çukurlara bağlıdır. Bilinen kareler, sorgu ve sınır verildiğinde gözlenen esintiler "diğer" karelerden (örneğin [4,4]) koşullu bağımsızdır. Toplamda diğer kareler Σ P(diğer) = 1 olarak çıkar. [4,4] ancak bir gün onun komşusunda esinti gözlenirse önemli olur.

## A10 — Naif varsayım bozulunca

1. **Hayır.** Cavity verildiğinde P(t, c | cavity) = 0.14 / 0.2 = 0.70, ama P(t | cavity) P(c | cavity) = 0.7 · 0.9 = 0.63.
2. Tam tablo: 0.14 / (0.14 + 0.016) ≈ **0.897**. Naif Bayes: α ⟨0.7 · 0.9 · 0.2, 0.1 · 0.2 · 0.8⟩ = α ⟨0.126, 0.016⟩ ≈ **0.887**. Fark yaklaşık 0.01.
3. Naif Bayes'in olasılık **değerleri** yanlış olabilir, ama çoğu zaman **sıralaması** doğru kalır: Hangi sınıfın daha olası olduğu değişmez. Sınıflandırmada önemli olan budur. Bu yüzden varsayım "naif" olsa da pratikte iyi çalışır. Olasılıkların kendisi kararda kullanılacaksa (örneğin beklenen fayda hesabında) bu hata önemli olabilir.
