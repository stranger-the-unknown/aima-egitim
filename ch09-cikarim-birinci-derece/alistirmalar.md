# Bölüm 9 — Alıştırmalar

Sorular özgündür. Çözümler `cozumler/` klasöründe; önce kendin dene.

Zorluk: ★ kolay · ★★ orta · ★★★ zor

---

## A1 — Önermeselleştirme ★

Alan D = {a, b}. ∀x ∃y R(x, y) cümlesini önerme mantığına (∧ / ∨ açılımıyla) çevir. Kaç atomik önerme sembolü gerekir?

## A2 — Elle birleştirme ★

Sonuçları yaz (ya da "başarısız"):
1. f(x) ve f(Ankara)
2. f(x) ve g(Ankara)
3. x ve f(x)

`python ornekler/birlesim_unification.py` ile kontrol et.

## A3 — İleri mi geri mi? ★

Yüzlerce olgu ve onlarca kural içeren bir KB'ye tek bir soru soruyorsun ("USB en son nerede görüldü?"). İleri mi geri zincirleme mi tercih edersin? Neden?

## A4 — Kayıp USB örneği ★

```bash
python ornekler/geriye_zincir.py
```

1. SonGorulen(USB, ?yer) hangi yeri üretir?
2. IzSur(USB, ?kim) kimleri döndürür? Hangi olgular zincire girer?

## A5 — Neden KB ∧ ¬α? ★

KB ⊨ α'yı denetlerken neden KB ∧ ¬α üzerinde çelişki (boş tümce) aranır? Bir cümleyle açıkla.

## A6 — Skolemleştirme ★★

Her cümleyi CNF'ye çevir; Skolem sabitlerini ve fonksiyonlarını açıkça göster:
1. ∀x ∃y Anne(y, x)
2. ∃y ∀x Sever(x, y)
3. ∀x (∀y Hayvan(y) ⇒ Sever(x, y)) ⇒ ∃y Sever(y, x)
4. ¬∃x (Öğrenci(x) ∧ ∀y (Ders(y) ⇒ Alır(x, y)))

## A7 — Zor birleştirmeler ★★

1. UNIFY(P(x, f(x)), P(f(y), y))
2. UNIFY(Q(x, y, z), Q(y, z, A))
3. UNIFY(R(g(x), x), R(y, h(y)))
4. UNIFY(Knows(x, Mother(x)), Knows(John, y))

Her biri için θ'yı ya da başarısızlık nedenini yaz. `fol_cikarim.birlestir` ile doğrula.

## A8 — Suç KB'sini genişlet (kod) ★★

`ornekler/suclu_bati.py`'deki KB'ye şunları ekle:
- Amerika'nın düşmanı başka bir ülke: Enemy(Nopo, America), Owns(Nopo, R1), Rocket(R1)
- Roketler de silahtır: Rocket(x) ⇒ Weapon(x)
- Nopo'nun roketlerini Amerikalı Smith satmıştır: Rocket(x) ∧ Owns(Nopo, x) ⇒ Sells(Smith, x, Nopo); American(Smith)

1. İleri zincirleme kaç turda biter? Hangi suçlular bulunur?
2. Geri zincirleme Criminal(x) için hangi yanıtları hangi sırayla üretir?

## A9 — Çözümleme ile kanıt (kod) ★★★

Aşağıdaki bilgileri FOL'a, sonra CNF'ye çevir ve çözümlemeyle "Marcus, Sezar'dan nefret ediyordu" sonucunu kanıtla:

1. Marcus bir insandı.
2. Marcus Pompeiliydi.
3. Bütün Pompeililer Romalıydı.
4. Sezar bir hükümdardı.
5. Her Romalı ya Sezar'a sadıktı ya da ondan nefret ediyordu.
6. İnsanlar yalnızca sadık olmadıkları hükümdarlara suikast girişiminde bulunur.
7. Marcus, Sezar'a suikast girişiminde bulundu.

## A10 — Tablolama (kod) ★★★

`ornekler/prolog_yol.py`'deki (b) programı için basit bir **tablolama** yaz: Her alt hedef (değişken adlarından bağımsız biçimiyle) tabloya bir kez girer. Yanıtlar, tablo değişmeyene kadar tekrar tekrar hesaplanır.
1. (b) programı artık sonlanıyor mu? yol(A, q) hangi yanıtları veriyor?
2. Tabloda hangi alt hedefler yer aldı?
3. Tablolama ile ileri zincirleme arasındaki benzerlik ve fark nedir?
