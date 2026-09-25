# A1 çözümü — CPT okuma

Yangın ve sigara yokken **P(Alarm = T) = 0.001**.

Anlamı: Hiçbir neden yokken alarmın kendiliğinden çalma olasılığı (arıza, yanlış alarm) çok düşük ama sıfır değil. Bu sayı, modelde yer almayan bütün nedenleri (böcek, toz, elektrik dalgalanması) özetler.

**Neden 4 sayı?** Alarm Boole değişken ve iki Boole ebeveyni var: 2² = 4 koşullama durumu. Her satırda P(Alarm = F) = 1 − P(Alarm = T) olduğu için yalnızca P(Alarm = T) yazılır. Genel kural: k Boole ebeveynli bir Boole düğüm 2ᵏ bağımsız sayı ister.
