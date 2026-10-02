# Bölüm 14 — Alıştırmalar

Sorular özgündür. Çözümler `cozumler/` klasöründe; önce kendin dene.

Zorluk: ★ kolay · ★★ orta · ★★★ zor

Şemsiye dünyası: P(R_t | R_{t−1}) = 0.7 / 0.3, P(U_t | R_t) = 0.9 / 0.2, P(R_0) = ⟨0.5, 0.5⟩.

---

## A1 — Geçiş mi, algılayıcı mı? ★

1. Geçiş modeli hangi soruyu yanıtlar? Algılayıcı modeli hangisini?
2. `ornekler/zamansal.py`'deki `semsiye_hmm()` içinde hangisi `T`, hangisi `sensor`?
3. Birinci dereceden Markov varsayımı şemsiye dünyasında neden yalnızca bir yaklaşımdır? Nasıl iyileştirilir?

## A2 — Filtreleme elle ★

P(R_2 | u_1, u_2) = ⟨0.883, 0.117⟩ biliniyor. 3. gün şemsiye **yok**. P(R_3 | u_1, u_2, ¬u_3)'ü tahmin ve güncelleme adımlarıyla hesapla. Neden bu kadar düştü?

## A3 — Dört görev ★

Filtreleme, tahmin, yumuşatma ve en olası açıklama için birer cümle ve günlük hayattan birer örnek yaz.

## A4 — Yumuşatma elle ★★

Gözlemler: u_1, u_2, ¬u_3.
1. Geri mesaj b_{3:3}'ü hesapla.
2. P(R_2 | u_1, u_2, ¬u_3)'ü hesapla. Filtrelenmiş P(R_2 | u_1, u_2) = 0.883 ile karşılaştır.

## A5 — Viterbi ile adım adım en olası durum (kod) ★★

Şemsiye dünyasında, Viterbi'nin en olası dizisinin, her günün yumuşatılmış dağılımındaki en olası durumlardan **farklı** olduğu en kısa gözlem dizisini bul. Farkı sezgisel olarak açıkla.

## A6 — Karışma süresi (kod) ★★

Tahmin, başlangıçta "kesin yağmur" (⟨1, 0⟩) iken durağan dağılımın 0.01 yakınına kaç adımda ulaşır?
1. Geçiş 0.7 / 0.3 (kitaptaki model)
2. Geçiş 0.9 / 0.1 (hava inatçı)
3. P(yağmur | dün yağmur) = 0.7, P(yağmur | dün kuru) = 0.2. Durağan dağılım nedir?

## A7 — Kalman ikinci adım ★★

Kitaptaki örnekten devam et: P(x_1 | z_1) = N(2.155, 0.862), σx² = 4, σz² = 1. İkinci gözlem z_2 = 1.0.
1. μ_2 ve σ_2²'yi hesapla.
2. σz → ∞ ve σz → 0 limitlerinde μ_{t+1} ne olur? Sezgisel olarak açıkla.

## A8 — Uzun koridor (kod) ★★

`ornekler/lokalizasyon.py`'yi 7 karelik tek sıralı bir koridorla çalıştır ("......."), ε = 0.
1. Algılayıcı hatasızken bile robot yerini kesin bilebilir mi? Neden?
2. İnanç dağılımında hangi ilginç yapıyı görüyorsun? (İpucu: Robot her adımda mutlaka bir kare hareket ediyor.)

## A9 — Parçacık filtresiyle konumlandırma (kod) ★★★

Herhangi bir HMM için genel bir parçacık filtresi yaz (geçiş satırından örnekle, algılayıcıyla ağırlıklandır, yeniden örnekle). `lokalizasyon.py`'nin labirentinde ε = 0.1 ile N = 20, 100, 1000 parçacığın beklenen konum hatasını kesin filtreyle karşılaştır.

## A10 — Hangi model? (kod) ★★★

Şemsiye gözlemlerini "inatçı hava" modelinden (0.9 / 0.1) üret. Sonra P(yağmur | dün yağmur) ∈ {0.5, 0.7, 0.9, 0.95} olan dört modelin log-olabilirliğini log P(e_{1:t}) hesapla.
1. 60 günlük veride hangi model kazanıyor?
2. 500 günlük veride?
3. Bu, zamansal modelleri veriden öğrenmek hakkında ne söyler?
