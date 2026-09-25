# AIMA Eğitim — Yapay Zekâ: Modern Bir Yaklaşım

Russell & Norvig'in **Artificial Intelligence: A Modern Approach (AIMA), 4. baskı** kitabını baştan sona Türkçe notlar, örnek kod ve alıştırmalarla çalışmak için hazırlanmış bir eğitim deposu.

> Bu depo kitabın metnini kopyalamaz. Kavramları kendi sözlerimizle açıklar; algoritmalar herkese açık, bilinen yöntemlerin eğitici Python uygulamalarıdır.

## Bu depo nedir?

- **Türkçe öğretim notları** — her bölüm için özgün özet ve açıklamalar
- **Çalıştırılabilir örnekler** — arama, ajanlar, mantık vb. için net Python kodu
- **Alıştırmalar ve quizler** — kavramı pekiştirmek için özgün sorular
- **Müfredat yol haritası** — 28 bölüm, haftalık tempo önerisi

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
├── ch13-olasiliksal-akil/       ← 🟢 hazır (Bayes ağı, enumeration)
└── …
```

## Telif ve kullanım

- Kitap metni **kopyalanmaz** ve yakın parafraz yapılmaz.
- Notlar özgün Türkçe öğretim içeriğidir.
- Algoritmalar kamuya açık yöntemlerin eğitici uygulamalarıdır.
- Ticari kitap içeriğini paylaşmak veya dağıtmak yasaktır; lütfen kitabı yasal yoldan edinin.

## Durum

- **Bölüm 1 (Giriş):** 🟢 hazır — notlar, özet, örnekler, alıştırmalar, quiz
- **Bölüm 2 (Akıllı ajanlar):** 🟢 hazır — notlar, modele dayalı süpürge, mimari karşılaştırma, alıştırmalar, quiz
- **Bölüm 3 (Çözüm arama):** 🟢 hazır — notlar, Romanya BFS/DFS/UCS/A*, alıştırmalar, quiz
- **Bölüm 4 (Karmaşık ortamlar):** 🟢 hazır — yerel arama, N-vezir tepe tırmanma, SA/TSP, alıştırmalar, quiz
- **Bölüm 5 (Rakip arama):** 🟢 hazır — minimax/α-β, XOX ajan-ajan, alıştırmalar, quiz
- **Bölüm 6 (Kısıt sağlama):** 🟢 hazır — CSP notları, harita boyama + N-vezir CSP, alıştırmalar, quiz
- **Bölüm 7 (Mantıksal ajanlar):** 🟢 hazır — önerme KB tell/ask, 2×2 ızgara mantığı, alıştırmalar, quiz
- **Bölüm 8 (Birinci derece mantık):** 🟢 hazır — FOL notları, Parent/Ancestor KB, TR↔FOL çeviri, alıştırmalar, quiz
- **Bölüm 9 (FOL çıkarım):** 🟢 hazır — birleştirme, geriye zincirleme, alıştırmalar, quiz
- **Bölüm 10 (Bilgi temsili):** 🟢 hazır — kategori/ontoloji, varsayılan akıl, alıştırmalar, quiz
- **Bölüm 11 (Klasik planlama):** 🟢 hazır — STRIPS şema, bloklar BFS, alıştırmalar, quiz
- **Bölüm 12 (Belirsiz bilgi):** 🟢 hazır — olasılık, Bayes kuralı, naif Bayes mini, alıştırmalar, quiz
- **Bölüm 13 (Olasılıksal akıl):** 🟢 hazır — Bayes ağı CPT, enumeration, alıştırmalar, quiz
- **Bölüm 14–28:** müfredatta planlı

İyi çalışmalar! Sorularını asistanla birlikte adım adım çözebilirsin.
