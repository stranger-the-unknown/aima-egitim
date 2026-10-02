# Bölüm 18 — Çok ajanlı karar verme

> AIMA 4. baskı, Bölüm 18 · *Multiagent Decision Making*

## Öğrenme hedefleri

1. Çok ajanlı ortamları (tek karar verici, ortak amaç, ayrı tercihler) ayırt etmek.
2. Normal biçimli oyunlarda baskın stratejileri, Nash dengelerini ve Pareto en iyi sonuçları bulmak.
3. İki kişilik sıfır toplamlı oyunları maksimin (doğrusal programlama) ile çözmek.
4. Tekrarlı oyunlarda işbirliğinin nasıl sürdürülebildiğini açıklamak.
5. Uzun biçimli oyunları geriye tümevarımla çözmek; inandırıcı olmayan tehditleri tanımak.
6. Çekirdek ve Shapley değeriyle işbirlikçi oyunları analiz etmek.
7. Açık artırmaları, VCG'yi, oylama kurallarını ve pazarlık protokollerini karşılaştırmak.

## Çalışma sırası

1. Kitapta Bölüm 18'i oku.
2. [`notlar.md`](notlar.md)
3. Örnekleri çalıştır.
4. [`alistirmalar.md`](alistirmalar.md) → [`cozumler/`](cozumler/)
5. [`quiz.md`](quiz.md)

## Dosyalar

| Dosya | İçerik |
|---|---|
| `ornekler/oyun_kurami.py` | Kütüphane: baskınlık, Nash, Pareto, sosyal refah, miyop en iyi tepki, maksimin (simpleks); mahkûm ikilemi, koordinasyon, yazı-tura, Morra |
| `ornekler/tekrarli_oyunlar.py` | 100 turda geriye tümevarım, sonlu durum makineleri, ortalamaların limiti, halk teoremi |
| `ornekler/uzun_bicim.py` | Geriye tümevarım, alt oyun yetkinliği, basit poker, ataş oyunu |
| `ornekler/isbirlikci_oyunlar.py` | Koalisyon yapıları, çekirdek, Shapley değeri, MC-ağları |
| `ornekler/mekanizma_tasarimi.py` | İngiliz ve Vickrey açık artırmaları, gelir eşitliği, reklam yuvaları, VCG, ortak kaynaklar, oylama, pazarlık |
| `alistirmalar.md` | 10 alıştırma |
| `cozumler/` | Tüm çözümler (A1, A3–A10 kod) |
| `quiz.md` | 12 soru + cevaplar |

## Kitapla doğrulama

`tests/test_ch18_oyun_kurami.py`:

| Değer | Kitap | Kod |
|---|---|---|
| Mahkûm ikilemi | (tanık, tanık) baskın ve tek Nash; Pareto en iyi olmayan tek sonuç | ✔ |
| Koordinasyon / yazı-tura | iki saf denge / saf denge yok | ✔ |
| Morra | −3 ≤ U ≤ 2; p = 7/12; değer −1/12 | ✔ (kesişim ve LP) |
| 100 turluk ikilem | her turda tanık, 500 yıl | ✔ |
| Sonsuz tekrar | GÜVERCİN −1, ŞAHİN–GÜVERCİN 0/−10, ŞAHİN −5, ACIMASIZ–ACIMASIZ −1 ve denge | ✔ |
| Şekil 18.4 | (yukarı, yukarı) alt oyun yetkin; (aşağı, aşağı) Nash | ✔ |
| Basit poker matrisi | 16 hücre; dengeler (rk, cf), (kk, cf) | ✔ (ağaçtan türetilir) |
| Ataş oyunu | 1 + 1 ⇔ θ ∈ [0.446, 0.554] | ✔ |
| Koalisyonlar | 7 koalisyon, 5 ve 15 yapı; boş çekirdek; (6, 14) çekirdekte | ✔ |
| MC-ağı | ν = 0, 4, 4, 6, 11; Shapley (2.5, 4.5, 4) | ✔ |
| Açık artırmalar | İngiliz b_o + d; reklam yuvaları 1, 2, 2.6; VCG vergileri 20 | ✔ |
| Ortak kaynaklar | −104 ve −10 | ✔ |
| Condorcet paradoksu, pazarlık | döngü; (1 − γ₂, γ₂); Rubinstein | ✔ |
