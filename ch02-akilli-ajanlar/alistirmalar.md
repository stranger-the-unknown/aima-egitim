# Bölüm 2 — Alıştırmalar

Özgün sorular. Kitap metnini kopyalamayın; kendi cümlelerinizle yanıtlayın.

---

## A1 — Fonksiyon vs program

Bir trafik ışığı kontrolcüsü düşünün. “Ajan fonksiyonu” ile “ajan programı”nı bu örnekte ayırt ederek kısaca tanımlayın. Programın fonksiyonu neden her zaman mükemmel gerçekleştiremeyeceğini bir cümleyle açıklayın.

## A2 — PEAS + ortam eksenleri

**Senaryo:** Restoran için masa öneren mobil uygulama (kullanıcı konumu, tercih, müsaitlik).

1. PEAS tablosunu doldurun (her satır 1–2 madde).
2. Ortamı şu eksenlerde sınıflandırın: gözlem, determinizm, dinamiklik, tek/çok ajan. Gerekçeyi birer cümle yazın.

## A3 — Mimari seçimi

Aşağıdaki her durum için **en uygun** ajan mimarisini seçin ve bir cümle gerekçe yazın:

1. Asansör kapısı: engel algılanırsa açılmayı durdur.
2. Depo robotu: koridorun görünmeyen kısmındaki rafların doluluk bilgisini hatırlayarak rota seçer.
3. Tatil planlayıcı: bütçe, süre ve ilgi alanları arasında ödünleşim yaparak gezi sırası üretir.
4. Oyun ajanı: rakibin stratejisi zamanla değişiyor; geçmiş maçlardan politika güncelliyor.

## A4 — Modele dayalı süpürge

`ornekler/model_based_vacuum.py` dosyasını çalıştırın.

1. Basit refleks ile modele dayalı ajanın adım sayılarını not edin (Senaryo 1).
2. Modele dayalı ajanın neden daha az “boş” adım attığını belleğin rolüyle açıklayın.
3. (İsteğe bağlı) Üçüncü bir oda C eklemek için bellekte hangi değişikliği yapardınız? Kısa tasarım notu yazın.

## A5 — Öğrenen ajan diyagramı

Bir çevrimiçi reklam tıklama ajanı için öğrenen ajanın dört parçasını (performans öğesi, eleştirmen, öğrenme öğesi, problem üreteci) bu probleme özel doldurun. Her parça için somut bir örnek cümle yeter.
