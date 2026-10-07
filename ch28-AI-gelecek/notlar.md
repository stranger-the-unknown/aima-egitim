# Bölüm 28 — Yapay zekânın geleceği

> **Kitapta:** AIMA 4. baskı, Bölüm 28 *"The Future of AI"*.
> Önce kitabı oku, sonra bu notlarla pekiştir. Metin özgündür; kitaptan alıntı yoktur.
> Bu bölüm kitabın genel bir değerlendirmesidir; notlar onu önceki bölümlere bağlar.

## Bu bölümün haritası

| Kitap alt bölümü | Bu nottaki karşılığı | Kod |
|---|---|---|
| Giriş | §1 Neredeyiz? | — |
| 28.1 AI Components | §2 Algılayıcı ve eyleyiciler, dünya durumu, eylem seçimi, ne istediğimize karar vermek, öğrenme, kaynaklar | `hesaplama_sinirlari.py` (kaynak eğilimleri) |
| 28.2 AI Architectures | §3 Mimariler, gerçek zamanlı YZ, üst-akıl yürütme, sınırlı en iyilik, genel YZ, YZ mühendisliği, gelecek | `hesaplama_sinirlari.py` |

## Öğrenme hedefleri

1. YZ bileşenlerinin her birinde nerede olduğumuzu ve neyin eksik olduğunu önceki bölümlere bağlayarak açıklamak.
2. Kaba kuvvetin neden yetmediğini sayısal bir örnekle göstermek.
3. Her an kesilebilir algoritmaları, karar kuramsal üst-akıl yürütmeyi ve sınırlı en iyiliği açıklamak.
4. Dar ve genel YZ tartışmasını ve YZ mühendisliğinin olgunlaşma sorununu değerlendirmek.

---

## 1. Neredeyiz?

Kitap YZ'yi **yaklaşık akılcı etmenler tasarlamak** olarak gördü (Bölüm 2): refleks etmenlerinden bilgi tabanlı karar kuramsal etmenlere ve pekiştirmeli öğrenen derin öğrenme etmenlerine. Bileşen teknolojileri de çeşitli: mantıksal, olasılıksal ya da sinirsel akıl yürütme; atomik, ayrışık ya da yapılandırılmış temsiller; farklı öğrenme algoritmaları; algılayıcılar ve eyleyiciler. Uzmanların ortanca tahmini, geniş görev yelpazesinde yaklaşık insan düzeyinde YZ için 50–100 yıl (Bölüm 1); önümüzdeki on yılda ekonomiye yılda trilyonlarca dolar katması bekleniyor. Bölümün sorusu: Doğru **bileşenlere**, **mimarilere** ve **hedeflere** sahip miyiz?

---

## 2. YZ bileşenleri

