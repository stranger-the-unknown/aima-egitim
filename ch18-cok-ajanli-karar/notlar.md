# Bölüm 18 — Çok ajanlı karar verme

> **Kitapta:** AIMA 4. baskı, Bölüm 18 *"Multiagent Decision Making"*.
> Önce kitabı oku, sonra bu notlarla pekiştir. Metin özgündür; kitaptan alıntı yoktur.

## Bu bölümün haritası

| Kitap alt bölümü | Bu nottaki karşılığı | Kod |
|---|---|---|
| 18.1 Properties of Multiagent Environments | §1 Tek / çok karar verici, çok aktörlü planlama, eşzamanlılık, uzlaşım | — (A2) |
| 18.2.1–18.2.2 Normal form games, Social welfare | §2 Baskınlık, Nash dengesi, Pareto, sosyal refah, Morra ve maksimin | `oyun_kurami.py` |
| 18.2.3 Repeated games | §3 Geriye tümevarım, sonlu durum makineleri, halk teoremleri | `tekrarli_oyunlar.py` |
| 18.2.4 Sequential games: The extensive form | §4 Alt oyun yetkinliği, eksik bilgi, basit poker | `uzun_bicim.py` |
| 18.2.5 Uncertain payoffs and assistance games | §5 Ataş oyunu | `uzun_bicim.py` |
| 18.3 Cooperative Game Theory | §6 Koalisyonlar, çekirdek, Shapley değeri, MC-ağları | `isbirlikci_oyunlar.py` |
| 18.4 Making Collective Decisions | §7 Sözleşme ağı, açık artırmalar, VCG, oylama, pazarlık | `mekanizma_tasarimi.py` |

## Öğrenme hedefleri

1. Çok ajanlı ortamları (tek karar verici, ortak amaç, ayrı tercihler) ayırt etmek.
2. Normal biçimli bir oyunda baskın stratejileri, Nash dengelerini ve Pareto en iyi sonuçları bulmak.
3. İki kişilik sıfır toplamlı bir oyunu maksimin (doğrusal programlama) ile çözmek.
4. Tekrarlı oyunlarda işbirliğinin nasıl sürdürülebildiğini açıklamak.
5. Uzun biçimli oyunları geriye tümevarımla çözmek; inandırıcı olmayan tehditleri tanımak.
6. Çekirdek ve Shapley değeriyle işbirlikçi oyunları analiz etmek.
7. Açık artırmaların, VCG'nin, oylama kurallarının ve pazarlık protokollerinin özelliklerini karşılaştırmak.

---

## 1. Çok ajanlı ortamlar

### 1.1 Tek karar verici

- **İyiliksever ajan varsayımı:** Diğer aktörler kendilerine söyleneni yapar. Yine de eşzamanlama gerekir: ortak eylemler (düet), birbirini dışlayan eylemler (tek priz), ardışık eylemler (biri yıkar, öbürü kurular).
- **Çok efektörlü planlama** (yürürken konuşmak), **çok gövdeli planlama** (fabrikadaki teslimat robotları). Algılar birleştirilebiliyorsa bu yine tek ajanlı bir problemdir; iletişim kısıtlıysa **merkezî olmayan planlama** (planlama merkezî, yürütme ayrık).

### 1.2 Çok karar verici

Diğer aktörler de karar verir (**karşı taraflar**):
- **Ortak amaç:** Asıl sorun **koordinasyon**.
- **Ayrı tercihler:** Tam zıt (satranç gibi sıfır toplamlı) ya da daha karmaşık. Burada **oyun kuramı** gerekir: stratejik karar verme kuramı.

Oyun kuramının yapay zekâdaki iki kullanımı:
1. **Ajan tasarımı:** Rasyonel rakiplere karşı en iyi stratejiyi hesaplamak.
2. **Mekanizma tasarımı:** Oyunun kurallarını, herkes kendi faydasını en büyüklerken toplumsal iyilik de en büyüklenecek biçimde koymak.

**İşbirlikçi oyun:** Bağlayıcı anlaşma mümkün. **İşbirlikçi olmayan oyun:** Bağlayıcı anlaşma yok (ama ajanlar yine de kendi çıkarları için işbirliği yapabilir).

### 1.3 Çok aktörlü planlama

**Eşzamanlılık** modelleri:
- **Serpiştirilmiş yürütme:** Yalnızca her planın kendi sırası korunur. İki eylemli iki plan için 6 serpiştirme vardır; plan bunların **hepsinde** doğru olmalıdır. Serpiştirme sayısı üstel büyür.
- **Gerçek eşzamanlılık:** Kısmi sıralama.
- **Mükemmel eşzamanlama:** Ortak saat, adım adım ortak eylemler. Kitap bunu kullanır.

n aktörde tek eylem yerine **ortak eylem** ⟨a₁, …, aₙ⟩ vardır: dallanma bⁿ. Gevşek bağlı problemlerde aktörleri olabildiğince ayırıp etkileşimleri sonradan düzeltmek gerekir.

**Çiftler tenis örneği:** A ve B topu karşılamalı ve biri fileyi korumalı. İki doğru ortak plan:
- Plan 1: A sağ dip çizgiye gidip vurur, B bekler.
- Plan 2: A sol fileye gider, B sağ dip çizgiye gidip vurur.

