# Bölüm 6 — Kısıt sağlama problemleri (CSP)

> AIMA 4. baskı, Bölüm 6 · *Constraint Satisfaction Problems*

## Öğrenme hedefleri

1. Problemleri değişken, alan ve kısıt olarak modellemek.
2. AC-3'ü uygulamak; yay tutarlılığının güç ve sınırlarını göstermek.
3. Geri izlemeyi MRV, derece, LCV, ileri kontrol ve MAC ile hızlandırmak ve etkilerini ölçmek.
4. Min-çatışma yerel aramasını açıklamak.
5. Ağaç yapısı, kesme kümesi ve simetriden yararlanmak.

## Çalışma sırası

1. Kitapta Bölüm 6'yı oku.
2. [`notlar.md`](notlar.md)
3. Örnekleri çalıştır.
4. [`alistirmalar.md`](alistirmalar.md) → [`cozumler/`](cozumler/)
5. [`quiz.md`](quiz.md)

## Dosyalar

| Dosya | İçerik |
|---|---|
| `ornekler/kisit.py` | CSP kütüphanesi: AC-3, geri izleme (MRV/derece/LCV, ileri kontrol/MAC), min-çatışma, ağaç çözücü, kesme kümesi |
| `ornekler/avustralya_csp.py` | Kitaptaki örnek: ileri kontrol izi, MAC, LCV, 18 çözüm, {SA} kesme kümesi |
| `ornekler/harita_boyama_csp.py` | Türkiye'nin 7 bölgesi (il sınırlarına göre): 3 renk yetmez, 4 renk yeter |
| `ornekler/n_vezir_csp.py` | N-vezir: sezgisellerin ve çıkarımın maliyete etkisi |
| `ornekler/min_catisma_vezir.py` | Min-çatışma (numpy): adım sayısı n'den bağımsız |
| `ornekler/sudoku_csp.py` | Sudoku: AC-3 kolay bulmacayı tek başına çözer; zor bulmaca için MRV + MAC |
| `ornekler/kriptaritmetik.py` | TWO + TWO = FOUR (7 çözüm), SEND + MORE = MONEY |
| `alistirmalar.md` | 10 alıştırma |
| `cozumler/` | Tüm çözümler (A7, A9, A10 kod) |
| `quiz.md` | 12 soru + cevaplar |

> **Düzeltme notu:** Deponun ilk sürümünde Türkiye haritasının komşulukları hatalıydı (İç Anadolu–Güneydoğu sınırı eklenmiş, Akdeniz–Doğu Anadolu sınırı atlanmıştı) ve harita 3 renkle "çözülüyordu". Gerçek komşuluklarla 4 renk gerekir; bkz. A3 çözümü.

## Kitapla doğrulama

`tests/test_ch06_csp.py`:

| Değer | Kitap | Kod |
|---|---|---|
| Avustralya, 3 renk, çözüm sayısı | 6 × 3 = 18 (renk permütasyonları × Tazmanya) | ✔ |
| İleri kontrol: WA=K, Q=Y, V=M sonrası SA | boş alan | ✔ |
| MAC: WA=K, Q=Y | tutarsızlığı hemen bulur | ✔ |
| LCV: WA=K, NT=Y iken Q | kırmızı, maviden önce | ✔ |
| {SA} kesme kümesi | kalan graf ağaç | ✔ |
| NT < SA < WA simetri kırma | d! kat azalma (18 → 3) | ✔ |
| Min-çatışma, büyük n | adım sayısı n'den bağımsız | ✔ |
| TWO + TWO = FOUR | (çözüm sayısı: 7, kaba kuvvetle doğrulandı) | ✔ |
