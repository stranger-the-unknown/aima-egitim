# A2 çözümü — Potansiyel alan yolu

Varsayılan parametrelerde yol engel hücrelerine girmeden hedefe (`G`) ulaşmalıdır; durum mesajı `hedefe_ulasti` olur.

- **`K_rep` artarsa:** engellerden daha erken / daha güçlü kaçış; yol uzayabilir, dar geçitlerde yerel minimum riski artabilir.
- **`D0` artarsa:** itme daha uzaktan başlar; engel “şişmesi” büyür.
- **`K_attr` artarsa:** hedefe çekim baskın gelir; engellere daha yakın geçişler görülebilir.

Potansiyel alanların bilinen zayıf yanı yerel minimumdur; A* gibi global planlayıcılarla karşılaştırma iyi bir sonraki adımdır (Ch.03).
