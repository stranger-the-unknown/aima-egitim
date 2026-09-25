# Bölüm 11 — Alıştırmalar

Özgün sorular. Kitap metnini kopyalamayın.

---

## A1 — Aksiyon parçaları

`Koy(X, Y)` aksiyonu için (blok X’i, açık blok Y’nin üstüne koymak) önkoşul / add / delete listelerini kendi cümlelerinizle yazın. (`ElBos` yerine `Tutuyor(X)` kullanın.)

## A2 — Durum geçişi elle

Başlangıç: `{On(A,Masa), On(B,Masa), Clear(A), Clear(B), ElBos}`.  
Aksiyon: kaldır A (masadan). Yeni durumda hangi liteller olmalı? Hangileri silinir?

## A3 — Şema yazdırma

```bash
python ornekler/aksiyon_semasi.py
```

Çıktıdaki bir şemayı seçip: “Bu aksiyon neden Clear şartı ister?” diye bir cümle yazın.

## A4 — Bloklar BFS

```bash
python ornekler/strips_bloklar.py
```

1. Üretilen plan kaç adım?
2. Hedef litelleri nelerdi?
3. Aynı problemi “önce B’yi A’nın üstüne” hedefiyle değiştirirseniz plan değişir mi? (kodda `hedef`i düzenleyip deneyin)

## A5 — İleri vs geri

Çok az uygulanabilir aksiyon, çok büyük hedef tanımı olan bir domain’de ileri mi geri mi daha umut verici olabilir? Sezginizi bir cümleyle yazın.
