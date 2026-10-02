# Bölüm 10 — Bilgi temsili

> **Kitapta:** AIMA 4. baskı, Bölüm 10 *"Knowledge Representation"*.
> Önce kitabı oku, sonra bu notlarla pekiştir. Metin özgündür; kitaptan alıntı yoktur.

## Bu bölümün haritası

| Kitap alt bölümü | Bu nottaki karşılığı | Kod |
|---|---|---|
| 10.1 Ontological Engineering | §1 Üst ontoloji, genel amaçlı ontolojiler | — |
| 10.2 Categories and Objects | §2 Kategoriler, taksonomi, parçalar, ölçüler, şeyler ve maddeler | `ontoloji_mini.py`, `anlamsal_ag.py` |
| 10.3 Events | §3 Olay hesabı, süreçler, zaman aralıkları | `olay_hesabi.py` |
| 10.4 Mental Objects and Modal Logic | §4 Önermesel tutumlar, göndergesel geçirimsizlik, olası dünyalar | `modal_bilgi.py` |
| 10.5 Reasoning Systems for Categories | §5 Anlamsal ağlar, betimleme mantıkları | `anlamsal_ag.py` |
| 10.6 Reasoning with Default Information | §6 Sınırlandırma, varsayılan mantık, doğruluk bakımı | `varsayilan_akil.py`, `anlamsal_ag.py` |

## Öğrenme hedefleri

1. Genel amaçlı bir ontolojinin yapısını ve kategorilerin FOL'da nasıl temsil edildiğini açıklamak.
2. Olay hesabıyla zamanla değişen dünyayı modellemek; Allen aralık ilişkilerini kullanmak.
3. Önermesel tutumlar için neden modal mantık gerektiğini göstermek.
4. Anlamsal ağlarda kalıtımı ve varsayılanların geçersiz kılınmasını uygulamak.
5. Monoton olmayan akıl yürütmeyi (sınırlandırma, varsayılan mantık) ve doğruluk bakım sistemlerini açıklamak.

---

## 1. Ontoloji mühendisliği

**Ontoloji**, bir alanın kavramlarını ve aralarındaki ilişkileri düzenler. **Üst ontoloji**, en genel kavramlardan başlar ve özel kavramlara iner:

```text
Her Şey
├── Soyut Nesneler: Kümeler, Sayılar, Temsil Nesneleri (Kategoriler, Cümleler, Ölçüler: Zamanlar, Ağırlıklar)
└── Genelleştirilmiş Olaylar
    ├── Aralıklar (Anlar)
    ├── Yerler
    ├── Fiziksel Nesneler: Şeyler (Hayvanlar, Ajanlar, İnsanlar), Maddeler (Katı, Sıvı, Gaz)
    └── Süreçler
```

Genel amaçlı bir ontoloji, herhangi bir alanda **özel eklerle** kullanılabilmeli ve farklı alanları birleştirebilmelidir. Pratikte bu çok zordur. Farklı yaklaşımlar: elle yazılmış büyük bilgi tabanları (CYC), yapılandırılmış kaynaklardan çıkarılanlar (DBpedia, Wikidata), metinden otomatik çıkarılanlar ve topluluk tarafından oluşturulanlar (schema.org).

---

## 2. Kategoriler ve nesneler

