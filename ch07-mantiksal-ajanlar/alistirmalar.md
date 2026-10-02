# Bölüm 7 — Alıştırmalar

Sorular özgündür. Çözümler `cozumler/` klasöründe; önce kendin dene.

Zorluk: ★ kolay · ★★ orta · ★★★ zor

---

## A1 — TELL / ASK ★

Bilgi tabanlı ajanın bir turunu dört adımda yaz: algı → ? → ? → eylem. TELL ve ASK nereye girer?

## A2 — Gerektirme ★

Semboller P, Q. KB = { P, P ⇒ Q }.

1. KB ⊨ Q mudur? Modellerle düşün.
2. KB ⊨ P ∧ Q mudur?
3. KB ⊨ ¬P midir?

## A3 — "Bilinmiyor" yanıtı ★

```bash
python ornekler/onerme_mantigi.py
```

1. ASK(Bulut) neden "bilinmiyor"? KB'nin doğru olduğu modelleri yazarak açıkla.
2. KB'ye hangi tek cümleyi eklersen ASK(Bulut) "evet" olur? Hangisini eklersen "hayır" olur?
3. "P ⇒ Q ile Q ⇒ P eşdeğer değildir" iddiasını bir karşı modelle göster.

## A4 — CNF dönüşümü ★★

(A ∨ B) ⇒ (C ∧ ¬D) cümlesini adım adım CNF'ye çevir. Sonucu `onerme.cnf` ile doğrula.

## A5 — Model sayısı ★

1. 5 önerme sembolü varsa kaç model vardır?
2. Kitaptaki R1–R5 KB'si kaç sembol içerir, kaç model? KB kaç modelde doğrudur?
3. 4×4 Wumpus dünyasının tamamı için her karede P, W, B, S sembolleri kullanılırsa kaç sembol ve kaç model olur? Doğruluk tablosu neden pratik değildir?

## A6 — Elle çözümleme ★★

R1–R5 KB'sinden **P22 ∨ P31** cümlesini çözümleme ile kanıtla:
1. Gerekli kuralları CNF'ye çevir.
2. Sorgunun değilini ekle.
3. Boş tümceye giden çözümleme adımlarını yaz. Kodla karşılaştır (`onerme.cozumleme`).

## A7 — İleri ve geri zincirleme (kod) ★★

Kitaptaki Horn KB'sine konuyla ilgisiz 10 kural ekle: A ⇒ X1, X1 ⇒ X2, …, X9 ⇒ X10.

1. İleri zincirleme Q'yu bulana kadar kaç sembol çıkarıyor? Eklemeden önce kaçtı?
2. Geri zincirleme kaç alt hedefe bakıyor? Eklemeden önce kaçtı?
3. Hangi durumlarda ileri zincirleme tercih edilir?

## A8 — Doğruluk tablosu ve DPLL (kod) ★★

`ornekler/wumpus_mantik.py` içindeki tam 4×4 bilgi tabanında (fizik kuralları + [1,1], [2,1], [1,2] algıları):
1. Kaç farklı sembol var? Doğruluk tablosu kaç model denerdi?
2. "KB ⊨ W13" sorusu için DPLL kaç çağrıda karar veriyor?
3. Birim tümce ve saf sembol sezgiselleri kapatılınca çağrı sayısı ne oluyor?

## A9 — WalkSAT'ta p (kod) ★★

n = 30 sembollü, m/n = 4,0 oranında 20 **karşılanabilir** rastgele 3-CNF cümlesi üret (DPLL ile kontrol et). WalkSAT'ı p = 0; 0,2; 0,5; 0,8; 1,0 ile 5000 çevirmeye kadar çalıştır. Başarı sayısını ve medyan çevirme sayısını tablo yap. Uç değerlerin (p = 0 ve p = 1) sorunu nedir?

## A10 — Ardıl durum aksiyomları ★★★

1. HaveArrow^{t+1} için ardıl durum aksiyomunu yaz.
2. WumpusAlive^{t+1} için yaz. (İpucu: Wumpus, ok atıldığında ve ok onu vurduğunda ölür. "Vurmak" için bir yardımcı ifade kullanabilirsin.)
3. Ajan [1,1]'deyken ve doğuya bakarken "İleri" eyleminin L^{t+1}_{1,1} üzerindeki etkisini ardıl durum aksiyomu biçiminde yaz.
4. Etki aksiyomları + çerçeve aksiyomlarıyla kaç aksiyom gerekirdi (m eylem, n akışkan)? Ardıl durum aksiyomlarıyla kaç?
