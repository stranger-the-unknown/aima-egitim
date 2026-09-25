# Bölüm 20 — Alıştırmalar

Özgün sorular. Kitap metnini kopyalamayın.

---

## A1 — MLE sezgisi

Bir madeni para 10 kez atıldı; 7 yazı, 3 tura. θ = P(yazı) için θ_MLE nedir?
Aynı veride Beta(2, 2) önseli ile θ_MAP kabaca nasıl değişir? (formül veya sayı)

## A2 — Kod: Bernoulli MLE

```bash
python ornekler/mle_beta_Bernoulli.py
```

Çıktıdaki MLE ile MAP’i karşılaştırın. α=β büyüdükçe MAP nereye gider? N büyüdükçe?

## A3 — EM demosu

```bash
python ornekler/em_karisim_mini.py
```

E adımında “sorumluluk” ne anlama geliyor? Birkaç iterasyon sonra θ tahminleri nasıl değişiyor?

## A4 — Tam vs eksik veri

Hangi durumda doğrudan MLE yeter, hangi durumda EM’e ihtiyaç duyarsınız? Kendi cümlelerinizle bir örnek verin.

## A5 — Bayesyen vs nokta tahmin

Tek bir θ̂ (MLE/MAP) kullanmak ile sonradan dağılımı entegre etmek arasında pratik fark nedir? Küçük veri setinde hangisi daha temkinli davranır, neden?
