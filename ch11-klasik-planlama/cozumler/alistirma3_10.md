# A3–A10 çözümleri

Kodlu kısımlar: `python cozumler/alistirma4_10_kod.py` (bölüm klasöründen).

---

## A3 — İleri ve geri, elle

1. `Load(C1, P1, SFO)` önkoşulları sağlanıyor (C1 ve P1 SFO'da). At(C1, SFO) silinir, In(C1, P1) eklenir:
   `{In(C1,P1), At(C2,JFK), At(P1,SFO), At(P2,JFK)}` + değişmeyen statik atomlar (Cargo, Plane, Airport).
2. g' = (g − EKLE) ∪ ÖN:
   `{At(C2,SFO)} ∪ {In(C1,P1), At(P1,JFK), Cargo(C1), Plane(P1), Airport(JFK)}`.
   Yani: "C2 SFO'da, C1 P1'in içinde ve P1 JFK'de" olan her durumdan tek adımda hedefe varılır.
3. **Hayır.** Fly(P1, SFO, JFK) yalnızca At(P1, JFK) ekler. Bu atom hedefte yok. İlgili bir eylem, hedefin bir atomunu eklemelidir. (Fly, 2. maddedeki gerilemiş hedef için ise ilgilidir: At(P1, JFK)'yi ekler.)

## A4 — Unutulan önkoşul

Planlayıcı 2 adımlık bir plan bulur: `Remove(Spare,Trunk), PutOn(Spare,Axle)`. Bu plan patlak lastiği aksta bırakıp yedeği de aynı aksa takar. Fiziksel olarak imkânsızdır.

Ders: **Planlayıcı yalnızca modelin söylediğini bilir.** Eksik bir önkoşul, gerçekte geçersiz ama modelde "daha kısa" olan planlara kapı açar. Planlayıcı da onları seve seve bulur. Planlar yanlış çıkınca önce modele bakmak gerekir.

**LeaveOvernight:** Bu problemde hiçbir plana yaramaz. Bütün At atomlarını siler. Hiçbir eylem, silinmiş bir lastiği geri getiremez (Remove ve PutOn, lastiğin bir yerde olmasını gerektirir). Bu yüzden LeaveOvernight'tan sonra hedefe hiç ulaşılamaz.

## A5 — Sussman anomalisi

1. Önce On(A, B): `MoveToTable(C,A), Move(A,Table,B)`. Şimdi B'yi C'nin üstüne koymak için B serbest olmalı, ama A onun üstünde. `MoveToTable(A,B), Move(B,Table,C)` ile On(B, C) sağlanır ama On(A, B) **bozulur**.
2. Önce On(B, C): `Move(B,Table,C)`. Artık kule B-C-A (üstten alta). A'yı almak için önce B'yi, sonra C'yi indirmek gerekir: On(B, C) **bozulur**.
3. Doğru plan: `MoveToTable(C,A), Move(B,Table,C), Move(A,Table,B)`. İlk alt hedefin (On(A, B)) çözümüne, ikinci alt hedef için bir hazırlık adımı (B'yi C'ye koymak) **araya girmelidir**. Alt hedefleri sırayla ve birbirinden habersiz çözen bir planlayıcı bu serpiştirmeyi yapamaz.

## A6 — Sezgisellerin kabul edilebilirliği

1. `Load(C1,P1,SFO), Load(C2,P1,SFO), Fly(P1,SFO,JFK), Unload(C1,P1,JFK), Unload(C2,P1,JFK)`: **h\* = 5**.
2. Gevşetilmiş maliyetler: In(C1, P1) = In(C2, P1) = At(P1, JFK) = 1.
   - At(C1, JFK): Unload(C1, P1, JFK) ile. h_max: 1 + max(1, 1) = 2. h_add: 1 + (1 + 1) = 3. C2 için de aynı.
   - **h_max** = max(2, 2) = **2** ≤ 5.
   - **h_add** = 3 + 3 = **6 > 5**. Fly(P1, SFO, JFK) iki kargoya birden hizmet ediyor, ama h_add onu her hedef için ayrı ayrı sayıyor. Paylaşılan alt planlar iki kez sayılınca h_add kabul edilemez olur.
   - (Seviye toplamı: 2 + 2 = 4. Burada h\*'ın altında ama genelde kabul edilebilir değildir.)
3. Gerçek problemin her çözümü, gevşetilmiş problemin de bir çözümüdür (silme listesi olmayınca hiçbir şey bozulmaz). Gevşetilmiş bir planda her atom a için: a'yı ilk üreten eylemden önce o eylemin bütün önkoşulları üretilmiş olmalı. Tümevarımla, a'nın üretilmesi en az "en pahalı önkoşulun maliyeti + 1" adım sürer. Bu tam olarak h_max'ın hesabıdır. Yani h_max ≤ h⁺ ≤ h\*.

## A7 — Kahve robotu

```python
Sema("Git", ["a", "b"], ["Robot(a)", "Bitisik(a,b)"], ekle=["Robot(b)"], sil=["Robot(a)"])
Sema("KahveYap", ["y"], ["Robot(y)", "Makine(y)", "ElBos"], ekle=["Tutuyor"], sil=["ElBos"])
Sema("Birak", ["y"], ["Robot(y)", "Tutuyor"], ekle=["KahveVar(y)", "ElBos"], sil=["Tutuyor"])
```

1. `Bitisik` ve `Makine` statiktir; temellendirme 8 eylem bırakır.
2. **6 adım:** Git(Ofis,Koridor), Git(Koridor,Mutfak), KahveYap(Mutfak), Git(Mutfak,Koridor), Git(Koridor,Ofis), Birak(Ofis).
3. **12 adım** (6 + 6). Tek fincan taşınabildiği için robot mutfağa iki kez gider. Genişletilen düğüm: BFS 62, h_max 48, h_add 27. h_add en az düğümü genişletti ve yine en kısa planı buldu. Bu garanti değildir (A6).

## A8 — Çizelgeyi değiştir

1. Araba 1: 30 + 30 + 10 = 70. Araba 2: 40 + 15 + 10 = 65. Toplam **70 dk**. Kritik yol artık **Araba 1**'in işleridir (MotorTak1, TekerTak1, Denetle1). Araba 2'nin 5 dk bolluğu var.
2. **95 dk.** MotorTak1 önce (0–30), MotorTak2 sonra (30–70). TekerTak2, MotorTak2'yi beklemek zorunda: 70–85, Denetle2 85–95. Ters sıra (önce MotorTak2) 110 dk verir. Yine kısa iş önce.
3. **Değişmez.** Denetimler 60–70 ve 85–95 arasında; hiç çakışmıyorlar.

## A9 — Metro inceltmesi

```python
ILKEL["Yürü(Ev,İstasyon)"] = (lambda d: d["yer"] == "Ev", lambda d: {**d, "yer": "İstasyon"})
ILKEL["Metro(İstasyon,Havalimanı)"] = (lambda d: d["yer"] == "İstasyon" and d["kart"], ...)
INCELTMELER["Git(Ev,Havalimanı)"].append(["Yürü(Ev,İstasyon)", "Metro(İstasyon,Havalimanı)"])
```

1. `Yürü(Ev,İstasyon), Metro(İstasyon,Havalimanı)`. Araba yok, taksi için para yetmiyor; üçüncü inceltme işe yarıyor.
2. Plan yok. Üç inceltmenin hiçbiri uygulanamıyor.
3. `Sür(Ev,Otopark), Servis(Otopark,Havalimanı)`. Genişlik öncelikli arama inceltmeleri listedeki sırayla dener. İlk geçerli plan araba planıdır. Hiyerarşik arama burada "ilk bulduğu" planı döndürür. Maliyeti (para, süre) dikkate almak için, eylemlere maliyet verip en ucuz öncelikli arama yapmak gerekir.

## A10 — Geri arama

1. Alt hedef g = (poz, neg). Eylem a:
   - **İlgili:** EKLE(a) ∩ poz ≠ ∅ ya da SİL(a) ∩ neg ≠ ∅ (bir hedefe katkı yapar).
   - **Tutarlı:** SİL(a) ∩ poz = ∅ ve EKLE(a) ∩ neg = ∅ (hiçbir hedefi bozmaz).
   - **Gerileme:** poz' = (poz − EKLE(a)) ∪ ÖN(a), neg' = (neg − SİL(a)) ∪ ÖN_DEĞİL(a). poz' ∩ neg' ≠ ∅ ise bu alt hedef imkânsızdır, atılır.
   - Başlangıç durumu s₀ için poz ⊆ s₀ ve neg ∩ s₀ = ∅ ise plan bulunmuştur. Plan, bulunan eylemlerin **ters** sırasıdır (her eylem planın başına eklenir).
2. Üç problemde de doğru ve en kısa planlar çıkar (yedek lastik 3, bloklar 3, hava kargo 6 adım). Sıralar ileri aramanınkinden farklı olabilir.
3. Geri arama bu problemlerde **daha çok** düğüm genişletir (yedek lastik 10'a karşı 5, bloklar 113'e karşı 12, hava kargo 301'e karşı 56). Neden: Gerilemiş alt hedefler, gerçek durumların **kısmi betimleridir** ve birçoğu hiçbir ulaşılabilir duruma karşılık gelmez. Örneğin hava kargoda At(P1, SFO) ∧ At(P1, JFK) içeren bir alt hedef üretilebilir. Uçak aynı anda iki yerde olamaz, ama kodumuz bunu bilmez. İleri arama ise yalnızca gerçekten ulaşılabilir durumları üretir. Pratikte geri aramaya **durum kısıtları** (değişmezler, mutex'ler) eklenerek bu tür alt hedefler budanır. Ya da, kitabın da belirttiği gibi, iyi sezgisellerle ileri arama tercih edilir.
