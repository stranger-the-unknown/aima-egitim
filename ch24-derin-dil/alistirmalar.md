# Bölüm 24 — Alıştırmalar

Sorular özgündür. Çözümler `cozumler/` klasöründe; önce kendin dene.

Zorluk: ★ kolay · ★★ orta · ★★★ zor

---

## A1 — One-hot'tan gömmeye ★

Sözlükte 100 000 sözcük var (kitaptaki örnek boyut).
1. Bir sözcüğün one-hot vektörü kaç boyutludur? İki farklı sözcüğün one-hot vektörleri arasındaki kosinüs benzerliği nedir? Bu neden sorundur?
2. Her sözcüğe 300 boyutlu bir gömme verirsek gömme tablosunda kaç sayı vardır?
3. Bütün 5-gramların sayımını tutmak için kaç farklı 5-gram olasıdır?

## A2 — Benzetmeyi elle çöz ★

İki boyutlu yapay gömmeler: Atina (1, 3), Yunanistan (1, 1), Oslo (4, 3), Norveç (4, 1), Roma (7, 3), İtalya (7, 1).
1. "Atina Yunanistan'a neyse Oslo neye?" sorusunu Yunanistan − Atina + Oslo vektörünü hesaplayarak yanıtla.
2. "Yunanistan Atina'ya neyse İtalya neye?" için hangi vektörü hesaplarsın?
3. En yakın sözcüğü ararken soruda geçen üç sözcüğü neden aday listesinden çıkarırız?

## A3 — Pencere boyutu (kod) ★★

`gomme.py`'deki derlemde birlikte geçme penceresini 1, 2 ve 4 alarak "kedi"nin en yakın üç komşusunu bul. Pencere büyüdükçe komşular nasıl değişiyor? Küçük ve büyük pencerenin ne tür benzerlikleri yakalaması beklenir?

## A4 — RNN dil modelinin parametreleri ★★

Sözlük v = 10 000 sözcük, gömme boyutu 100, gizli durum boyutu 200 olan bir RNN dil modeli düşün (sapmaları yok say).
1. Gömme tablosu, W_x,z, W_z,z ve W_z,y matrislerinde kaçar parametre vardır? Toplam?
2. Cümle uzunluğu 20'den 200'e çıkarsa parametre sayısı ne olur?
3. Aynı sözlükle bir trigram modelinin tablosu en çok kaç olasılık içerir? Kitabın O(1), O(n) ve O(vⁿ) karşılaştırmasını kendi sözlerinle açıkla.

## A5 — Dikkati elle hesapla (kod ile kontrol) ★★

Kaynak durumları s₁ = (1, 0), s₂ = (0, 1), s₃ = (1, 1); önceki hedef durumu h = (2, 0).
1. Ham puanları rⱼ = h · sⱼ, dikkat olasılıklarını ve bağlam vektörünü hesapla.
2. h = (0, 0) olsaydı ne olurdu?
3. h = (20, 0) olsaydı? Puanların büyüklüğü softmax'ı nasıl etkiler; bunun öz-dikkatteki √d ile ilgisi nedir?

## A6 — Konum kodlaması (kod) ★★

`konum_kodlamasi(50, 32)` ile sin/cos konum vektörleri üret. 10. konumun vektörünün 10, 11, 12, 15 ve 30. konumlarınkiyle iç çarpımını, ayrıca 30. ile 35. konumunkini hesapla.
1. İç çarpım neye bağlı? Neden? (İpucu: sin a sin b + cos a cos b)
2. Kitaptaki transformer konum gömmelerini öğrenir: En çok n uzunluklu girdi için n vektör. Bu yaklaşımın sin/cos kodlamasına göre bir zayıflığı nedir?

## A7 — Öz-dikkatin yapısı ★★

1. Öz-dikkatte W_q = W_k olsaydı rᵢⱼ ile rⱼᵢ arasında nasıl bir ilişki olurdu? Kitap neden öz-dikkatin asimetrik olduğunu vurgular?
2. n sözcüklük bir cümlede bir dikkat başı kaç puan (rᵢⱼ) hesaplar? Cümle 512'den 1024 sözcüğe çıkınca bu sayı kaç katına çıkar?
3. RNN'de n sözcüğü kodlamak için kaç **sıralı** adım gerekir? Öz-dikkatte?

## A8 — Işın genişliği (kod) ★★

`kod_cozme.py`'deki küçük modelle:
1. Açgözlü kod çözücünün ürettiği cümlenin olasılığını elle hesapla.
2. "La puerta de entrada es roja" cümlesinin olasılığını elle hesapla.
3. b = 2 için ışının her adımdaki içeriğini yaz. "La entrada" ile başlayan hipotez ne zaman ışından düşer?
4. b = 1, 2, 3 sonuçlarını kodla karşılaştır.

## A9 — Maskeli dil modeli (kod) ★★

"kedi [MASK] içti" cümlesindeki boşluğu `gomme.py`'deki derlemle tahmin et:
1. Yalnızca soldaki "kedi"yi kullanarak (soldan sağa bir dil modeli gibi) hangi adaylar çıkar?
2. Hem soldaki hem sağdaki sözcüğü kullanınca?
3. Maskeli dil modeli eğitmek için neden etiketli veri gerekmez?

## A10 — Aktarım öğrenmesi tasarla ★★★

Türkçe ürün yorumlarında olumlu/olumsuz duygu sınıflandırması yapacaksın; elinde yalnızca 2 000 etiketli yorum var.
1. Üç yaklaşımı karşılaştır: (a) sıfırdan RNN, (b) önceden eğitilmiş sözcük gömmeleri + küçük bir sınıflandırıcı, (c) önceden eğitilmiş bir transformer + ince ayar.
2. "Bu ürün hiç de kötü değil" cümlesinde hangi yaklaşım neden daha başarılı olur?
3. Türkçenin eklemeli yapısı statik gömmeler için neden ek bir zorluktur?
4. Önceden eğitilmiş modeli kullanmanın iki riskini yaz ve nasıl değerlendireceğini açıkla.
