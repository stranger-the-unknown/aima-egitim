# Çözümler — A8, A9, A10 (kod)

Kodlar bu klasörde; çalıştırıp çıktıyı kendi sonuçlarınla karşılaştır.

## A8 — Üçüncü gevşetme: `alistirma8_gevsetme.py`

- Kitap örneği için: h1 = 8, **h_gevşek = 8**, h2 = 18, gerçek maliyet = 26.
- h_gevşek **h1'i baskılar**: Yanlış yerdeki her taş en az bir kez taşınmalıdır, boşluk kendi yerindeyse bazen ek bir hamle gerekir.
- h2'yi **baskılamaz**, h2 de onu baskılamaz. 2000 rastgele durumun çoğunda h2 daha büyüktür, ama bazılarında (ör. `1 2 _ / 4 7 8 / 3 6 5`) h_gevşek = 10 > h2 = 8 olur. Bu yüzden en iyi seçim **max(h2, h_gevşek)** olur. Bu da kabul edilebilirdir ve ikisini de baskılar.

## A9 — Ağırlıklı A*: `alistirma9_agirlikli.py`

| W | Çözüm | Üretilen | W·C* |
|---|---|---|---|
| 1,0 | 26 | 10.548 | 26 |
| 1,5 | 26 | 2.753 | 39 |
| 2,0 | 30 | 1.033 | 52 |
| 5,0 | 42 | 1.423 | 130 |

- W = 1,5'te optimal çözüm hâlâ bulunuyor ama 4 kat daha az düğümle. Pratikte "biraz ağırlık" çok verimli olabilir.
- W büyüdükçe çözüm uzar ama **W·C* sınırı her zaman tutar**.
- W = 5'in W = 2'den *fazla* düğüm üretmesi şaşırtıcı değil. Açgözlüye yaklaşan arama bazen yanlış bir yola dalar ve oradan çıkması uzun sürer. "Daha çok ağırlık = her zaman daha hızlı" diye bir garanti yoktur.

## A10 — Kurt, keçi, lahana: `alistirma10_kurt_keci_lahana.py`

1. **Durum:** (çiftçi, kurt, keçi, lahana). Her biri 0/1 (hangi kıyıda). 2⁴ = **16** durum var, bunların **10'u güvenli**. Kayığın konumu çiftçininkiyle aynı olduğu için ayrıca tutmaya gerek yok. Bu, iyi bir soyutlama örneğidir.
2. **BFS çözümü (7 geçiş):** keçi → (yalnız dön) → kurt → keçiyi geri getir → lahana → (yalnız dön) → keçi. Püf nokta 4. adım: Keçiyi *geri götürmek*, sezgiye ters ama zorunlu bir hamledir.
3. **Evet, aynı sonucu verir.** Tüm geçişlerin maliyeti 1 olduğu için UCS'nin f = g sıralaması BFS'in derinlik sıralamasıyla aynıdır. İkisi de 7 geçişlik optimal çözümü bulur.
