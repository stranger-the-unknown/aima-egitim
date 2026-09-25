# A3–A10 çözümleri

Kodlu kısımlar: `python cozumler/alistirma_kod.py` (bölüm klasöründen).

---

## A3 — Temellendirme

1. Düğümler: 3 Honest + 3 Kindness + 4 Quality + 3 × 4 = 12 Recommendation = **22**.
2. RecCPT: Honest (2) × Kindness (5) × Quality (5) = **50 satır**, her satır 5 puan üzerinde bir dağılım. Bağlama özgü bağımsızlıkla: dürüst müşteriler için HonestRecCPT'nin 5 × 5 = **25** satırı + dürüst olmayanlar için **1** ortak dağılım (⟨0.4, 0.1, 0.0, 0.1, 0.4⟩) = 26 dağılım.

## A4 — Bilinmeyen yazar

1. Honest(C1), Kindness(C1), Quality(B2), **Author(B2)**, **Fan(C1, A1)**, **Fan(C1, A2)**: altı ebeveyn.
2. Author(B2) bir **çoğullayıcı** (seçici) gibi çalışır: Değeri A1 ise Fan(C1, A1), A2 ise Fan(C1, A2) öneriyi etkiler. Hangi nesnenin (yazarın) ilişkide yer aldığı bilinmediği için buna **ilişkisel belirsizlik** denir. Aday yazar sayısı arttıkça ebeveyn sayısı da artar.
3. MCMC her adımda **tam bir olası dünya** tutar. O dünyada Author(B2) belirli bir değerdedir, bu yüzden yalnızca bir Fan değişkeni gerçekten ebeveyndir. MCMC geçişleri Author(B2)'nin değerini değiştirerek bağımlılık yapısının kendisini değiştirir.

## A5 — Tek bir puan

| Kanıt | E[Quality(B1)] | P(Honest(C1)) |
|---|---|---|
| (yok) | 3.20 | 0.990 |
| C1: B1 → 5 | **4.40** | **0.983** |
| C1: B1 → 5, B2 → 5 | **4.32** | **0.976** |

Tek bir 5, kalite tahminini belirgin biçimde yükseltir. Dürüstlük olasılığı hafifçe düşer, çünkü dürüst olmayan müşteriler de sık sık 5 verir (0.4). İki kitaba birden 5 verilmesi, "her şeye 5 veren biri" açıklamasını biraz daha olası kılar. Bu yüzden B1'in kalitesine duyulan güven biraz azalır.

## A6 — Şans oyunu mu, beceri oyunu mu?

| β | Ayşe | Burak |
|---|---|---|
| 25/6 (beceri) | 32.5 | 17.5 |
| 25 (şans) | **34.8** | **15.2** |

Sezgiye ters görünebilir: Şans ağırlıklı oyunda fark **daha büyük** çıkar. Neden? Beceri oyununda, Ayşe biraz daha iyiyse bile neredeyse her maçı kazanır. İlk birkaç galibiyet "Ayşe daha iyi" bilgisini verir, sonrakiler pek bir şey eklemez. Şans oyununda ise küçük bir beceri farkıyla 10'da 10 yapmak çok olasılık dışıdır; bu sonuç ancak **büyük** bir fark varsa açıklanabilir. (Karışık sonuçlarda, örneğin 6–4'te, iki model de oyuncuları birbirine yakın görür.)

## A7 — Kaç müşteri?

P(#Customer = 1, 2, 3) ≈ **0.169, 0.335, 0.497**, 4 kimlikle aynı.

5 kimlik üreten dünyalar: 1 sahtekâr (5 kimlik); 1 dürüst + 1 sahtekâr (4); 2 dürüst + 1 sahtekâr (3); ayrıca 2 sahtekâr (2 + 3 ya da 3 + 2) gibi çok daha düşük olasılıklı dünyalar. Baskın dünyalar, 4 kimlik durumundakilerle aynı yapıdadır ("n − 1 dürüst + 1 sahtekâr") ve UniformInt(2, 5) her sayıya aynı olasılığı (1/4) verdiği için oranlar değişmez. Küçük farklar (iki sahtekârlı dünyalar) ancak üçüncü basamakta görülür.

## A8 — Poisson ile nesne sayısı

1. std = √10⁶ = **1000**, yani %0.1. Gerçekçi değil: Gerçekte yuvadaki karınca sayısını bu kadar kesin bilmeyiz; "yüz binlerle milyonlar arası" gibi bir belirsizlik vardır. Kitap bu tür durumlar için büyüklük mertebesi dağılımlarını önerir.
2. **Sybil saldırısı:** Bir kişi birçok sahte kimlik açıp aynı ürünü defalarca över ya da yerer ve itibar sistemini yanıltır. Kapalı evren varsayımı her kimliğin ayrı bir kişi olduğunu kabul eder, bu yüzden sahte kimliklerin oyları gerçek bağımsız oylar gibi sayılır. Açık evren modeli kimliklerin sahipleri hakkında belirsizliği temsil eder ve "bu kimlikler aynı kişiye mi ait?" sorusunu sorabilir.

## A9 — Veri ilişkilendirme

1. Her adımda 2 olası eşleşme; ama etiketler simetrik (A ile B'nin adları değiştirilebilir), bu yüzden ilk adımı sabitleriz: 2⁵ = **32** hipotez. Genel olarak n hedef ve T adım için (n!)^T mertebesinde.
2. Bir çalıştırmada (tohum 6) gerçek hipotez en olası hipotezdi, ama olasılığı yalnızca **≈ 0.13**. İkinci ve üçüncü hipotezler 0.09 ve 0.07. Hedefler gürültüye göre birbirine yakın olduğunda sonsal çok yayılır.
3. En yakın komşu filtresi 5. adımda yanlış eşleşme seçti. Tek bir hipoteze bağlanan yöntem, bir hata yaptığında bunu bilemez ve hatalı eşleşme sonraki tahminleri de bozar. Olasılık dağılımı tutan yöntemler (MCMC, çok hipotezli izleme) belirsizliği korur ve yeni kanıt geldikçe düzeltebilir.

## A10 — Harf harf mi, kelime kelime mi?

p = 0.2, 10 test kelimesi, 15 deneme:

| | Harf doğruluğu | Kelime tamamen doğru |
|---|---|---|
| Viterbi (en olası dizi) | %63.3 | **%10.7** |
| İleri–geri (her harf ayrı) | **%65.5** | %10.0 |

Her yöntem kendi ölçütünü en iyiler: İleri–geri her harfin **ayrı ayrı** doğru olma olasılığını, Viterbi **bütün dizinin** doğru olma olasılığını en büyükler. Harf harf seçim tutarsız diziler (düşük olasılıklı geçişler) üretebilir. Metin arama, yazım denetimi gibi harf hatalarının tek tek sayıldığı işler için ileri–geri; bir kod ya da plaka gibi dizinin bütün olarak doğru olması gereken işler için Viterbi daha uygundur.
