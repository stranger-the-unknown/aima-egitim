# Bölüm 5 — Alıştırmalar

Sorular özgündür. Çözümler `cozumler/` klasöründe; önce kendin dene.

Zorluk: ★ kolay · ★★ orta · ★★★ zor

---

## A1 — Minimax sezgisi ★

Kök MAX; iki MIN çocuğu var; her MIN düğümünün iki yaprağı var. Yaprak değerleri soldan sağa: 3, 5, 2, 9.

1. Sol ve sağ MIN düğümlerinin değeri nedir?
2. Kök MAX hangi çocuğu seçer? Değeri kaçtır?
3. "Rakip en iyi oynar" varsayımı burada nerede kullanıldı?

## A2 — Alfa-beta fikri ★

Alfa-beta minimax ile **aynı hamleyi** mi üretir, yoksa yaklaşık bir sonuç mu verir? Budama neyi "keser"? α ve β'yı birer cümleyle tanımla.

## A3 — İki optimal XOX ajanı ★

```bash
python ornekler/minimax_tictactoe.py
python ornekler/minimax_tictactoe.py --alpha-beta
```

1. Oyun nasıl bitti? Bu sonuç neden "doğal"?
2. İlk hamlede incelenen düğüm sayısını iki koşuda karşılaştır. Oran kaç?

## A4 — Pozisyondan hamle ★

```bash
python ornekler/minimax_tictactoe.py --mod en-iyi --tahta "X.O.X.O.."
python ornekler/minimax_tictactoe.py --mod en-iyi --tahta "X.O.X.O.." --hizli-kazan
```

1. Sıra kimde? İki komut hangi hücreleri öneriyor?
2. İlk komutun önerisi yanlış mı? Minimax neden hemen kazanan hamleyi tercih etmiyor?
3. `--hizli-kazan` faydayı nasıl değiştiriyor? Bu değişiklik minimax değerinin "anlamını" nasıl etkiliyor?

## A5 — Ufuk etkisi ★★

Satrançta 4 katlık derinlikte kesip EVAL kullanıyorsun. Bunun neden **kusurlu karar** üretebileceğini ufuk etkisiyle açıkla. Bir örnek ver (ör. taş kaybının bir hamle öteye itilmesi). Sessizlik araması ve tekil genişletme bu sorunu nasıl hafifletir?

## A6 — Elle alfa-beta ★★

Kök MAX; üç MIN çocuğu (B, C, D); her birinin üç yaprağı var:

    B: 5 7 3     C: 4 8 1     D: 6 2 9

1. Minimax değerlerini hesapla.
2. Alfa-betayı soldan sağa elle izle. Hangi yapraklar budanır?
3. Çocukları ve yaprakları yeniden sıralayarak budamayı en çoğa çıkar. Kaç yaprağa bakmak yeterli olur? Knuth–Moore formülüyle karşılaştır.

## A7 — XOX için değerlendirme fonksiyonu (kod) ★★

Bir XOX konumu için şu değerlendirmeyi tanımla: Satır, sütun ve çaprazlardan (8 hat), içinde yalnızca X olan hatları say. İçinde 2 X olan hat 3 puan, 1 X olan hat 1 puan. O için aynısını hesapla ve farkı al.

1. Boş tahtada X ortaya oynadıktan sonra değer kaçtır? Köşeye oynadıktan sonra?
2. Bu fonksiyonla **derinlik sınırlı** minimax yaz. Derinlik 1, 2 ve 4 ile oynayan ajanlar tam minimax'a karşı kaybediyor mu?
3. En sığ hangi derinlikte hiç kaybetmiyor?

## A8 — MCTS'te C ve yineleme sayısı (kod) ★★

`ornekler/mcts_xox.py` ile C ∈ {0; 0,5; 1,4; 5} ve yineleme ∈ {50, 200, 1000} için MCTS'i (X) tam minimax'a (O) karşı 10'ar oyun oynat. Tabloyu doldur (kayıp sayısı). C = 0 ne zaman sorun çıkarır? Çok büyük C'nin bedeli nedir?

## A9 — Beklenti-minimaks ★★

MAX iki hamle arasında seçiyor. a1'den sonra adil bir para atılıyor: yazı → değer 8, tura → değer 4. a2'den sonra hilesiz bir zar atılıyor: 6 gelirse değer 30, diğer sonuçlarda değer 3.

1. İki hamlenin beklenen değerini hesapla. Hangisi seçilir?
2. Tüm değerleri 3 ile çarpıp 1 ekle. Karar değişir mi?
3. Tüm değerlerin karekökünü al (sıra korunur). Karar değişir mi? Neden? Bu dönüşüm nasıl bir "oyuncu kişiliğini" temsil eder?

## A10 — Dört-Bir-Arada'da değerlendirme (kod) ★★★

`ornekler/dortlu_ab.py` içindeki `degerlendir` fonksiyonunun iki sade sürümünü yaz:
- (a) yalnızca merkez sütun bonusu,
- (b) yalnızca "3 taş + 1 boş" pencereleri (tehditler).

Derinlik 3'te bu iki sürümü ve özgün fonksiyonu birbirine karşı (her ikili için 6 oyun, başlayan oyuncu dönüşümlü) oynat. Hangi öznitelik daha önemli? Sonuçları "ağırlıklı doğrusal değerlendirme" fikriyle yorumla.