- **Şeyleştirme** (*reification*): Kategoriyi bir nesne gibi ele almak. Basketbolları gibi bir kategori, bir yüklem (Basketbol(b)) ya da bir nesne olarak yazılabilir: b ∈ Basketbolları.
- **Taksonomi:** Alt kategori ilişkisi. Kediler ⊂ Memeliler ⊂ Hayvanlar. Özellikler **kalıtımla** aşağı akar: Tüm memeliler sıcakkanlıdır, Tekir bir kedidir, o hâlde Tekir sıcakkanlıdır.
- **Ayrık kategoriler:** Ayrık({Hayvanlar, Sebzeler}). **Kapsayıcı ayrışma:** Amerikalılar ya Kanadalı ya da ABD'li… **Bölüntü:** Hem ayrık hem kapsayıcı.
- **Doğal türler:** Domates gibi kategorilerin kesin tanımı yoktur. "Tipik domates kırmızı ve yuvarlaktır" gibi bir Tipik(Kategori) fonksiyonuyla ifade edilebilir.
- **Fiziksel bileşim:** ParçasıDır(Bükreş, Romanya). Yığın: BunchOf({Elma1, Elma2, Elma3}), parçaları üyeler olan bileşik nesne.
- **Ölçüler:** Uzunluk(L1) = İnç(1,5) = Santimetre(3,81). Birim fonksiyonları sayıyı ölçüye çevirir; ölçüler sıralanabilir ama birimler arası dönüşüm aksiyomları gerekir.
- **Şeyler ve maddeler:** "Bir elma" sayılabilir (bir şey); "tereyağı" sayılamaz (bir madde). Bir maddeyi bölersen yine aynı madde kalır, bir şeyi bölersen kalmaz.
  - **İçsel** özellikler (yoğunluk, kaynama noktası) parçalara geçer.
  - **Dışsal** özellikler (ağırlık, şekil) parçalara geçmez.

`ontoloji_mini.py` küçük bir taksonomide kalıtım sorgularını, `anlamsal_ag.py` ise kalıtımın varsayılanlarla etkileşimini gösterir.

---

## 3. Olaylar

### 3.1 Olay hesabı

Bölüm 7'deki durum temelli yaklaşım "eylem sırasında" olanları ya da eşzamanlı olayları ifade etmekte zorlanır. **Olay hesabı** nesneleri **olaylar**, **akışkanlar** ve **zaman noktaları** olarak ele alır:

| Yüklem | Anlamı |
|---|---|
| T(f, t) | f akışkanı t anında doğru |
| Happens(e, t₁, t₂) | e olayı t₁'de başlayıp t₂'de bitti |
| Initiates(e, f, t) | e, t anında f'yi doğru yapar |
| Terminates(e, f, t) | e, t anında f'yi yanlış yapar |

Temel aksiyom (atalet): f, bir olay tarafından başlatıldıysa ve arada hiçbir olay onu sonlandırmadıysa doğrudur. Bu, ardıl durum aksiyomlarının zamanlı karşılığıdır. `olay_hesabi.py` bir ışık, bir kapı ve bir kişi için T(f, t) zaman çizelgesi çıkarır.

**Süreçler:** "Uçmak" gibi olayların her alt parçası da aynı türden bir olaydır (sıvı olaylar, sürekli olaylar). "Uçağın İstanbul'dan Ankara'ya uçuşu" gibi olaylar ise ayrık olaylardır; parçası aynı olay değildir. Şeyler ile maddeler arasındaki farkın zamandaki karşılığıdır.

### 3.2 Zaman aralıkları

**Anlar** sıfır süreli, **genişletilmiş aralıklar** süreli aralıklardır. Kitaptaki Allen ilişkileri (`olay_hesabi.py` her birini tarihsel bir örnekle gösterir):

| İlişki | Tanım | Örnek |
|---|---|---|
| Meet(i, j) | Son(i) = Baş(j) | Fatih'in saltanatı — II. Bayezid'in saltanatı (1481) |
| Before(i, j) | Son(i) < Baş(j) | Fatih — Kanuni |
| During(i, j) | Baş(j) < Baş(i) < Son(i) < Son(j) | Süleymaniye'nin inşası (1550–57) — Kanuni'nin saltanatı |
| Overlap(i, j) | Baş(i) < Baş(j) < Son(i) < Son(j) | Kanuni'nin saltanatı — Sinan'ın başmimarlığı |
| Starts(i, j) | Baş(i) = Baş(j) | Cumhuriyet'in ilk yılı — Atatürk'ün cumhurbaşkanlığı |
| Finishes(i, j) | Son(i) = Son(j) | Sinan'ın başmimarlığı — Sinan'ın hayatı |
| Equals(i, j) | uçlar eşit | |

Kitaptaki **Overlap** simetrik değildir: i, j'den önce başlamalıdır.

**Akışkanlar ve nesneler:** "ABD Başkanı" zamanla farklı kişileri gösterir. Bu yüzden onu, farklı aralıklarda farklı nesnelere eşit olan bir akışkan-nesne olarak düşünmek gerekir: T(Başkan(ABD) = Washington, AD1790).

