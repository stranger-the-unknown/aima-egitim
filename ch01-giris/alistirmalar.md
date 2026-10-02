# Bölüm 1 — Alıştırmalar

Sorular özgündür, kitaptaki alıştırmaların kopyası değildir. Her alıştırmanın çözümü `cozumler/` klasöründe. Önce kendin dene, sonra karşılaştır.

Zorluk: ★ kolay · ★★ orta · ★★★ zor

---

## A1 — PEAS yazma ★

**Kütüphanede rafları tarayan mobil bir robot** için PEAS tablosu hazırla. Her hücreye en az iki madde yaz.

İpucu: Başarı ölçütünde hem hızı hem de kitaplara ve raflara verilen hasarı düşün.

---

## A2 — Ortam sınıflandırma ★

Aşağıdaki üç senaryoyu ortam özelliklerine göre sınıflandır (gözlemlenebilirlik, determinizm, epizodiklik, dinamiklik, süreklilik, ajan sayısı):

1. İki odalı süpürge dünyası (`vacuum_agent.py` ile aynı model)
2. Çevrimiçi satranç (insan rakibe karşı, süre sınırlı)
3. Yoğun yağmurda otonom araç

Her özellik için **nedenini** bir cümleyle yaz.

---

## A3 — Ajan türü seçimi ★★

Bir **akıllı termostat** düşün: hedef sıcaklık, enerji maliyeti ve kullanıcı konforu önemli.

1. Basit refleks ajanı yeterli olur mu? Neden?
2. Hangi ajan türünü önerirsin (modele dayalı / hedefe dayalı / faydaya dayalı / öğrenen)? Gerekçeni yaz.
3. Öğrenme eklemek neyi iyileştirir?

---

## A4 — Refleks ajanını iyileştirme (kod) ★★

`ornekler/vacuum_agent.py` içindeki basit refleks ajanı, her şey temiz olsa bile odalar arasında gidip gelmeye devam eder.

1. Küçük bir **iç durum** (bellek) ekleyerek modele dayalı bir ajan yaz: iki oda da temizlendiyse `Bekle` seçsin.
2. Aynı başlangıç koşullarında, 10 adımlık bir simülasyonda iki ajanın hareket sayısını karşılaştır.
3. Kısa bir paragrafla açıkla: bellek neden gerekliydi?

---

## A5 — Başarı ölçütü tuzağı ★★

Bir haber öneri sistemi için üç farklı **P** (performans ölçütü) tanımı yaz:

1. Tıklama sayısını en yükseğe çıkaran
2. Kullanıcıya uzun vadede bilgi kazandırmayı hedefleyen
3. Zararlı veya yanıltıcı içeriği cezalandıran

Her birinin yol açabileceği **istenmeyen davranışı** bir cümleyle belirt. Bu alıştırmanın dersi: başarı ölçütünü tasarlamak, sistemin ahlakını da tasarlamaktır.

---

## A6 — ELIZA'yı kır, sonra düzelt (kod) ★★

`ornekler/eliza_mini.py` dosyasını çalıştır.

1. `KURALLAR` listesine kendi kuralını ekle: "…den korkuyorum" kalıbını yakalasın ve "Bu korku ne zaman başladı?" gibi bir yanıt versin.
2. Programı saçmalatan **üç yeni cümle** bul. Her biri farklı bir zayıflığı göstersin (olumsuzluk, Türkçenin ek yapısı, bağlam, çok anlamlılık…).
3. Bir sorgucu olarak ELIZA'yı **en fazla üç soruda** ele verecek bir strateji öner. Neden işe yarar?
4. "Turing testini geçmek zekânın kanıtıdır" iddiasına karşı bir paragraf yaz.

---

## A7 — Kral Midas avı ★★★

Aşağıdaki üç sistem için:

- (a) Sistemin standart modeldeki **amaç fonksiyonunu** tek cümleyle yaz.
- (b) Bu amacı *harfiyen* en iyileyen ama insanların *istemeyeceği* bir davranış senaryosu kur.
- (c) Senaryoyu önleyecek bir tasarım değişikliği öner (amaca terim eklemek, insandan onay istemek, belirsizlik bırakmak…).

Sistemler:
1. Bir e-ticaret sitesinin "sepete ekleme oranını artır" diyen öneri motoru
2. "Temizlik süresini en aza indir" amacıyla çalışan bir ev temizlik robotu
3. "Sınav başarı ortalamasını yükselt" amacıyla ders öneren bir eğitim asistanı

Son olarak şu soruyu yanıtla: (c)'deki çözümlerin hangisi, *amacı daha iyi yazmaya* dayanıyor, hangisi *amacın asla tam yazılamayacağını* kabul ediyor? İkinci yaklaşım neden daha sağlam?

---

## A8 — Zaman çizelgesi ve "neden" ★

Notlardaki zaman çizelgesinden **dört** olay seç. Her biri için "bu olay hangi sorunu çözdü veya hangi sorunu ortaya çıkardı?" sorusunu tek cümleyle yanıtla. Sonra olayları neden–sonuç okları ile bir zincire bağla (ör. "kombinatoryal patlama → alana özgü bilgi → uzman sistemler").
