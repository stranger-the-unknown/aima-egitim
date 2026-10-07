# Bölüm 27 — Alıştırmalar

Sorular özgündür. Çözümler `cozumler/` klasöründe; önce kendin dene. Tartışma sorularında tek doğru yanıt yoktur; argümanların gücü önemlidir.

Zorluk: ★ kolay · ★★ orta · ★★★ zor

---

## A1 — Turing testi ve Çin odası ★

1. Turing testinin kuralları nelerdir? 2014'teki Eugene Goostman sonucu testin neyi ölçtüğü hakkında ne düşündürür?
2. Çin odası argümanını üç adımda özetle. "Sistem yanıtı" (anlayan tek tek parçalar değil bütün sistemdir) ve kitaptaki "insan hücreleri de anlamaz" itirazı argümanın hangi adımına saldırır?

## A2 — Gödel itirazı ★★

Lucas'ın argümanını ve kitabın üç yanıtını kendi sözlerinle yaz. Sence en güçlü yanıt hangisi, neden?

## A3 — Yeniden tanımlama (kod) ★★

Bir posta kodunda 1 000, 10 000 ve 100 000 kişi olan yapay nüfuslarda doğum tarihi + cinsiyet ile tek başına kalanların oranını bul; e^(−n/K) yaklaşımıyla (K olası değer çifti sayısı) karşılaştır. Yalnızca doğum yılı tutulursa k-anonimlik düzeyi nedir? Neden en kalabalık posta kodu en güvenlisi?

## A4 — Fark saldırısı ve diferansiyel mahremiyet (kod) ★★

1. Kitaptaki iki toplu yanıttan ($81 234 / 12 kişi; $81 199 / 13 kişi) 41 yaşındaki çalışanın maaşını hesapla.
2. Sayım sorgularına Laplace(1/ε) gürültüsü eklenince, birinin hasta olup olmadığını iki sorgunun farkından tahmin eden saldırganın başarısını ε = 0.1, 0.5, 1, 2, 5 için bul ve e^ε/(1 + e^ε) üst sınırıyla karşılaştır. Bu sınır nereden gelir?

## A5 — Güvenli toplama (kod) ★

Dört kullanıcılı güvenli toplamada dördüncü kullanıcı yanıt vermezse sunucunun hesapladığı toplam ne olur? Bu, protokolün hangi gereksinimini açıklar?

## A6 — Kalibrasyon ve fırsat eşitliği (kod) ★★★

Taban oranları (0.3, 0.3), (0.3, 0.5), (0.2, 0.6) olan iki grup için kalibre bir puanla tek eşik (0.5) kullan. Yanlış pozitif ve yanlış negatif oranlarını ve kalibrasyonu karşılaştır. Kleinberg vd. sonucunu bu sayılarla açıkla. COMPAS'taki %45 / %23 farkı neyi gösterir?

## A7 — Vekil değişkenler (kod) ★★

Geçmişte yanlı kararlarla etiketlenmiş bir kredi verisinde grup sütunu silinip posta kodu bırakılıyor. Posta kodunun grupla ilişkisi P(z = 1 | B) = 0.5, 0.8, 0.95 iken onay oranlarını bul. Sonucu "farkında olmayarak adalet" açısından yorumla. Grup sütununu tamamen silmenin başka bir sakıncası nedir?

## A8 — Örneklem boyu dengesizliği (kod) ★★

Azınlığın payı %1, %5, %20, %50 iken tek doğrusal modelin grup başına hatasını bul. Kitapta önerilen önlemlerden üçünü say ve hangisinin bu örnekte neden işe yarayacağını açıkla.

## A9 — Düşük etki ve şartname oyunu (kod) ★★

1. Kahve getiren robotun vazoyu kırmaktan vazgeçtiği λ eşiğini bul. Etki ölçüsü olarak "değiştirilen nesne sayısı"nın bir zayıflığı nedir?
2. Temizlik robotunu "temizlenen kir başına +1" ödülüyle γ = 0 ve γ = 0.95 için çalıştır. Neden yalnızca uzak görüşlü etmen hileye başvuruyor? Bu, daha yetenekli etmenler için ne anlama gelir?

## A10 — Sor mu, uygula mı? ★★★

İyi plan +10, felaket −100, soru maliyeti 1.
1. İnsan her zaman doğru yanıt veriyorsa robotun sormak yerine doğrudan uygulamaya başladığı P(plan doğru) eşiğini elle türet.
2. İnsan %95 ve %80 doğru yanıt veriyorsa eşik nasıl değişir? Sonucu kitaptaki "insanlar felaket bir plana izin verebilir" uyarısıyla yorumla.
3. Vinge (1993) "30 yıl içinde", Kurzweil (2017) "2045" dedi. Kitaptaki "336 yıl" hesabını yap.
