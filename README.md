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
- İsteğe bağlı: `numpy`, `matplotlib`

```bash
cd aima-egitim
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/check_setup.py
```

Örnekler:

```bash
python ch01-giris/ornekler/vacuum_agent.py
python ch02-akilli-ajanlar/ornekler/model_based_vacuum.py
python ch03-cozum-arama/ornekler/romania_arama.py
```

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
├── ch04–ch07/              ← stub / öğrenme hedefleri
└── …
```

## Telif ve kullanım

- Kitap metni **kopyalanmaz** ve yakın parafraz yapılmaz.
- Notlar özgün Türkçe öğretim içeriğidir.
- Algoritmalar kamuya açık yöntemlerin eğitici uygulamalarıdır.

## Durum

- **Bölüm 1 (Giriş):** 🟢 hazır — notlar, özet, örnekler, alıştırmalar, quiz
- **Bölüm 2 (Akıllı ajanlar):** 🟢 hazır — notlar, modele dayalı süpürge, mimari karşılaştırma, alıştırmalar, quiz
- **Bölüm 3 (Çözüm arama):** 🟢 hazır — notlar, Romanya BFS/DFS/UCS/A*, alıştırmalar, quiz
- **Bölüm 4–7:** öğrenme hedefleri önizlemesi (stub)
- **Bölüm 8–28:** müfredatta planlı

İyi çalışmalar!
