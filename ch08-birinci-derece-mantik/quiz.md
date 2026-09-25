# Bölüm 8 — Quiz

Cevaplar dosyanın sonunda.

---

**S1.** FOL'un ontolojik bağlılığı nedir? Önerme mantığınınkinden farkı ne?

**S2.** Bir FOL modeli hangi bileşenlerden oluşur? FOL'da fonksiyonlar neden "toplam" olmalıdır?

**S3.** ∀ ve ∃ niceleyicilerinin "doğal eşleri" hangi bağlaçlardır? Neden?

**S4.** ∀x ∃y Sever(x, y) ile ∃y ∀x Sever(x, y) arasındaki fark nedir? Hangisi diğerini gerektirir?

**S5.** ¬∀x P(x) cümlesini ∃ ile yaz.

**S6.** "Ali'nin en az iki kardeşi vardır" cümlesini doğru yaz. Eşitlik neden gerekli?

**S7.** Veritabanı anlamının üç varsayımı nelerdir? 2 sabit ve 1 ikili ilişkiyle kaç model verirler?

**S8.** ASK ile ASKVARS arasındaki fark nedir?

**S9.** Aksiyom, tanım ve teorem arasındaki fark nedir?

**S10.** Kardeş tanımında x ≠ y neden gereklidir?

**S11.** Bilgi mühendisliğinin yedi adımını say.

**S12.** Kitaptaki tam toplayıcıda toplam = 0 ve elde = 1 veren girişler hangileridir?

---

## Cevaplar

1. Olgular, **nesneler** ve **ilişkiler**. Önerme mantığı yalnızca olgulara bağlıdır.
2. Alan (boş olmayan nesneler kümesi), ilişkiler (demet kümeleri) ve fonksiyonlar. Fonksiyonlar toplam olmalıdır, çünkü her terim bir nesneye gönderme yapmalıdır. SolBacak(Taç) gibi "anlamsız" girdiler için bile bir çıktı nesnesi gerekir.
3. ∀ ile ⇒, ∃ ile ∧. ∀x A(x) ∧ B(x) "herkes hem A hem B" der (çok güçlü); ∃x A(x) ⇒ B(x) ise A olmayan bir nesneyle bile doğru olur (çok zayıf).
4. Birincisi "herkes (belki farklı) birini sever", ikincisi "herkesin sevdiği biri var" der. **İkincisi birincisini gerektirir**, tersi doğru değildir.
5. ∃x ¬P(x)
6. ∃x, y Kardeş(x, Ali) ∧ Kardeş(y, Ali) ∧ x ≠ y. Standart anlamda iki farklı değişken (ya da sabit) aynı nesneyi gösterebilir; x ≠ y olmadan cümle tek bir kardeşle de doğru olur.
7. Benzersiz isimler, kapalı dünya, alan kapanışı. **16** model (2⁴).
8. ASK evet/hayır döndürür (KB ⊨ α mı?). ASKVARS, sorguyu doğru yapan **yerine koymaları** döndürür ({x/John} gibi).
9. Aksiyom: alan hakkında temel kabul. Tanım: bir kavramı diğerleri cinsinden ⇔ ile veren aksiyom. Teorem: aksiyomlardan mantıksal olarak çıkan cümle; KB'ye eklenmesi gerekmez ama çıkarımı hızlandırabilir.
10. Aksi hâlde ortak ebeveyni olan herkes, x = y durumunda kendi kendinin kardeşi olur.
11. (1) Görevi belirle, (2) ilgili bilgiyi topla, (3) sözcük dağarcığına karar ver, (4) genel alan bilgisini kodla, (5) problem örneğini tanımla, (6) sorguları sor, (7) hata ayıkla.
12. **{1, 1, 0}, {1, 0, 1}, {0, 1, 1}.** Tam olarak iki girişin 1 olduğu durumlar (1 + 1 = 10₂).
