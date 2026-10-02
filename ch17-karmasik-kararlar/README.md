# Bölüm 17 — Karmaşık kararlar almak

> AIMA 4. baskı, Bölüm 17 · *Making Complex Decisions*

## Öğrenme hedefleri

1. Bir sıralı karar problemini MDP olarak tanımlamak.
2. İndirimli toplamsal ödülü ve neden kullanıldığını açıklamak.
3. Bellman denklemini yazmak; değer yinelemesi ve politika yinelemesiyle çözmek.
4. Değer yinelemesinin neden yakınsadığını ve hata sınırlarını yorumlamak.
5. Ödül şekillendirmenin en iyi politikayı neden değiştirmediğini göstermek.
6. Haydut problemlerinde keşif–sömürü dengesini ve Gittins indeksini açıklamak.
7. POMDP'de inanç durumunu güncellemek ve faydanın inanç üzerindeki biçimini yorumlamak.

## Çalışma sırası

1. Kitapta Bölüm 17'yi oku.
2. [`notlar.md`](notlar.md)
3. Örnekleri çalıştır.
4. [`alistirmalar.md`](alistirmalar.md) → [`cozumler/`](cozumler/)
5. [`quiz.md`](quiz.md)

## Dosyalar

| Dosya | İçerik |
|---|---|
| `ornekler/mdp.py` | MDP kütüphanesi: 4 × 3 dünya, değer yinelemesi, politika değerlendirme ve yinelemesi |
| `ornekler/dort_uc_dunya.py` | Şekil 17.3, r'ye göre 9 politika, sonlu ufuk, indirim, şekillendirme teoremi |
| `ornekler/deger_yineleme.py` | Fayda hatası ve politika kaybı, büzülme, yineleme sınırları |
| `ornekler/politika_yineleme.py` | Politika yinelemesi, değiştirilmiş PI, LP kısıtları, beklenti-maks, ε-ufku |
| `ornekler/haydut.py` | Gittins indeksi, yeniden başlatma MDP'si, Bernoulli haydudu, UCB, Thompson |
| `ornekler/pomdp.py` | İki durumlu POMDP: inanç güncellemesi, α-vektörleri, baskın plan budama |
| `alistirmalar.md` | 10 alıştırma |
| `cozumler/` | Tüm çözümler (A2, A4, A5, A7–A10 kod) |
| `quiz.md` | 12 soru + cevaplar |

## Kitapla doğrulama

`tests/test_ch17_mdp.py`:

| Değer | Kitap | Kod |
|---|---|---|
| Diziyle hedefe ulaşma | 0.32776 | ✔ |
| Şekil 17.3 faydaları (γ = 1, r = −0.04) | 0.8516 … 0.4279 | ✔ (değer ve politika yinelemesiyle) |
| Politikanın değiştiği r değerleri, politika sayısı | −1.6497, −0.7311, −0.4526, −0.0850, −0.0273; 9 | ✔ |
| Sonlu ufuk, (3,1) | N = 3 → Yukarı, N = 100 → Sol | ✔ |
| γ = 0.9: politika en iyi iken fayda hatası | ~0.51 | ✔ |
| ε-ufku | γ = 0.5 → 5, γ = 0.9 → 44 | ✔ |
| Deterministik haydut | 1.9, 2.0, 2.025; Gittins 1.0133; yeniden başlatma 2.0266 | ✔ |
| Bernoulli Gittins (3,2) > (7,4) | 0.7057 > 0.6922 | ✔ sıralama; bizde 0.7072 > 0.6940 |
| İki durumlu POMDP | α[Kal] = (0.1, 0.9); derinlik 2'de 4, derinlik 8'de 144 plan | ✔ |

Notlarda iki ayrıntı açıklandı: Kitabın "(3,1)'de iki eylem eşit" ifadesi yalnızca r ≈ −0.0448'de doğrudur; Bernoulli indekslerinde kitapla aramızda ~0.002 fark vardır.
