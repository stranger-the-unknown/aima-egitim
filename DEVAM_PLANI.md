# Devam planı (çalışma notu)

> Bu dosya, `egitim-iyilestirme` dalındaki iyileştirme çalışmasının nerede kaldığını kaydeder.
> Çalışmaya yeni bir oturumda (ya da başka bir bilgisayarda) devam ederken **önce bunu oku**.
> Çalışma bitip `main`'e birleştirilmeden önce bu dosya silinebilir.

Son güncelleme: 2026-10-02

---

## 1. Durum özeti

| Bölüm | Durum |
|---|---|
| 1–28 | **Bitti.** Notlar kitabın 4. baskı alt bölümlerine eşlendi; kitap örnekleri kodlandı ve testlerle doğrulandı; 8–10 alıştırmanın hepsi çözüldü; 10–12 soruluk quiz (cevap harfleri dağıtılmış). |

Bütün testler geçiyor: `python -m pytest -q`

Bölüm 16–22 2026-10-02'de, 23–28 2026-10-07'de bitti. Bölüm 17'deki değer yinelemesi çift sayım hatası, dosyalar yeniden yazılarak giderildi (`ornekler/mdp.py` kütüphanesi; `politika_degerlendirme.py` → `politika_yineleme.py`).

---

## 2. Açık konular (önemli)

1. **Bölüm 17 değer yinelemesi hatası — DÜZELTİLDİ (2026-10-02).** Not: Eski plandaki "beklenen" faydalar (0.812, 0.868, …) 3. baskıya aitti. 4. baskıda ödül geçişe ait (R(s, a, s′)) ve Şekil 17.3 değerleri 0.8516 0.9078 0.9578 / 0.8016 · 0.7003 / 0.7453 0.6953 0.6514 0.4279; testler bunları doğruluyor.
2. **PDF'teki baskı hatası (Bölüm 13):** Elimizdeki PDF'te Şekil 13.2'deki Alarm tablosu yanlış basılmış (.70/.01 tekrarı). Standart değerler (.95/.94/.29/.001) kullanıldı; `ch13-olasiliksal-akil/notlar.md` §1'de açıklandı.
3. **Bölüm 20 klasör adı — DÜZELTİLDİ (2026-10-02):** `ch20-bilgi-ogrenme` → `ch20-olasiliksal-ogrenme`; README ve MUFREDAT güncellendi.
4. **Kök dosyalar — büyük ölçüde YAPILDI (2026-10-07):** `README.md` örnek komutları ve dizin ağacı güncel (bütün yollar var); `SOZLUK.md` bütün bölümlerin "Terimler" tablolarından `python scripts/sozluk_uret.py` ile üretiliyor (876 terim; elle düzenlenmez). `BITIRME.md` yeni dosyalara bağlandı. Kalan: `MUFREDAT.md` ve `CONTRIBUTING.md` metinlerini baştan okuyup güncellemek. Modül adları bölümler arasında benzersiz olmalı (ch26'da `lokalizasyon.py`/`planlama.py` → `robot_lokalizasyon.py`/`hareket_planlama.py` yapıldı).
5. **Pull request:** Bölüm 1–22, PR #1 ile 2026-10-02'de `main`'e birleştirildi (merge commit). Bölüm 23–28 yine `egitim-iyilestirme` dalında sürecek ve yeni bir PR'la gelecek (kullanıcıya sorulmadan PR açılmaz, birleştirmeyi kullanıcı yapar).

---

## 3. Kurallar (her bölüm için)

- **Kitap metni depoya kopyalanmaz.** Kitap yalnızca başlıkları ve sayıları doğrulamak için kullanılır; anlatım özgün Türkçe.
- Her iddiayı kitaptan kontrol et: 4. baskı eski baskılardan farklı (örneğin GraphPlan yalnızca kısaca geçiyor; PlanSAT ve Sınırlı PlanSAT ikisi de PSPACE).
- Bölüm klasörü yapısı: `README.md`, `notlar.md`, `ornekler/`, `alistirmalar.md`, `cozumler/`, `quiz.md`.
- `notlar.md` düzeni: kitap alt bölümü → not bölümü → kod eşleme tablosu; öğrenme hedefleri; bölümler; "Sık yapılan hatalar"; "Kendini yokla"; "Kod rehberi"; "Terimler" (Türkçe / İngilizce / kısa açıklama).
- Kitabın kendi örnekleri kodlanır ve `tests/test_chNN_*.py` kitaptaki sayıları doğrular. Testler betikleri `tests/yardimci.py` içindeki `yukle("chNN-.../ornekler/x.py")` ile yükler.
- `tests/test_duman.py` her `ch*/**/*.py` betiğini çalıştırır (180 sn sınır); betikler hızlı kalmalı.
- `ornekler/` içindeki, başka betiklerce adıyla içe aktarılan yardımcı modüllerin adları bölümler arasında benzersiz olmalı (ör. `planlama.py`, `olasilik.py`, `bayes_agi.py`, `zamansal.py`).
- Kitap bir sayı vermiyorsa (ör. HonestRecCPT) kendi varsayımını kodda ve notta açıkça "varsayım" diye belirt.
- Quiz cevap harflerini dağıt (hepsi aynı harf olmasın).
- Her bölüm bitince commit + push (`egitim-iyilestirme` dalına; `main`'e değil).

---

## 4. Sonraki bölümler için not edilmiş kitap değerleri (yeniden doğrula)

- **26:** Monte Carlo konumlandırma.

---

## 5. Yeni bir bilgisayarda (Linux) kurulum

```bash
git clone -b egitim-iyilestirme https://github.com/stranger-the-unknown/aima-egitim.git
cd aima-egitim
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m pytest -q
```

Kitabı doğrulama için metne çevirmek (poppler-utils paketi):

```bash
pdftotext -layout "Artificial-Intelligence-A-Modern-Approach-4th edition.pdf" aima.txt
```

PDF sayfa numarası ≈ kitap sayfa numarası + 13 (Bölüm 13 civarında ölçüldü).
