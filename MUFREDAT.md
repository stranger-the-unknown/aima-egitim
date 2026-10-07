# Müfredat — AIMA 4. baskı yol haritası

Toplam **28 bölüm**, yaklaşık **32 hafta** (haftada bir bölüm; uzun bölümlerde iki hafta). Bölümlerin hepsi hazır.

Her bölüm klasöründe aynı düzen vardır:

| Dosya | İçerik |
|---|---|
| `README.md` | Öğrenme hedefleri, dosyalar, **kitapla doğrulama** tablosu |
| `notlar.md` | Kitabın alt bölümlerine eşlenmiş özgün Türkçe notlar, sık yapılan hatalar, kendini yokla, terimler |
| `ornekler/` | Çalıştırılabilir Python örnekleri (yalnızca numpy ve matplotlib) |
| `alistirmalar.md` | 8–10 özgün alıştırma (★ kolay · ★★ orta · ★★★ zor) |
| `cozumler/` | Bütün alıştırmaların çözümleri (Markdown; kodlu çözümler `.py` dosyalarında) |
| `quiz.md` | 10–12 soru + cevaplar |

Bütün terimler tek yerde: [`SOZLUK.md`](SOZLUK.md). Kapanış ve tekrar yolu: [`BITIRME.md`](BITIRME.md).

---

## Kısım I — Yapay zekâ

**Öğrenme çıktıları:** Yapay zekânın ne olduğunu, akılcı etmen fikrini, PEAS ve ortam özelliklerini açıklamak; etmen mimarilerini ayırt etmek.

| # | Klasör | Konu (kitaptaki ad) | Hafta | Öne çıkan örnekler |
|---|---|---|---|---|
| 1 | `ch01-giris/` | Giriş (*Introduction*) | 1 | Süpürge etmeni, PEAS örnekleri, mini ELIZA |
| 2 | `ch02-akilli-ajanlar/` | Akıllı etmenler (*Intelligent Agents*) | 2 | Tablo etmeni, model tabanlı süpürge, performans ölçütü, mimari karşılaştırması |

## Kısım II — Problem çözme

**Öğrenme çıktıları:** Arama problemi tanımlamak; bilgisiz ve bilgili aramayı uygulamak; yerel arama, belirsiz ortamlarda arama, oyunlar ve kısıt sağlama problemlerini çözmek.

| # | Klasör | Konu | Hafta | Öne çıkan örnekler |
|---|---|---|---|---|
| 3 | `ch03-cozum-arama/` | Arama yoluyla problem çözme (*Solving Problems by Searching*) | 3–4 | Romanya haritasında BFS, UCS, A*; 8-bulmaca ve sezgiseller |
| 4 | `ch04-karmasik-ortamlar/` | Karmaşık ortamlarda arama (*Search in Complex Environments*) | 5 | Tepe tırmanma (n-vezir), benzetimli tavlama, genetik algoritma, VE–VEYA arama, inanç durumları, LRTA* |
| 5 | `ch05-rakip-arama/` | Rakip arama ve oyunlar (*Adversarial Search and Games*) | 6–7 | Minimax ve alfa–beta (XOX), beklenti-minimax, MCTS |
| 6 | `ch06-kisit-saglama/` | Kısıt sağlama problemleri (*Constraint Satisfaction Problems*) | 8 | Harita boyama (MRV, ileri denetim), n-vezir, min-çatışma, sudoku, kriptaritmetik |

## Kısım III — Bilgi, akıl yürütme ve planlama

**Öğrenme çıktıları:** Önermeler ve birinci derece mantıkla bilgi temsil etmek; çıkarım yapmak; ontolojiler kurmak; planlama problemlerini tanımlayıp çözmek.

