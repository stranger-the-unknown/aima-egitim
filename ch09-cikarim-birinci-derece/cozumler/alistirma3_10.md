# Çözümler — A3–A10

Kodla doğrulanan kısımlar: `alistirma7_10_kod.py`.

## A3 — İleri mi geri mi?

**Geri zincirleme.** Tek bir, belirli bir soru var. Geri zincirleme yalnızca soruyla ilgili kurallara ve olgulara iner. İleri zincirleme ise yüzlerce olgudan başlayıp soruyla ilgisiz birçok sonuç türetir. İleri zincirleme, belirli bir soru yokken ya da çok sayıda sorunun aynı ara sonuçları paylaştığı durumlarda (ör. her yeni algıyla bilgiyi güncel tutmak) daha uygundur.

## A4 — Kayıp USB örneği

1. SonGorulen(USB, ?yer) → **Lab3**. Güvenilir tanık Emre, USB'nin sahibi Selin'i Lab3'te görmüş. (Ayla'nın gözlemi Emre hakkındadır, ama USB Emre'nin değil.)
2. IzSur(USB, ?kim) → **Ayla** (ilk yanıt). Zincire giren olgular: Guvenilir(Ayla), Gordu(Ayla, Emre, Koridor), Gordu(Emre, Selin, Lab3), Sahip(USB, Selin). Yani Ayla, USB sahibini görmüş birini (Emre'yi) görmüştür: İz sürülecek ilk kişidir.

## A5 — Neden KB ∧ ¬α?

Çözümleme **çürütme açısından tamdır**: KB ⊨ α ⟺ KB ∧ ¬α karşılanamaz. Çözümleme de karşılanamazlığı her zaman boş tümceyi türeterek gösterebilir. α'yı doğrudan türetmek için tam bir yöntem değildir, ama ¬α'dan çelişki üretmek tamdır.

## A6 — Skolemleştirme

1. ∀x ∃y Anne(y, x) → **Anne(F(x), x)**. y, x'e bağlıdır: "x'in annesi" = F(x).
2. ∃y ∀x Sever(x, y) → **Sever(x, C)**. ∃ en dıştadır; tek bir Skolem **sabiti** yeter.
3. ∀x (∀y Hayvan(y) ⇒ Sever(x, y)) ⇒ ∃y Sever(y, x):
   - ⇒ eliminasyonu: ∀x ¬(∀y ¬Hayvan(y) ∨ Sever(x, y)) ∨ ∃y Sever(y, x)
   - ¬ içe: ∀x (∃y Hayvan(y) ∧ ¬Sever(x, y)) ∨ ∃z Sever(z, x)   (değişkenler standartlaştırıldı)
   - Skolem: (Hayvan(F(x)) ∧ ¬Sever(x, F(x))) ∨ Sever(G(x), x)
   - Dağılma: **(Hayvan(F(x)) ∨ Sever(G(x), x)) ∧ (¬Sever(x, F(x)) ∨ Sever(G(x), x))**. Kitaptaki A1 ve A2 tümcelerinin aynısı.
4. ¬∃x (Öğrenci(x) ∧ ∀y (Ders(y) ⇒ Alır(x, y))):
   - ¬ içe: ∀x ¬Öğrenci(x) ∨ ∃y (Ders(y) ∧ ¬Alır(x, y))
   - Skolem: ¬Öğrenci(x) ∨ (Ders(H(x)) ∧ ¬Alır(x, H(x)))
   - Dağılma: **(¬Öğrenci(x) ∨ Ders(H(x))) ∧ (¬Öğrenci(x) ∨ ¬Alır(x, H(x)))**. H(x): "x'in almadığı ders".

## A7 — Zor birleştirmeler

| Çift | Sonuç | Neden |
|---|---|---|
| P(x, f(x)) — P(f(y), y) | **başarısız** | x/f(y); sonra f(x) = f(f(y)) ile y birleşmeli: occurs check |
| Q(x, y, z) — Q(y, z, A) | **{x/A, y/A, z/A}** | x = y, y = z, z = A zinciri |
| R(g(x), x) — R(y, h(y)) | **başarısız** | y/g(x); sonra x ile h(g(x)): occurs check |
| Knows(x, Mother(x)) — Knows(John, y) | **{x/John, y/Mother(John)}** | |

## A8 — Genişletilmiş suç KB'si

1. İleri zincirleme yine **2 turda** biter. İlk turda iki ülke için satış, silah ve düşmanlık olguları, ikinci turda iki suçlu çıkar: **Smith** ve **West**. Kurallar paralel "tetiklendiği" için KB büyüse de tur sayısı değişmedi. Tur sayısı, türetme zincirinin derinliğine bağlıdır.
2. Geri zincirleme yanıtları **West, Smith** sırasıyla üretir. Suç kuralının ilk öncülü American(x)'tir. Olgular listesinde American(West), American(Smith)'ten önce geldiği için önce x = West denenir ve kanıtlanır, sonra x = Smith. Geri zincirlemenin yanıt sırası, öncüllerin ve olguların sırasına bağlıdır.

## A9 — Marcus

CNF tümceleri:
1. İnsan(Marcus)
2. Pompeili(Marcus)
3. ¬Pompeili(x) ∨ Romalı(x)
4. Hükümdar(Sezar)
5. ¬Romalı(x) ∨ Sadık(x, Sezar) ∨ Nefret(x, Sezar)
6. ¬İnsan(x) ∨ ¬Hükümdar(y) ∨ ¬Suikast(x, y) ∨ ¬Sadık(x, y)
7. Suikast(Marcus, Sezar)
8. Hedefin değili: ¬Nefret(Marcus, Sezar)

Kod **7 adımda** boş tümceyi türetir: ¬Nefret + (5) → Sadık ∨ ¬Romalı; + (3) → Sadık ∨ ¬Pompeili; + (2) → Sadık(Marcus, Sezar); + (6) → ¬Hükümdar(Sezar) ∨ ¬İnsan(Marcus) ∨ ¬Suikast(Marcus, Sezar); + (1), (4), (7) → □.

6. cümleyi FOL'da yazarken dikkat: "yalnızca sadık olmadıkları hükümdarlara" ifadesi ∀x, y İnsan(x) ∧ Hükümdar(y) ∧ Suikast(x, y) ⇒ ¬Sadık(x, y) demektir. Yönü ters yazmak kanıtı imkânsız kılar.

## A10 — Tablolama

1. **Evet, sonlanıyor.** yol(A, q) yanıtları: yol(A, B), yol(A, C), yol(A, D), yol(A, E).
2. Tabloda tek bir alt hedef var: **yol(A, _0)**. Özyineli kuralın ilk öncülü yol(A, y), değişken adları dışında sorgunun kendisidir. Tablolama onu yeniden açmaz, tablodaki (o ana kadarki) yanıtlarını kullanır ve tablo değişmeyene kadar yineler.
3. **Benzerlik:** İkisi de bir sabit noktaya kadar yanıt biriktirir ve döngüye girmez. **Fark:** Tablolama hâlâ hedef güdümlüdür. Yalnızca sorgunun doğurduğu alt hedefler için yanıt hesaplar (burada yalnızca A'dan çıkan yollar). İleri zincirleme ise tüm yolları (B'den ve C'den çıkanlar dahil) türetir. Bu, sihirli kümeler fikrine yakındır.
