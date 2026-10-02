# Bölüm 20 — Alıştırmalar

Sorular özgündür. Çözümler `cozumler/` klasöründe; önce kendin dene.

Zorluk: ★ kolay · ★★ orta · ★★★ zor

---

## A1 — İki limon ★

Şeker torbalarında (önsel ⟨0.1, 0.2, 0.4, 0.2, 0.1⟩) art arda iki limonlu şeker çıktı.
1. Beş hipotezin sonsal olasılıklarını elle hesapla. Hangisi MAP?
2. Sonraki şekerin limon olma olasılığını Bayesçi olarak hesapla. MAP öğrenen ne derdi?

## A2 — Ambalaj ağı ★

Kiraz/limon ve kırmızı/yeşil ambalaj; θ = P(kiraz), θ₁ = P(kırmızı | kiraz), θ₂ = P(kırmızı | limon).
1. c kiraz (r_c kırmızı, g_c yeşil) ve ℓ limon (r_ℓ kırmızı, g_ℓ yeşil) için log olabilirliği yaz.
2. Üç parametrenin ML değerlerini türet. Neden birbirinden bağımsız çıkıyorlar?

## A3 — Önsel ne kadar önemli? (kod) ★★

Kitabın önseli yerine düzgün önsel (her torba 1/5) kullan.
1. 1 limondan sonra P(sonraki limon) nedir?
2. İki önselde P(h5 | d) > 0.9 için kaç limon gerekir? Neden farklı?

## A4 — Beta ile hesap ★★

Önsel Beta(2, 2). 3 kiraz, 1 limon görüldü.
1. Sonsal dağılım nedir? Ortalaması? Tepe noktası (mod = (a − 1)/(a + b − 2))?
2. ML tahminiyle karşılaştır. Önsel hangi yönde çekti, neden?
3. Bu önsel kaç "sanal" şekere denktir?

## A5 — Aynı ipucu, birden çok kez (kod) ★★

P(hasta) = 0.2; P(belirti | hasta) = 0.8, P(belirti | sağlıklı) = 0.3. Aynı belirti, yanlışlıkla k ayrı nitelik olarak kaydedilmiş (kopyalar). Naif Bayes P(hasta | belirtiler) için ne der (k = 1, 2, 5, 10)? Bu, naif Bayes'in hangi zayıflığını gösterir?

## A6 — Bayesçi eğim (kod) ★★

y = 0.8x + N(0, 1) gürültü, x ∈ [−2, 2], önsel θ ~ N(0, 10²). N = 1, 5, 20, 200 örnekte θ_N ve σ_N'yi hesapla. σ_N veri sayısıyla nasıl azalır?

## A7 — EM'in ilk adımını elle izle (kod) ★★

Karışmış torba örneğinde (kitaptaki sayımlar ve başlangıç değerleri) 273 kırmızı delikli kirazın θ⁽¹⁾'e katkısını elle hesapla: (273/1000) · P(Bag = 1 | kiraz, kırmızı, delikli). Sonucu kitaptaki 0.22797 ile karşılaştır.

## A8 — Başlangıç noktası (kod) ★★

Karışmış torba EM'ini üç başlangıçtan 200 yineleme çalıştır: hepsi 0.5; kitabın başlangıcı; torba 1 ile 2'nin rolleri ters. Sonuçları ve log olabilirlikleri karşılaştır.

## A9 — Kaç bileşen? (kod) ★★★

3 bileşenli bir Gauss karışımından 800 nokta üret; 500'üyle eğit, 300'üyle test et. k = 1, 2, 3, 4, 6 için eğitim ve test log olabilirliklerini karşılaştır. Eğitim olabilirliğine göre k seçmek neden yanlıştır?

## A10 — Gizli değişkenin değeri ★★★

Kalp hastalığı ağı: 3 etken, 3 değerli gizli Hastalık, n belirti; her değişken 3 değerli.
1. n = 3 için gizli değişkenle ve gizli değişkensiz parametre sayılarını elle hesapla (78 ve 708).
2. n = 5 ve n = 8 için tekrarla (kod). Fark nasıl büyür?