| # | Klasör | Konu | Hafta | Öne çıkan örnekler |
|---|---|---|---|---|
| 7 | `ch07-mantiksal-ajanlar/` | Mantıksal etmenler (*Logical Agents*) | 9 | Önermeler mantığı, ileri/geri zincirleme, wumpus dünyası, SAT faz geçişi |
| 8 | `ch08-birinci-derece-mantik/` | Birinci derece mantık (*First-Order Logic*) | 10 | Modeller, akrabalık alanı, Türkçeden mantığa çeviri, tam toplayıcı devresi |
| 9 | `ch09-cikarim-birinci-derece/` | Birinci derece mantıkta çıkarım (*Inference in First-Order Logic*) | 11 | Birleştirme, ileri/geri zincirleme, çözümleme, Prolog'da kural sırası tuzağı |
| 10 | `ch10-bilgi-temsili/` | Bilgi temsili (*Knowledge Representation*) | 12 | Ontoloji, olay hesabı, kip mantığı, anlamsal ağlar, varsayılan akıl yürütme |
| 11 | `ch11-klasik-planlama/` | Otomatik planlama (*Automated Planning*) | 13 | Eylem şemaları, blok dünyası, hiyerarşik planlama, kritik yol zamanlaması |

## Kısım IV — Belirsiz bilgi ve akıl yürütme

**Öğrenme çıktıları:** Olasılık ve Bayes ağlarıyla belirsizliği modellemek; zamansal modeller ve olasılıksal programlar kurmak; karar kuramı, MDP, POMDP ve oyun kuramını kullanmak.

| # | Klasör | Konu | Hafta | Öne çıkan örnekler |
|---|---|---|---|---|
| 12 | `ch12-belirsiz-bilgi/` | Belirsizliği nicelemek (*Quantifying Uncertainty*) | 14 | Bayes kuralı, diş hekimi alanı, Hollanda kitabı, naif Bayes, wumpus'ta olasılık |
| 13 | `ch13-olasiliksal-akil/` | Olasılıksal akıl yürütme (*Probabilistic Reasoning*) | 15–16 | Hırsız alarmı ağı, kesin çıkarım, örnekleme, nedensel ağlar |
| 14 | `ch14-zamansal-olasilik/` | Zamanda olasılıksal akıl yürütme (*Probabilistic Reasoning over Time*) | 17 | Şemsiye dünyası (HMM), Kalman süzgeci, parçacık süzgeci, lokalizasyon |
| 15 | `ch15-olasiliksal-programlama/` | Olasılıksal programlama (*Probabilistic Programming*) | 18 | Üretimsel modeller, reddetme örneklemesi, beceri derecelendirme, açık evren |
| 16 | `ch16-basit-kararlar/` | Basit kararlar (*Making Simple Decisions*) | 19 | Fayda kuramı, karar ağları, bilgi değeri, iyimserlik laneti |
| 17 | `ch17-karmasik-kararlar/` | Karmaşık kararlar (*Making Complex Decisions*) | 20 | 4×3 dünyası, değer ve politika yinelemesi, haydut problemleri, POMDP |
| 18 | `ch18-cok-ajanli-karar/` | Çok etmenli karar verme (*Multiagent Decision Making*) | 21 | Nash dengesi, uzun biçimli ve tekrarlı oyunlar, iş birlikçi oyunlar, mekanizma tasarımı |

## Kısım V — Makine öğrenmesi

**Öğrenme çıktıları:** Gözetimli öğrenme modellerini kurup değerlendirmek; olasılıksal modelleri veriden öğrenmek; derin ağları ve pekiştirmeli öğrenmeyi uygulamak.

| # | Klasör | Konu | Hafta | Öne çıkan örnekler |
|---|---|---|---|---|
| 19 | `ch19-ogrenme-orneklerden/` | Örneklerden öğrenme (*Learning from Examples*) | 22–23 | Karar ağacı, model seçimi, doğrusal modeller, parametrik olmayan modeller, topluluklar |
| 20 | `ch20-olasiliksal-ogrenme/` | Olasılıksal modelleri öğrenme (*Learning Probabilistic Models*) | 24 | Bayesçi öğrenme, ML/MAP, naif Bayes, sürekli modeller, EM |
| 21 | `ch21-derin-ogrenme/` | Derin öğrenme (*Deep Learning*) | 25 | Hesap çizgesi ve geri yayılım, MLP, CNN, RNN, otokodlayıcı |
| 22 | `ch22-pekistirmeli-ogrenme/` | Pekiştirmeli öğrenme (*Reinforcement Learning*) | 26 | ADP, TD, Q-öğrenme, SARSA, yaklaşık PÖ ve politika araması |

