# A1 çözümü — Yerel arama ne zaman?

**Cevap: Senaryo 2.**

Senaryo 1’de *yol* ürünün kendisi: hangi şehirlerden geçtiğimiz önemli; Bölüm 3 tarzı (BFS/UCS/A*) uygundur.

Senaryo 2’de ara yollar değil, **geçerli bir final atama** önemli. Durum uzayı devasa olabilir; bellekte tüm arama ağacını tutmak gerekmez. Mevcut atamayı komşu atamalara (ders yerini değiştirmek gibi) kaydırarak iyileştirmek — yani yerel arama — daha doğal bir çerçevedir.
