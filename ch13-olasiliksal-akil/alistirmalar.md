# Bölüm 13 — Alıştırmalar

Sorular özgündür. Çözümler `cozumler/` klasöründe; önce kendin dene.

Zorluk: ★ kolay · ★★ orta · ★★★ zor

A1–A2 özgün ofis alarmı ağını kullanır (`ornekler/bayes_agi_kucuk.py`, `ornekler/cpt_goster.py`):
Yangin → Alarm ← SigaraDumanı, Alarm → MudurArar. P(Yangin) = 0.01, P(SigaraDumanı) = 0.05,
P(Alarm | Y, S): TT 0.95, TF 0.88, FT 0.70, FF 0.001; P(MudurArar | Alarm): 0.80 / 0.05.

---

## A1 — CPT okuma ★

Yangın ve sigara dumanı yokken P(Alarm = T) nedir? Bu satır ne anlama gelir? Alarm CPT'sinde neden 4 sayı yeter, 8 değil?

## A2 — Ortak olasılık ★

P(Yangin = T, SigaraDumanı = F, Alarm = T, MudurArar = T)'yi CPT girdilerinin çarpımı olarak yaz ve hesapla.

## A3 — Hırsız ağında bir dünya ★

P(j, ¬m, ¬a, ¬b, ¬e)'yi hesapla. Bu dünya ne anlatıyor? John neden hâlâ arıyor olabilir?

## A4 — Numaralandırma elle ★★

P(Burglary | alarm)'ı elle hesapla. Gizli değişken hangisi? JohnCalls ve MaryCalls neden hesaba girmez?
Sonra P(Burglary | alarm, earthquake)'yi tahmin et ve kodla karşılaştır (`hirsiz_alarmi.py`). Aradaki farkın adı nedir?

## A5 — Bağımsızlıkları oku ★★

Yağmurlama ağında (`ornekler/ornekleme.py`):
1. Sprinkler'ın Markov örtüsü nedir?
2. Sprinkler ⊥ Rain? Sprinkler ⊥ Rain | Cloudy? Sprinkler ⊥ Rain | Cloudy, WetGrass? d-ayrımla gerekçelendir.
3. Cloudy ⊥ WetGrass | Sprinkler, Rain doğru mu?
Cevaplarını tam ortak dağılımdan sayısal olarak doğrula.

## A6 — Ters sıra (kod) ★★

Yağmurlama ağını WetGrass, Sprinkler, Rain, Cloudy sırasıyla yeniden kur (her düğüme öncüllerinden en küçük yeterli ebeveyn kümesini seç). Kaç parametre gerekir? Orijinal sıradaki (9) ile karşılaştır. `hirsiz_alarmi.minimal_ebeveynler` fonksiyonunu kullanabilirsin.

## A7 — Gürültülü-VEYA ★★

Öksürüğün üç nedeni: soğuk algınlığı (q = 0.5), grip (q = 0.3), alerji (q = 0.4).
1. P(öksürük | ¬soğuk, grip, alerji) nedir?
2. Hiçbir neden yokken P(öksürük) nedir? Bu gerçekçi mi?
3. 0.1 olasılıklı bir sızıntı nedeni ekle. İki sorunun cevabı nasıl değişir?

## A8 — İlgisiz değişkenler (kod) ★★

P(Burglary | johnCalls) sorgusunda hangi değişkenler ilgisizdir? Numaralandırma ve değişken elemenin çarpma sayılarını karşılaştır (`BayesAgi.carpma_sayisi`).

## A9 — 3-SAT'ı Bayes ağına indirgemek (kod) ★★★

(A ∨ B ∨ ¬C) ∧ (¬A ∨ C ∨ D) ∧ (B ∨ ¬C ∨ ¬D) ∧ (¬B ∨ ¬D ∨ A) cümlesini Bayes ağına kodla: Değişkenler 0.5 olasılıklı kökler, her cümle deterministik bir VEYA düğümü, S hepsinin VE'si.
1. P(S = true) kaçtır? Cümle karşılanabilir mi?
2. P(S = true) · 2⁴ neyi verir? Kaba kuvvetle doğrula.
3. Bu, Bayes ağında kesin çıkarımın karmaşıklığı hakkında ne söyler?

## A10 — Örnekleme yöntemlerini karşılaştır (kod) ★★★

Hırsız ağında P(Burglary | johnCalls, maryCalls) için N = 10 000 ve 100 000 örnekle ret örneklemesi, olabilirlik ağırlıklandırma ve Gibbs örneklemesi çalıştır.
1. Ret örneklemesinde kaç örnek kabul edildi? Neden bu kadar az?
2. Hangi yöntem kesin değere (0.284) en yakın? Neden?
3. Kanıt ağın yapraklarında. Bu olabilirlik ağırlıklandırmayı nasıl etkiler?