## Kısım VI — İletişim, algı ve eylem

**Öğrenme çıktıları:** Dil modellerini ve ayrıştırmayı, gömmeleri ve transformer'ı, görüntü oluşumu ve özelliklerini, robot algısı, planlaması ve denetimini uygulamak.

| # | Klasör | Konu | Hafta | Öne çıkan örnekler |
|---|---|---|---|---|
| 23 | `ch23-dogal-dil/` | Doğal dil işleme (*Natural Language Processing*) | 27 | n-gram, HMM etiketleme, PCFG ve CYK, bileşimsel anlambilim |
| 24 | `ch24-derin-dil/` | Doğal dil işleme için derin öğrenme (*Deep Learning for NLP*) | 28 | Sözcük gömmeleri, dikkat ve öz-dikkat, ışın araması |
| 25 | `ch25-bilgisayarli-goru/` | Bilgisayarlı görü (*Computer Vision*) | 29 | İzdüşüm, kenar ve doku, optik akış, stereo, nesne tespiti (NMS) |
| 26 | `ch26-robotik/` | Robotik (*Robotics*) | 30 | Monte Carlo lokalizasyonu, EKF, C-uzayı, PRM/RRT, PID ve LQR, DAGGER |

## Kısım VII — Sonuç

**Öğrenme çıktıları:** Yapay zekânın felsefi, etik ve güvenlik boyutlarını tartışmak; mahremiyet ve adalet ölçütlerini hesaplamak; alanın geleceğine bilinçli bakmak.

| # | Klasör | Konu | Hafta | Öne çıkan örnekler |
|---|---|---|---|---|
| 27 | `ch27-felsefe-etik/` | YZ'nin felsefesi, etiği ve güvenliği (*Philosophy, Ethics, and Safety of AI*) | 31 | Diferansiyel mahremiyet, adalet ölçütleri, hata ağacı, şartname oyunu |
| 28 | `ch28-AI-gelecek/` | YZ'nin geleceği (*The Future of AI*) | 32 | Kaba kuvvetin sınırları, hesaplamanın değeri, sınırlı en iyilik |

---

## Bölümler arası bağlantılar

Bazı bölümler öncekilerin kodunu ya da kavramlarını doğrudan kullanır; sırayı değiştirecekseniz bunlara dikkat edin.

- **3 → 4, 5, 11:** Arama altyapısı; yerel arama, oyunlar ve planlama aynı fikirleri genişletir.
- **7 → 8 → 9, 10:** Önermeler mantığından birinci derece mantığa ve çıkarıma.
- **12 → 13 → 14, 15:** Olasılık → Bayes ağları → zamansal modeller ve olasılıksal programlar.
- **16 → 17 → 18, 22:** Fayda → MDP (Bölüm 22 Bölüm 17'nin `mdp.py`'sini kullanır) → oyunlar ve pekiştirmeli öğrenme.
- **19 → 20, 21:** Bölüm 20, Bölüm 19'un `karar_agaci.py`'sini kullanır; derin öğrenme 19'daki genelleme fikirlerine dayanır.
- **21 → 24, 25:** Derin ağlar → dil için derin öğrenme ve görü.
- **14, 17, 25 → 26:** Süzme, MDP/POMDP ve görü robotikte birleşir.
- **18, 22, 26 → 27:** Yardım oyunları, ters PÖ ve insan–robot etkileşimi değer hizalama tartışmasının temelidir.

## Tempo önerisi

- **Düzenli:** haftada bir bölüm, uzun bölümlerde iki hafta (yaklaşık 8 ay).
- **Yoğun:** Kısım başına 2–4 hafta; her bölümde en az notlar, örnekler ve ★/★★ alıştırmalar.
- Her bölüm sonunda: kitap → notlar → kod → alıştırmalar → quiz döngüsünü tamamlayın; zorlandıklarınızı `bekleyen-isler.md` dosyasına yazın.

## Resmi kaynaklar

- [AIMA resmi site](https://aima.cs.berkeley.edu/)
- [aimacode (GitHub)](https://github.com/aimacode)
