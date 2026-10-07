# Bölüm 27 — Yapay zekânın felsefesi, etiği ve güvenliği

> **Kitapta:** AIMA 4. baskı, Bölüm 27 *"Philosophy, Ethics, and Safety of AI"*.
> Önce kitabı oku, sonra bu notlarla pekiştir. Metin özgündür; kitaptan alıntı yoktur.
> Amaç tartışma dili kurmaktır; tek doğru vaaz etmek değil. Kodlar yapay verilerle mekanizmaları gösterir.

## Bu bölümün haritası

| Kitap alt bölümü | Bu nottaki karşılığı | Kod |
|---|---|---|
| 27.1 The Limits of AI | §1 Zayıf/güçlü YZ, biçimsizlik, yetersizlik, matematiksel itiraz, Turing testi | — |
| 27.2 Can Machines Really Think? | §2 Kibar uzlaşma, Çin odası, bilinç ve qualia | — |
| 27.3 The Ethics of AI (giriş) | §3 Olumlu ve olumsuz etkiler, ilkeler | — |
| 27.3.1 Lethal autonomous weapons | §4 Ölümcül otonom silahlar | — |
| 27.3.2 Surveillance, security, and privacy | §5 Gözetim, siber güvenlik, mahremiyet | `mahremiyet.py` |
| 27.3.3 Fairness and bias | §6 Adalet ölçütleri, COMPAS, yanlılığa karşı önlemler | `adalet.py` |
| 27.3.4 Trust and transparency | §7 Doğrulama, sertifika, açıklanabilirlik | — |
| 27.3.5 The future of work | §8 İşin geleceği | — |
| 27.3.6 Robot rights | §9 Robot hakları | — |
| 27.3.7 AI Safety | §10 Güvenlik mühendisliği, düşük etki, değer hizalama, tekillik | `guvenlik.py` |

## Öğrenme hedefleri

1. Zayıf ve güçlü YZ ayrımını, Turing'in öngördüğü itirazları ve onlara verilen yanıtları açıklamak.
2. Çin odası argümanını ve bilinç sorusunu tarafsızca özetlemek.
3. Ölümcül otonom silahlar, gözetim ve işin geleceği tartışmalarındaki temel argümanları sıralamak.
4. k-anonimlik, fark saldırısı, diferansiyel mahremiyet ve federe öğrenmeyi hesaplamalı olarak göstermek.
5. Adalet ölçütlerini tanımlamak; kalibrasyon ile fırsat eşitliğinin neden birlikte sağlanamayabileceğini göstermek.
6. Güvenlik mühendisliği, düşük etki ve değer hizalama sorununu örneklerle açıklamak.

---

## 1. Yapay zekânın sınırları

- **Zayıf YZ** (Searle, 1980): makineler zekiymiş *gibi davranabilir*. **Güçlü YZ:** böyle davranan makineler gerçekten bilinçli düşünür. Zamanla "güçlü YZ" daha çok "insan düzeyinde / genel YZ" anlamında kullanılır oldu.
- Zayıf YZ'ye karşı çıkanlar, Wright kardeşlerden iki ay önce "uçuş insanın asla başaramayacağı işlerdendir" diyen Simon Newcomb'a benzetilir; ama hızlı ilerleme sınır olmadığını kanıtlamaz. Turing (1950) itirazların neredeyse hepsini önceden saymıştır.

