# Çözümler — A3–A10

Kodla doğrulanan kısımlar: `alistirma6_10_kod.py`.

## A3 — Ontoloji örneği

1. is_a("Kedi", "Hayvan") → **EVET** (Kedi ⊂ Memeli ⊂ Hayvan; alt küme geçişlidir).
2. is_a("Tekir", "Memeli") → **EVET**. Tekir ⊂ Kedi ⊂ Memeli. Script bunu "Tekir alt kategorisi" bölümünde zaten gösterir.

## A4 — Şeyler ve maddeler

| | Tür | İçsel özellik (parçalara geçer) | Dışsal özellik (geçmez) |
|---|---|---|---|
| Çay | madde | tat, renk | miktar |
| Bir bardak çay | şey | (içindeki çayın) tadı | hacim (bir bardak) |
| Kum | madde | tane sertliği, bileşim | kütle |
| Bir kum tanesi | şey | bileşim | boyut, şekil |
| Altın | madde | yoğunluk, erime noktası | ağırlık |
| Bir altın bilezik | şey | ayar (altın oranı) | şekil, ağırlık |

Test: Nesneyi ikiye böl. İki parça da aynı türden mi? Çay → çay (madde); bir bardak çay → iki yarım bardak (şey değil).

## A5 — Tek tip bir FOL yığını

1. **Tekrar ve tutarsızlık:** "Her memeli sıcakkanlıdır" gibi genel bilgiler her nesne için tekrar tekrar yazılır. Biri güncellenip diğeri unutulunca KB çelişkili hâle gelir. Kategoriler bu bilgiyi tek bir yerde tutar ve kalıtımla dağıtır.
2. **Verimsiz çıkarım ve yeniden kullanılamazlık:** Ortak bir yapı olmadan çıkarım motoru ilgili bilgiyi bulmak için tüm cümleleri taramak zorundadır. Başka bir alanla birleştirmek de neredeyse imkânsızdır. Ortak bir üst ontoloji, farklı bilgi tabanlarının aynı kavramlar üzerinde anlaşmasını sağlar.

## A6 — Olay hesabı

Yeni olaylarla:
- **İçeride(Ali):** t = 3–6 ve 9–11'de doğru. 6'da çıkınca 7'den itibaren yanlış, 8'de girince 9'dan itibaren tekrar doğru.
- **Açık(Kapı):** t = 2–3 ve 6–13'te doğru.

t = 10'da **Açık(Kapı) doğru**. Kapı 5'te açıldı ve arada onu kapatan bir olay olmadı. Bunu belirleyen, olay hesabının atalet aksiyomudur: T(f, t) ⇐ Happens(e, t₁) ∧ Initiates(e, f, t₁) ∧ t₁ < t ∧ ¬∃e', t₂ (Happens(e', t₂) ∧ Terminates(e', f, t₂) ∧ t₁ < t₂ < t).

**Önkoşul:** Happens(EveGir(a), t) ⇒ T(Açık(Kapı), t). Olay hesabında bu, olayların olabilmesi için bir kısıttır. Bir planlayıcı, bu aksiyomu ihlal eden olay dizilerini dışlar.

## A7 — Allen ilişkileri

1. I. Dünya Savaşı (1914–1918) — Vahdettin'in saltanatı (1918–1922): **Meet** (biri bittiği yıl diğeri başlıyor).
2. Atatürk'ün cumhurbaşkanlığı (1923–1938) — hayatı (1881–1938): **Finishes** (ikisi de 1938'de biter). Ayrıca Baş(hayat) < Baş(cumhurbaşkanlığı) olduğu için Allen'ın özgün tanımındaki "finishes" da geçerlidir.
3. Atatürk'ün hayatı (1881–1938) — İnönü'nün cumhurbaşkanlığı (1938–1950): **Meet**.
4. **Hayır.** Overlap(i, j) için i'nin önce başlaması gerekir. Doğru olan **Overlap(Kanuni, Sinan)**'dır: 1520 < 1538 < 1566 < 1588.

## A8 — Olası dünyalar

1. Ayşe'nin erişebildiği dünyalar: {(Mayıs, 1), (Mayıs, 2), …, (Mayıs, 31)}. Gerçek dünya (Mayıs, 14) bunların içindedir (bilgi doğrudur).
2. K(Ay = Mayıs) **doğru**; K(Gün = 14) **yanlış**; K(Gün ≤ 31) **doğru** (her dünyada); ∃g K(Gün = g) **yanlış** (Ayşe günü "bilmiyor", de re).
3. "Ayın ilk yarısında" bilgisiyle erişilebilir dünyalar {1, …, 15} olur. K(Gün ≤ 15) artık doğrudur, ama gün hâlâ bilinmez. Yeni bilgi = erişilebilir dünyaları **eleme**.

## A9 — Özgüllük

1. Anormal yüklemleriyle:
   - Öğrenci(x) ∧ ¬Ab₁(x) ⇒ Yetişkin(x)
   - LiseÖğrencisi(x) ∧ ¬Ab₂(x) ⇒ ¬Yetişkin(x)
   - LiseÖğrencisi(x) ⇒ Öğrenci(x); LiseÖğrencisi(Ali)

   Ab₁ ve Ab₂ sınırlandırılınca **iki** tercih edilen model vardır: {Ab₁, ¬Yetişkin} ve {Ab₂, Yetişkin}. Yetişkin(Ali) **bilinmiyor**. Nixon elmasının aynısıdır.
2. **Özgüllük ilkesi:** Daha özel kategorinin (lise öğrencisi) varsayılanı önceliklidir, yani önce Ab₂ en aza indirilir. Tek model kalır: {Ab₁, ¬Yetişkin}. Yetişkin(Ali) **hayır**. Anlamsal ağlar bu ilkeyi "en yakın atadan miras al" kuralıyla otomatik uygular. Nixon'da ise iki kategori birbirinin alt kümesi olmadığı için özgüllük bir çözüm sunmaz.

## A10 — ATMS etiketleri

1. IslakÇim: **{Yağmur}, {Sulama}**. KayganYol: **{Yağmur}**. Şemsiye: **{Yağmur}**.
2. Gökkuşağı: **{Güneş, Yağmur}, {Güneş, Sulama}**. Etiketler kurallar boyunca birleşir: IslakÇim'in her ortamı Güneş ile birleştirilir.
3. JTMS tek bir güncel inanç durumunu tutar. Farklı varsayım kümeleri arasında geçiş yaparken ("yağmur yağsaydı?", "sulama yapılsaydı?") her seferinde yeniden hesaplar. ATMS ise tüm ortamları **aynı anda** tutar: "Hangi varsayımlar altında Gökkuşağı doğru?" sorusu bir tablo bakışıyla yanıtlanır. Birçok alternatif senaryonun karşılaştırıldığı teşhis ve planlama işlerinde avantajlıdır. Etiketler aynı zamanda **açıklamadır**: Gökkuşağı'nın bir açıklaması "Güneş ve Sulama"dır.
