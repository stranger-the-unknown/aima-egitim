# Bölüm 10 — Alıştırmalar

Sorular özgündür. Çözümler `cozumler/` klasöründe; önce kendin dene.

Zorluk: ★ kolay · ★★ orta · ★★★ zor

---

## A1 — Kategori zinciri ★

Canlı → Hayvan → Kuş → Penguen hiyerarşisini çiz. Penguenler ⊂ Canlılar doğru mu? Neden?

## A2 — Üyelik ve alt küme ★

Tekir ∈ Kediler ile Kediler ⊂ Memeliler arasındaki farkı birer cümleyle açıkla. Hangisi nesne–kategori, hangisi kategori–kategori ilişkisidir?

## A3 — Ontoloji örneği ★

```bash
python ornekler/ontoloji_mini.py
```

1. is_a("Kedi", "Hayvan") ne döndürür?
2. Tekir alt kategorisini Kedi'nin altına ekle. is_a("Tekir", "Memeli") ne olmalı?

## A4 — Şeyler ve maddeler ★★

Aşağıdakileri "şey" (sayılabilir) ya da "madde" (sayılamaz) olarak sınıflandır. Her biri için bir **içsel** ve bir **dışsal** özellik söyle:
1. Çay 2. Bir bardak çay 3. Kum 4. Bir kum tanesi 5. Altın 6. Bir altın bilezik

## A5 — Tek tip bir FOL yığını ★

"Bütün bilgimi yüzlerce bağımsız FOL cümlesi olarak yazdım; ortak kategori yok." Bu yaklaşımın iki sakıncasını yaz.

## A6 — Olay hesabı (kod) ★★

`ornekler/olay_hesabi.py`'deki olay listesine şunları ekle: 5'te "KapıyıAç", 6'da "EvdenÇık(Ali)", 8'de "EveGir(Ali)".
1. İçeride(Ali) ve Açık(Kapı) için yeni zaman çizelgesini çıkar.
2. t = 10'da Açık(Kapı) doğru mu? Hangi aksiyom bunu belirliyor?
3. "EveGir(Ali) ancak kapı açıkken mümkündür" önkoşulunu nasıl eklersin?

## A7 — Allen ilişkileri ★

Kitaptaki tanımlara göre aşağıdaki çiftler arasında hangi ilişkiler geçerlidir?
1. Birinci Dünya Savaşı (1914–1918) — Vahdettin'in saltanatı (1918–1922)
2. Atatürk'ün cumhurbaşkanlığı (1923–1938) — Atatürk'ün hayatı (1881–1938)
3. Atatürk'ün hayatı (1881–1938) — İnönü'nün cumhurbaşkanlığı (1938–1950)
4. Kanuni'nin saltanatı (1520–1566) — Sinan'ın başmimarlığı (1538–1588): Overlap(Sinan, Kanuni) doğru mu?

## A8 — Olası dünyalar (kod) ★★

Ayşe, Ali'nin doğum gününün Mayıs'ta olduğunu biliyor ama hangi gün olduğunu bilmiyor. Ali'nin doğum günü aslında 14 Mayıs.
1. Ayşe'nin erişebildiği dünyaları tanımla.
2. Şunları değerlendir: K_Ayşe(Ay = Mayıs), K_Ayşe(Gün = 14), K_Ayşe(Gün ≤ 31), ∃g K_Ayşe(Gün = g).
3. Ali, Ayşe'ye "ayın ilk yarısında" dediğinde bilgi nasıl değişir?

## A9 — Özgüllük ve sınırlandırma (kod) ★★★

Varsayılanlar:
- Öğrenciler genellikle yetişkindir.
- Lise öğrencileri genellikle yetişkin değildir.
- Lise öğrencileri öğrencidir.
- Ali bir lise öğrencisidir.

1. Anormal yüklemleriyle yaz ve sınırlandır. Kaç tercih edilen model var? Yetişkin(Ali) için ne denir?
2. "Daha özel olan varsayılan önceliklidir" ilkesini öncelikli sınırlandırmayla uygula. Sonuç ne olur?

## A10 — ATMS etiketleri (kod) ★★★

`ornekler/anlamsal_ag.py`'deki JTMS örneğine (Yağmur, Sulama varsayımları) bir ATMS katmanı ekle: Her inanç için onu doğru kılan **en küçük varsayım kümelerini** (etiket) hesapla.
1. IslakÇim, KayganYol ve Şemsiye'nin etiketleri nedir?
2. Yeni bir kural ekle: IslakÇim ∧ Güneş ⇒ Gökkuşağı (Güneş de bir varsayım). Gökkuşağı'nın etiketi ne olur?
3. ATMS, JTMS'e göre hangi durumda avantajlıdır?