| Bileşen | Durum | Eksik olan | Bağlantı |
|---|---|---|---|
| **Algılayıcılar ve eyleyiciler** | Hazır programlanabilir robotlar; otonom araç lidarı $75 000'dan $1 000'a (tek yonga $10'a inebilir); radar kâğıt yaprağı sayabiliyor; MEMS, 3B baskı | Robotik bugün 1980'lerin başındaki kişisel bilgisayar gibi; önce endüstride (kontrollü ortam), sonra evde | Bölüm 25, 26 |
| **Dünya durumunu temsil** | Nesne tanıma, alt düzey yüklemler ("fincan masada") | Üst düzey eylemleri az örnekle tanımak; süzme algoritmaları ayrışık temsil kullanır, nesne ve ilişki yok; "yukarı çıkan aşağı iner" gibi soyut zaman kavramları; tekniklerin birleştirilmesi | Bölüm 4, 7, 10, 14, 15, 21, 24 |
| **Eylem seçimi** | Hiyerarşik planlama ve hiyerarşik pekiştirmeli öğrenme | Milyarlarca adımlık planlar (dört yılda mezun olmak); POMDP'ye genişletme; hiyerarşik durum ve davranış temsillerini kendiliğinden kurmak | Bölüm 3, 11, 17 |
| **Ne istediğimize karar vermek** | Fayda en büyütme ilkede genel | Doğru fayda fonksiyonunu seçmek; her insan farklı → tercih belirsizliği altında çalışmak; ödül fonksiyonları için bilgi mühendisliği, ters PÖ, doğrusal zamansal mantık; tıklamaya dayalı tercih toplama bağımlılık yaratır; "iyi geçirilen zaman" hareketi; uzun vadeli çıkarımızı koruyan **kişisel etmenler** | Bölüm 16, 17, 22, 27 |
| **Öğrenme** | Yeterli veri ve önceden tanımlı özniteliklerle insan düzeyi | Az veri, gözetimsiz veri, karmaşık yapılandırılmış temsiller; öğrenmeyi önsel bilgiyle birleştirmek (araba modellerini "Insight, Prius'a benzer ama ızgarası büyük" öğüdüyle öğrenmek); **türevlenebilir programlama**; **zayıf gözetimli** ve **öngörücü öğrenme** (LeCun); Hinton (2017): "Hepsini at ve yeniden başla" | Bölüm 19–22 |
| **Kaynaklar** | 1970'lerden beri genel işlemcilerde 100 000 kat, özel donanımla ek 1 000 kat hızlanma; web'e her gün 10¹⁸ bayttan fazla veri; paylaşılan veriden **paylaşılan modellere** geçiş | Kuantum bilgisayarlar şimdilik birkaç on kübit; büyük ölçekli ML için donanım ve yazılım atılımları gerekli | Bölüm 21, 24 |

Kaynak eğilimleri (kitaptaki sayılar; katlanma süreleri bizim hesabımız): 1 MB depolama 1969'da $1 milyon, 2019'da $0.02'den az (yaklaşık **2 yılda bir yarıya**); süper bilgisayar hızı aynı dönemde 10¹⁰ kattan fazla (**~1.5 yılda bir iki katına**); ImageNet modeli eğitimi 2014'te bir gün, 2018'de 2 dakika; en büyük modellerin eğitim hesabı 2012–2018 arasında **3.5 ayda bir iki katına** (AlphaZero için bir eksaflop/saniye-günden fazla; bazı etkili çalışmalar 100 milyon kat az hesap kullandı); arXiv'de makine öğrenmesi makaleleri 2009–2017 arasında iki yılda bir ikiye; YouTube'a her dakika 300 saat video.

---

## 3. YZ mimarileri (`hesaplama_sinirlari.py`)

- **Hangi mimari?** "Hepsi!" Zaman kritikse refleks, ileriyi planlamak için bilgiye dayalı akıl yürütme, çok veri ya da değişen ortam için öğrenme. Uzun süredir süren ayrım: **simgesel** (mantıksal/olasılıksal çıkarım) ve **bağlantıcı** (yorumlanmamış çok sayıda parametre üzerinde kayıp en küçültme) sistemler; ikisini birleştirmek (ör. olasılıksal programlama + derin öğrenme) açık bir sorun.
- **Gerçek zamanlı YZ:** Kaza gören taksi saniyenin onda birinde fren mi direksiyon mu karar vermeli ve o anı en önemli sorulara (şeritler boş mu, arkada kamyon var mı) harcamalıdır. Karmaşık alanlarda bütün problemler gerçek zamanlı olur.
- **Her an kesilebilir algoritmalar:** Çıktının niteliği zamanla artar; kesildiği anda makul bir karar hazırdır (oyun ağacında yinelemeli derinleştirme, Bayes ağlarında MCMC). Kodumuzda Monte Carlo kestiriminin hatası 10 örnekte 0.025, 100 000 örnekte 0.0006 (≈ 1/√n).
- **Karar kuramsal üst-akıl yürütme:** Bilgi değeri kuramını (Bölüm 16) tek tek hesaplamaların seçimine uygular: Bir hesaplamanın değeri, karar niteliğindeki beklenen iyileşme eksi eylemi geciktirmenin maliyetidir. MCTS'de bir sonraki oyunun başlayacağı yaprağın haydut kuramından türetilen seçimi bir örnektir. Kodumuzda benzetim ucuzladıkça etmen daha çok düşünür (maliyet 0.1 → 1.6, 0.001 → 7.7 benzetim) ve net faydası artar. Basit (miyop) hesap, tek bir benzetimin kararı değiştirmeyeceğini görüp erken durabilir; kitap üst düzey pekiştirmeli öğrenmenin bu **miyopiden** kaçındığını söyler (A5'te birkaç adım ileri bakan sürüm doğru eylemi %61 yerine %71 seçer).
- **Yansıtıcı mimari:** Ortam durumu ile etmenin kendi hesaplama durumunun birleşik durum uzayında karar verme ve öğrenme. Uzun vadede alfa–beta, gerileme planlaması, değişken eleme gibi göreve özgü algoritmaların yerini hesaplamayı iyi kararlara yönlendiren genel yöntemlerin alması beklenir.
- **Kaba kuvvet neden yetmez?** Fiziğin izin verdiği en hızlı 1 kg'lık aygıt saniyede ~10⁵¹ işlem yapar (2020'nin en hızlı süper bilgisayarından milyar trilyon trilyon kat hızlı; bir yıldızın bütün enerjisini tüketir). Borges'in *Babil Kitaplığı*'ndaki gibi İngilizce sözcük dizilerini sayarsa bir yılda ancak **11 sözcüklük** dizilere ulaşır (kodumuzda 100 000 sözcüklük sözlükle 11; 12 sözcük için ~32 yıl); 410 sayfalık kitaplar söz konusu bile değil. Bir insan hayatının ayrıntılı planı kabaca **yirmi trilyon** kas hareketidir. Bu yüzden "akılcı etmen" hedefi fazla iddialıdır.
- **Sınırlı en iyilik:** etmen = mimari + program. Mimariyi sabitle, programı mimarinin destekleyebildiği bütün programlar üzerinde değiştir: Belirli bir görev ortamında en iyi performansı veren program (ya da eşdeğerlik sınıfı) **sınırlı en iyidir**. Mükemmel akılcılığa yakın olmayabilir ama vardır ve istenir; zor olan onu (ya da yakınını) bulmaktır. Basit gerçek zamanlı ortamlarda bulunabilmiştir; MCTS'nin başarısı üst düzey karar vermeye ilgiyi canlandırdı. Kodumuzdaki oyuncak örnekte zaman pahalıysa en iyi arama derinliği 2, ucuzsa 8'dir.
- **Genel YZ:** 21. yüzyıldaki ilerleme dar görev yarışmalarıyla geldi (DARPA Grand Challenge, ImageNet, Go, satranç, poker, Jeopardy!). Turing'in listesine karşı Heinlein'ın "uzmanlaşma böcekler içindir" listesi (bez değiştirmekten sone yazmaya). Hiçbir YZ iki listeye de yetmez. Kitabın görüşü: Birçok yeni atılım gerekecek ama alan makul bir keşif–kullanım dengesi kurdu. Wright kardeşlere 1903'te "dikey kalkan, sesten hızlı, Ay'a inen genel uçuş makinesi tasarlayın" demek de, ardından her yıl ladin ağacından çift kanatlıları biraz iyileştiren yarışmalar düzenlemek de yanlış olurdu. Bileşen çalışmaları yeni alanlar açtı (GAN'lar, transformer dil modelleri); "davranış çeşitliliğine" doğru adımlar: tek bir sistemin yüz dili tanıyıp yüz dile çevirmesi, tek bir modelin beş NLP görevini yapması.
- **YZ mühendisliği:** Programcılık, yazılım mühendisliği uygulamaları, araçlar ve ekosistem oluşunca sanayi oldu. YZ henüz bu olgunlukta değil: TensorFlow, Keras, PyTorch, Caffe, Scikit-Learn, SciPy var ama GAN'lar ve derin PÖ hâlâ deneyim ve kurcalama ister. Jeff Dean: milyonlarca görev için her birini sıfırdan yapmak yerine tek dev bir sistemden göreve uygun parçaları çıkarmak (BERT, GPT-2; 68 milyar parametreli "aşırı büyük" topluluk).
- **Gelecek:** YZ şimdiye dek matbaa, sıhhi tesisat, hava yolculuğu ve telefon gibi devrimci teknolojilere benziyor: olumlu etkiler ve dezavantajlı kesimleri orantısız etkileyen yan etkiler. Farkı: Bu teknolojileri mantıksal sınırlarına götürmek insanın dünyadaki üstünlüğünü tehdit etmez; YZ'yi götürmek edebilir (Bölüm 27). Turing'in 1950 makalesinin son cümlesinin ruhu hâlâ geçerli: Önümüzü ancak biraz görebiliyoruz ama yapılacak çok şey olduğunu görebiliyoruz.

