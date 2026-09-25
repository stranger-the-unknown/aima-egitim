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
source .venv/bin/activate   # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
python scripts/check_setup.py
```

İlk örnek:

```bash
python ch01-giris/ornekler/vacuum_agent.py
python ch01-giris/ornekler/peas_ornekleri.py
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
├── ch01-giris/          ← ilk hazır bölüm
├── ch02-akilli-ajanlar/ ← yakında
├── …                    ← ch03–ch07 stub
└── …
```

## Telif ve kullanım

- Kitap metni **kopyalanmaz** ve yakın parafraz yapılmaz.
- Notlar özgün Türkçe öğretim içeriğidir.
- Algoritmalar kamuya açık yöntemlerin eğitici uygulamalarıdır.
- Ticari kitap içeriğini paylaşmak veya dağıtmak yasaktır; lütfen kitabı yasal yoldan edinin.

## Durum

- **Bölüm 1 (Giriş):** hazır — notlar, örnekler, alıştırmalar, quiz
- **Bölüm 2–7:** öğrenme hedefleri önizlemesi (stub)
- **Bölüm 8–28:** müfredatta planlı

İyi çalışmalar! Sorularını asistanla birlikte adım adım çözebilirsin.
