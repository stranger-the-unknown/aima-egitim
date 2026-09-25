# Bölüm 3 — Alıştırmalar

Özgün sorular. Kitap metnini kopyalamayın.

---

## A1 — Problem formülasyonu

**Senaryo:** 3×3 ızgarada bir robot sol üstten sağ alta gidecek; dört yön (yukarı/aşağı/sol/sağ); her adım maliyeti 1; engel yok.

Durum, başlangıç, eylemler, geçiş, hedef testi ve yol maliyetini yazın. Durum temsilini tek cümleyle gerekçelendirin.

## A2 — Ağaç vs graf

Arad ↔ Sibiu arasında gidiş-geliş mümkün. Ağaç aramada ne risk oluşur? Graf arama bunu nasıl önler? İki cümle yeter.

## A3 — Algoritma seçimi

Her durum için bir algoritma seçin ve gerekçeyi bir cümle yazın:

1. labirent, her adım maliyeti eşit, en az adım istiyorum
2. yolların km’leri farklı, en kısa km istiyorum, sezgisel yok
3. sezgisel iyi ve kabul edilebilir, optimal + yönlendirme istiyorum
4. sadece “hedefe yakın görünen”e gitmek istiyorum, optimal şart değil

## A4 — Romanya kodu

`ornekler/romania_arama.py` çalıştırın (Arad → Bucharest).

1. UCS ile A* maliyetlerini karşılaştırın — aynı mı?
2. Genişletilen düğüm sayılarını yazın; A* neden genellikle daha az genişletir?
3. DFS yolunu UCS yolu ile karşılaştırın — DFS neden optimal olmayabilir?

## A5 — Sezgisel tasarımı

Hedef Bucharest değil de **Iasi** olsaydı. SLD tablomuz yalnızca Bucharest için. h=0 kullanırsak A* hangi algoritmaya benzer? Iasi için kabul edilebilir bir sezgisel nasıl uydururdunuz? (Fikir yeterli; sayı tablosu zorunlu değil.)
