# Bölüm 17 — Quiz (5 soru)

Cevaplar dosyanın sonunda.

---

**S1.** MDP’de Markov özelliği neyi söyler?

**S2.** γ indirimi neden kullanılır?

**S3.** Değer yineleme bir adımda ne yapar?

**S4.** Politika değerlendirme ile değer yineleme farkı? (tek cümle)

**S5.** Açgözlü politika V’den nasıl üretilir?

---

## Cevaplar

**S1.** Geleceğin yalnızca şu anki duruma (ve eyleme) bağlı olduğunu; geçmiş yolun ek bilgi taşımadığını.

**S2.** Sonsuz ufukta toplamın yakınsaması / geleceğin biraz daha az ağır olması için.

**S3.** Her durumda Bellman optimal yedeklemesiyle V’yi günceller (max over actions).

**S4.** Değerlendirme sabit π için V^π çözer; değer yineleme doğrudan V*’a (max’lı) yürür.

**S5.** Her s için Q(s,a;V) en yüksek eylemi π(s) yaparak.
