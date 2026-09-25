# Bölüm 1 — Alıştırmalar (özgün)

Kitap sorularının kopyası değildir. Amacınız kavramı uygulamak.

---

## Alıştırma 1 — PEAS yazma

**Kütüphane içi mobil raf tarama robotu** için PEAS tablosu oluşturun (her hücrede en az 2 madde).

İpucu: Başarı ölçütünde hem hız hem kitap/raf hasarını düşünün.

---

## Alıştırma 2 — Ortam sınıflandırma

Aşağıdaki üç senaryoyu ortam özellikleri tablosuyla sınıflandırın  
(gözlemlenebilirlik, determinizm, epizodiklik, dinamiklik, süreklilik, ajan sayısı):

1. İki odalı süpürge dünyası (`vacuum_agent.py` ile aynı model)
2. Çevrimiçi satranç (insan rakibe karşı, süre sınırlı)
3. Yoğun yağmurda otonom araç

Her özellik için kısaca **neden**ini bir cümleyle yazın.

---

## Alıştırma 3 — Ajan türü seçimi

Bir **akıllı termostat** düşünün: hedef sıcaklık, enerji maliyeti ve kullanıcı konforu önemli.

1. Basit refleks yeterli olur mu? Neden?
2. Hangi ajan türünü önerirsiniz (modele / hedefe / faydaya / öğrenen)? Gerekçenizi yazın.
3. Öğrenme eklemek neyi iyileştirir?

---

## Alıştırma 4 — Refleks ajanını iyileştirme (kod)

`vacuum_agent.py` içindeki basit refleks ajanı, her şey temiz olsa bile odalar arasında gidip gelmeye devam edebilir.

1. Küçük bir **iç durum** (bellek) ekleyerek modele dayalı bir davranış yazın: her iki oda temizlendiyse `Bekle` seçsin.
2. Aynı başlangıç koşullarında adım sayısını karşılaştırın.
3. Kısa bir paragraf: bellek neden gerekliydi?

---

## Alıştırma 5 — Başarı ölçütü tuzağı

Bir haber öneri sistemi için üç farklı **P (performance)** tanımı yazın:

1. Tıklama sayısını maksimize eden
2. Kullanıcıya uzun vadeli bilgi kazandırmayı hedefleyen
3. Zararlı/yanıltıcı içeriği cezalandıran

Her birinin yol açabileceği **istenmeyen davranış**ı bir cümleyle belirtin. Sonuç: başarı ölçütü tasarımın ahlakını da belirler.
