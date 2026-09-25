# AIMA Eğitim — Yapay Zekâ: Modern Bir Yaklaşım

Russell & Norvig'in **Artificial Intelligence: A Modern Approach (AIMA), 4. baskı** kitabını baştan sona Türkçe notlar, örnek kod ve alıştırmalarla çalışmak için hazırlanmış bir eğitim deposu.

> Bu depo kitabın metnini kopyalamaz. Kavramları kendi sözlerimizle açıklar; algoritmalar herkese açık, bilinen yöntemlerin eğitici Python uygulamalarıdır.

## Bu depo nedir?

- **Türkçe öğretim notları** — her bölüm için özgün özet ve açıklamalar
- **Çalıştırılabilir örnekler** — arama, ajanlar, mantık vb. için net Python kodu
- **Alıştırmalar ve quizler** — kavramı pekiştirmek için özgün sorular
- **Müfredat yol haritası** — 28 bölüm, haftalık tempo önerisi
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
7. **Sonraki bölüme geç** — asistanla birlikte yeni bölüm notları ve kod eklenir (`CONTRIBUTING.md`).

## Önkoşullar

- **Python 3.10+**
- Temel Python (fonksiyon, sınıf, liste/sözlük)
- İsteğe bağlı: `numpy`, `matplotlib` (görselleştirme ve sayısal örnekler için)

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
python ch07-mantiksal-ajanlar/ornekler/wumpus_basit.py
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
python ch14-zamansal-olasilik/ornekler/hmm_filtreleme.py
python ch14-zamansal-olasilik/ornekler/viterbi_kucuk.py
python ch15-olasiliksal-programlama/ornekler/basit_uretimsel_model.py
python ch15-olasiliksal-programlama/ornekler/reddetme_ornekleme.py
python ch16-basit-kararlar/ornekler/beklenen_fayda.py
python ch16-basit-kararlar/ornekler/voi_mini.py
python ch17-karmasik-kararlar/ornekler/deger_yineleme.py
python ch17-karmasik-kararlar/ornekler/politika_degerlendirme.py
python ch18-cok-ajanli-karar/ornekler/mahkum_ikilemi.py
python ch18-cok-ajanli-karar/ornekler/nash_2x2.py
python ch19-ogrenme-orneklerden/ornekler/karar_agaci_mini.py
python ch19-ogrenme-orneklerden/ornekler/lineer_siniflandirma.py
python ch20-bilgi-ogrenme/ornekler/mle_beta_Bernoulli.py
python ch20-bilgi-ogrenme/ornekler/em_karisim_mini.py
python ch21-derin-ogrenme/ornekler/aktivasyon_goster.py
python ch21-derin-ogrenme/ornekler/mlp_numpy_mini.py
python ch22-pekistirmeli-ogrenme/ornekler/q_ogrenme_grid.py
python ch22-pekistirmeli-ogrenme/ornekler/epsilon_greedy_bandit.py
python ch23-dogal-dil/ornekler/n_gram_mini.py
python ch23-dogal-dil/ornekler/bow_siniflandirma.py
python ch24-derin-dil/ornekler/embedding_benzerlik.py
python ch24-derin-dil/ornekler/dikkat_skoru.py
python ch25-bilgisayarli-goru/ornekler/konvolusyon_mini.py
python ch25-bilgisayarli-goru/ornekler/histogram_ozellik.py
python ch26-robotik/ornekler/grid_lokalizasyon.py
python ch26-robotik/ornekler/potansiyel_alan_path.py
python ch27-felsefe-etik/ornekler/etik_senaryo_karti.py --demo
python ch27-felsefe-etik/ornekler/guvenlik_kontrol_listesi.py
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
├── README.md
├── MUFREDAT.md
├── CONTRIBUTING.md
├── requirements.txt
├── scripts/check_setup.py
├── ch01-giris/             ← 🟢 hazır (+ ozet.md)
├── ch02-akilli-ajanlar/    ← 🟢 hazır
├── ch03-cozum-arama/       ← 🟢 hazır (Romanya arama)
├── ch04-karmasik-ortamlar/ ← 🟢 hazır (tepe tırmanma, SA)
├── ch05-rakip-arama/       ← 🟢 hazır (minimax XOX)
├── ch06-kisit-saglama/     ← 🟢 hazır (harita boyama CSP)
├── ch07-mantiksal-ajanlar/ ← 🟢 hazır (önerme KB, ızgara)
├── ch08-birinci-derece-mantik/ ← 🟢 hazır (FOL sözlük, çeviri)
├── ch09-cikarim-birinci-derece/ ← 🟢 hazır (unify, geriye zincir)
├── ch10-bilgi-temsili/          ← 🟢 hazır (ontoloji, default)
├── ch11-klasik-planlama/        ← 🟢 hazır (STRIPS BFS)
├── ch12-belirsiz-bilgi/         ← 🟢 hazır (Bayes, naif Bayes)
├── ch13-olasiliksal-akil/        ← 🟢 hazır (Bayes ağı, enumeration)
├── ch14-zamansal-olasilik/      ← 🟢 hazır (HMM filtre, Viterbi)
├── ch15-olasiliksal-programlama/ ← 🟢 hazır (üretimsel model, reddetme)
├── ch16-basit-kararlar/         ← 🟢 hazır (MEU, VOI)
├── ch17-karmasik-kararlar/      ← 🟢 hazır (MDP, değer yineleme)
├── ch18-cok-ajanli-karar/       ← 🟢 hazır (oyun teorisi, Nash)
├── ch19-ogrenme-orneklerden/    ← 🟢 hazır (karar ağacı, perceptron)
├── ch20-bilgi-ogrenme/          ← 🟢 hazır (MLE/MAP, EM mini)
├── ch21-derin-ogrenme/          ← 🟢 hazır (numpy MLP XOR, aktivasyon)
├── ch22-pekistirmeli-ogrenme/   ← 🟢 hazır (Q-öğrenme, bandit)
├── ch23-dogal-dil/              ← 🟢 hazır (bigram LM, BoW)
├── ch24-derin-dil/              ← 🟢 hazır (gömü, dikkat skoru)
├── ch25-bilgisayarli-goru/      ← 🟢 hazır (konvolüsyon, histogram)
├── ch26-robotik/                ← 🟢 hazır (lokalizasyon, potansiyel alan)
├── ch27-felsefe-etik/           ← 🟢 hazır (senaryo kartı, güvenlik listesi)
├── ch28-AI-gelecek/             ← 🟢 hazır (yetenek haritası, proje fikirleri)
└── BITIRME.md                   ← tebrik + tekrar yolu
```

## Telif ve kullanım

- Kitap metni **kopyalanmaz** ve yakın parafraz yapılmaz.
- Notlar özgün Türkçe öğretim içeriğidir.
- Algoritmalar kamuya açık yöntemlerin eğitici uygulamalarıdır.
- Ticari kitap içeriğini paylaşmak veya dağıtmak yasaktır; lütfen kitabı yasal yoldan edinin.

## Durum

- **Bölüm 1–19:** 🟢 hazır (önceki commit’lerde)
- **Bölüm 20 (Olasılıksal modellerle öğrenme):** 🟢 hazır — MLE/MAP Bernoulli, EM iki-para, alıştırmalar, quiz
- **Bölüm 21 (Derin öğrenme):** 🟢 hazır — aktivasyon karşılaştırma, numpy MLP XOR, alıştırmalar, quiz
- **Bölüm 22 (Pekiştirmeli öğrenme):** 🟢 hazır — Q-öğrenme gridworld, ε-açgözlü bandit, alıştırmalar, quiz
- **Bölüm 23 (Doğal dil):** 🟢 hazır — bigram LM, BoW naif Bayes, alıştırmalar, quiz
- **Bölüm 24 (Derin dil):** 🟢 hazır — gömü kosinüs, dikkat softmax, alıştırmalar, quiz
- **Bölüm 25 (Bilgisayarlı görü):** 🟢 hazır — 2D konvolüsyon, histogram özellik, alıştırmalar, quiz
- **Bölüm 26 (Robotik):** 🟢 hazır — ızgara lokalizasyonu, potansiyel alan yolu, alıştırmalar, quiz
- **Bölüm 27 (Felsefe, etik, güvenlik):** 🟢 hazır — senaryo kartı, güvenlik kontrol listesi, alıştırmalar, quiz
- **Bölüm 28 (AI’nin geleceği):** 🟢 hazır — yetenek haritası, proje fikirleri, alıştırmalar, quiz
- **Müfredat 1–28:** 🟢 tamamlandı — bkz. [`BITIRME.md`](BITIRME.md)

İyi çalışmalar! Sorularını asistanla birlikte adım adım çözebilirsin.
