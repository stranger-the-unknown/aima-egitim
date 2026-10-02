# Çözüm — A3: Akıllı termostat

## 1. Basit refleks yeterli mi?

Klasik termostat zaten bir basit refleks ajanıdır: "Sıcaklık < hedef ise ısıt, değilse kapat." Tek amaç sıcaklığı hedefte tutmaksa bu **yeterlidir**.

Ama soruda üç ölçüt var: sıcaklık, **enerji maliyeti** ve **konfor**. Bu durumda refleks yetmez, çünkü:

- Elektrik fiyatı saate göre değişiyorsa, "şimdi ısıtmak mı, ucuz saatte önceden ısıtmak mı?" sorusu *geleceği* düşünmeyi gerektirir.
- Ev boşken ısıtmak israftır. Evde kimse olmadığını anlamak için geçmiş algılar (hareket sensörü, telefon konumu) gerekir; tek bir algı yetmez.

## 2. Önerilen tür: faydaya dayalı ajan (ve modele dayalı iç durum)

- **Model:** Evin ısınma ve soğuma hızı, dış sıcaklık tahmini, evde kimse var mı.
- **Fayda:** `U = −(konforsuzluk cezası) − (enerji maliyeti)`. Hedefe dayalı bir ajan yalnızca "21 °C'ye ulaştım mı?" diye sorar. Faydaya dayalı ajan ise "20,5 °C'de kalıp 3 TL tasarruf etmek, 21 °C için ödemekten iyi mi?" ödünleşimini hesaplayabilir.
- Birden fazla, birbiriyle çatışan ölçüt olduğu için **fayda** doğal seçimdir.

## 3. Öğrenme neyi iyileştirir?

- Kullanıcının gerçek tercihleri ("sabah 7'de 22 °C istiyor, gece 18 °C yeter") elle yazılmak yerine **gözlemden** öğrenilir.
- Evin fiziksel modeli (ne kadar hızlı ısınıyor) veriden kalibre edilir. Böylece ön ısıtma zamanlaması iyileşir.
- Kullanıcı ayarı elle değiştirdiğinde bu bir **geri bildirim** sinyalidir. Öğrenen ajanın "eleştirmen" parçası bunu kullanır.

> Bağlantı: Tercihleri gözlemden öğrenme fikri, Bölüm 1'deki "amacından emin olmayan makine" tartışmasının küçük bir örneğidir.