---

## Sık yapılan hatalar

| Yanılgı | Doğrusu |
|---|---|
| "Yeterince hızlı bilgisayar her şeyi kaba kuvvetle çözer." | 10⁵¹ işlem/s bile bir yılda 11 sözcüklük dizileri ancak sayar; karmaşıklık üsteldir. |
| "Hedef mükemmel akılcılıktır." | Hesaplama sınırlıyken ulaşılabilir hedef sınırlı en iyiliktir. |
| "Daha çok düşünmek hep daha iyidir." | Hesaplamanın değeri maliyetini aşmıyorsa düşünmeyi bırakıp harekete geçmek gerekir. |
| "Fayda fonksiyonunu yazmak kolaydır; zor olan optimizasyondur." | Doğru fayda fonksiyonunu bulmak başlı başına zor bir problemdir. |
| "Genel YZ için dar görevlerde çalışmak boşa zahmettir." | Bileşen çalışmaları yeni fikirler doğurdu (GAN, transformer); denge önemlidir. |
| "Derin öğrenme her öğrenme sorununu çözdü." | Az veri, yapılandırılmış temsiller ve önsel bilgiyle birleştirme hâlâ açık sorunlar. |

## Kendini yokla

1. Robotik neden 1980'lerin başındaki kişisel bilgisayarlara benzetiliyor?
2. Mevcut süzme algoritmalarının dünya durumunu temsil etmedeki iki eksiği nedir?
3. Uzun vadeli planlar için hiyerarşi neden zorunludur; eksik olan nedir?
4. Tıklamaya dayalı tercih toplamanın sorunu nedir? "Kişisel etmen" fikri neyi önerir?
5. Türevlenebilir programlama ve öngörücü öğrenme nedir?
6. Her an kesilebilir algoritmaya iki örnek ver.
7. Karar kuramsal üst-akıl yürütme bir hesaplamanın değerini nasıl tanımlar?
8. Sınırlı en iyilik nedir; neden mükemmel akılcılıktan daha uygun bir hedeftir?
9. Kitap genel YZ tartışmasında Wright kardeşler örneğiyle ne anlatır?
10. YZ'yi önceki devrimci teknolojilerden ayıran nedir?

