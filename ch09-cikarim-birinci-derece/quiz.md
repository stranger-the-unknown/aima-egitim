# Bölüm 9 — Quiz

Cevaplar dosyanın sonunda.

---

**S1.** Evrensel ve varoluşsal örnekleme arasındaki fark nedir? EI'da neden yeni bir sabit gerekir?

**S2.** Önermeselleştirme neden pratik değildir? Herbrand teoremi ne söyler?

**S3.** FOL'da gerektirme neden yalnızca "yarı karar verilebilir"dir?

**S4.** UNIFY(Knows(John, x), Knows(y, Mother(y))) sonucu nedir?

**S5.** UNIFY(Knows(John, x), Knows(x, Elizabeth)) neden başarısız olur? Nasıl düzeltilir?

**S6.** En genel birleştirici (MGU) nedir? Knows(John, x) ile Knows(y, z) için MGU'yu yaz.

**S7.** Occurs check nedir? Prolog neden çoğu zaman bunu atlar?

**S8.** Kitaptaki suç örneğinde ileri zincirleme kaç turda biter? Her turda ne türetilir?

**S9.** Mantıksal olarak eşdeğer iki Prolog programı neden farklı davranabilir? Bir çare söyle.

**S10.** ∀x ∃y Anne(y, x) cümlesini Skolemleştir.

**S11.** Destek kümesi stratejisi nedir? Ne zaman tamlığı korur?

**S12.** "Yapıcı olmayan kanıt" ne demektir? Kedi örneğinde nasıl ortaya çıkar?

---

## Cevaplar

1. UI, ∀ değişkenini **herhangi** bir temel terimle değiştirir (birçok kez uygulanabilir). EI ise ∃ değişkenini **bir kez**, KB'de hiç geçmeyen yeni bir sabitle değiştirir. Var olan bir sabit kullanılsaydı, o nesne hakkında gerektirilmeyen bir bilgi eklenmiş olurdu.
2. Fonksiyon sembolleri varken temel terimler sonsuzdur, üstelik gereksiz birçok örnek üretilir. Herbrand: Cümle gerektiriliyorsa önermeselleştirilmiş KB'nin sonlu bir alt kümesiyle kanıtlanabilir. Bu yüzden terim derinliğini artırarak aramak tamdır.
3. Gerektirilen her cümle için kanıt bulan bir algoritma vardır, ama gerektirilmeyen cümlelerde algoritma sonsuza kadar çalışabilir. Genel durumda "hayır" yanıtını garanti eden bir algoritma yoktur (Turing, Church).
4. **{y/John, x/Mother(John)}**
5. İki cümle aynı x adını paylaşır, ama bunlar farklı ∀-cümlelerinden gelir. Değişkenleri ayırınca (x → x17) birleşirler: {x/Elizabeth, x17/John}.
6. Diğer tüm birleştiricileri özelleştirerek elde edebildiğimiz birleştirici. **{y/John, x/z}**
7. Bir değişkenin, kendisini içeren bir terimle birleşmesini engelleyen denetim (x ile f(x)). Maliyeti ifade boyutunda karesel olabildiği için hız uğruna atlanır. Bunun bedeli sağlamlıktan ödün vermektir.
8. **2 tur.** 1: Sells(West, M1, Nono), Weapon(M1), Hostile(Nono). 2: Criminal(West).
9. Prolog'un derinlik öncelikli denetimi kural ve öncül sırasına bağlıdır. Sol özyineli bir kural (yol(X, Z) :- yol(X, Y), …) sonsuz döngüye yol açar. Çareler: sırayı değiştirmek, tablolama ya da ileri zincirleme.
10. **Anne(F(x), x)**
11. Her çözümlemede en az bir ebeveynin hedeften (¬α'dan) türemiş olması. KB'nin kendi içinde tutarlı olması (karşılanabilir olması) koşuluyla tamlığı korur.
12. Bir ∃ sorgusunun doğru olduğu kanıtlanır ama değişkene tek bir değer bağlanmaz. Kedi örneğinde ilk yanıt tümcesi Yanıt(Curiosity) ∨ Yanıt(Jack) olur: Bir katil vardır, ama hangisi olduğu bu kanıtta belirlenmez.