---

## 4. Zihinsel nesneler ve modal mantık

**Önermesel tutumlar:** Bilir, İnanır, İster, Bildirir. Bunlar sıradan yüklemler gibi davranmaz.

- Bilir(Lois, Uçar(Süpermen)) ve Süpermen = Clark ise, FOL'un eşitlik kuralları Bilir(Lois, Uçar(Clark))'ı da türetir. Bu **göndergesel saydamlıktır** ve burada yanlıştır, çünkü Lois Clark'ın Süpermen olduğunu bilmez. Önermesel tutumlar için **göndergesel geçirimsizlik** gerekir: Hangi ismin kullanıldığı önemlidir.
- **Modal mantık:** K_A P ("A, P'yi bilir") gibi **modal işleçler** cümleleri argüman olarak alır.
- **Olası dünyalar anlamı:** Model, **erişilebilirlik ilişkisiyle** bağlanmış bir dünyalar kümesidir. K_A P, w'de ancak ve ancak P, A'nın w'den erişebildiği (A'nın bildikleriyle tutarlı) her dünyada doğruysa doğrudur.

`modal_bilgi.py` kitaptaki örnekleri değerlendirir:
- K_Lois Uçar(Süpermen) = doğru, K_Lois Uçar(Clark) = **yanlış** (Lois'in erişebildiği bir dünyada Clark başka biridir).
- K_Lois[K_Clark Kimlik ∨ K_Clark ¬Kimlik] = doğru: Lois, Clark'ın kimliğini bildiğini bilir.
- "Bond birinin casus olduğunu biliyor": ∃x K_Bond Casus(x) (belirli biri) yanlış, K_Bond ∃x Casus(x) (bir casus var) doğru.

**Aksiyomlar ve sorunlar:**
- (K_A P ∧ K_A(P ⇒ Q)) ⇒ K_A Q: Ajan, bildiklerinin sonuçlarını da bilir. Bu **mantıksal her şeyi bilme** sorununa yol açar: Ajan, bildiği aksiyomlardan çıkan her teoremi bilir.
- K_A P ⇒ P: Bilgi doğrudur (erişim yansımalıysa). İnanç için geçerli değildir.
- Diğer modaliteler: **zorunluluk/olanak** (□, ◇), **zaman mantığı** (her zaman, sonunda, sonraki).

---

## 5. Kategoriler için akıl yürütme sistemleri

### 5.1 Anlamsal ağlar

Kategoriler ve nesneler düğüm, ilişkiler bağlantıdır (AltKüme, Üye, kardeşi…). Avantajları görsellik ve **kalıtımın** verimli hesaplanmasıdır. Sınırları:
- İkili ilişkiler doğaldır. n'li ilişkiler, olayın kendisi düğüm yapılarak (şeyleştirilerek) ifade edilir: Uçuş olayı E1; Uçan(E1, Ali), Başlangıç(E1, İstanbul), Varış(E1, Ankara).
- Değilleme, ayrılma ve iç içe niceleyiciler doğrudan ifade edilemez.

**Varsayılanlar:** Kişiler kategorisine bağlı "2 bacak" bilgisi, kişi olan her nesne için varsayılandır. Daha özel bilgi (Uzun John Silver'ın 1 bacağı var) onu geçersiz kılar. Bu, klasik mantıktan farklı olarak **monoton olmayan** bir davranıştır. `anlamsal_ag.py` bunu ve Nixon elmasındaki çatışmayı gösterir.

### 5.2 Betimleme mantıkları

Kategori tanımlarını ve kategoriler arası **kapsamayı** (bir kategori diğerinin alt kümesi mi?) verimli hesaplamak için tasarlanmış dillerdir (CLASSIC, OWL'un temeli). Örnek: Bekar = And(Evli Değil, Yetişkin, Erkek). Temel çıkarımlar:
- **Kapsama:** Bir kategori diğerinin alt kümesi mi?
- **Sınıflandırma:** Bir nesne bir kategoriye ait mi?

Değilleme ve ayrılma genellikle yoktur ya da sınırlıdır. Böylece kapsama polinom zamanda hesaplanabilir. İfade gücü ile işlem kolaylığı arasındaki ödünleşimin tipik bir örneğidir.

---

## 6. Varsayılan bilgiyle akıl yürütme

İnsanlar sık sık "sonuca atlar": Park etmiş bir arabanın dört tekerleği olduğunu varsayarız, üçünü görsek bile. Yeni bir kanıt gelirse (araba kriko üstünde) sonucu geri alırız. Bu **monoton olmayan** akıl yürütmedir: İnanç kümesi, yeni bilgi geldikçe hep büyümez.

### 6.1 Sınırlandırma (circumscription)

Bazı yüklemler (Anormal₁ gibi) "olabildiğince yanlış" kabul edilir. Bir cümle, KB'nin **tercih edilen** (anormali en az olan) tüm modellerinde doğruysa varsayılan olarak gerektirilir. Bir **model tercihi mantığıdır**.

- Kuş(x) ∧ ¬Anormal₁(x) ⇒ Uçar(x): Kuş(Tweety)'den Uçar(Tweety) çıkar. Penguen(Tweety) öğrenilince bu sonuç düşer (`varsayilan_akil.py`).
- **Nixon elması:** Nixon hem Quaker (varsayılan olarak pasifist) hem Cumhuriyetçi (varsayılan olarak pasifist değil). Anormal₂ ve Anormal₃ sınırlandırılınca **iki** tercih edilen model vardır: Birinde pasifisttir, diğerinde değildir. Akıl yürütücü "bilinmiyor" der. **Öncelikli sınırlandırma** (önce Anormal₃'ü en aza indir: dinî inanç siyasi görüşten önce gelir) "pasifist" sonucunu verir.

### 6.2 Varsayılan mantık

Varsayılan kural: P : J₁, …, Jₙ / C. "P doğruysa ve her Jᵢ tutarlıysa C'yi varsay." Örnek: Kuş(x) : Uçar(x) / Uçar(x).

Bir KB'nin **genişlemesi**, varsayılanların tutarlı bir şekilde uygulanmasıyla elde edilen en büyük inanç kümesidir. Nixon için iki genişleme vardır. "Temkinli" akıl yürütme yalnızca tüm genişlemelerde ortak olana inanır, "cesur" akıl yürütme herhangi birine inanır.

**Sorunlar:** Varsayılanlar karar vermek için yeterince bilgi taşımaz ("frenlerim her zaman çalışır" dik bir yokuşta yetersizdir). Olasılık ve fayda (Bölüm 12–16) bu konuda daha sağlam bir temel sunar.

### 6.3 Doğruluk bakım sistemleri (TMS)

Varsayılan sonuçlar yanlış çıkabilir; onları geri çekmek ve bunlardan türetilmiş her şeyi güncellemek gerekir.
- Basit yaklaşım: Cümleleri eklenme sırasıyla tut, geri çekince o noktaya dön. Çok pahalıdır.
- **JTMS** (gerekçe tabanlı): Her inanç, onu destekleyen **gerekçelerle** (öncül kümeleriyle) saklanır. Bir varsayım geri çekilince yalnızca **tüm desteğini** kaybeden inançlar düşer (`anlamsal_ag.py`: Yağmur geri çekilince IslakÇim kalır, çünkü Sulama'dan bağımsız bir gerekçesi vardır).
- **ATMS** (varsayım tabanlı): Her inancın hangi varsayım kümeleri altında doğru olduğunu tutar. Farklı varsayım "dünyaları" arasında hızlı geçiş yapar. **Açıklama** üretmek için de kullanılır.

---

## Sık yapılan hatalar

| Yanılgı | Doğrusu |
|---|---|
| "Üye (∈) ile AltKüme (⊂) aynıdır." | Tekir ∈ Kediler (nesne–kategori); Kediler ⊂ Memeliler (kategori–kategori). |
| "Maddeler de şeyler gibi sayılır." | Tereyağı bölünce yine tereyağıdır; bir elma bölünce "bir elma" değildir. |
| "Eşitlik her bağlamda yerine koymaya izin verir." | Önermesel tutumlarda (bilmek, inanmak) izin vermez: göndergesel geçirimsizlik. |
| "Overlap simetriktir." | Kitaptaki tanımda Overlap(i, j) için i önce başlamalıdır. |
| "Varsayılan akıl yürütme mantıksız bir kısayoldur." | Kesin bilgi yokken işe yarayan, ama yeni bilgiyle geri alınabilen sonuçlar üretir. Sınırlandırma ve varsayılan mantık bunu biçimsel olarak tanımlar. |
| "Nixon elmasında akıl yürütücü bir karar vermeli." | Çatışan varsayılanlar varsa doğru yanıt "bilinmiyor"dur. Öncelik, ancak ek bilgiyle verilebilir. |

## Kendini yokla

1. "Su" ve "bir bardak su" arasındaki fark nedir? Hangisi madde, hangisi şey?
2. Kanuni'nin saltanatı (1520–1566) ile Mimar Sinan'ın başmimarlığı (1538–1588) arasında Overlap(Sinan, Kanuni) doğru mu? Neden?
3. K_A(P ∨ ¬P) neden her zaman doğrudur, K_A P ∨ K_A ¬P neden değildir?
4. Tweety örneğinde "penguen" bilgisi eklenince tercih edilen model neden değişir?
5. JTMS, basit "geri al" yaklaşımına göre neden daha verimlidir?

## Kod rehberi

```bash
python ornekler/ontoloji_mini.py     # taksonomi ve kalıtım
python ornekler/anlamsal_ag.py       # varsayılan geçersiz kılma, Nixon çatışması, JTMS
python ornekler/olay_hesabi.py       # olay hesabı, Allen ilişkileri
python ornekler/modal_bilgi.py       # Süpermen/Clark, Bond, bilmek ve inanmak
python ornekler/varsayilan_akil.py   # sınırlandırma, Nixon elması, varsayılan mantık
```

## Terimler

| Türkçe | İngilizce | Kısa açıklama |
|---|---|---|
| ontoloji / üst ontoloji | ontology / upper ontology | Kavramların düzeni / en genel kavramlar |
| şeyleştirme | reification | Bir kavramı nesne olarak ele alma |
| taksonomi / kalıtım | taxonomy / inheritance | Alt kategori hiyerarşisi / özelliklerin aşağı akması |
| ayrık / kapsayıcı ayrışma / bölüntü | disjoint / exhaustive decomposition / partition | Kategori kümesi ilişkileri |
| doğal tür | natural kind | Kesin tanımı olmayan kategori |
| şey / madde | thing / stuff | Sayılabilir / sayılamaz (count / mass) |
| içsel / dışsal özellik | intrinsic / extrinsic property | Parçalara geçen / geçmeyen özellik |
| olay hesabı | event calculus | Olaylar, akışkanlar, zaman noktaları |
| süreç | process (liquid event) | Her parçası aynı türden olay |
| önermesel tutum | propositional attitude | Bilmek, inanmak, istemek |
| göndergesel saydamlık / geçirimsizlik | referential transparency / opacity | İsmin önemli olmaması / olması |
| modal işleç / modal mantık | modal operator / modal logic | K_A gibi cümle alan işleçler |
| olası dünya / erişilebilirlik | possible world / accessibility relation | Modal mantığın anlamı |
| mantıksal her şeyi bilme | logical omniscience | Ajanın tüm sonuçları bildiği varsayımı |
| anlamsal ağ | semantic network | Düğüm ve bağlantılarla temsil |
| betimleme mantığı | description logic | Kategori tanımları ve kapsama için dil |
| kapsama / sınıflandırma | subsumption / classification | Kategori ⊂ kategori mi / nesne ∈ kategori mi |
| monoton olmayan mantık | nonmonotonic logic | Yeni bilgiyle sonuçların geri alınabildiği mantık |
| sınırlandırma | circumscription | Anormalleri en aza indiren model tercihi |
| öncelikli sınırlandırma | prioritized circumscription | Anormaller arasında öncelik |
| varsayılan mantık / genişleme | default logic / extension | Varsayılan kurallar / tutarlı inanç kümesi |
| doğruluk bakım sistemi | truth maintenance system (JTMS, ATMS) | Geri çekmeleri verimli yöneten sistem |