İkisi aynı anda vurursa sorun çıkar: **eşzamanlı eylem kısıtı** (`Hit` başka biri aynı anda vurmuyorsa etkilidir; soğutucuyu taşımak ise iki kişiyi **gerektirir**).

**Koordinasyon:** Herkes kendi planını yapınca A Plan 2'yi, B Plan 1'i seçerse kimse vurmaz. Çözümler:
- **Uzlaşım** (convention): "Kendi tarafında kal", "yolun sağından git". Yaygınlaşınca **toplumsal yasa**.
- **İletişim:** "Benim!" diye bağırmak; ya da planın ilk adımını yapmak (**plan tanıma**): A fileye yürürse B Plan 2'yi anlar.

---

## 2. Normal biçimli oyunlar (`oyun_kurami.py`)

Oyuncular aynı anda (ya da birbirinin seçimini bilmeden) eylem seçer. Bileşenler: **oyuncular**, **eylemler**, **fayda fonksiyonu** (iki kişide **fayda matrisi**).

- **Strateji** = politika. **Saf strateji:** belirlenimci. **Karma strateji:** [p: a; (1 − p): b].
- **Strateji profili:** Her oyuncuya bir strateji.

### 2.1 Baskınlık ve mahkûm ikilemi

Ali ve Bo ayrı ayrı sorgulanıyor:

| | Ali: tanık ol | Ali: sus |
|---|---|---|
| **Bo: tanık ol** | A = −5, B = −5 | A = −10, B = 0 |
| **Bo: sus** | A = 0, B = −10 | A = −1, B = −1 |

Bo ne yaparsa yapsın Ali için tanık olmak daha iyidir: **baskın strateji**. s, s′'yü **güçlü** baskılar: her durumda daha iyi; **zayıf** baskılar: bir durumda daha iyi, hiçbirinde kötü değil. İkisi de baskın stratejiyi oynar: **(tanık, tanık)**, 5'er yıl.

### 2.2 Nash dengesi

Hiçbir oyuncu **tek başına** stratejisini değiştirip kazanamıyorsa profil bir **Nash dengesidir** (Nash, 1950; Nobel 1994): Herkes diğerlerine **en iyi tepkiyi** veriyor. Baskın strateji dengesi her zaman bir Nash dengesidir (A2).

- **Koordinasyon oyunu:** (t, l) = (10, 10), (b, r) = (1, 1), diğerleri 0. Baskın strateji yok; **iki** Nash dengesi. **Odak noktası:** Öne çıkan sonuç, burada açıkça (t, l).
- **Yazı-tura eşleştirme:** Aynıysa Ali, farklıysa Bo 1 $ kazanır. **Saf Nash dengesi yok**; karma denge (½, ½). **Nash teoremi:** Her (sonlu) oyunun karma stratejilerde en az bir Nash dengesi vardır.

### 2.3 Sosyal refah

- **Pareto en iyi:** Kimseyi kötüleştirmeden birini iyileştiren başka bir sonuç yok.
- **Faydacı sosyal refah:** Faydaların toplamı. Sorunları: dağılımı görmez; ortak bir fayda ölçeği varsayar ("kurabiyeleri bin kat daha çok sevdiğini söyleyen **fayda canavarı**").
- **Eşitlikçi sosyal refah:** En kötü durumdakinin faydasını en büyüklemek (maksimin) ya da **Gini katsayısı** gibi ölçüler.

**İkilemin özü:** (tanık, tanık) hem baskın strateji dengesi hem tek Nash dengesidir, ama Pareto en iyi **olmayan** tek sonuçtur; (sus, sus) ise hem faydacı hem eşitlikçi refahı en büyükler. Güçlü bir çözüm kavramı, toplum açısından her testte kalan bir sonuca götürür.

**Dengeyi hesaplamak:** Saf dengeler için bütün profilleri dene (n oyuncu, m eylem: mⁿ profil). **Miyop en iyi tepki:** En iyi tepkiyi oynamayan birini değiştir, tekrarla. Koordinasyon oyununda dengeye varır; yazı-turada döngüye girer.

### 2.4 Sıfır toplamlı oyunlar: maksimin

**İki parmaklı Morra:** O ve E bir ya da iki parmak gösterir; toplam f tekse O, çiftse E f dolar kazanır. E için matris:

| | O: bir | O: iki |
|---|---|---|
| **E: bir** | +2 | −3 |
| **E: iki** | −3 | +4 |

