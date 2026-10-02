# Bölüm 22 — Pekiştirmeli öğrenme

> AIMA 4. baskı, Bölüm 22 · *Reinforcement Learning*

## Öğrenme hedefleri

1. Pekiştirmeli öğrenmeyi denetimli öğrenmeden ayırt etmek; model tabanlı ve modelsiz yaklaşımları karşılaştırmak.
2. Sabit bir politikanın faydalarını doğrudan kestirim, ADP ve TD ile öğrenmek.
3. Keşif–sömürü dengesini, keşif fonksiyonlarını ve GLIE'yi açıklamak.
4. Q-öğrenme ve SARSA'yı uygulamak ve karşılaştırmak.
5. İşlev yaklaşımını ve politika aramasını tanımak.
6. Taklit öğrenme ve ters pekiştirmeli öğrenmeyi açıklamak.

## Çalışma sırası

1. Kitapta Bölüm 22'yi oku (önce Bölüm 17'yi bitirmiş ol).
2. [`notlar.md`](notlar.md)
3. Örnekleri çalıştır.
4. [`alistirmalar.md`](alistirmalar.md) → [`cozumler/`](cozumler/)
5. [`quiz.md`](quiz.md)

## Dosyalar

| Dosya | İçerik |
|---|---|
| `ornekler/pasif_ogrenme.py` | Kitabın üç denemesi; doğrudan fayda kestirimi, ADP, TD; benzetimle karşılaştırma |
| `ornekler/aktif_ogrenme.py` | Açgözlü ve keşifçi ADP (R⁺ = 2, Nₑ = 5), Q-öğrenme (keşif fonksiyonu ve GLIE), SARSA |
| `ornekler/yaklasik_ve_politika.py` | Doğrusal işlev yaklaşımı, delta kuralı, TD + yaklaşım, REINFORCE |
| `alistirmalar.md` | 10 alıştırma |
| `cozumler/` | Tüm çözümler (A2, A3, A6, A8, A9 kod) |
| `quiz.md` | 12 soru + cevaplar |

Örnekler Bölüm 17'nin `ch17-karmasik-kararlar/ornekler/mdp.py` kütüphanesini kullanır.

## Kitapla doğrulama

`tests/test_ch22_pekistirmeli.py`:

| Değer | Kitap | Kod |
|---|---|---|
| 1. denemede ödül-kalan | (1,1) 0.76; (1,2) 0.80, 0.88; (1,3) 0.84, 0.92 | ✔ |
| ADP: (3,3)'te Sağ | 4 kez; P̂ = 1/2 | ✔ |
| TD örneği | U(1,3): 0.84 → hedef 0.92 | ✔ |
| Pasif yöntemler | Şekil 17.3 faydalarına yakınsar | ✔ |
| Keşifçi ADP | sıfıra yakın politika kaybı | ✔ |
| Doğrusal yaklaşım | θ = (0.5, 0.2, 0.1) → Û(1,1) = 0.8; u = 0.4 iken θ'lar 0.4α azalır | ✔ |
