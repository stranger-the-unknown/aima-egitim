# Bölüm 17 — Alıştırmalar

Sorular özgündür. Çözümler `cozumler/` klasöründe; önce kendin dene.

Zorluk: ★ kolay · ★★ orta · ★★★ zor

---

## A1 — Neden politika? ★

4 × 3 dünyada [Yukarı, Yukarı, Sağ, Sağ, Sağ] dizisinin ajanı hedefe ulaştırma olasılığını elle hesapla.
1. Diziyi tam uygulayan yol hangisidir? Olasılığı nedir?
2. Ajanın şans eseri öbür yoldan (alttan) hedefe varmasının olasılığı nedir?
3. Bu sonuç, çözümün neden bir dizi değil bir politika olması gerektiğini nasıl gösterir?

## A2 — İndirim (kod) ★

10 adımda +1'e varan bir geçmiş düşün (9 geçiş −0.04, 10. geçiş +1).
1. γ = 1, 0.9 ve 0.5 için geçmişin faydasını hesapla.
2. γ = 0.95 hangi faiz oranına denktir?
3. Ödüller ±1 ile sınırlıysa γ = 0.9'da bir geçmişin faydası en çok kaç olabilir?

## A3 — Bellman denklemi ★

Şekil 17.3'teki faydaları (notlar §1.4) kullan.
1. (1, 1) için dört eylemin Q değerini hesapla. Hangisi en iyi? Sonuç U(1, 1) = 0.7453 ile tutarlı mı?
2. Aynısını (3, 1) için Sol ve Yukarı eylemleri için yap. Kitaptaki "(3,1)'de iki eylem eşit" ifadesini değerlendir.

## A4 — Dokuz politika (kod) ★★

r < 0 aralığında 4 × 3 dünyanın kaç farklı en iyi politikası vardır? Politikanın değiştiği r değerlerini bul ve kitaptaki değerlerle (−1.6497, −0.7311, −0.4526, −0.0850, −0.0273) karşılaştır. (İpucu: γ = 1 iken politika yinelemesine **uygun** bir politikadan başla. Neden?)

## A5 — Sonlu ufuk (kod) ★★

(3, 1)'de kalan adım sayısı N'ye göre en iyi eylem nedir? Sol hangi N'den itibaren en iyi olur? Bu davranışı açıkla.

## A6 — Politika değerlendirme ★★

İki durumlu bir MDP: X ve Y. Sabit π politikasıyla:
- X'te: 0.5 olasılıkla X'te kalır (ödül 1), 0.5 olasılıkla Y'ye geçer (ödül 0).
- Y'de: 0.8 olasılıkla Y'de kalır (ödül 0), 0.2 olasılıkla X'e geçer (ödül 2).
- γ = 0.5.

1. U^π(X) ve U^π(Y)'yi doğrusal denklemleri çözerek bul.
2. Aynı sonucu U₀ = 0'dan başlayan basit Bellman güncellemeleriyle yaklaşık bul (3 adım). Hata nasıl azalıyor?

## A7 — Tehlikeli yardım (kod) ★★

Ajana yardım etmek için 4 × 3 dünyada (γ = 0.99) hedefe (4, 3) Manhattan uzaklığını azaltan her geçişe +0.2 bonus verelim (uzaklaşmanın cezası yok).
1. En iyi politika ne olur? Ajan uca varıyor mu?
2. Bunun yerine Φ(s) = −0.2 × uzaklık(s) potansiyeliyle şekillendirme yap. Politika değişir mi?
3. Φ uç durum (4, 2)'de sıfır alınmazsa ne olur? Neden?

## A8 — Gittins indeksi (kod) ★★

1. γ = 0.8 için 1, 0, 0, 10, 0, 0, … ödül dizisinin Gittins indeksini ve en iyi durma zamanını bul.
2. Bernoulli haydudunda tahmini aynı (2/3) olan (2, 1), (4, 2), (8, 4), (16, 8) durumlarının indekslerini karşılaştır (γ = 0.9). Keşif bonusu deneme sayısıyla nasıl değişir?

## A9 — 4 × 3 POMDP'de inanç (kod) ★★★

Ajan 9 uç olmayan durum üzerinde düzgün bir inançla başlıyor, Sol yapıyor ve algılıyor.
1. Algılayıcı komşu duvar **sayısını** (1 ya da 2) 0.9 olasılıkla doğru söylüyor ve "1 duvar" diyor. Yeni inanç nedir? (Önce her durumun komşu duvar sayısını bul; engel (2, 2) de duvar sayılır.)
2. Algılayıcı 4 bitlik olsun (her yöndeki duvarı ayrı ayrı, her bit 0.1 olasılıkla yanlış) ve "yalnızca güneyde duvar" desin. Yeni inanç nedir?
3. Kitap bu durumda ajanın "büyük olasılıkla (3, 1)'de" olduğunu söyler. Hangi algılayıcı için doğrudur?

## A10 — Algılayıcı ne kadar değerli? (kod) ★★★

İki durumlu POMDP'de (A, B; Kal, Git) algılayıcı doğruluğunu 0.5, 0.6, 0.9 ve 1.0 yap. Derinlik 8 için U(b)'yi b(B) = 0, 0.5 ve 1'de hesapla.
1. Doğruluk 0.5 iken U(0.5) neden tam 4'tür?
2. Doğruluk arttıkça U(0.5) ile U(0) arasındaki fark nasıl değişir? Bunu bilginin değeriyle ilişkilendir.
