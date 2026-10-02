# Çözümler — A3–A10

## A3 — Ata ilişkisi

1. Olgular Ebeveyn(Leyla, Deniz) ve Ebeveyn(Deniz, Ece). Birinci kural (Ebeveyn ⇒ Ata) Ata(Deniz, Ece)'yi verir. İkinci kural (Ebeveyn(x, y) ∧ Ata(y, z) ⇒ Ata(x, z)), x = Leyla, y = Deniz, z = Ece için Ata(Leyla, Ece)'yi verir.
2. Hiçbir kural Ece'yi ata konumuna koyacak bir olgudan başlamaz. Ece'nin çocuğu yoktur, bu yüzden ileri zincirleme hiçbir Ata(Ece, …) türetmez.
3. Mantıksal olarak HAYIR yalnızca "**kanıtlanamadı**" demektir: KB, Ata(Ece, Leyla)'nın yanlış olduğunu da gerektirmez; ¬Ata(Ece, Leyla) hiçbir aksiyomdan çıkmaz. İkisini aynı sayan varsayım **kapalı dünya varsayımıdır** (veritabanı anlamı, §2.5): Doğru olduğu bilinmeyen yanlıştır. Prolog ve veritabanları böyle çalışır ("başarısızlık olarak değil").

## A4 — İki klasik hata

1. ∀x Kral(x) ∧ Kişi(x) her nesnenin hem kral hem kişi olmasını ister. Modelde taç, bacaklar ve Richard kral değildir. Cümle **yanlıştır**.
2. ⇒, öncülü yanlış olduğunda doğrudur. Taç **olmayan** tek bir nesne (ör. Richard) yeter: Taç(Richard) yanlış olduğu için ⇒ doğrudur, ∃ da sağlanır. Cümle, taçla ilgili hiçbir şey söylemeden neredeyse her modelde doğru olur.
3. ∀x Kral(x) ⇒ Kişi(x) ve ∃x Taç(x) ∧ Başında(x, John).

## A5 — Tuzak teşhisi

Evet, yanlış. ∀x ∀y (Ebeveyn(x, y) ∧ Ata(x, y)), **her** x, y çifti için hem Ebeveyn hem Ata doğru olsun der. Yani herkes herkesin ebeveynidir! Doğrusu: ∀x ∀y Ebeveyn(x, y) ⇒ Ata(x, y). ∀ ile ⇒ doğal eştir.

## A6 — Türkçeden FOL'a

1. ∀x Öğrenci(x) ⇒ ∃y Danışman(y, x)
2. ∃d Ders(d) ∧ ¬∃x (Öğrenci(x) ∧ Alır(x, d))
3. ∃x, y Kardeş(x, Ali) ∧ Kardeş(y, Ali) ∧ x ≠ y ∧ ∀z (Kardeş(z, Ali) ⇒ (z = x ∨ z = y))
   "Tam olarak iki" için hem "en az iki" (x ≠ y) hem de "en fazla iki" (∀z …) gerekir.
4. ∀x TıraşEder(Berber, x) ⇔ ¬TıraşEder(x, x)
   Bu cümle **karşılanamaz**: x = Berber koyunca TıraşEder(Berber, Berber) ⇔ ¬TıraşEder(Berber, Berber) çelişkisi çıkar (berber paradoksu). FOL'da doğru yazılmış bir cümle bile tutarsız olabilir.
5. ∀x, y Öğrenci(x) ∧ Öğrenci(y) ∧ x ≠ y ⇒ Numara(x) ≠ Numara(y)

## A7 — Yeğen, enişte, yenge (`alistirma7_yegen_eniste.py`)

Tanımlar:
- ∀x, y Yeğen(x, y) ⇔ ∃k Kardeş(k, y) ∧ Ebeveyn(k, x)
- ∀x, y Enişte(x, y) ⇔ Erkek(x) ∧ ∃w Eş(x, w) ∧ (Hala(w, y) ∨ Teyze(w, y) ∨ (Kardeş(w, y) ∧ Kadın(w)))
- ∀x, y Yenge(x, y) ⇔ Kadın(x) ∧ ∃h Eş(x, h) ∧ (Amca(h, y) ∨ Dayı(h, y) ∨ (Kardeş(h, y) ∧ Erkek(h)))

Kod, örnek ailede Ali'nin Ahmet, Mehmet, Deniz ve Can'ın eniştesi olduğunu (eşi Zeynep, ilk ikisinin kız kardeşi, son ikisinin halası), Elif'in de Zeynep, Mehmet ve Ece'nin yengesi olduğunu çıkarır. **Eş** ilişkisinin simetrik olduğu ayrıca belirtilmelidir (kodda iki yön de eklenir). Aksi hâlde Eş(Ali, Zeynep) biliniyorken Eş(Zeynep, Ali) çıkarılamaz.

## A8 — Peano aritmetiği

1. 1 = S(0), 2 = S(S(0)). Kanıt:
   - +(S(0), S(0)) = S(+(0, S(0)))  (ikinci aksiyom, m = 0, n = S(0))
   - +(0, S(0)) = S(0)               (birinci aksiyom, m = S(0))
   - Yerine koyunca: +(S(0), S(0)) = S(S(0)) ∎
2. Aksiyomlar toplamayı **ilk** argüman üzerinden tanımlar: +(0, m) = m. +(m, 0) = m için m üzerinde **tümevarım** gerekir. Taban: +(0, 0) = 0 (birinci aksiyom). Adım: +(S(k), 0) = S(+(k, 0)) = S(k). Tümevarım ilkesi birinci derece mantıkta tek bir aksiyomla değil, bir **aksiyom şemasıyla** ifade edilir (her formül için bir aksiyom).

## A9 — Wumpus FOL'da

1. **Nedensel:** ∀r Wumpus(r) ⇒ (∀s Komşu(r, s) ⇒ Kokulu(s)) — wumpus komşularını kokutur.
   **Teşhis:** ∀s Kokulu(s) ⇒ ∃r Komşu(r, s) ∧ Wumpus(r) — koku varsa komşuda wumpus vardır.
   Tam tanım için ikisi birlikte: ∀s Kokulu(s) ⇔ ∃r Komşu(r, s) ∧ Wumpus(r).
2. Önerme mantığında her kare için bir kural: 4×4'te **16** cümle (n×n'de n²). FOL'da boyuttan bağımsız **1** cümle (∀s Esintili(s) ⇔ ∃r Komşu(r, s) ∧ Çukur(r)), artı Komşu'nun tek tanımı.
3. ∃x Wumpus(x) ∧ ∀y (Wumpus(y) ⇒ y = x)

## A10 — İki bitlik toplayıcı (`alistirma10_iki_bit.py`)

1. Bağlantılar dosyanın başındaki açıklamada. Kilit bağlantı: Bağlı(Çıkış(2, FA0), Giriş(3, FA1)), yani dalgalı elde.
2. 32 girişin hepsinde toplam doğru (**0 hata**). Örnek: 11₂ + 10₂ + 1 = 6.
3. FA1'in eldesine FA0'ın toplam biti bağlanınca **24** satır hatalı çıkar. Doğru kalan 8 satır, FA0'ın toplam ve elde bitlerinin eşit olduğu girişlerdir (a₀ + b₀ + elde₀ = 0 ya da 3). Bu desen, hatanın yerini daraltmak için güçlü bir ipucudur. Bilgi mühendisliğinin 7. adımı ("hata ayıkla") tam olarak budur.
