# A2 çözümü — MRV sezgisi

1. MRV **İç Anadolu**’yu seçer: kalan domain boyutu 1 < 3. En kısıtlı değişkeni önce sabitlemek, boş domaini erken yakalar (fail-first).

2. İki değişkenin kalan domain boyutu eşitse **derece** sezgiseli, atanmamış komşusu en çok olanı seçer; böylece seçim daha fazla değişkene yayılır ve ilerideki tutarsızlıklar daha çabuk ortaya çıkar.
