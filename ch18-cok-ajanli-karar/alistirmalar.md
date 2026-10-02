# Bölüm 18 — Alıştırmalar

Sorular özgündür. Çözümler `cozumler/` klasöründe; önce kendin dene.

Zorluk: ★ kolay · ★★ orta · ★★★ zor

---

## A1 — Tavuk oyunu (kod) ★

İki sürücü birbirine doğru gidiyor. İkisi de kaçarsa (0, 0); biri kaçar, öbürü dümdüz giderse kaçan −1, giden +1; ikisi de dümdüz giderse (−10, −10).
1. Baskın strateji var mı? Saf Nash dengelerini ve Pareto en iyi sonuçları bul.
2. Karma Nash dengesini bul. Bu dengede çarpışma olasılığı nedir?

## A2 — Baskın denge ve serpiştirme ★

1. Her baskın strateji dengesinin bir Nash dengesi olduğunu kanıtla. Tersi doğru mu?
2. A'nın planı [a₁, a₂], B'nin planı [b₁, b₂, b₃]. Kaç serpiştirme vardır? Genel formülü yaz.
3. Çiftler tenis örneğinde A Plan 2'yi, B Plan 1'i seçerse ne olur? "Kendi tarafında kal" uzlaşımı hangi planı eler?

## A3 — Üç parmaklı Morra (kod) ★★

Oyuncular 1, 2 ya da 3 parmak gösterir; toplam çiftse E, tekse O toplam kadar kazanır.
1. E için 3 × 3 fayda matrisini yaz.
2. Saf stratejilerle değer için alt ve üst sınırları bul.
3. LP ile oyunun değerini ve bir denge stratejisini bul. Stratejinin O'nun her saf eylemine karşı ne getirdiğini kontrol et.

## A4 — Ne zaman biteceği bilinmeyen oyun (kod) ★★

Mahkûm ikilemi her turdan sonra δ olasılıkla sürüyor. İki oyuncu da ACIMASIZ oynuyor.
1. Sonsuza dek susmanın beklenen toplam faydası nedir? Bir kez tanık olup sonra hep tanık olmanınki?
2. ACIMASIZ–ACIMASIZ hangi δ değerleri için bir dengedir?
3. Sabit 100 turluk oyunla farkı açıkla.

## A5 — Basit poker (kod) ★★

1. Matristeki kr–fc hücresini (2/3) elle hesapla.
2. Saf dengeleri bul. Oyuncu 2'nin cf stratejisi sezgisel olarak ne anlama gelir?
3. Oyuncu 1 her zaman artırmak zorunda olsaydı (yalnızca rr) oyuncu 2 ne yapardı ve oyuncu 1 ne kaybederdi?

## A6 — Ataş oyununun dili (kod) ★★

Robbie'nin orta seçeneği 50 + 50 yerine 45 + 45 ya da 40 + 40 olsun.
1. Harriet hangi θ değerleri için 1 + 1 yapar?
2. Dengede Harriet ile Robbie arasındaki "dil" nasıl değişir? Bu değişiklik Harriet'e bir şey kaybettirir mi?

## A7 — Eldiven oyunu (kod) ★★

Oyuncu 1'de bir sol, oyuncu 2 ve 3'te birer sağ eldiven var. Bir çift eldiven 1 değerinde, tek eldiven 0.
1. ν'yi bütün koalisyonlar için yaz. Oyun süperadditif mi?
2. Shapley değerini hesapla.
3. Çekirdeği bul. Shapley değeri çekirdekte mi? Sonucu yorumla.

## A8 — VCG (kod) ★★

İki özdeş mal ve dört teklifçi: değerler 30, 25, 10, 5. Her teklifçi en çok bir mal ister.
1. VCG ile kazananları ve vergileri bul.
2. Hiçbir teklifçinin değerinden farklı teklif vererek kazanamadığını göster.
3. İkinci fiyat açık artırmasıyla ilişkisini açıkla.

## A9 — Hangi kural, hangi kazanan? (kod) ★★★

9 seçmen: 4'ü A ≻ C ≻ B, 3'ü B ≻ C ≻ A, 2'si C ≻ B ≻ A.
1. Çoğulluk, Borda, anında ikinci tur ve Condorcet kazananını bul.
2. Çoğullukta C'yi destekleyen 2 seçmen yalan söyleyerek sonucu kendi lehlerine değiştirebilir mi? Bu hangi teoremin örneğidir?

## A10 — Sabır (kod) ★★★

1. Dönüşümlü teklif pazarlığında γ₁ = 0.9, γ₂ = 0.8 için 1, 2, 3 turluk oyunları geriye tümevarımla çöz. Tur sayısı artarken A1'in payı neye yakınsar?
2. γ₁ = γ₂ = γ ise Rubinstein payı nedir? γ → 1 iken ne olur?
