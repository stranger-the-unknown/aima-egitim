# Bölüm 2 — Alıştırmalar

Sorular özgündür. Çözümler `cozumler/` klasöründe; önce kendin dene.

Zorluk: ★ kolay · ★★ orta · ★★★ zor

---

## A1 — Fonksiyon ve program ★

Bir trafik ışığı kontrolcüsü düşün. Bu örnekte "ajan fonksiyonu" ile "ajan programı"nı ayırt ederek kısaca tanımla. Programın fonksiyonu neden her zaman mükemmel gerçekleştiremeyeceğini bir cümleyle açıkla.

## A2 — PEAS ve ortam eksenleri ★

**Senaryo:** Restoranda masa öneren bir mobil uygulama (kullanıcı konumu, tercihler, müsaitlik).

1. PEAS tablosunu doldur (her satırda 1–2 madde).
2. Ortamı şu eksenlere göre sınıflandır: gözlemlenebilirlik, belirlilik, dinamiklik, tek/çok ajan. Her biri için bir cümlelik gerekçe yaz.

## A3 — Mimari seçimi ★★

Aşağıdaki her durum için **en uygun** ajan mimarisini seç ve bir cümleyle gerekçelendir:

1. Asansör kapısı: engel algılanırsa kapanmayı durdurur.
2. Depo robotu: koridorun görünmeyen kısmındaki rafların doluluğunu hatırlayarak rota seçer.
3. Tatil planlayıcısı: bütçe, süre ve ilgi alanları arasında ödünleşim yaparak gezi sırası üretir.
4. Oyun ajanı: rakibin stratejisi zamanla değişiyor; geçmiş maçlardan politikasını güncelliyor.

## A4 — Modele dayalı süpürge ★★

`ornekler/model_based_vacuum.py` dosyasını çalıştır.

1. Senaryo 1'de basit refleks ajanı ile modele dayalı ajanın adım sayılarını not et.
2. Modele dayalı ajanın neden daha az "boş" adım attığını belleğin rolüyle açıkla.
3. Üçüncü bir oda (C) eklemek için belleği nasıl değiştirirdin? Kısa bir tasarım notu yaz.

## A5 — Öğrenen ajan diyagramı ★

Çevrimiçi reklam gösteren bir ajan için öğrenen ajanın dört parçasını (performans öğesi, eleştirmen, öğrenme öğesi, problem üreteci) bu probleme özel olarak doldur. Her parça için somut bir örnek cümle yeter.

## A6 — Ölçütü kır, ölçütü onar (kod) ★★

`ornekler/performans_olcutu.py` dosyasını çalıştır.

1. "Süpürülen toz" ölçütünde hileci ajanın neden kazandığını adım adım açıkla.
2. "Temiz zemin" ölçütüne her **hareket** için −0,5 puan ekle. Dürüst ajan hâlâ en iyi ajan mı? Daha iyi bir ajan yazabilir misin?
3. "Temiz zemin" ölçütünü de istismar eden bir ajan hayal edebilir misin? (İpucu: Algılayıcıya müdahale etmek, ya da "temiz" sayılma koşulunu kandırmak.) Bu, ölçütün mü yoksa ortam modelinin mi eksikliği?

## A7 — Tablo ne kadar büyük? ★★

`ornekler/tablo_ajan.py` içindeki formülü kullan.

1. Süpürge dünyasında (|P| = 4) tablo satır sayısı hangi T için ilk kez **bir milyonu** aşar?
2. Algılayıcıya bir de "saat" (1–24) eklensin, yani |P| = 4 × 24 olsun. T = 10 için tablo boyutu kaça çıkar?
3. Aynı ajan fonksiyonunu birkaç satırlık bir programla gerçekleştirmek neden mümkün? Bu, tablo ile program arasındaki farkı nasıl gösterir?

## A8 — Temsil türleri ★★

Aşağıdaki her durumu **atomik**, **ayrışık** veya **yapılandırılmış** temsille modellemenin en doğal olduğunu söyle ve gerekçelendir:

1. Bir metro hattında istasyondan istasyona en kısa yolu bulmak
2. Bir sınav takvimini, hiçbir öğrencinin iki sınavı çakışmayacak biçimde hazırlamak
3. "Ali'nin annesinin kardeşi, Ayşe'nin öğretmenidir" gibi cümlelerden aile ve okul ilişkileri çıkarmak
4. Bir hastanın ateş, öksürük ve test sonuçlarından hastalık olasılığını hesaplamak

## A9 — Ortam sınıflandırma meydan okuması ★★★

Aşağıdaki görevleri yedi eksende sınıflandır. En az **iki** hücrede "duruma göre değişir" diyebileceğin bir sınır noktası bul ve iki farklı yorumu açıkla.

1. Wordle oynayan bir ajan
2. Borsada otomatik alım-satım yapan bir ajan
3. Mars'ta kaya örneği toplayan bir gezgin