**von Neumann'ın maksimin yöntemi:**
- Önce E stratejisini açıklasın (O'nun lehine): Saf stratejilerle değer −3. Önce O açıklasın: +2. Gerçek değer **−3 ≤ U ≤ 2**.
- İkinci oynayan her zaman saf strateji seçebilir (karma, saf stratejilerin doğrusal birleşimidir).
- E [p: bir; 1−p: iki] açıklarsa O'nun iki tepkisi: 5p − 3 ve 4 − 7p. E kesişimi seçer: **p = 7/12**, değer **−1/12**. O için de aynı: q = 7/12, değer −1/12.
- Alt ve üst sınır çakışır: Oyunun değeri **−1/12** (O olmak daha iyi). **Maksimin dengesi** [7/12: bir; 5/12: iki].

**von Neumann teoremi:** Her iki kişilik sıfır toplamlı oyunun karma stratejilerde bir maksimin dengesi vardır; bu oyunlardaki her Nash dengesi her iki oyuncu için maksimindir. Maksimin oynayan oyuncu (1) iyi oynayan rakibe karşı daha iyisini yapamaz, (2) stratejisi açığa çıksa bile aynı sonucu alır.

n eylemde genel çözüm bir **doğrusal programlamadır** (eylem sayısında polinom). Kodumuz küçük bir simpleks ile Morra'nın değerini −0.08333 bulur. Sıfır toplamlı olmayan oyunlarda: Destek kümelerini sırayla dene, her biri için denklemleri çöz; iki oyuncuda doğrusal, üç ve fazlasında doğrusal değil.

---

## 3. Tekrarlı oyunlar (`tekrarli_oyunlar.py`)

**Aşama oyunu** defalarca oynanır. Strateji: her geçmiş için bir eylem.

**Sabit, sonlu ve herkesçe bilinen** tur sayısı (ör. 100): Son tur tek seferlik oyundur → tanık; bir önceki turun sonrakine etkisi yok → tanık; … **Geriye tümevarım**: Her turda tanıklık, toplam 500 yıl. Üç koşuldan biri kalkarsa (sabit, sonlu, bilinen) bu akıl yürütme çöker.

**Sonsuz tekrar:** Stratejiler **çıktılı sonlu durum makineleri** (Şekil 18.3):

| Makine | Davranış |
|---|---|
| ŞAHİN | Hep tanık |
| GÜVERCİN | Hep sus |
| ACIMASIZ | Susarak başlar; karşı taraf bir kez tanık olursa sonsuza dek tanık |
| KISASA KISAS | Susarak başlar; karşının bir önceki hamlesini kopyalar (affedicidir) |

Fayda: **ortalamaların limiti** lim (1/T) Σ U_t. İki sonlu makine eninde sonunda aynı durum çiftine döner; ortalama, tekrarlanan döngü üzerinden hesaplanır.

| Eşleşme | Faydalar | Nash? |
|---|---|---|
| GÜVERCİN – GÜVERCİN | −1 / −1 | Hayır (biri ŞAHİN'e geçip 0 alır) |
| ŞAHİN – GÜVERCİN | 0 / −10 | Hayır |
| ŞAHİN – ŞAHİN | −5 / −5 | Evet (aşama oyununun dengesi tekrarlı oyunda da denge) |
| ŞAHİN – ACIMASIZ | −5 / −5 | Hayır (Ali ACIMASIZ'a geçerse −1) |
| ACIMASIZ – ACIMASIZ | −1 / −1 | **Evet** |

ACIMASIZ–ACIMASIZ'da sapan oyuncu bir kez tanık olunca karşısı sonsuza dek tanık olur ve sapan en çok −5 alır. Tek seferlik oyunda imkânsız olan işbirliği **rasyonel olarak** sürdürülür. Genel sonuç **Nash halk teoremleri**: Her oyuncunun en az **güvenlik değerini** (kendi başına garanti edebileceği fayda) aldığı her sonuç, sonsuz tekrarlı oyunda bir Nash dengesiyle sürdürülebilir. ACIMASIZ stratejiler bu teoremlerin anahtarıdır. (Kitap Şekil 18.3'teki TAT-FOR-TIT'in ne yaptığını okura sorar.)

---

## 4. Uzun biçimli (ardışık) oyunlar (`uzun_bicim.py`)

**Uzun biçim:** Oyun ağacı; oyuncular, eylemler, uç durumlardaki faydalar. **Tam bilgi:** Oyuncu ağacın neresinde olduğunu bilir (satranç, Go).

**Geriye tümevarım:** Uç durumlardan geriye, her düğümde karar verecek oyuncunun faydasını en büyükleyen çocuğun fayda profilini taşı (şans düğümlerinde beklenen değer). Ağaç boyutunda polinom zaman; bulunan stratejiler Nash dengesidir. Her tam bilgili uzun biçimli oyunun saf bir Nash dengesi vardır.

**İnandırıcı olmayan tehdit (Şekil 18.4):** Oyuncu 1 "aşağı" derse (0, 0). "Yukarı" derse oyuncu 2 "yukarı" (1, 1) ya da "aşağı" (0, 0) seçer.
- Geriye tümevarım: (yukarı, yukarı), (1, 1).
- (aşağı, aşağı) da bir Nash dengesidir: Oyuncu 2 "aşağı oynarım" diye tehdit eder. Ama o düğüme gelince yukarı seçeceği için tehdit **inandırıcı değildir**.
- **Alt oyun yetkin Nash dengesi:** Her alt oyunda Nash dengesi olan profil. (yukarı, yukarı) öyledir, (aşağı, aşağı) değildir. Geriye tümevarımın bulduğu dengeler her zaman alt oyun yetkindir.

**Şans ve eşzamanlı hamleler:** Olasılık dağılımıyla oynayan bir **Şans** oyuncusu. Eşzamanlı hamle için oyunculara keyfî bir sıra verilir ama önceki hamle sonrakine gösterilmez. Oyuncular kendi hamlelerini hatırlar: **mükemmel hatırlama**.

**Eksik bilgi:** Oyuncu gerçek durumdan emin değil. **Bilgi kümeleri:** Oyuncunun ayırt edemediği durumlar (Bölüm 5'teki inanç durumları). Geriye tümevarım burada çalışmaz.

**Basitleştirilmiş poker (Şekil 18.5):** Destede 2 as, 2 papaz; her oyuncuya bir kart (AA ve KK 1/6, AK ve KA 1/3). Oyuncu 1 artırır (r, oyun 2 puan) ya da bekler (k, oyun 1 puanla biter). Artırırsa oyuncu 2 görür (c) ya da çekilir (f, 1 puan kaybeder). Kartlar aynıysa 0; değilse papazlı olan asa öder.

Her oyuncunun iki bilgi kümesi (as / papaz) ve kümede iki eylemi var → 2² = 4 saf strateji. Normal biçim (oyuncu 1'in faydası; kodumuz ağaçtan türetir ve kitapla birebir aynı bulur):

| | cc | cf | ff | fc |
|---|---|---|---|---|
| **rr** | 0 | −1/6 | 1 | 7/6 |
| **kr** | −1/3 | −1/6 | 5/6 | 2/3 |
| **rk** | 1/3 | **0** | 1/6 | 1/2 |
| **kk** | 0 | **0** | 0 | 0 |

İki saf denge: oyuncu 2 **cf** (asla görür, papazla çekilir), oyuncu 1 **rk** ya da **kk**. Oyunun değeri 0.

**Ölçek sorunu:** I bilgi kümesi ve küme başına a eylem → a^I saf strateji; normal biçim üstel büyür. **Sıra biçimi** (Koller ve ark., 1996): Ağaç boyutunda doğrusal; 25 000 durumlu poker türleri bir iki dakikada çözülür. İki kişilik Texas hold 'em ~10¹⁸ durum: **soyutlama** (renkleri yok saymak 4! = 24 kat küçültür, el sınıfları, teklif miktarlarını 10⁰, 10¹, 10², 10³ ile sınırlamak) → ~10⁷ durum. Libratus ve DeepStack ikili, Pluribus altı kişilik pokerde insan şampiyonları yendi.

**Oyun kuramının sınırları:** Sürekli durum ve eylemlerde zorlanır (Cournot rekabeti gibi uzantılar var); oyunun **bilindiğini** varsayar. Bilinmeyen eylemler temsil edilemez; bilinmeyen stratejiler için **Bayes–Nash dengesi**; bilinmeyen şans ve faydalar için şans düğümleri eklenir, ama her ekleme ağacı ikiye katlar. Bu yüzden oyun kuramı daha çok dengedeki ortamları **analiz etmek** için kullanılır.

---

## 5. Belirsiz faydalar ve yardım oyunları

Bölüm 16'daki kapatma düğmesinde Robbie Harriet'in tercihlerinden emin değildi. **Yardım oyunu:** Harriet ve Robbie aynı (Harriet'in) faydasını paylaşır ama yalnızca Harriet onu bilir. Oyunu çözünce öğretme, gösterme, izin isteme gibi davranışlar **kendiliğinden** ortaya çıkar.

**Ataş oyunu (Şekil 18.6):** Harriet 2 ataş, 1 + 1 ya da 2 zımba yapar; sonra Robbie 90 ataş, 50 + 50 ya da 90 zımba. Harriet'in faydası p θ + s (1 − θ); Robbie'nin önseli θ ~ U(0, 1).

Tek başına Harriet (θ = 0.45) 2 zımba yapardı (1.10 $). Ama Robbie izliyor. Miyop en iyi tepkiyle:
1. Açgözlü Harriet: θ > 0.5 ise 2 ataş, θ = 0.5 ise 1 + 1, θ < 0.5 ise 2 zımba.
2. Robbie: 2 ataş görürse θ ~ U(0.5, 1), ortalama 0.75 → 90 ataş; 1 + 1 → 50 + 50; 2 zımba → 90 zımba.
3. Harriet artık θ yarıya **yakın** olduğunda da 1 + 1 yapar: 51 ≥ 92θ ve 51 ≥ 92(1 − θ) ⇔ θ ∈ **[0.446, 0.554]** (tam olarak 41/92 – 51/92).
4. Robbie'nin tepkisi değişmez: Denge.

Harriet tercihlerini basit bir "kodla" öğretir; Robbie θ'yı tam bilmez ama tam bilseydi yapacağını yapar.

---

## 6. İşbirlikçi oyun kuramı (`isbirlikci_oyunlar.py`)

**Karakteristik fonksiyon biçimli, aktarılabilir faydalı oyun** G = (N, ν): ν(C), C koalisyonunun elde edebileceği değer; ν(∅) = 0.

- **Koalisyon yapısı:** Oyuncuların bölüntüsü. N = {1, 2, 3}: 7 koalisyon, **5** yapı; N = {1, 2, 3, 4}: **15** yapı (sayılar Bell sayılarıdır).
- **Sonuç:** (yapı, ödeme vektörü); her koalisyon değerini üyelerine tam dağıtır. Örnek: ν({1}) = 4, ν({2, 3}) = 10 → ({{1}, {2, 3}}, (4, 5, 5)).
- **Süperadditif:** ν(C ∪ D) ≥ ν(C) + ν(D). Büyük koalisyon en yüksek toplamı verir ama yine de oluşmayabilir.

### 6.1 Çekirdek

**Paylaşım (imputation):** Σ xᵢ = ν(N) ve **bireysel rasyonellik** xᵢ ≥ ν({i}).
**Çekirdek:** Her C için x(C) ≥ ν(C) olan paylaşımlar: Hiçbir koalisyonun ayrılmak için nedeni yok. Doğrusal eşitsizlikler, ama 2ⁿ tane; birçok oyun sınıfında boş olup olmadığını sınamak co-NP-tam.

- **Boş çekirdek:** N = {1, 2, 3}, iki ya da üç kişilik her koalisyon 1, tekliler 0. Süperadditif ama her paylaşımda bir ikili ayrılıp 1'i paylaşarak kazanır.
- **Çekirdek adil olmayabilir:** ν({1}) = ν({2}) = 5, ν({1, 2}) = 20. (6, 14) çekirdektedir ama artığın 9/10'unu oyuncu 2'ye verir.

### 6.2 Shapley değeri

Her oyuncuya, büyük koalisyonun olası bütün **oluşma sıralarında** öncekilere kattığı **marjinal katkının** ortalaması:

```text
mc_i(C) = ν(C ∪ {i}) − ν(C)          φ_i = (1/n!) Σ_p mc_i(p_i)
```

Shapley değeri şu adalet aksiyomlarını sağlayan **tek** paylaşımdır: **Verimlilik** (hepsi dağıtılır), **kukla oyuncu** (katkısı olmayan bir şey almaz), **simetri** (aynı katkıya aynı pay), **toplamsallık** (iki oyunun toplamında paylar toplanır). Yukarıdaki örnekte (10, 10).

### 6.3 Hesaplama

ν'yi 2ⁿ'lik tabloyla vermek imkânsız. **Marjinal katkı ağları (MC-ağları):** (Cᵢ, xᵢ) kuralları; ν(C) = Cᵢ ⊆ C olan kuralların toplamı. Kitaptaki kurallar {({1,2}, 5), ({2}, 2), ({3}, 4)}: ν({1}) = 0, ν({3}) = 4, ν({1,3}) = 4, ν({2,3}) = 6, ν({1,2,3}) = 11. Her kural kendi içinde simetrik bir oyundur; toplamsallık ve simetriden Shapley polinom zamanda: (2.5, 4.5, 4). Kodumuz bunu bütün sıralamalar üzerinden de doğrular.

**En iyi koalisyon yapısı** (küme bölüntüleme problemi): NP-zor. Koalisyon yapısı grafının ilk iki düzeyi (en çok iki koalisyonlu yapılar) her koalisyonu içerir; bunları aramak en iyinin **en az 1/n'ini** garanti eder. Kodumuzdaki en kötü durum örneğinde sınır sıkıdır.

---

## 7. Toplu kararlar (`mekanizma_tasarimi.py`)

**Mekanizma** = dil (izin verilen stratejiler) + merkezin sonucu belirleme kuralı.

### 7.1 Sözleşme ağı

En eski ve en yaygın görev paylaşma protokolü: **görev duyurusu** → **teklif verme** → **ödüllendirme** (yüklenici) → yürütme (gerekirse alt görevlerle yeniden duyuru). Araç çağırma uygulamalarında her gün bir türü işler.

### 7.2 Açık artırmalar

**Özel değer** (çirkin bir kazak) ya da **ortak değer** (petrol sahası; herkesin farklı bilgisi var). Amaçlar: satıcının gelirini ve toplam faydayı en büyüklemek; **verimli** açık artırma malı en çok değer verene verir. En önemlisi yeterince teklifçi çekmek ve **gizli anlaşmayı** önlemek. (Kitaptaki 1999 Almanya frekans ihalesi: Mannesmann'ın 18.18 milyonluk teklifi, %10 artış kuralıyla "20 milyonda yarı yarıya paylaşalım" mesajıydı.)

| Mekanizma | Kural | Strateji |
|---|---|---|
| **İngiliz (artan teklif)** | Fiyat d adımlarla artar, son kalan kazanır | Baskın: değerin altındayken teklif ver. En yüksek değerli b_o + d öder. İletişim pahalı; güçlü bir teklifçi rakipleri caydırabilir |
| **Kapalı zarf (birinci fiyat)** | Tek teklif, en yüksek kazanır ve teklifini öder | Baskın strateji yok; rakipleri tahmin etmek gerekir |
| **Vickrey (ikinci fiyat)** | En yüksek kazanır, **ikinci** en yüksek teklifi öder | **Gerçek değeri teklif etmek baskındır**: dürüst (strateji geçirmez) |

- **Açığa çıkarma ilkesi:** Her mekanizma eşdeğer bir dürüst mekanizmaya dönüştürülebilir.
- **Gelir eşitliği teoremi:** Değerleri yalnızca kendileri bilen (dağılımı herkes bilen) teklifçilerde bütün bu mekanizmalar aynı beklenen geliri verir. Kodumuzda 4 teklifçi, U(0, 1) değerlerle birinci ve ikinci fiyatın ikisi de ~0.600 = (n − 1)/(n + 1).
- **Reklam yuvaları (n + 1 fiyat) dürüst değildir:** v = 200, 180, 100; üst yuva %5, alt %2 tıklanır. Dürüst teklifle b₁ üst yuvayı alır, 180 öder: (200 − 180) × 0.05 = **1**. 101–179 arası teklif verirse alt yuvayı 100'e alır: (200 − 100) × 0.02 = **2**. Doğru mekanizmada (Aggarwal ve ark., 2006) yalnızca ek tıklamalar için üst fiyat ödenir: 20 × 0.03 + 100 × 0.02 = **2.6**.

### 7.3 Ortak kaynakların trajedisi ve VCG

100 ülke: Kirliliği azaltmak −10; kirletmek −5 ve diğer her ülkeye −1. Kirletmek baskındır; herkes kirletince her ülke **−104**, herkes azaltsa **−10**. **Dışsallıkları** fiyatlandırmak gerekir (karbon vergisi gibi).

**Vickrey–Clarke–Groves (VCG):** Toplam faydayı en büyükler ve dürüsttür.
1. Herkes değerini bildirir. 2. Merkez, kazananları Σ vᵢ'yi en büyükleyecek biçimde seçer. 3. Her kazanan, varlığının kaybedenlere verdiği kaybı **vergi** olarak öder.

Kitaptaki örnek: 3 kablosuz verici, teklifler 100, 50, 40, 20, 10. Kazananlar 100, 50, 40 (toplam 190). Biri olmasaydı 20 kazanırdı → her kazanan **20** öder. Kritik değer 20'dir; ondan farklı bir şey bildirmek akıl dışıdır. Kombinasyonel açık artırmalarda da kullanılır, ama 2ᴺ alt kümeyle en iyi sonucu bulmak NP-tamdır.

### 7.4 Oylama

**Toplumsal seçim kuramı:** Seçmen tercihlerini bir **toplumsal refah fonksiyonuyla** (tam sıralama) ya da **toplumsal seçim fonksiyonuyla** (kazanan kümesi) birleştirmek.

**Condorcet paradoksu:** a ≻₁ b ≻₁ c, c ≻₂ a ≻₂ b, b ≻₃ c ≻₃ a. Seçmenlerin 2/3'ü a'yı b'ye, b'yi c'ye, c'yi a'ya tercih eder: Hangi aday seçilirse seçilsin çoğunluk başka birini ister.

İstenen özellikler: **Pareto koşulu**, **Condorcet kazananı koşulu** (her ikili karşılaşmayı kazanan aday birinci olmalı), **ilgisiz seçeneklerden bağımsızlık** (IIA), **diktatör yok**. **Arrow teoremi:** En az üç seçenekte dördünü birden sağlayan kural yoktur.

Kurallar: **basit çoğunluk** (iki aday), **çoğulluk** (en çok birinci tercih), **Borda sayımı** (k aday: k, k−1, … puan), **onay oylaması**, **anında ikinci tur** (en az birinci tercihi alan elenir), **gerçek çoğunluk** (Condorcet kazananı; her seçim sonuçlanmaz).

Kodumuzdaki 9 seçmenlik örnekte (4: A ≻ C ≻ B, 3: B ≻ C ≻ A, 2: C ≻ B ≻ A) çoğulluk **A**, anında ikinci tur **B**, Borda ve Condorcet **C** seçer.

**Gibbard–Satterthwaite teoremi:** İkiden fazla seçenekte Pareto koşulunu sağlayan her toplumsal seçim fonksiyonu ya **manipüle edilebilir** ya da diktatörlüktür. Aynı örnekte C'yi destekleyen 2 seçmen B'ye oy verirse kazanan A'dan B'ye döner ve onlar için daha iyidir (A9).

### 7.5 Pazarlık

**Dönüşümlü teklif protokolü:** Değeri 1 olan pastayı (x, 1 − x) bölmek. A1 teklif eder, A2 kabul ya da ret; sonra roller değişir. Anlaşma olmazsa **çatışma anlaşması** (herkes için en kötüsü).

- **Tek tur (ültimatom oyunu):** İlk teklif veren hepsini alır.
- **Sabit tur sayısı:** Son teklifi veren hepsini alır.
- **Sınırsız tur:** Her (x, 1 − x) bir Nash dengesiyle elde edilebilir: sonsuz denge.
- **Sabırsızlık** (indirim γᵢ): İki turda A1 (1 − γ₂, γ₂) önerir. Sınırsız turda (Rubinstein) A1 **(1 − γ₂)/(1 − γ₁γ₂)** alır. Sabırlı olan daha çok alır; eşit sabırda ilk teklif verenin üstünlüğü γ → 1 iken kaybolur (A10).

**Görev odaklı alanlar:** Görevlerin başlangıç dağılımı var; teklifler görevlerin yeniden dağılımı. Maliyet tekdüze, c(∅) = 0 (ör. freze tezgâhı kurulumu 10, görev başına 1: iki görev 12, beş görev 15). **Tekdüze taviz protokolü:** Eşzamanlı teklifler; biri karşı teklifi kendisininki kadar iyi bulunca anlaşma; her turda ya aynı teklif ya taviz; kimse taviz vermezse çatışma. **Zeuthen stratejisi:** Çatışma riskini en az göze alabilen (kaybedeceği daha çok olan) taviz verir.

(Not: Kitapta görev odaklı alanda faydanın tanımı c(Tᵢ) − c(Tᵢ⁰) diye basılmış; metindeki anlama, yani "kazanç"a göre doğrusu c(Tᵢ⁰) − c(Tᵢ)'dir.)

---

## Sık yapılan hatalar

| Yanılgı | Doğrusu |
|---|---|
| "Rasyonel oyuncular her zaman toplum için iyi sonuca varır." | Mahkûm ikileminde baskın strateji dengesi Pareto en iyi değildir. |
| "Nash dengesi tektir." | Koordinasyon oyununda iki denge var; sonsuz tekrarlı oyunlarda sonsuz sayıda. |
| "Her oyunun saf bir Nash dengesi vardır." | Yazı-turada yok; karma stratejilerde her zaman var (Nash). |
| "Stratejini gizlemek gerekir." | Maksimin stratejisi açığa çıksa bile aynı değeri garanti eder. |
| "Tekrarlı ikilemde de hep tanık olunur." | Yalnızca tur sayısı sabit, sonlu ve bilinirse; sonsuz tekrarda ACIMASIZ işbirliğini sürdürür. |
| "Her Nash dengesi makuldür." | İnandırıcı olmayan tehditlere dayanan dengeler alt oyun yetkin değildir. |
| "Çekirdekteki her paylaşım adildir." | Çekirdek istikrarı söyler, adaleti değil; adalet için Shapley. |
| "Birinci fiyat açık artırmada dürüst teklif en iyisidir." | Dürüst olan ikinci fiyat (Vickrey); n + 1 fiyatlı reklam yuvaları da dürüst değildir. |
| "İyi bir oylama kuralı bulunabilir." | Arrow ve Gibbard–Satterthwaite: Her kuralın bir kusuru vardır. |

## Kendini yokla

1. Çok efektörlü, çok gövdeli ve çok ajanlı planlama arasındaki fark nedir?
2. Baskın strateji dengesi neden her zaman bir Nash dengesidir?
3. Mahkûm ikilemine neden "ikilem" denir?
4. Morra'da oyunun değerini maksimin yöntemiyle bul. Neden ikinci oynayan saf strateji seçebilir?
5. ACIMASIZ–ACIMASIZ neden bir Nash dengesidir, GÜVERCİN–GÜVERCİN neden değildir?
6. Alt oyun yetkin Nash dengesi hangi sorunu çözer?
7. Basit pokerde neden 4 × 4'lük bir matris çıkar? Gerçek pokerde bu yaklaşım neden işe yaramaz?
8. Çekirdek ile Shapley değeri hangi soruları yanıtlar?
9. Vickrey açık artırmasında dürüst teklif neden baskındır?
10. Arrow teoremi ne söyler?

## Kod rehberi

```bash
python ornekler/oyun_kurami.py        # mahkûm ikilemi, koordinasyon, yazı-tura, Morra (LP)
python ornekler/tekrarli_oyunlar.py   # geriye tümevarım, sonlu durum makineleri, halk teoremi
python ornekler/uzun_bicim.py         # alt oyun yetkinliği, basit poker, ataş oyunu
python ornekler/isbirlikci_oyunlar.py # koalisyon yapıları, çekirdek, Shapley, MC-ağları
python ornekler/mekanizma_tasarimi.py # açık artırmalar, VCG, ortak kaynaklar, oylama, pazarlık
python cozumler/alistirma_kod.py      # A1, A3–A10
```

## Terimler

| Türkçe | İngilizce | Kısa açıklama |
|---|---|---|
| çok ajanlı sistem | multiagent system | Birden çok aktörlü ortam |
| iyiliksever ajan varsayımı | benevolent agent assumption | Aktörler söyleneni yapar |
| çok efektörlü / çok gövdeli planlama | multieffector / multibody planning | Tek karar verici, çok efektör / gövde |
| merkezî olmayan planlama | decentralized planning | Yürütme kısmen ayrık |
| karşı taraf | counterpart | Diğer karar verici |
| koordinasyon problemi | coordination problem | Aynı plan/dengede buluşma sorunu |
| oyun kuramı | game theory | Stratejik karar verme kuramı |
| mekanizma tasarımı | mechanism design | Oyunun kurallarını tasarlamak |
| işbirlikçi / işbirlikçi olmayan oyun | cooperative / non-cooperative game | Bağlayıcı anlaşma var / yok |
| serpiştirilmiş yürütme | interleaved execution | Planların sırası korunarak karışması |
| ortak eylem / ortak plan | joint action / joint plan | Her aktörün eyleminin demeti |
| eşzamanlı eylem kısıtı | concurrent action constraint | Hangi eylemlerin birlikte olabileceği |
| uzlaşım / toplumsal yasa | convention / social law | Ortak plan seçimine kısıt |
| plan tanıma | plan recognition | Diğerinin planını hamlesinden anlamak |
| normal biçimli oyun | normal form game | Eşzamanlı, tek hamleli oyun |
| fayda matrisi | payoff matrix | İki kişilik oyunun tablosu |
| saf / karma strateji | pure / mixed strategy | Belirlenimci / rastgele politika |
| strateji profili | strategy profile | Herkesin stratejisi |
| çözüm kavramı | solution concept | Rasyonel oyunun tanımı |
| mahkûm ikilemi | prisoner's dilemma | Baskın denge Pareto en iyi değil |
| baskın strateji (güçlü / zayıf) | dominant strategy (strong / weak) | Her durumda daha iyi strateji |
| en iyi tepki | best response | Diğerlerine karşı en iyi strateji |
| Nash dengesi | Nash equilibrium | Kimse tek başına sapmak istemez |
| odak noktası | focal point | Öne çıkan denge |
| yazı-tura eşleştirme | matching pennies | Saf dengesi olmayan oyun |
| Pareto en iyi | Pareto optimal | Kimseyi kötüleştirmeden iyileştirme yok |
| faydacı / eşitlikçi sosyal refah | utilitarian / egalitarian social welfare | Toplam / en kötünün faydası |
| miyop en iyi tepki | myopic best response | Tekrarlanan tek oyunculu iyileştirme |
| sıfır toplamlı oyun | zero-sum game | Faydaların toplamı sabit |
| maksimin dengesi | maximin equilibrium | Sıfır toplamlı oyunun çözümü |
| tekrarlı oyun / aşama oyunu | repeated game / stage game | Tekrar tekrar oynanan oyun |
| geriye tümevarım | backward induction | Sondan başa çözüm |
| kısasa kısas | tit-for-tat | Karşının son hamlesini kopyala |
| ortalamaların limiti | limit of means | Sonsuz dizinin ortalama faydası |
| halk teoremleri | folk theorems | Hangi sonuçların sürdürülebildiği |
| güvenlik değeri | security value | Garanti edilebilen fayda |
| uzun biçimli oyun | extensive-form game | Oyun ağacı biçimi |
| tam / eksik bilgi | perfect / imperfect information | Ağaçtaki yerini bilmek / bilmemek |
| inandırıcı tehdit | credible threat | Gerçekten uygulanacak tehdit |
| alt oyun yetkin Nash dengesi | subgame perfect Nash equilibrium | Her alt oyunda denge |
| mükemmel hatırlama | perfect recall | Oyuncu kendi hamlelerini unutmaz |
| bilgi kümesi | information set | Ayırt edilemeyen durumlar |
| sıra biçimi | sequence form | Ağaçta doğrusal temsil |
| soyutlama | abstraction | Oyunu küçültmek |
| Bayes–Nash dengesi | Bayes–Nash equilibrium | Stratejiler üzerinde önselle denge |
| yardım oyunu | assistance game | İnsanın faydasını paylaşan robotla oyun |
| karakteristik fonksiyon | characteristic function | ν(C) |
| koalisyon / büyük koalisyon | coalition / grand coalition | Oyuncu alt kümesi / hepsi |
| koalisyon yapısı | coalition structure | Oyuncuların bölüntüsü |
| süperadditiflik | superadditivity | ν(C ∪ D) ≥ ν(C) + ν(D) |
| paylaşım / bireysel rasyonellik | imputation / individual rationality | Büyük koalisyon değerinin dağılımı |
| çekirdek | core | İtiraz edilemeyen paylaşımlar |
| Shapley değeri | Shapley value | Ortalama marjinal katkı |
| marjinal katkı | marginal contribution | ν(C ∪ {i}) − ν(C) |
| kukla / simetrik oyuncu | dummy / symmetric player | Katkısız / aynı katkılı |
| marjinal katkı ağı | marginal contribution net | Kurallarla sıkıştırılmış ν |
| sözleşme ağı | contract net | Görev duyurusu, teklif, ödül |
| özel / ortak değer | private / common value | Kişiye özgü / herkes için aynı ama belirsiz |
| İngiliz (artan teklif) açık artırması | English (ascending-bid) auction | Fiyat artarak ilerler |
| kapalı zarf açık artırması | sealed-bid auction | Tek gizli teklif |
| Vickrey (ikinci fiyat) açık artırması | Vickrey (second-price) auction | İkinci teklif ödenir; dürüst |
| verimli | efficient | Mal en çok değer verene |
| gizli anlaşma | collusion | Teklifçilerin fiyatı manipülasyonu |
| strateji geçirmez / dürüst mekanizma | strategy-proof / truth-revealing | Gerçeği söylemek baskın |
| açığa çıkarma ilkesi | revelation principle | Her mekanizmanın dürüst eşdeğeri var |
| gelir eşitliği teoremi | revenue equivalence theorem | Aynı beklenen gelir |
| ortak kaynakların trajedisi | tragedy of the commons | Bedelsiz ortak kaynağın tükenmesi |
| dışsallık | externality | Fiyatlanmayan yan etki |
| Vickrey–Clarke–Groves mekanizması | VCG mechanism | Toplam faydayı en büyükleyen dürüst mekanizma |
| kombinasyonel açık artırma | combinatorial auction | Mal kümelerine teklif |
| toplumsal seçim kuramı | social choice theory | Tercihleri birleştirme |
| toplumsal refah / seçim fonksiyonu | social welfare / choice function | Sıralama / kazanan üretir |
| Condorcet paradoksu / kazananı | Condorcet paradox / winner | Çoğunluk döngüsü / her ikiliyi kazanan |
| ilgisiz seçeneklerden bağımsızlık | independence of irrelevant alternatives | IIA |
| Arrow teoremi | Arrow's theorem | Dört koşul birlikte sağlanamaz |
| çoğulluk / Borda / onay oylaması | plurality / Borda count / approval voting | Oylama kuralları |
| anında ikinci tur | instant runoff voting | En zayıfı eleyerek tekrar |
| Gibbard–Satterthwaite teoremi | Gibbard–Satterthwaite theorem | Makul kurallar manipüle edilebilir |
| dönüşümlü teklif pazarlığı | alternating offers bargaining | Sırayla teklif |
| çatışma anlaşması | conflict deal | Anlaşmazlık sonucu |
| ültimatom oyunu | ultimatum game | Tek turluk pazarlık |
| görev odaklı alan | task-oriented domain | Görevlerin yeniden dağıtımı |
| tekdüze taviz protokolü | monotonic concession protocol | Her turda taviz ya da aynı teklif |
| Zeuthen stratejisi | Zeuthen strategy | Çatışma riskine göre taviz |
