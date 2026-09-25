# Çözüm — Alıştırma 1 (PEAS: kütüphane raf tarama robotu)

Örnek cevap (başka doğru PEAS’ler de mümkündür):

## P — Performance

- Rafların yüksek oranını doğru etiketle / envanterle eşleştirmek
- Tarama süresini makul tutmak (vardiya içinde bitirmek)
- Kitaplara ve raflara fiziksel zarar vermemek
- İnsanlara çarpmamak / yolları tıkamamak

## E — Environment

- Kütüphane koridorları ve raf sıraları
- Değişen ışık, zaman zaman engeller (sandalye, kutu)
- Diğer ziyaretçiler ve görevliler
- Raf düzeni ve barkod/RFID etiketleri

## A — Actuators

- Tekerlekli hareket (ileri, dönüş)
- Kamera yönlendirme / pan-tilt (varsa)
- Uyarı ışığı veya sesli uyarı
- Envanter sonucunu sunucuya gönderme

## S — Sensors

- Kamera (raf ve etiket görüntüleme)
- Lidar veya ultrason (engel mesafesi)
- Barkod / RFID okuyucu
- Tekerlek odometrisi veya iç konum tahmini

**Kontrol sorusu:** P içinde yalnızca “hız” olsaydı robot rafları savurarak geçerdi — bu yüzden hasar ve güvenlik de P’de olmalı.
