# Çözümler — A3, A4, A5

## A3 — Algoritma seçimi

| # | Durum | Algoritma | Gerekçe |
|---|---|---|---|
| 1 | Eşit maliyet, en az adım, bellek bol | **BFS** | Birim maliyette optimaldir ve basittir. |
| 2 | Farklı km'ler, sezgisel yok | **UCS** | f = g ile en ucuz yolu garanti eder. |
| 3 | İyi ve kabul edilebilir sezgisel var | **A\*** | Optimal kalır, sezgisel sayesinde çok daha az düğüm genişletir. |
| 4 | Dev uzay, derinlik bilinmiyor, bellek kısıtlı | **IDS** (sezgisel varsa **IDA\***) | Bellek O(bd); birim maliyette optimaldir. |
| 5 | Hızlı çözüm yeter | **Açgözlü** ya da **ağırlıklı A\*** | Daha az düğüm; ağırlıklı A* ayrıca W·C* sınırı verir. |

## A4 — Romanya kodu

1. UCS ve A* ikisi de **418 km** buldu. İkisi de optimaldir: UCS her zaman, A* ise h (SLD) kabul edilebilir olduğu için.
2. UCS **12**, A* **5** düğüm genişletti. A*, f = g + h > C* = 418 olan düğümleri hiç genişletmez. SLD, "yanlış yöne" giden şehirlerin (Zerind, Timisoara, Oradea…) f değerini 418'in üstüne çıkararak onları budar.
3. BFS, Arad → Sibiu → Fagaras → Bucharest yolunu (3 kenar, **450 km**) buldu. BFS kenar sayısını en aza indirir. 4 kenarlı ama 418 km'lik yol, BFS için "daha derin" olduğu için ikinci plandadır.
4. Bucharest ilk kez **f = 450** ile sınıra girer (Fagaras genişletilince). A* onu hemen kabul etmez, çünkü sınırda f = 417 olan Pitesti vardır; yani 450'den daha ucuz bir yol hâlâ mümkündür. Hedef testi kuyruktan *çıkarken* yapıldığı için 450'lik yol hiçbir zaman döndürülmez.

## A5 — Iasi için sezgisel

1. h = 0 ile f = g olur: A* **UCS**'e dönüşür.
2. En doğrudan yol, her şehrin **Iasi'ye kuş uçuşu uzaklığını** koordinatlardan hesaplamaktır. Yol, iki nokta arasındaki düz çizgiden kısa olamaz; bu yüzden kabul edilebilirdir.
3. **Evet, kabul edilebilirdir** (ve tutarlıdır). Üçgen eşitsizliğine göre, n ile Iasi arasındaki kuş uçuşu mesafe en az |SLD(n) − SLD(Iasi)| kadardır. Yol mesafesi de kuş uçuşu mesafeden kısa olamaz. Bu fikir, notlardaki **yer imi** (*landmark*) sezgiselinin ta kendisidir: Bucharest bir yer imi gibi kullanılır. Genelde zayıf bir sezgiseldir (bazı şehirler için 0'a yakın), ama tek bir tablo ile *her* hedef için kabul edilebilir bir tahmin verir. Birkaç yer imi kullanıp en büyüğünü almak onu güçlendirir.
