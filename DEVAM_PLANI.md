# Devam planı (çalışma notu)

> Bu dosya, `egitim-iyilestirme` dalındaki iyileştirme çalışmasının nerede kaldığını kaydeder.
> Çalışmaya yeni bir oturumda (ya da başka bir bilgisayarda) devam ederken **önce bunu oku**.
> Çalışma bitip `main`'e birleştirilmeden önce bu dosya silinebilir.

Son güncelleme: 2026-10-02

---

## 1. Durum özeti

| Bölüm | Durum |
|---|---|
| 1–16 | **Bitti.** Notlar kitabın 4. baskı alt bölümlerine eşlendi; kitap örnekleri kodlandı ve testlerle doğrulandı; 8–10 alıştırmanın hepsi çözüldü; 10–12 soruluk quiz (cevap harfleri dağıtılmış). |
| 17–28 | **Başlanmadı.** Hâlâ ilk (Grok) sürümleri duruyor. |

Bütün testler geçiyor: `python -m pytest -q`

Bölüm 16 2026-10-02'de bitti (eski `beklenen_fayda.py` ve `voi_mini.py` kaldırıldı; yerlerini yeni örnekler aldı).

---

## 2. Açık konular (önemli)

1. **Bölüm 17 değer yinelemesi hatası — HENÜZ DÜZELTİLMEDİ.**
   `ch17-karmasik-kararlar/ornekler/deger_yineleme.py` ve `politika_degerlendirme.py` (ikisinde de aynı kod var): uç durumların ödülü hem `V[s] = TERM[s]` ile hem de `reward()` içinde (`if sp in TERM: return TERM[sp]`) sayılıyor; yani iki kez. Daha önceki bir raporda bu hatanın düzeltildiği yazılmıştı; bu doğru değildi, yalnızca geçici bir denemede doğrulanmıştı, dosyalar değişmedi.
   Yapılacak: çift sayımı kaldır; kitabın 4×3 dünyasını ekle (γ = 1, uç olmayan her durumda ödül −0.04, hareket 0.8 / 0.1 / 0.1) ve kitaptaki faydaları test et. Beklenen değerler (kitaptan yeniden doğrula):
   ```
   0.812  0.868  0.918  +1
   0.762  (duvar) 0.660  −1
   0.705  0.655  0.611  0.388
   ```
2. **PDF'teki baskı hatası (Bölüm 13):** Elimizdeki PDF'te Şekil 13.2'deki Alarm tablosu yanlış basılmış (.70/.01 tekrarı). Standart değerler (.95/.94/.29/.001) kullanıldı; `ch13-olasiliksal-akil/notlar.md` §1'de açıklandı.
3. **Bölüm 20 klasör adı:** `ch20-bilgi-ogrenme` adı içerikle uyuşmuyor (kitapta "Learning Probabilistic Models"). Yeniden adlandırılırsa testler ve bağlantılar güncellenmeli.
4. **Kök dosyalar:** `README.md` ve `MUFREDAT.md` eski; bitince güncellenmeli. Bütün bölümlerin "Terimler" tablolarından bir `SOZLUK.md` üretilecek. `BITIRME`/`CONTRIBUTING` dosyaları gözden geçirilecek.
5. **Pull request:** Hepsi bitince `egitim-iyilestirme` → `main` için PR açılacak (kullanıcıya sorulmadan açılmayacak).

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

- **17:** 4×3 dünya faydaları (yukarıda); değer yinelemesi, politika yinelemesi, POMDP.
- **18:** İki parmaklı Morra oyununun değeri, mahkûm ikilemi.
- **19:** Restoran örneği: Kazanç(Patrons) ≈ 0.541 bit, Kazanç(Type) = 0.
- **20:** Şeker torbaları: bir limonlu şekerden sonra P(sonraki limon) = 0.65.
- **22:** 4×3 dünyada pasif TD öğrenmesi.
- **23:** CYK ayrıştırma.
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
