# Bölüm 15 — Olasılıksal programlama: Özgün Notlar

> Bu notlar kitabın metninin kopyası değildir. Anlatım özgün Türkçe ve **eğitim seviyesinde hafif** tutulmuştur.
> Amaç: “program yazmak = olasılık modeli kurmak” fikrini kavramak; ağır framework’lere girmeden.

---

## 1. Neden “program olarak model”?

Bayes ağında düğüm ve CPT’leri **elle çizersiniz**.  
Olasılıksal programlamada modeli bir **üretici süreç** gibi kodlarsınız:

```text
önce rastgele seçimler yap
sonra bunlardan gözlemler türet
sorgu: bazı gözlemler sabitken gizli seçimlerin sonsalı nedir?
```

Avantaj (sezgi): döngü, rastgele nesne sayısı, koşullu dallanma gibi yapıları dilin doğal ifadeleriyle yazmak kolaylaşır.

---

## 2. Üretimsel model = örnekleme reçetesi

Saf Python’da bile:

1. `önselden örnekle` (ör. bozuk para p ~ Uniform, sonra yazı/tura)
2. Gözlemi bu örnekten üret
3. Kanıta uymayanları at veya ağırlıkla düzelt
4. Kalan örneklerden sonsal frekansı oku

`basit_uretimsel_model.py` bunu küçük bir “hileli zar / iki hipotez” senaryosuyla gösterir.

---

## 3. Bayes ağı ile bağ

Her `sample()` çağrısı aslında joint’ten bir dünya çeker.  
Programdaki rastgele seçimler ≈ ağdaki rastgele değişkenler;  
`if` ile koşullu dallanma ≈ CPT’nin farklı satırları.

Fark: klasik BN sabit grafik ister; program **dinamik** yapıya (döngü uzunluğu, rastgele uzunlukta liste) izin verebilir — bu da “açık evren”e kapı açar.

---

## 4. İlişkisel / açık-evren sezgi (yüksek seviye)

- **İlişkisel:** yalnızca tek nesne değil; “öğrenciler, dersler, kayıt ilişkisi” gibi çoklu varlıklar ve aralarındaki bağlar.
- **Açık evren:** kaç nesne olduğu baştan sabit olmayabilir — “kaç ev var?”, “hangi plaka bu?” gibi sorularda nesne kümesi de belirsizdir.

Eğitim notu: burada dil veya solver yazmıyoruz; yalnızca **“grafik sabitse BN, yapı programdaysa PP”** ayrımını akılda tutun.

---

## 5. Koşullandırma yolları (küçük ölçek)

| Yöntem | Fikir |
|--------|--------|
| Naif sayım | Çok örnek üret; kanıta uyanların oranına bak |
| **Reddetme örneklemesi** | Kanıta uymayan örnekleri at; uyanlarda sorgu frekansı |
| Ağırlıklı / MCMC | İleri konular (bu bölümde kod yok) |

`reddetme_ornekleme.py` reddetmeyi küçük bir sorgu için gösterir. Kanıt nadirse çoğu örnek atılır → verimsiz ama sezgisi berrak.

---

## 6. Ajan bakışı

1. Dünyayı **nasıl üretirim?** diye program yaz.
2. Gözlemleri kanıt olarak bağla.
3. Reddetme veya daha iyi çıkarımla sonsal al.
4. Sonsalla karar ver (sonraki karar bölümleri).
5. Yapı karmaşıklaşınca PP dillerine / BN araçlarına geç.

---

## Kaynaklar

- [aima.cs.berkeley.edu](https://aima.cs.berkeley.edu/)
- [github.com/aimacode](https://github.com/aimacode)
