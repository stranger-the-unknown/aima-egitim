# Bölüm 3 — Alıştırmalar

Sorular özgündür. Çözümler `cozumler/` klasöründe; önce kendin dene.

Zorluk: ★ kolay · ★★ orta · ★★★ zor

---

## A1 — Problem formülasyonu ★

**Senaryo:** 3×3 ızgarada bir robot sol üst köşeden sağ alt köşeye gidecek. Dört yön var (yukarı/aşağı/sol/sağ), her adımın maliyeti 1, engel yok.

Durum uzayını, başlangıç durumunu, eylemleri, geçiş modelini, hedef testini ve eylem maliyetini yaz. Durum temsilini neden böyle seçtiğini tek cümleyle açıkla.

## A2 — Ağaç ve graf araması ★

Arad ile Sibiu arasında iki yönde de gidilebiliyor. Ağaç benzeri aramada ne risk oluşur? Graf araması bunu nasıl önler? İki cümle yeter.

## A3 — Algoritma seçimi ★

Her durum için bir algoritma seç ve bir cümleyle gerekçelendir:

1. Labirent: her adımın maliyeti eşit, en az adımlı yol isteniyor, bellek bol.
2. Yolların km'leri farklı, en kısa yol isteniyor, sezgisel yok.
3. İyi ve kabul edilebilir bir sezgisel var; optimal çözüm isteniyor.
4. Çok büyük bir durum uzayı, çözüm derinliği bilinmiyor, bellek çok kısıtlı.
5. Hızlı bir çözüm yeter, optimal olması şart değil.

## A4 — Romanya kodu ★

`ornekler/romania_arama.py` dosyasını çalıştır (Arad → Bucharest).

1. UCS ile A*'ın maliyetlerini karşılaştır. Aynı mı? Neden?
2. İki algoritmanın genişlettiği düğüm sayılarını yaz. A* neden daha az düğüm genişletiyor?
3. BFS yolu ile UCS yolunu karşılaştır. BFS neden km açısından optimal değil?
4. A* izinde Bucharest ilk kez hangi f değeriyle sınıra giriyor? A* neden onu hemen kabul etmiyor?

## A5 — Başka bir hedef için sezgisel ★★

Hedef Bucharest değil **Iasi** olsun. SLD tablomuz yalnızca Bucharest için var.

1. h = 0 kullanırsak A* hangi algoritmaya dönüşür?
2. Iasi için kabul edilebilir bir sezgisel nasıl elde ederdin? (Fikir yeterli.)
3. "Bucharest'e SLD farkı", yani |SLD(n) − SLD(Iasi)| Iasi için kabul edilebilir bir sezgisel midir? İpucu: üçgen eşitsizliği.

## A6 — IDS'nin bedeli ★★

1. b = 10, d = 5 için N(BFS) ve N(IDS) değerlerini hesapla (erken hedef testi olmadan, yalnızca düğüm sayıları).
2. Aynı hesabı b = 2, d = 10 için yap. IDS'nin "fazladan iş" oranı neden dallanma faktörü küçüldükçe büyüyor?
3. IDS'nin belleği O(bd), BFS'ninki O(b^d). b = 10, d = 12 için her düğüm 1 KB ise iki algoritmanın belleğini karşılaştır.

## A7 — Kabul edilebilir mi, tutarlı mı? ★★

Yönsüz graf: S–A (1), S–B (4), A–B (2), A–G (5), B–G (1). Hedef: G.

| düğüm | S | A | B | G |
|---|---|---|---|---|
| h₁ | 4 | 1 | 1 | 0 |
| h₂ | 4 | 3 | 1 | 0 |

1. Her düğüm için gerçek en ucuz maliyeti h*(n) hesapla.
2. h₁ ve h₂ kabul edilebilir mi? Tutarlı mı? Tutarsızlık varsa hangi kenarda?
3. A*'ı iki sezgiselle de elle çalıştır (ya da `arama.py` ile dene). İkisi de optimal yolu buluyor mu? `en_iyi_oncelikli` fonksiyonunun hangi satırı tutarsız sezgiselde optimalliği kurtarıyor?

## A8 — Üçüncü gevşetme (kod) ★★★

8-bulmacanın kuralından "A ile B komşu olmalı" koşulunu at: *Bir taş, B boşsa, herhangi bir A karesinden B'ye geçebilir.*

1. Bu gevşetilmiş problemin optimal çözüm maliyetini hesaplayan bir fonksiyon yaz. (İpucu: Boşluk, hedefte kendi yerinde değilse, orada olması gereken taşı boşluğa taşı. Yerindeyse, yanlış yerdeki herhangi bir taşı boşluğa taşı.)
2. Kitap örneği (7 2 4 / 5 _ 6 / 8 3 1) için değerini h1 ve h2 ile karşılaştır.
3. Bu sezgisel h1'i baskılar mı? h2'yi baskılar mı? Rastgele durumlarda dene.

## A9 — Ağırlıklı A* deneyi (kod) ★★

`arama.agirlikli_a_yildiz` fonksiyonunu kitaptaki 8-bulmaca örneğinde W = 1; 1,5; 2; 5 için çalıştır (h2 ile). Her W için çözüm uzunluğunu ve üretilen düğüm sayısını tablo hâline getir. Bulunan çözüm her zaman W · C* sınırının altında mı?

## A10 — Kurt, keçi, lahana (kod) ★★

Bir çiftçi kurdu, keçiyi ve lahanayı nehrin karşısına geçirecek. Kayığa çiftçiyle birlikte en fazla bir şey sığıyor. Çiftçi yokken kurt keçiyi, keçi de lahanayı yer.

1. Problemi `arama.Problem` alt sınıfı olarak formüle et. Durum temsili ne olmalı? Kaç durum var, kaçı "güvenli"?
2. BFS ile en kısa çözümü bul ve adımları yazdır.
3. Bu problemde BFS ile UCS aynı sonucu verir mi? Neden?
