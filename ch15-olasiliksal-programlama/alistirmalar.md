# Bölüm 15 — Alıştırmalar

Sorular özgündür. Çözümler `cozumler/` klasöründe; önce kendin dene.

Zorluk: ★ kolay · ★★ orta · ★★★ zor

---

## A1 — Program = model ★

Üretimsel bir programda "önce gizli seçimleri yap, sonra gözlemleri üret" sırası neden doğaldır? Bu, Bayes ağında örneklemeye nasıl benzer?

## A2 — Hileli zar ★

`python ornekler/basit_uretimsel_model.py` çalıştır. Kutunun hileli olma önseli 0.3, hileli zarda P(6) = 0.7.
1. P(hileli | 6)'yı elle hesapla. Örneklemeyle bulunan değer ne kadar yakın?
2. `python ornekler/reddetme_ornekleme.py` çıktısında kanıt "1 geldi" olunca neden örneklerin çoğu reddediliyor?

## A3 — Temellendirme ★

Kitap önerisi RPM'inde 3 müşteri ve 4 kitap var.
1. Açılmış Bayes ağında kaç düğüm olur? Kaç tanesi Recommendation düğümüdür?
2. RecCPT kaç satırdır? Bağlama özgü bağımsızlık (dürüst olmayanlar kitaba bakmaz) kullanılınca kaç ayrı dağılım belirtmek yeter?

## A4 — Bilinmeyen yazar ★★

Recommendation(c, b), müşteri yazarın hayranıysa Exactly(5) olsun: `if Fan(c, Author(b))`. B2'nin yazarı A1 ya da A2 olabilir.
1. Açılmış ağda Recommendation(C1, B2)'nin ebeveynleri hangileridir?
2. Author(B2)'nin rolü nedir? Bu duruma neden "ilişkisel belirsizlik" denir?
3. MCMC çıkarımı bu durumda neden ağı büyütmez?

## A5 — Tek bir puan (kod) ★★

Yalnızca C1, B1'e 5 vermiş olsun.
1. E[Quality(B1)] ve P(Honest(C1)) ne olur? Önsel E[Quality] = 3.2 ile karşılaştır.
2. C1, B2'ye de 5 verirse ikisi nasıl değişir? Neden?

## A6 — Şans oyunu mu, beceri oyunu mu? (kod) ★★

Ayşe, Burak'ı 10 maçın 10'unda yenmiş olsun. β = 25/6 (beceri ağırlıklı oyun) ve β = 25 (şans ağırlıklı oyun) için sonsal beceri ortalamalarını hesapla. Önce tahmin et: Hangisinde fark daha büyük çıkar? Sonucu açıkla.

## A7 — Kaç müşteri? (kod) ★★

Açık evren modelinde 5 giriş kimliği görüldü. P(#Customer = n) nedir? Neden 4 kimlik durumundakiyle aynı çıktı? (İpucu: Hangi dünyalar 5 kimlik üretebilir, olasılıkları nasıl?)

## A8 — Poisson ile nesne sayısı ★★

1. Bir karınca yuvasındaki karınca sayısı Poisson(10⁶) ile modellenirse standart sapma kaç olur? Bu model gerçekçi mi?
2. Kitaptaki sybil saldırısını kendi cümlelerinle açıkla. Kapalı evren varsayımı neden bu saldırıya karşı savunmasızdır?

## A9 — Veri ilişkilendirme (kod) ★★★

İki durağan hedef 1 boyutlu doğrunun 0 ve 1.5 noktalarında. Her adımda, etiketsiz iki gözlem geliyor (gürültü σ = 1). Hangi gözlemin hangi hedefe ait olduğu bilinmiyor.
1. 6 adımda kaç eşleşme hipotezi vardır (etiket simetrisini hesaba kat)?
2. Hedef konumları üzerinden integral alarak her hipotezin olasılığını hesapla. En olası hipotez gerçeğe eşit mi? Olasılığı kaç?
3. En yakın komşu filtresi ne buldu? Bu problemde tek bir hipoteze bağlanmak neden tehlikelidir?

## A10 — Harf harf mi, kelime kelime mi? (kod) ★★★

`metin_okuma.py`'deki ikili harf modelinde Viterbi en olası **diziyi** bulur. İleri–geri algoritmasıyla her harfin **ayrı ayrı** en olası değerini seç (Bölüm 14).
1. p = 0.2'de iki yöntemin harf doğruluğunu ve kelimenin tamamen doğru okunma oranını karşılaştır.
2. Sonuç neden böyle? Hangi uygulamada hangisini tercih edersin?
