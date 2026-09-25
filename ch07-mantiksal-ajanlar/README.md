# Bölüm 7 — Mantıksal ajanlar

> AIMA 4. baskı, Bölüm 7 · *Logical Agents*

## Öğrenme hedefleri

1. Bilgi tabanlı ajanın TELL/ASK döngüsünü açıklamak.
2. Gerektirmeyi modellerle tanımlamak ve doğruluk tablosuyla denetlemek.
3. CNF, çözümleme, ileri ve geri zincirlemeyi uygulamak.
4. DPLL ve WalkSAT'ı karşılaştırmak; faz geçişini göstermek.
5. Wumpus dünyasında mantıksal çıkarımla güvenli kareleri bulan bir ajan kurmak.

## Çalışma sırası

1. Kitapta Bölüm 7'yi oku.
2. [`notlar.md`](notlar.md)
3. Örnekleri çalıştır.
4. [`alistirmalar.md`](alistirmalar.md) → [`cozumler/`](cozumler/)
5. [`quiz.md`](quiz.md)

## Dosyalar

| Dosya | İçerik |
|---|---|
| `ornekler/onerme.py` | Önerme mantığı kütüphanesi: ayrıştırıcı, TT-ENTAILS, CNF, çözümleme, ileri/geri zincirleme, DPLL, WalkSAT |
| `ornekler/onerme_mantigi.py` | TELL/ASK; geçerlilik, karşılanabilirlik, eşdeğerlik |
| `ornekler/wumpus_mantik.py` | Kitaptaki R1–R5 (128 model, 3'ünde KB doğru); çözümleme kanıtı; 4×4 dünyada mantıksal ajan |
| `ornekler/ileri_geri_zincirleme.py` | Kitaptaki Horn KB: P⇒Q, L∧M⇒P, … |
| `ornekler/sat_faz_gecisi.py` | Rastgele 3-SAT: m/n ≈ 4,3 faz geçişi |
| `alistirmalar.md` | 10 alıştırma |
| `cozumler/` | Tüm çözümler (A4, A6–A9 kodla doğrulanır) |
| `quiz.md` | 12 soru + cevaplar |

```bash
python ornekler/wumpus_mantik.py
python ornekler/ileri_geri_zincirleme.py
python ornekler/sat_faz_gecisi.py
```

## Kitapla doğrulama

`tests/test_ch07_mantik.py`:

| Değer | Kitap | Kod |
|---|---|---|
| R1–R5: model sayısı, KB'nin doğru olduğu | 128, 3 | ✔ |
| KB ⊨ ¬P12; KB ⊭ ¬P22 | evet; hayır | ✔ |
| Çözümleme ile ¬P12 kanıtı | boş tümce | ✔ |
| Horn KB'de ileri zincirleme | Q çıkarılır | ✔ |
| 4×4 dünyada [1,1], [2,1], [1,2] sonrası | W13, P31, [2,2] güvenli | ✔ |
| Rastgele 3-SAT | m/n ≈ 4,3'te geçiş | ✔ (düşük oranda hep, yüksek oranda hiç karşılanabilir) |
