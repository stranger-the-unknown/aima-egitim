# Bölüm 10 — Bilgi temsili

> AIMA 4. baskı, Bölüm 10 · *Knowledge Representation*

## Öğrenme hedefleri

1. Ontolojileri, kategorileri, parçaları, ölçüleri, şeyleri ve maddeleri temsil etmek.
2. Olay hesabıyla ve Allen aralık ilişkileriyle zamanı modellemek.
3. Önermesel tutumlar için modal mantığı ve olası dünyaları kullanmak.
4. Anlamsal ağlarda kalıtımı ve varsayılanları uygulamak.
5. Sınırlandırma, varsayılan mantık ve doğruluk bakım sistemlerini açıklamak.

## Çalışma sırası

1. Kitapta Bölüm 10'u oku.
2. [`notlar.md`](notlar.md)
3. Örnekleri çalıştır.
4. [`alistirmalar.md`](alistirmalar.md) → [`cozumler/`](cozumler/)
5. [`quiz.md`](quiz.md)

## Dosyalar

| Dosya | İçerik |
|---|---|
| `ornekler/ontoloji_mini.py` | Taksonomi ve is_a kalıtımı |
| `ornekler/anlamsal_ag.py` | Anlamsal ağ: varsayılan geçersiz kılma (Uzun John Silver), Nixon çatışması; JTMS |
| `ornekler/olay_hesabi.py` | Olay hesabı (T, Happens, Initiates, Terminates); Allen ilişkileri, tarihsel örnekler |
| `ornekler/modal_bilgi.py` | Olası dünyalar: Süpermen/Clark, iç içe bilgi, Bond (de re / de dicto), bilmek ve inanmak |
| `ornekler/varsayilan_akil.py` | Sınırlandırma (Tweety, Nixon elması), öncelikli sınırlandırma, varsayılan mantık genişlemeleri |
| `alistirmalar.md` | 10 alıştırma |
| `cozumler/` | Tüm çözümler (A6, A8–A10 kod) |
| `quiz.md` | 12 soru + cevaplar |

## Kitapla doğrulama

`tests/test_ch10_temsil.py`:

| Değer | Kitap | Kod |
|---|---|---|
| Nixon elması, Anormal₂ ve Anormal₃ sınırlandırıldığında | 2 tercih edilen model; biri pasifist, biri değil | ✔ |
| Öncelikli sınırlandırma (önce Anormal₃) | Pasifist | ✔ |
| Tweety: kuş → uçar; penguen bilgisiyle → uçmaz | monoton olmayan | ✔ |
| Süpermen = Clark ∧ K_Lois Uçar(Süpermen) | K_Lois Uçar(Clark) çıkmaz | ✔ |
| Bond: ∃x K Casus(x) / K ∃x Casus(x) | farklı anlamlar | ✔ |
| Allen ilişkileri (kitaptaki tanımlar) | Meet, Before, During, Overlap, Starts, Finishes | ✔ |
| Kişilerin 2 bacağı var; Uzun John Silver'ın 1 | özel bilgi varsayılanı geçersiz kılar | ✔ |