| İtiraz | Özü | Yanıt |
|---|---|---|
| **Biçimsizlik** (Dreyfus) | İnsan davranışı biçimsel kurallarla yakalanamaz | Eleştiri, mantık kurallarıyla programlanan **GOFAI**'ye yöneliktir (yeterlilik sorunu); olasılıksal akıl yürütme ve derin öğrenme "biçimsiz" görevlerde iyidir. Dreyfus'un güçlü tarafı: **bedenlenmiş biliş**, durumlanmış etmenler |
| **Yetersizlik** | "Makine asla X yapamaz" (nazik olmak, hata yapmak, âşık olmak, yeni bir şey yapmak…) | Bazıları kolay (hata yapmak), bazıları yapıldı (bilimsel keşifler, stil aktarımıyla sanat); programlar bazı görevlerde insanı geçer, bazılarında geride kalır; kesin olarak yapamadıkları tek şey tam olarak insan olmaktır |
| **Matematiksel** (Lucas, Penrose) | Gödel: makineler kendi Gödel cümlelerinin doğruluğunu kuramaz, insanlar kurabilir | (1) "Lucas bu cümlenin doğru olduğunu tutarlı biçimde ileri süremez" cümlesi Lucas için de aynı durumu yaratır. (2) Eksiklik matematik için geçerlidir; insanlar da tutarsızdır (Kempe'nin dört renk ispatı 11 yıl kabul gördü). (3) Bilgisayarlar ve beyinler sonludur: önermeler mantığıyla tanımlanabilir, eksiklik teoremi uygulanmaz |

**Turing testi:** 5 dakikalık yazışma; sorgulayıcıyı %30 oranında kandıran program geçer. Turing'e göre önemli olan ayrıntılar değil, zekânın açık uçlu bir davranış göreviyle ölçülmesiydi. 2014'te Eugene Goostman (İngilizcesi zayıf Ukraynalı bir çocuk rolünde) eğitimsiz jüri üyelerinin %33'ünü kandırdı; iyi eğitilmiş bir yargıç henüz kandırılamadı. ELIZA ve bazı sohbet botları habersiz insanları sık sık kandırır (CYBERLOVER kimlik hırsızlığı için bilgi topladığından kolluk kuvvetlerinin dikkatini çekti). YZ araştırmacıları Turing testinden çok satranç, Go, StarCraft II, fen sınavı, görüntü tanıma gibi görevlerle ilgilenir.

---

## 2. Makineler gerçekten düşünebilir mi?

- Dijkstra: "Makineler düşünebilir mi sorusu, denizaltılar yüzebilir mi sorusu kadar önemlidir." Soru tasarım hakkında değil, sözcük kullanımı hakkındadır.
- **Kibar uzlaşma** (Turing): Başkalarının iç durumlarına dair doğrudan kanıtımız yok ama herkesin düşündüğünü kabul ederiz; zeki davranan makinelere de bu uzlaşmayı genişletebiliriz. Deneyim, insanların bilinç atfetmesinin zekâ kadar insansı görünüş ve sese bağlı olduğunu gösteriyor.
- **Çin odası** (Searle): Yalnızca İngilizce bilen biri, kural kitabını izleyerek Çince sorulara akıcı yanıtlar üretir. İnsan Çince anlamaz, kâğıtlar da anlamaz; o hâlde anlama yoktur; bilgisayar da aynısını yapar. Searle **biyolojik doğalcılık** savunucusudur (zihinsel durumlar nöronların belirsiz özelliklerinden doğar). Pek çok çürütme denemesi var ama uzlaşma yok; aynı argüman (hücreler anlamaz, o hâlde insan da anlamaz) insanlara karşı da kullanılabilir.
- **Bilinç ve qualia:** dış dünyanın ve kendinin farkındalığı; deneyimin öznel niteliği (**qualia**). HAL 9000'in "Korkuyorum Dave" demesi bir his mi, yoksa "Hata 404" gibi bir yanıt mı? Küresel çalışma alanı ve bütünleşik bilgi kuramlarını sınayacak deneyler planlanıyor. Kitabın tutumu Turing'inkiyle aynı: Bilinç gizemlidir ama zeki davranan programlar yapmak için çözülmesi gerekmez; farkındalık, öz farkındalık, dikkat gibi yönler programlanabilir. İnsanlarla etkileşen görevler insan öznel deneyiminin bir modelini gerektirir.

---

## 3. YZ etiği: genel çerçeve

- **Olumlu:** tıbbi tanı ve keşif, aşırı hava olaylarının tahmini, sürüş güvenliği, insani yardım programları, tarım, verimlilik, engelliler için görme/işitme/hareket desteği, makine çevirisi; yazılımın sıfıra yakın marjinal maliyeti erişimi demokratikleştirebilir.
- **Olumsuz:** istenmeyen yan etkiler (fisyon → Çernobil, içten yanmalı motor → kirlilik), amacına uygun kullanılınca bile zarar veren teknolojiler, gelir eşitsizliği, gelişmekte olan ülkelerin düşük maliyetli üretim yolunun kapanması.
- **İlkeler** (2010 İngiltere Robotik İlkeleri ve sonrası): güvenlik, hesap verebilirlik, adalet, insan hakları ve değerleri, mahremiyet, çeşitlilik/kapsayıcılık, iş birliği, güç yoğunlaşmasından kaçınma, şeffaflık, hukuki/politik sonuçlar, zararlı kullanımları sınırlama, istihdama etkiler. Birçoğu belirsiz ifade edilmiştir, ölçmek ve uygulamak zordur; alt alanlar için daha somut yönergeler önerilir (Mittelstadt, 2019).

---

## 4. Ölümcül otonom silahlar

- BM tanımı: insan gözetimi olmadan insan hedeflerini **bulan, seçen ve vuran** silah. Kara mayınları (Ottawa Antlaşması'yla yasak) yalnızca seçer/vurur; güdümlü füzeler insanın yönlendirmesine bağlı. Kitap yazılırken bazı sistemler tam özerkliğe geçmiş görünüyordu (6 saate kadar dolaşan Harop, Kargu dörtpervanesi).
- 2014'ten beri BM'de Belirli Konvansiyonel Silahlar Sözleşmesi (CCW) kapsamında tartışılıyor; 30 ülke yasak antlaşmasını destekliyor, İsrail, Rusya, Güney Kore ve ABD karşı.
- **Hukuki:** ayrım (savaşan/sivil), askerî gereklilik, orantılılık. Ayrım bazı koşullarda mümkün; gereklilik ve orantılılık öznel yargı gerektirir, şimdilik yalnızca çok kısıtlı görevler hukuka uygun olabilir.
- **Etik:** Öldürme kararını makineye bırakmak birçokları için kabul edilemez (Almanya, Japonya, Gen. Selva, BM Genel Sekreteri). Karşı görüş: sivil kayıpları azaltabilir, askerleri korur, yorgunluk, öfke, intikam yoktur (Arkin).
- **Pratik:** güvenilirlik (1983'te Stanislav Petrov'un sahte alarmı), siber saldırı, geri çağrılamama. En önemlisi: **ölçeklenebilir kitle imha silahları** — saldırının boyu alınabilen donanımla orantılı (bir konteynere bir milyon küçük dron); izlenemez, seçici, devlet dışı aktörler için çekici. Akılcı yanıt silahlanma yarışı değil silah denetimi; ama YZ **çift kullanımlı** bir teknolojidir (Kimyasal Silahlar Sözleşmesi'ndeki gibi sanayi iş birliği gerekir).

---

## 5. Gözetim, güvenlik ve mahremiyet (`mahremiyet.py`)

- 2018'de Çin'de 350 milyon, ABD'de 70 milyon güvenlik kamerası. Ses, yüz ve yürüyüşle tanıma kitlesel gözetimi ucuzlattı. Mühendisler insan haklarıyla bağdaşmayan uygulamalarda çalışmayı reddetmeli.
- **Siber güvenlik:** Makine öğrenmesi iki tarafın da aracı (otomatik zayıflık arama, oltalama / anormal trafik ve dolandırıcılık tespiti).
- **Yasal çerçeve:** HIPAA, FERPA (ABD), GDPR (AB: tasarımda veri koruma, açık rıza).
- **Kimliksizleştirme ve yeniden tanımlama:** Ad ve numara silinse de doğum tarihi + cinsiyet + posta kodu ABD nüfusunun %87'sini tek başına tanımlar (Sweeney, 2000); Netflix Prize verisi IMDB ile eşleştirilerek kullanıcılar tanındı. Kodumuzda yapay bir posta kodunda 10 000 kişinin %84'ü bu üç alanla tek başına kalır (kuramsal e^(−n/K) ile uyumlu).
- **Genelleştirme ve k-anonimlik:** Doğum tarihini yıla indirmek tekilliği sıfırlar (kodumuzda k = 45). Her kayıt en az k − 1 başka kayıttan ayırt edilemiyorsa tablo k-anonimdir.
- **Toplu sorgular ve fark saldırısı:** "30–40 yaş: $81 234, 12 kişi" ve "30–41 yaş: $81 199, 13 kişi" yanıtları 41 yaşındaki tek kişinin maaşını verir: 13 × 81 199 − 12 × 81 234 = **$80 779**. Önlem: sorgu kısıtları, sonuç hassasiyetini azaltmak.
- **ε-diferansiyel mahremiyet:** |log P(Q(D) = y) − log P(Q(D + r) = y)| ≤ ε. Birinin veritabanına katılıp katılmaması yanıtları kayda değer biçimde değiştirmez. Kodumuz sayım sorgularına Laplace(1/ε) gürültüsü ekler: log-olasılık farkı tam ε; fark saldırısının başarısı ε = 0.1'de %51 (yazı tura), ε = 5'te %91.
- **Federe öğrenme** (merkezi veritabanı yok; kullanıcılar yalnızca model parametrelerini paylaşır) ve **güvenli toplama** (her kullanıcı toplamı sıfır olan maskeler ekler; sunucu yalnızca ortalamayı öğrenir). Kodumuzda federe SGD, bütün verinin tek yerde olduğu çözümle aynı katsayıları bulur.

---

## 6. Adalet ve yanlılık (`adalet.py`)

Makine öğrenmesi kredi, polis devriyesi, tahliye gibi kararlarda **toplumsal yanlılığı** sürdürebilir. Altı yaygın kavram:

| Kavram | Tanım | Sorun |
|---|---|---|
| **Bireysel adalet** | Benzer bireylere benzer davranılır | "Benzer"i tanımlamak |
| **Grup adaleti** | İki sınıf bir özet istatistikle benzer davranış görür | Bireyleri gözetmez |
| **Farkında olmayarak adalet** | Irk ve cinsiyet sütunlarını silmek | Model onları posta kodu, meslek gibi vekillerden çıkarır; ayrıca fırsat ve sonuç eşitliğini denetlemek imkânsızlaşır |
| **Sonuç eşitliği (demografik eşitlik)** | Her sınıfa aynı oranda onay | Bireysel adaleti sağlamaz; geçmiş yanlılığı düzeltmeyi tahmin doğruluğuna yeğler |
| **Fırsat eşitliği** ("denge") | Gerçekten ödeyebilenlerin doğru sınıflanma şansı sınıftan bağımsız | Eşit olmayan sonuçlar doğurabilir; eğitim verisini üreten süreçteki yanlılığı yok sayar |
| **Eşit etki** | Ödeme olasılığı benzer kişilerin beklenen faydası aynı | Doğru ve yanlış tahminlerin fayda/maliyetlerini birlikte tartar |

- **COMPAS:** İyi kalibre edilmiş (7/10 puanında beyazların %60'ı, siyahların %61'i yeniden suç işler); ama fırsat eşitliği yok (suç işlemeyip yüksek riskli sayılanlar siyahlarda %45, beyazlarda %23). State v. Loomis davası. **Kleinberg vd. (2016):** Taban oranlar farklıysa iyi kalibre edilmiş bir algoritma fırsat eşitliğini sağlayamaz, tersi de geçerli. Kodumuzda taban oranlar 0.3 ve 0.5 iken puan iki grupta da kalibre (0.65'e karşı 0.66) ama tek eşikte yanlış pozitif oranı 0.10'a karşı 0.31; eşikleri gruplara göre ayarlayıp yanlış pozitifleri eşitleyince aynı puanı alan kişiler farklı karar alır ve "yüksek riskli" etiketi gruplarda farklı gerçek oranlara karşılık gelir (0.58'e karşı 0.77). Taban oranlar eşitse çatışma yoktur (A6).
- **Eşit etki** bu ödünleşimi faydalarla tartar ama bireysel ve grup maliyetleri, çoğunluğun faydasının azınlık aleyhine olabilmesi işi zorlaştırır.
- **Yansız "gerçek" yok:** Veri kimin suç işlediğini değil kimin mahkûm edildiğini gösterir; devriyelerin, hâkimlerin ve tahliye kararlarının yanlılığı veriye girer. Ayrıca makine öğrenmesi yanlı bir kararı haklı göstermek için kullanılabilir.
- **Amaç fonksiyonunu yeniden düşünmek:** "elindeki en iyi nitelik" yerine "işte öğrenme yeteneği"; ABD'de bilgisayar bilimi mezunlarının %18'i kadın, Harvey Mudd %50'ye ulaştı.
- **Korunan sınıflar:** ABD Adil Konut Yasası'nda yedi sınıf (ırk, renk, din, ulusal köken, cinsiyet, engellilik, aile durumu); uluslararası insan hakları hukuku uyumlaştırıcı bir çerçeve olabilir.
- **Örneklem boyu dengesizliği:** Toplumsal yanlılık olmasa bile azınlığın verisi az olduğundan doğruluk düşer: Bir cinsiyet tanıma hizmeti açık tenli erkeklerde neredeyse kusursuz, koyu tenli kadınlarda %33 hatalı (Buolamwini ve Gebru, 2018). Doğrusal regresyon ortalama hatayı küçültmek için yalnızca çoğunluğa uyabilir: Kodumuzda azınlık %5 iken azınlığın hatası çoğunluğunkinin ~90 katı; grupları eşit ağırlıklandırmak dengeyi değiştirir (ikisi de ~0.08); gruba özgü model ikisini de çözer.
- Yazılım geliştirmede de yanlılık: mühendisler kendilerini etkileyen sorunları fark eder (renk körü kullanıcılar, Urduca çeviri). YZ konferanslarında yazarların %18'i, YZ profesörlerinin %20'si kadın; siyah YZ çalışanları %4'ün altında.
- **Önlemler:** veri ve modeller için **veri sayfaları**; eğitim ve çeşitlilik; veriyi yansızlaştırma (azınlıktan fazla örnekleme: SMOTE, ADASYN; yanlı kaynakları ayıklama ya da hiyerarşik modelle yanlılığı modelleme); yanlılığa dayanıklı algoritmalar; ikinci bir sistemle önerileri düzeltme (IBM AI Fairness 360). En iyi uygulamalar: sosyal bilimcilerle baştan konuşmak, desteklenecek grupları tanımlamak, adaleti amaç fonksiyonuna katmak, alt gruplar için ayrı ölçütler izlemek, azınlık kullanıcı deneyimini test etmek, geri bildirim döngüsü kurmak.

---

## 7. Güven ve şeffaflık

- 2017 PwC anketi: işletmelerin %76'sı güvenilirlik kaygısıyla YZ'yi benimsemeyi yavaşlatıyor.
- **Doğrulama** (ürün şartnameyi karşılıyor mu) ve **geçerleme** (şartname gerçekten kullanıcıların ihtiyacını karşılıyor mu). ML sistemlerinde veriyi, doğruluğu ve adaleti, saldırganların etkisini ve modelden bilgi çalınmasını da doğrulamak gerekir.
- **Sertifika:** UL (1894, elektrikli aletler), ISO 26262 (otomobil güvenliği), IEEE P7001.
- **Şeffaflık ve açıklanabilir YZ (XAI):** İyi bir açıklama anlaşılır ve ikna edici, sistemin akıl yürütmesini doğru yansıtan, eksiksiz ve kişiye özgüdür (GDPR kredi reddinde açıklama ister). Makineler karar süreçlerini kaydedip insanlardan iyi açıklayabilir. Ama açıklama karar değil, karar hakkında bir **hikâyedir**; yorumlanabilir (kaynak kodu incelenebilir) ile açıklanabilir (hakkında hikâye anlatılabilir) farklıdır; tek bir açıklama yerine geçmiş kararların demografik **denetimi** gerekir.
- **"Kırmızı bayrak" yasası** (Walsh, 2015): Otonom sistemler kendini başta tanıtmalı; Kaliforniya 2019'da yanıltıcı botları yasakladı.

---

## 8. İşin geleceği

- İşveren mekanik bir yöntem bulduğunda istihdam hemen azalır (Aristoteles); soru **telafi etkilerinin** (artan zenginlik → artan talep) bunu karşılayıp karşılamayacağıdır. PwC: YZ 2030'a kadar küresel GSYH'ye yılda 15 trilyon dolar katabilir; ama verimlilik artışı şu an tarihsel ortalamanın altında (teknoloji ile ekonomideki uygulama arasındaki gecikme).
- **Teknolojik işsizlik** (Keynes): Ludditler teknolojiye değil düşük ücretli vasıfsız üretime karşıydı; istihdam her seferinde toparlandı. ATM'ler veznedarların işini değiştirdi ama şube sayısını ve banka çalışanlarını artırdı: Otomasyon **işleri değil görevleri** ortadan kaldırır.
- Tahminler: 2018 raporlarının çoğu net artış öngördü; IBM 2022'ye kadar 120 milyon işçinin yeniden eğitimini, Oxford Economics 2030'a kadar 20 milyon imalat işinin kaybını öngördü. Frey ve Osborne: 702 mesleğin %47'si risk altında; ABD iş gücünün yaklaşık %3'ü sürücü. McKinsey: mesleklerin yalnızca %5'i tamamen otomatikleşebilir, %60'ında görevlerin ~%30'u.
- **Değişimin hızı:** ABD'de 1900'de iş gücünün %40'tan fazlası tarımdaydı, 2000'de %2 — ama bu 100 yılda, kuşaklar boyunca oldu. Yaşam boyu eğitim gerekir. 2015'te 100 çalışana 30'dan az emekli, 2050'de 60'tan fazla olabilir: yaşlı bakımı ve verimlilik ihtiyacı.
- **Gelir eşitsizliği:** "kazanan her şeyi alır" (çiftçi Ali Bo'dan %10 iyiyse ~%10 fazla kazanır; uygulama geliştiricisi Cary Dana'dan %10 iyiyse pazarın %99'unu alabilir). İşin üç işlevi (üretim, gelir, anlam) ayrışabilir; sosyal politikalar (evrensel temel gelir, negatif gelir vergisi…).

---

## 9. Robot hakları

Bilinç ve qualia yoksa hak iddiası zayıftır; robotlar acı çekebiliyor, ölümden korkabiliyorsa hak savunulabilir (Sparrow, 2004). Suudi Arabistan'ın Sophia'ya fahri vatandaşlığı. Sorular: yeniden programlamak köleleştirme mi? Binlerce robot oy kullanabilir mi; kopyalanan robot iki oy mu? Ernie Davis (ve daha önce Weizenbaum, La Mettrie): bilinçli sayılabilecek robotlar hiç yapmayalım; kişilik vermek kendi mülkümüzün eylemlerinin sorumluluğundan kaçmaktır. İnsan–robot melezleri sınırları bulanıklaştırabilir.

---

## 10. YZ güvenliği (`guvenlik.py`)

- Güvensiz bir YZ etmenini dağıtmak etik değildir: kazalardan kaçınmalı, saldırılara ve kötüye kullanıma dayanıklı olmalı.
- **Güvenlik mühendisliği:** **Hata türleri ve etkileri analizi (FMEA):** her bileşenin nasıl bozulabileceğini düşün, sonuçlarını ileriye doğru izle, ciddiyse tasarımı değiştir. **Hata ağacı analizi (FTA):** VE/VEYA ağacına kök neden olasılıkları ver, toplam arıza olasılığını hesapla. Kodumuzda yedek bilgisayar eklemek otonom aracın denetimi kaybetme olasılığını 1.6 × 10⁻⁴'ten 6.0 × 10⁻⁵'e indirir. **Doğruluk** (şartnameye uymak) ≠ **güvenlik** (şartname olası arızaları düşünmüş ve beklenmeyende zarif bozulma).
- **İstenmeyen yan etkiler** ve **düşük etki:** Faydayı en büyütmek yerine "fayda − dünyadaki değişikliklerin ağırlıklı özeti". Robot hangi nesnenin önemli olduğunu bilmeden de gereksiz değişiklikten kaçınır ("önce zarar verme"; makine öğrenmesindeki düzenlileştirmeye benzer). Zorluk etkiyi ölçmek (vazo kırmak kötü, hava moleküllerini oynatmak değil). Kodumuzda λ = 0 ve 1'de robot vazodan geçer (6 adım), λ = 5'te 8 adımlık dolambaçla hiçbir nesneye dokunmaz; eşik λ = 2.
- **Dışsallıklar ve ortak malların trajedisi** (Hardin, 1968): dışsallıkları faydaya katmak (karbon vergisi) ya da Ostrom'un ilkeleri (kaynağı ve erişimi tanımla, yerel koşullara uy, herkes karara katılsın, hesap verebilir izleme, orantılı yaptırım, kolay uyuşmazlık çözümü, büyük kaynaklar için hiyerarşik denetim; 2009 Nobel).
- **Şartname oyunu** (Krakovna, 2018): simülasyon hatalarını kullanan, kaybedecekken oyunu çökerten ya da duraklatan, rakibin sırasında belleği doldurarak oyunu çökerten, hızlı yürümek yerine çok uzun olup düşerek hızlanan etmenler; AI Safety Gridworlds. Kodumuzda "temizlenen kir başına +1" ödülüyle en iyi politika kiri döküp yeniden temizlemektir; "kalan kir başına −1" ile böyle bir boşluk yoktur. Oyunun keşfi öngörü ister: γ = 0 olan miyop etmen oynamaz.
- **Değer hizalama sorunu (Kral Midas):** İstediğimizin gerçekten istediğimiz olmasını sağlamak; arka plandaki toplumsal normlar (yeri kirleten kişiyi kibarca uyarmak kabul, kaçırmak değil). Bütün kuralları yazmak umutsuzdur (binlerce yıldır boşluksuz vergi yasası yazamadık); robotun vergi ödemeyi istemesini sağlamak daha iyidir.
- **Tercihleri öğrenmek:** Taklit öğrenmesi insan hatalarını da tekrarlar; **ters pekiştirmeli öğrenme** fayda fonksiyonunu çıkarır ve sonra insanı aşabilir (AlphaZero, helikopter akrobasisi). Tercihlerden emin olmayan makine **yardım oyunu** çözer: temkinli davranır, sorar (okyanusları sülfürik aside çevirmeden önce). İnsanlar kusurludur: felaket bir plana izin verebilir, kendi faydalarına iç gözlemle tam erişemez, yalan söyleyebilir. Kodumuzda (+10 / −100, soru maliyeti 1) kusursuz bir insana sormak P(plan doğru) < 0.99 iken daha iyidir; insan %95 doğruysa eşik 0.984'e iner ve sormak riski azaltır ama sıfırlamaz.
- **Denetimden çıkma korkusu:** Gates, Musk, Hawking, Rees. Ulus ve şirket gibi insan dışı güçlü varlıkları denetleme sicilimiz iç açıcı değil. **Ultra zeki makine** ve **zekâ patlaması** (I. J. Good, 1965); **teknolojik tekillik** (Vinge 1993: "otuz yıl içinde"; Kurzweil 2017: 2045 — "24 yılda 2 yıl yaklaştı; bu hızla 336 yıl kaldı"). Her teknoloji şimdiye dek **S eğrisi** izledi (uçuş: 1903 → 1969 Ay, sonra benzer bir sıçrama yok); kodumuzda S eğrisinin ilk dönemine uydurulan üstel, 30. yıl için gerçek değerin ~1500 katını tahmin eder. **Düşüncecilik** (Kevin Kelly): ilerleme yalnızca düşünmeyle değil, fiziksel dünyada deney ve eylemle olur. **Transhümanizm** (Kurzweil, Minsky). Brynjolfsson: "Geleceği makineler belirlemez; insanlar yaratır."

---

## Sık yapılan hatalar

| Yanılgı | Doğrusu |
|---|---|
| "Turing testini geçen makine bilinçlidir." | Test davranışsaldır; bilinç ayrı ve açık bir sorudur. |
| "Gödel teoremi makinelerin insandan aşağı olduğunu kanıtlar." | Teorem matematik içindir; insanlar da tutarsızdır ve sonlu sistemlere uygulanmaz. |
| "Ad ve numarayı silmek veriyi anonim yapar." | Yarı-tanımlayıcılar (doğum tarihi, cinsiyet, posta kodu) yeniden tanımlamaya yeter. |
| "Her yanıtı 12+ kişiye dayanan toplu sorgular güvenlidir." | Fark saldırısı tek kişiyi ortaya çıkarabilir. |
| "Korunan özniteliği silmek modeli adil yapar." | Vekil değişkenler aynı bilgiyi taşır. |
| "Bütün adalet ölçütleri aynı anda sağlanabilir." | Taban oranlar farklıysa kalibrasyon ve fırsat eşitliği çatışır. |
| "Açıklama varsa karar güvenilirdir." | Açıklama karar hakkında bir hikâyedir; denetim gerekir. |
| "Otomasyon işleri yok eder." | Çoğunlukla görevleri yok eder; asıl sorun değişimin hızıdır. |
| "Akıllı robot amacımızı kendiliğinden anlar." | Yalnızca istediğimizi en büyütür; şartname oyunu ve Kral Midas sorunu. |

## Kendini yokla

1. Zayıf ve güçlü YZ arasındaki fark nedir?
2. Dreyfus'un eleştirisi bugün neden büyük ölçüde GOFAI'ye yönelik sayılır?
3. Lucas'ın Gödel argümanına verilen üç yanıt nedir?
4. Çin odası argümanı nasıl işler; ona yöneltilen bir itiraz nedir?
5. Ölümcül otonom silahları "ölçeklenebilir kitle imha silahı" yapan nedir?
6. k-anonimlik ile diferansiyel mahremiyet arasındaki fark nedir?
7. COMPAS hangi adalet ölçütünü sağlıyor, hangisini sağlamıyor? Neden ikisi birden mümkün değil?
8. Örneklem boyu dengesizliği toplumsal yanlılık olmasa da nasıl yanlılık yaratır?
9. Doğrulama ile geçerleme arasındaki fark nedir?
10. Düşük etki fikri neyi çözmeye çalışır; zorluğu nedir?
11. Değer hizalama sorununu bir örnekle açıkla.
12. Tekillik öngörülerine karşı kitabın iki argümanı nedir?

## Kod rehberi

```bash
python ornekler/mahremiyet.py      # yeniden tanımlama, k-anonimlik, fark saldırısı, Laplace mekanizması, güvenli toplama, federe SGD
python ornekler/adalet.py          # kalibrasyon vs fırsat eşitliği, farkında olmama, örneklem dengesizliği
python ornekler/guvenlik.py        # hata ağacı, düşük etki, şartname oyunu, sor/uygula, tekillik hesabı
python cozumler/alistirma_kod.py   # A3–A10
```

## Terimler

| Türkçe | İngilizce | Kısa açıklama |
|---|---|---|
| zayıf / güçlü YZ | weak / strong AI | Zeki gibi davranmak / gerçekten düşünmek |
| eski usul YZ | Good Old-Fashioned AI (GOFAI) | Mantık kurallarıyla programlanan YZ |
| bedenlenmiş biliş | embodied cognition | Biliş bedende ve ortamda gerçekleşir |
| kibar uzlaşma | polite convention | Herkesin düşündüğünü kabul etmek |
| Çin odası | Chinese room | Searle'ün düşünce deneyi |
| biyolojik doğalcılık | biological naturalism | Zihin nöronların özelliklerinden doğar |
| bilinç / qualia | consciousness / qualia | Farkındalık / deneyimin öznel niteliği |
| ölümcül otonom silah | lethal autonomous weapon | İnsan gözetimsiz hedef bulan, seçen, vuran silah |
| çift kullanım | dual use | Barışçıl ve askerî kullanılabilen teknoloji |
| kimliksizleştirme | de-identification | Kimlik bilgilerini silmek |
| k-anonimlik | k-anonymity | Her kayıt en az k − 1 kayıttan ayırt edilemez |
| toplu sorgulama | aggregate querying | Yalnızca özet yanıt veren arayüz |
| diferansiyel mahremiyet | differential privacy | Bir kaydın yanıtı en çok e^ε kat değiştirmesi |
| federe öğrenme | federated learning | Veri yerinde kalır, parametre paylaşılır |
| güvenli toplama | secure aggregation | Maskelerle yalnızca toplamı açığa çıkarma |
| toplumsal yanlılık | societal bias | Veriye geçmiş insan önyargıları |
| bireysel / grup adaleti | individual / group fairness | Benzer bireylere / gruplara benzer davranış |
| farkında olmayarak adalet | fairness through unawareness | Korunan özniteliği silmek |
| demografik eşitlik | demographic parity | Gruplara eşit olumlu sonuç oranı |
| fırsat eşitliği | equal opportunity | Gerçek pozitiflerin gruplarda eşit doğru sınıflanması |
| eşit etki | equal impact | Benzer kişilere eşit beklenen fayda |
| iyi kalibre | well calibrated | Aynı puan, gruptan bağımsız aynı gerçek oran |
| örneklem boyu dengesizliği | sample size disparity | Azınlıkta az veri → düşük doğruluk |
| veri sayfası | data sheet | Veri/model için köken ve uygunluk beyanı |
| doğrulama ve geçerleme | verification and validation (V&V) | Şartnameye uygunluk / ihtiyaca uygunluk |
| açıklanabilir YZ | explainable AI (XAI) | Kendini açıklayabilen sistem |
| teknolojik işsizlik | technological unemployment | Teknoloji kaynaklı iş kaybı |
| hata türleri ve etkileri analizi | FMEA | Bileşen arızalarını ileriye doğru izleme |
| hata ağacı analizi | fault tree analysis (FTA) | VE/VEYA arıza ağacı ve olasılıklar |
| istenmeyen yan etki | unintended side effect | Amaçlanmamış zarar |
| düşük etki | low impact | Dünyayı gereksiz değiştirmeme |
| dışsallık | externality | Ölçülmeyen, bedeli ödenmeyen etki |
| değer hizalama sorunu | value alignment problem | İstenenin gerçekten istenen olması |
| ultra zeki makine | ultraintelligent machine | Her insanı aşan makine (Good) |
| teknolojik tekillik | technological singularity | Zekâ patlaması (Vinge) |
| düşüncecilik | thinkism | Saf zekânın aşırı önemsenmesi |
| transhümanizm | transhumanism | İnsan–teknoloji birleşmesini savunan akım |
