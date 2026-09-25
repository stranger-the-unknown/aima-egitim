# Bölüm 28 — AI’nin geleceği: Özgün Notlar

> Bu notlar kitabın metninin kopyası değildir. Anlatım özgün Türkçe öğretim dilindedir.
> Amaç: spekülasyonu abartmadan yön bulmak; öğrenmeye devam etmek.

---

## 1. Eğilimler (abartısız)

Kabaca üç hat (birbirini dışlamaz):

| Hat | Örnek yön | Dikkat |
|-----|-----------|--------|
| **Ölçek + veri** | Büyük modeller, çok görevli öğrenme | Maliyet, enerji, değerlendirme kalitesi |
| **Araç kullanan ajanlar** | Arama, kod, API çağrısı | Güvenlik, yetki sınırı |
| **Gömülü / robotik AI** | Algı–eylem, simülasyon | Gerçek dünya belirsizliği |

Ayrıca: **açık ağırlıklar vs kapalı API**, **düzenleme**, **değerlendirme bilimini** (benchmark’ların doygunluğu) izlemek gerekir. Trend ≠ kaçınılmaz gelecek.

---

## 2. AGI tartışmaları (üst düzey)

- **Tanım belirsiz:** “genel zekâ” ölçütü üzerinde uzlaşma yok.
- **Süre tahminleri** spekülatiftir; nokta tahmin yerine senaryo + varsayım yazın.
- **Risk / fayda:** hem abartılı kıyamet hem “hiç sorun yok” uçlarından kaçının; Ch.27 güvenlik dilini kullanın.
- **Pratik odak:** Bugün dar sistemlerde güvenilirlik, adillik, izleme — bunlar AGI gelsin gelmesin değerlidir.

---

## 3. Tamamlayıcı teknolojiler

AI tek başına ürün olmaz:

- **Veri mühendisliği** — kalite, hat, özellik deposu
- **Yazılım mühendisliği** — test, CI, gözlemlenebilirlik
- **HCI / ürün** — kullanıcı ihtiyacı, yanlış beklenti yönetimi
- **Robotik / gömülü** — algı–eylem (Ch.26)
- **Güvenlik / gizlilik** — tehdit modeli (Ch.27)
- **Alan bilgisi** — sağlık, hukuk, eğitim… dikey uzmanlık

`yetenek_haritasi.py` AIMA kısımlarını bu yığınlara bağlar.

---

## 4. Öğrenmeye devam

1. **Zayıf halkayı seç** — quiz’lerde takıldığın bölüm (ör. olasılık, RL).
2. **Küçük proje** — `proje_fikirleri.py` listesinden 1–2 tane; 1–2 haftalık kapsam.
3. **Resmi kod** — [aimacode](https://github.com/aimacode) ile karşılaştır; kopyalama değil, API farkını gör.
4. **Modern yığın** — bir çerçeve (PyTorch / JAX / klasik sklearn) + bir dağıtım pratiği (basit API).
5. **Okuma disiplini** — makale özetleri: iddia / yöntem / sınır / yeniden üretilebilirlik.

Kök dizindeki `BITIRME.md` tebrik + önerilen tekrar yolu içerir.

---

## 5. Bu müfredatı bitirmek ne demek?

28 bölümün not + kod + alıştırma döngüsünü tamamladınız. Bu bir bitiş çizgisi değil; **ortak dil** kazandınız: arama, mantık, olasılık, karar, öğrenme, dil, görü, robotik, etik.

Sonraki adım sizin: zayıf nokta → proje → paylaşılabilir portföy.
