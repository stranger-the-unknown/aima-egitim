# Bölüm 27 — Felsefe, etik ve güvenlik: Özgün Notlar

> Bu notlar kitabın metninin kopyası değildir. Anlatım özgün Türkçe öğretim dilindedir.
> Amaç: tartışma dili kurmak; tek doğru vaaz etmek değil. Dengeli ve eğitici tutun.

---

## 1. Zayıf (dar) AI vs güçlü / genel AI

- **Zayıf / dar AI:** Belirli görevde başarılı sistem (çeviri, satranç, görüntü sınıflandırma). Bilinç iddiası yok; araç.
- **Güçlü / genel AI (AGI tartışması):** Geniş görevlerde insan düzeyinde veya ötesi esneklik — **henüz gerçekleşmiş bir olgu değil; araştırma ve spekülasyon alanı.**

Eğitimde faydalı ayrım: bugün ürettiğimiz sistemlerin çoğu dar AI’dır. Performans ≠ bilinç; skor tablosu felsefi soruyu otomatik çözmez.

---

## 2. Turing testi: sınırlar

Alan Turing’in “taklit oyunu” fikri: yargıç, metin üzerinden insanla makineyi ayırt edebilir mi?

**Ne ölçebilir?** Davranışsal ikna / dil performansı (belirli koşullarda).

**Ne ölçmez (kolayca)?**

- İç deneyim / bilinç
- Anlama vs örüntü eşleme ayrımı (tartışmalı)
- Güvenlik, adillik, uzun vadeli hizalama

Bugünün sohbet modelleri bazı etkileşimlerde “ikna edici” olabilir; bu, Turing’in sorduğu felsefi sorunun kapandığını göstermez. Test **yeterlilik ölçütü** olarak da eleştirilir: geçmek ≠ güvenli / yararlı / adil.

---

## 3. Çin odası — tartışma için adil özet (kendi sözlerimizle)

John Searle’ün düşünce deneyi (özet, kitap kopyası değil):

Bir odada, Çince bilmeyen biri kural kitabına bakarak Çince sorulara Çince yanıtlar üretir. Dışarıdan “Çince anlıyor” gibi görünür; içerideki kişi kendi ifadesiyle anlamaz.

**Savın özü (Searle tarafı):** Saf sembol manipülasyonu, tek başına “anlama” / “zihinsellik” için yeterli olmayabilir.

**Karşı / nüanslar (özet):**

- Sistem olarak oda (kişi + kurallar + bellek) anlayabilir mi? (“sistem yanıtı”)
- Robot gövdesi / dünya etkileşimi eklenirse değişir mi? (“robot yanıtı”)
- “Anlama” operasyonel olarak nasıl tanımlanır? Davranış mı, iç süreç mi?

**Sınıf kullanımı:** Doğru cevabı ezberletmek değil; tarafları ayırt etmek ve kendi gerekçenizi yazmak. Bu notlar vaaz etmez.

---

## 4. Hizalama ve güvenlik temaları

**Hizalama (alignment):** Sistemin hedefleri / davranışı, kullanıcı ve toplumun meşru beklentileriyle ne kadar örtüşüyor?

Pratik katmanlar (yüksek düzey):

| Katman | Örnek soru |
|--------|------------|
| Belirtim | Metrik doğru şeyi mi ölçüyor? |
| Eğitim verisi | Yanlılık, zehirli içerik, gizlilik? |
| Dağıtım | Kim kullanır, hangi kısıtlar var? |
| İzleme | Hata / kötüye kullanım nasıl yakalanır? |
| Müdahale | Geri alma, insan onayı, kill-switch? |

**Güvenlik:** Kazara zarar (hata, dağıtım hatası) ve kötüye kullanım (bilinçli zarar) riskleri. Ölçek büyüdükçe etki yüzeyi büyür — abartı ve inkâr arasında **risk yönetimi** dili kullanın.

---

## 5. Adillik, gizlilik, hesap verebilirlik

- **Adillik:** Farklı gruplarda hata oranları / fırsatlar nasıl dağılır? “Eşit muamele” ile “eşit sonuç” gerilimi.
- **Gizlilik:** Veri toplama, saklama, yeniden kimlikleme riski; rıza ve amaç sınırlılığı.
- **Hesap verebilirlik:** Bir karar yanlış çıktığında kim sorumlu — geliştirici, kurum, operatör, model satıcısı? Log, açıklama, itiraz yolu var mı?

`etik_senaryo_karti.py` eylem seçiminin hangi gerilimleri açtığını listeler.
`guvenlik_kontrol_listesi.py` proje öncesi/sonrası kontrol şablonu basar.

---

## 6. Dengeli çalışma ilkesi

1. İddiayı abartmadan yazın (“kesin bilinçli” / “hiç risk yok”).
2. Karşı argümanı çarpıtmadan özetleyin.
3. Somut bağlam (sağlık, işe alım, kredi, moderasyon) seçin.
4. Teknik düzeltme ile kurumsal düzeltmeyi ayırın.