## Kod rehberi

```bash
python ornekler/hesaplama_sinirlari.py   # Borges hesabı, kaynak eğilimleri, her an kesilebilir algoritma, hesaplamanın değeri, sınırlı en iyilik
python ornekler/yetenek_haritasi.py      # (kitap dışı) AIMA bölümlerinden modern araçlara çalışma yol haritası
python ornekler/proje_fikirleri.py       # (kitap dışı) bölümlere göre portföy mini proje fikirleri
python cozumler/alistirma_kod.py         # A2–A6
```

## Terimler

| Türkçe | İngilizce | Kısa açıklama |
|---|---|---|
| kişisel etmen | personal agent | Kullanıcının uzun vadeli çıkarını savunan yazılım etmeni |
| iyi geçirilen zaman | time well spent | Dikkat ekonomisine karşı hareket |
| türevlenebilir programlama | differentiable programming | Bütün sistemin gradyanla optimize edilebilmesi |
| zayıf gözetimli öğrenme | weakly supervised learning | Az etiket, çok etiketsiz veri |
| öngörücü öğrenme | predictive learning | Dünyanın gelecek durumlarını tahmin etmeyi öğrenmek |
| paylaşılan model | shared model | Hazır eğitilmiş, API ile sunulan model |
| simgesel / bağlantıcı | symbolic / connectionist | Mantıksal-olasılıksal çıkarım / ağırlık öğrenen ağlar |
| gerçek zamanlı YZ | real-time AI | Zaman sınırı altında karar |
| her an kesilebilir algoritma | anytime algorithm | Niteliği zamanla artan, her an yanıt veren algoritma |
| karar kuramsal üst-akıl yürütme | decision-theoretic metareasoning | Hesaplamaları bilgi değeriyle seçmek |
| yansıtıcı mimari | reflective architecture | Kendi hesaplamaları üzerine akıl yürüten mimari |
| sınırlı en iyilik | bounded optimality | Sabit mimarideki en iyi program |
| insan düzeyinde YZ | human-level AI (HLAI) | Genel YZ |
