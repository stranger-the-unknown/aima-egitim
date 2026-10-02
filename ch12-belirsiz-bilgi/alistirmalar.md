# Bölüm 12 — Alıştırmalar

Sorular özgündür. Çözümler `cozumler/` klasöründe; önce kendin dene.

Zorluk: ★ kolay · ★★ orta · ★★★ zor

---

## A1 — Bayes elle ★

Bir fabrikada parçaların %2'si kusurlu: P(K) = 0.02. Sensör, kusurlu parçada %95 olasılıkla uyarı veriyor: P(U | K) = 0.95. Sağlam parçada da %10 olasılıkla yanlış uyarı veriyor: P(U | ¬K) = 0.10.
Uyarı görüldüğünde P(K | U) nedir? Önce sezgisel bir tahmin yap, sonra adım adım hesapla.

## A2 — Marjinalleştirme ve koşullama ★

| A | B | P |
|---|---|---|
| T | T | 0.12 |
| T | F | 0.18 |
| F | T | 0.28 |
| F | F | 0.42 |

P(A = T), P(B = T) ve P(B = T | A = T)'yi hesapla.

## A3 — Bağımsızlık ★

A2'deki A ve B bağımsız mı? Tek bir hücreyi kontrol etmek yeterli mi, yoksa dört hücrenin hepsine mi bakmalısın? (İpucu: Boole değişkenlerinde tek hücre yeter mi? Gerekçelendir.)

## A4 — Diş hekimi tablosu ★★

`ornekler/dis_hekimi.py`'deki tablodan elle hesapla, sonra kodla doğrula:
1. P(toothache)
2. P(Cavity | catch)
3. P(toothache | cavity)
4. P(cavity | toothache ∨ catch)

## A5 — Kendi Hollanda kitabın ★★

Bir ajanın inançları: P(a) = 0.5, P(b) = 0.5, P(a ∧ b) = 0.4, P(a ∨ b) = 0.5.
1. Hangi aksiyom çiğneniyor? P(a ∨ b) kaç olmalıydı?
2. Ajana karşı her sonuçta kazandıran bir bahis kombinasyonu kur. (İpucu: "fiyatı p olan, önerme doğruysa 1$ ödeyen bilet" diye düşün. 1[a ∨ b] = 1[a] + 1[b] − 1[a ∧ b] eşitliğini kullan.)

## A6 — Salgın ★★

Menenjit örneğinde P(s) = 0.01 veriliyor.
1. P(s | ¬m) kaç olmalı ki P(s) = 0.01 olsun?
2. Salgında P(m) 10 katına çıkıyor. P(s | m) ve P(s | ¬m) değişmiyor. Yeni P(s) ve P(m | s) ne olur?
3. P(m | s) tam 10 katına çıktı mı? Neden?

## A7 — Naif Bayes ile haber sınıflandırma ★★

İki kategori: P(spor) = 0.4, P(ekonomi) = 0.6. Kelime olasılıkları P(HasWord | Kategori):

| Kelime | spor | ekonomi |
|---|---|---|
| gol | 0.5 | 0.02 |
| maç | 0.6 | 0.05 |
| borsa | 0.01 | 0.4 |

1. "gol" ve "maç" geçen, "borsa" geçmeyen bir belgenin kategori dağılımı nedir?
2. "borsa" kelimesine hiç bakmasaydık (gözlenmemiş) sonuç ne olurdu? Neden gözlenmeyen kelimeler hesaptan çıkar?
3. Eğitim verisinde ekonomi haberlerinde "gol" hiç geçmemiş olsun: P(gol | ekonomi) = 0. "gol" ve "borsa" geçen bir ekonomi haberi ne olarak sınıflandırılır? Sorun ne, nasıl düzeltilir?

## A8 — Havalimanı: en yüksek beklenen fayda (kod) ★★

Planlar ve uçağı yakalama olasılıkları (varsayım): A60: 0.70, A90: 0.97, A120: 0.99, A180: 0.999, A1440: 0.9999. Yol ortalama 55 dk. Havalimanında beklenen her dakikanın maliyeti 1 birim.
1. Uçağı yakalamanın değeri 1000 birimse hangi plan seçilmeli?
2. Uçuş çok önemliyse (değer 10 000) hangisi?
3. Bu, "rasyonel seçim yalnızca olasılıklara bağlıdır" iddiası hakkında ne söyler?

## A9 — Wumpus'ta önselin etkisi (kod) ★★★

`ornekler/wumpus_olasilik.py`'deki kitap durumu için çukur önseli p = 0.01, 0.2 ve 0.5 iken P(P₁,₃) ve P(P₂,₂)'yi hesapla.
1. p çok küçükken P(P₂,₂) neden 1'e yaklaşır?
2. p = 0.5'te sonuçları sezgisel olarak açıkla.
3. [4,4]'teki çukurun [1,3] hakkındaki inancı neden etkilemediğini koşullu bağımsızlıkla açıkla.

## A10 — Naif varsayım bozulunca (kod) ★★★

Diş hekimi tablosunun cavity satırını şöyle değiştir: (t, c) = 0.14, (t, ¬c) = 0, (¬t, c) = 0.04, (¬t, ¬c) = 0.02. ¬cavity satırı aynı kalsın.
1. Toothache ve Catch, Cavity verildiğinde hâlâ koşullu bağımsız mı?
2. P(cavity | toothache, catch)'i hem tam tablodan hem naif Bayes formülüyle hesapla. Fark ne kadar?
3. Naif Bayes'in varsayımı yanlışken bile neden iyi çalışabildiğini bu sonuçla tartış.
