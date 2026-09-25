# A2 çözümü — Filtreleme adımı

`hmm_filtreleme.py` çıktısında t=3 (Şemsiye=F) sonrası `P(Yagmur=T)` yaklaşık **0.19** civarıdır
(tam değer çalıştırdığınızdaki satıra bakın; tipik olarak 0.2’nin altında).

Neden düşer: şemsiyesiz gözlem, yağmur hipotezini duyucu modelinde zayıf bırakır; update adımı
yağmur kütlesini küçültür.
