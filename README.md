# AIMA Eğitim — Yapay Zekâ: Modern Bir Yaklaşım

Russell & Norvig'in **Artificial Intelligence: A Modern Approach (AIMA), 4. baskı** kitabını baştan sona Türkçe notlar, örnek kod ve alıştırmalarla çalışmak için hazırlanmış bir eğitim deposu.

> Bu depo kitabın metnini kopyalamaz. Kavramları kendi sözlerimizle açıklar; algoritmalar herkese açık, bilinen yöntemlerin eğitici Python uygulamalarıdır.

## Bu depo nedir?

- **Türkçe öğretim notları** — her bölüm için özgün özet ve açıklamalar
- **Çalıştırılabilir örnekler** — arama, ajanlar, mantık vb. için net Python kodu
- **Alıştırmalar ve quizler** — kavramı pekiştirmek için özgün sorular
- **Müfredat yol haritası** — 28 bölüm, haftalık tempo önerisi
- **Sözlük** — [`SOZLUK.md`](SOZLUK.md): bütün bölümlerin Türkçe–İngilizce terimleri (`python scripts/sozluk_uret.py` ile üretilir)
- **Kapanış** — [`BITIRME.md`](BITIRME.md) tebrik + önerilen tekrar yolu

Kitabı yasal olarak edinmeniz gerekir. Resmi kaynaklar:

- Kitap ve kaynaklar: [https://aima.cs.berkeley.edu/](https://aima.cs.berkeley.edu/)
- Resmi kod deposu: [https://github.com/aimacode](https://github.com/aimacode)

## Asistanla birlikte nasıl çalışacağız?

Bu depo, bir yapay zekâ asistanıyla (ör. Grok) etkileşimli ders gibi kullanılmak üzere tasarlandı:

1. **Müfredata bak** — `MUFREDAT.md` içinde sıradaki bölümü seç.
2. **Kitabı oku** — ilgili AIMA bölümünü kendi nüshandandan oku.
3. **Notlara geç** — `chXX-.../notlar.md` ile kavramları kendi dilinde pekiştir.
4. **Kodu çalıştır** — `ornekler/` altındaki scriptleri çalıştır, değiştir, dene.
5. **Alıştırma yap** — `alistirmalar.md`; takılırsan asistanla çöz.
6. **Quiz çöz** — `quiz.md` ile hızlı kontrol.
7. **Not al** — anlaşılmayan ya da hatalı görünen yerleri yerel `bekleyen-isler.md` dosyasına yaz; düzeltmeler `CONTRIBUTING.md`'deki kurallarla yapılır.

## Önkoşullar

- **Python 3.10+**
- Temel Python (fonksiyon, sınıf, liste/sözlük)
- `numpy` (örneklerin çoğu için gerekli), `matplotlib` (isteğe bağlı grafikler), `pytest` (testler)

Kurulum:

```bash
cd aima-egitim
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python scripts/check_setup.py
```

Örnekler:

```bash
python ch01-giris/ornekler/vacuum_agent.py
python ch02-akilli-ajanlar/ornekler/model_based_vacuum.py
python ch03-cozum-arama/ornekler/romania_arama.py
python ch04-karmasik-ortamlar/ornekler/tepe_tirmanma_n_queens.py --yeniden-baslat 20
python ch04-karmasik-ortamlar/ornekler/simule_tavlama_demo.py
python ch05-rakip-arama/ornekler/minimax_tictactoe.py --mod ajan-ajan
python ch06-kisit-saglama/ornekler/harita_boyama_csp.py --mrv --forward
python ch06-kisit-saglama/ornekler/n_vezir_csp.py --n 8
python ch07-mantiksal-ajanlar/ornekler/onerme_mantigi.py
python ch07-mantiksal-ajanlar/ornekler/wumpus_mantik.py
python ch08-birinci-derece-mantik/ornekler/fol_sozluk.py
python ch08-birinci-derece-mantik/ornekler/fol_ceviri.py
python ch09-cikarim-birinci-derece/ornekler/birlesim_unification.py
python ch09-cikarim-birinci-derece/ornekler/geriye_zincir.py
python ch10-bilgi-temsili/ornekler/ontoloji_mini.py
python ch10-bilgi-temsili/ornekler/varsayilan_akil.py
python ch11-klasik-planlama/ornekler/aksiyon_semasi.py
python ch11-klasik-planlama/ornekler/strips_bloklar.py
python ch12-belirsiz-bilgi/ornekler/bayes_kurali.py
python ch12-belirsiz-bilgi/ornekler/naive_bayes_mini.py
python ch13-olasiliksal-akil/ornekler/cpt_goster.py
python ch13-olasiliksal-akil/ornekler/bayes_agi_kucuk.py
python ch14-zamansal-olasilik/ornekler/semsiye.py
python ch14-zamansal-olasilik/ornekler/kalman.py
python ch14-zamansal-olasilik/ornekler/parcacik_filtresi.py
python ch15-olasiliksal-programlama/ornekler/basit_uretimsel_model.py
python ch15-olasiliksal-programlama/ornekler/reddetme_ornekleme.py
python ch16-basit-kararlar/ornekler/fayda_kurami.py
python ch16-basit-kararlar/ornekler/bilgi_degeri.py
python ch17-karmasik-kararlar/ornekler/deger_yineleme.py
python ch17-karmasik-kararlar/ornekler/dort_uc_dunya.py
python ch18-cok-ajanli-karar/ornekler/oyun_kurami.py
python ch18-cok-ajanli-karar/ornekler/mekanizma_tasarimi.py
python ch19-ogrenme-orneklerden/ornekler/karar_agaci.py
python ch19-ogrenme-orneklerden/ornekler/topluluk.py
python ch20-olasiliksal-ogrenme/ornekler/istatistiksel_ogrenme.py
python ch20-olasiliksal-ogrenme/ornekler/em_algoritmasi.py
python ch21-derin-ogrenme/ornekler/hesap_grafigi.py
python ch21-derin-ogrenme/ornekler/mlp_egitim.py
python ch22-pekistirmeli-ogrenme/ornekler/pasif_ogrenme.py
python ch22-pekistirmeli-ogrenme/ornekler/aktif_ogrenme.py
python ch23-dogal-dil/ornekler/dil_modelleri.py
python ch23-dogal-dil/ornekler/ayristirma.py
python ch24-derin-dil/ornekler/gomme.py
python ch24-derin-dil/ornekler/dikkat.py
python ch24-derin-dil/ornekler/kod_cozme.py
python ch25-bilgisayarli-goru/ornekler/goruntu_olusumu.py
python ch25-bilgisayarli-goru/ornekler/ozellikler.py
python ch25-bilgisayarli-goru/ornekler/tespit.py
python ch26-robotik/ornekler/robot_lokalizasyon.py
python ch26-robotik/ornekler/hareket_planlama.py
python ch26-robotik/ornekler/kontrol.py
python ch26-robotik/ornekler/insan_robot.py
python ch27-felsefe-etik/ornekler/mahremiyet.py
python ch27-felsefe-etik/ornekler/adalet.py
python ch27-felsefe-etik/ornekler/guvenlik.py
python ch28-AI-gelecek/ornekler/hesaplama_sinirlari.py
python ch28-AI-gelecek/ornekler/yetenek_haritasi.py
python ch28-AI-gelecek/ornekler/proje_fikirleri.py
```

## Çalışma yöntemi (önerilen döngü)

| Adım | Ne yaparsın |
|------|-------------|
| 1. Oku | AIMA'da ilgili bölümü oku |
| 2. Not | `notlar.md` ile kavramları kendi cümlelerinle gözden geçir |
| 3. Kod | Örnekleri çalıştır, parametreleri değiştir |
| 4. Alıştırma | `alistirmalar.md` sorularını çöz |
| 5. Quiz | `quiz.md` ile kendini test et |
| 6. Özet | Kısa bir “öğrendiklerim” notu yaz (isteğe bağlı) |

## Depo yapısı (özet)

```
aima-egitim/
├── README.md                    ← bu dosya
├── MUFREDAT.md                  ← 28 bölümlük yol haritası, bölümler arası bağlantılar
├── SOZLUK.md                    ← bütün bölümlerin terimleri (scripts/sozluk_uret.py üretir)
├── BITIRME.md                   ← kapanış ve tekrar yolu
├── CONTRIBUTING.md              ← katkı ve doğrulama kuralları
├── DEVAM_PLANI.md               ← geliştirme durumu ve açık konular
├── requirements.txt
├── scripts/                     ← check_setup.py, sozluk_uret.py
├── tests/                       ← her bölüm için test_chNN_*.py + test_duman.py (her betiği çalıştırır)
├── ch01-giris/                  ← süpürge etmeni, PEAS, mini ELIZA (+ ozet.md)
├── ch02-akilli-ajanlar/         ← tablo etmeni, model tabanlı süpürge, performans ölçütü
├── ch03-cozum-arama/            ← Romanya haritası (BFS, UCS, A*), 8-bulmaca
├── ch04-karmasik-ortamlar/      ← tepe tırmanma, benzetimli tavlama, genetik algoritma, VE–VEYA, LRTA*
├── ch05-rakip-arama/            ← minimax, alfa–beta, beklenti-minimax, MCTS
├── ch06-kisit-saglama/          ← harita boyama, n-vezir, min-çatışma, sudoku
├── ch07-mantiksal-ajanlar/      ← önermeler mantığı, zincirleme, wumpus, SAT
├── ch08-birinci-derece-mantik/  ← modeller, akrabalık, çeviri, tam toplayıcı
├── ch09-cikarim-birinci-derece/ ← birleştirme, zincirleme, çözümleme, Prolog
├── ch10-bilgi-temsili/          ← ontoloji, olay hesabı, kip mantığı, varsayılan akıl yürütme
├── ch11-klasik-planlama/        ← otomatik planlama: eylem şemaları, hiyerarşik plan, zamanlama
├── ch12-belirsiz-bilgi/         ← Bayes kuralı, naif Bayes, Hollanda kitabı
├── ch13-olasiliksal-akil/       ← Bayes ağları, kesin çıkarım, örnekleme, nedensellik
├── ch14-zamansal-olasilik/      ← HMM (şemsiye), Kalman, parçacık süzgeci
├── ch15-olasiliksal-programlama/ ← üretimsel modeller, beceri derecelendirme, açık evren
├── ch16-basit-kararlar/         ← fayda, karar ağları, bilgi değeri
├── ch17-karmasik-kararlar/      ← MDP (4×3), değer/politika yinelemesi, haydutlar, POMDP
├── ch18-cok-ajanli-karar/       ← Nash dengesi, tekrarlı oyunlar, mekanizma tasarımı
├── ch19-ogrenme-orneklerden/    ← karar ağacı, model seçimi, doğrusal modeller, topluluklar
├── ch20-olasiliksal-ogrenme/    ← Bayesçi öğrenme, ML/MAP, EM
├── ch21-derin-ogrenme/          ← geri yayılım, MLP, CNN, RNN, otokodlayıcı
├── ch22-pekistirmeli-ogrenme/   ← ADP, TD, Q-öğrenme, SARSA, politika araması
├── ch23-dogal-dil/              ← n-gram, HMM etiketleme, PCFG ve CYK, anlambilim
├── ch24-derin-dil/              ← gömme, dikkat, transformer, ışın araması
├── ch25-bilgisayarli-goru/      ← izdüşüm, kenar, doku, optik akış, stereo, NMS
├── ch26-robotik/                ← MCL, EKF, C-uzayı, PRM/RRT, PID/LQR, DAGGER
├── ch27-felsefe-etik/           ← mahremiyet, adalet ölçütleri, güvenlik
└── ch28-AI-gelecek/             ← kaba kuvvetin sınırları, üst-akıl yürütme, proje fikirleri
```

## Telif ve kullanım

- Kitap metni **kopyalanmaz** ve yakın parafraz yapılmaz.
- Notlar özgün Türkçe öğretim içeriğidir.
- Algoritmalar kamuya açık yöntemlerin eğitici uygulamalarıdır.
- Ticari kitap içeriğini paylaşmak veya dağıtmak yasaktır; lütfen kitabı yasal yoldan edinin.

## Durum

- **28 bölümün hepsi tamam:** Notlar kitabın 4. baskısının alt bölümlerine eşlendi; kitaptaki sayısal örnekler kodla yeniden üretildi ve testlerle doğrulandı; her bölümde 8–10 alıştırma (hepsi çözümlü) ve 10–12 soruluk quiz var.
- **Testler:** `python -m pytest -q` (~380 test; GitHub Actions'ta Python 3.10, 3.12 ve 3.13 ile her push'ta çalışır).
- Geliştirme ayrıntıları ve açık konular: [`DEVAM_PLANI.md`](DEVAM_PLANI.md). Kapanış: [`BITIRME.md`](BITIRME.md).

İyi çalışmalar! Sorularını asistanla birlikte adım adım çözebilirsin.
