# Bölüm 19 — Alıştırmalar

Sorular özgündür. Çözümler `cozumler/` klasöründe; önce kendin dene.

Zorluk: ★ kolay · ★★ orta · ★★★ zor

---

## A1 — Kazancı elle hesapla ★

Restoran verisinde (Şekil 19.2) Hungry ve Price niteliklerinin bilgi kazancını elle hesapla. Patrons'un 0.541'lik kazancıyla karşılaştır. (B(5/7) ≈ 0.863, B(1/5) ≈ 0.722, B(3/7) ≈ 0.985, B(1/3) ≈ 0.918.)

## A2 — Kaç fonksiyon? ★

1. 3 Boolean niteliğin kaç farklı Boolean fonksiyonu vardır? 20 niteliğin?
2. 3 nitelikli eşlik (parity) fonksiyonunu temsil eden en küçük karar ağacı kaç yapraklıdır? Neden?
3. Bir karar ağacı y > A₁ + A₂ fonksiyonunu neden kötü temsil eder?

## A3 — Patrons olmasaydı (kod) ★★

Patrons niteliğini çıkarıp 12 örnekten ağaç öğren. Hangi nitelik köke gider? Ağaç kaç düğümlü olur? Sonucu yorumla.

## A4 — χ² ile anlamlılık (kod) ★★

Kökte her nitelik için Δ sapmasını, serbestlik derecesini ve p değerini hesapla. Hangi nitelikler %5 düzeyinde anlamlıdır? 12 örnekle istatistiksel anlamlılık hakkında ne söyleyebilirsin?

## A5 — Kimlik niteliği (kod) ★★

Her örneğe benzersiz bir "Kimlik" niteliği ekle (k0, k1, …, k11).
1. Kimlik'in bilgi kazancı nedir? Neden?
2. **Kazanç oranı** = kazanç / bölünme bilgisi (−Σ (|Eₖ|/|E|) log₂ (|Eₖ|/|E|)). Kimlik, Patrons, Type ve Hungry için hesapla. Kazanç oranı sorunu çözüyor mu?

## A6 — Gürültüde budama (kod) ★★

Gerçek restoran ağacından 200 örnek üret ve etiketlerin %20'sini rastgele çevir. Tam ağacı ve χ² ile budanmış ağacı karşılaştır: eğitim doğruluğu, test doğruluğu, düğüm sayısı.

## A7 — Gradyan inişini elle izle ★★

Veri: (1, 3), (2, 5). Başlangıç w₀ = w₁ = 0, α = 0.1, toplu gradyan inişi (kurallar notlar §6.2'de).
1. İlk adımdan sonra w₀ ve w₁ nedir? Kare kayıp nasıl değişti?
2. Kapalı biçim çözümü nedir?
3. α = 1 alsaydın ne olurdu?

## A8 — L1 ve L2 (kod) ★★

`dogrusal_modeller.py`'deki 8 nitelikli veride (yalnızca 2'si ilgili) λ = 0, 0.05, 0.3, 1, 3 için L1 ve L2 düzenlileştirmeyle kaç ağırlığın tam sıfır olduğunu ve ilgili ağırlıkların nasıl küçüldüğünü karşılaştır.

## A9 — Kaymış çember (kod) ★★★

Pozitif örnekler merkezi (1, 0.5), yarıçapı 1.2 olan bir çemberin içinde.
1. Kitaptaki F(x) = (x₁², x₂², √2 x₁x₂) bu veriyi doğrusal ayırır mı?
2. Hangi üç özellik (ve sabit terim) yeter? Neden?

## A10 — Uzmanlara ne kadar güvenmeli? (kod) ★★★

Rastgele ağırlıklı çoğunlukta K = 10 uzman var ve en iyi uzmanın 250 hata yapacağını düşünüyorsun.
1. Sınırı en küçük yapan β nedir? β = 0.5'e göre ne kazandırır?
2. β → 1 ve β → 0 uçlarında ne olur? Uzmanların başarısı zamanla değişiyorsa hangisi daha tehlikelidir?
