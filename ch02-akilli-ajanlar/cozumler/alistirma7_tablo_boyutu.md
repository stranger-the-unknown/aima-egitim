# Çözüm — A7: Tablo ne kadar büyük?

Formül: `satır(P, T) = P + P² + … + P^T = (P^(T+1) − P) / (P − 1)`

## 1. |P| = 4 için bir milyon ne zaman aşılır?

| T | satır sayısı |
|---|---|
| 9 | 349.524 |
| **10** | **1.398.100** |

İlk kez **T = 10** adımda bir milyonu aşar. Yalnızca 10 adımlık bir süpürge için bile tablo bir milyondan fazla satır tutar.

## 2. Saat algısı eklenince (|P| = 96, T = 10)

`satır(96, 10) = 67.183.087.426.509.579.360 ≈ 6,7 × 10¹⁹`

Algı sayısının 24 katına çıkması, tabloyu yaklaşık **24¹⁰ ≈ 6 × 10¹³** kat büyüttü. Tablo algı sayısında **polinom**, yaşam süresinde **üstel** büyür.

## 3. Birkaç satırlık program neden yetiyor?

Refleks kuralı yalnızca **son algıya** bakıyor: "Kirliyse süpür, değilse diğer odaya git." Tablodaki milyonlarca satır aslında aynı dört kuralı tekrar ediyor. Program bu **düzenliliği** sıkıştırıyor.

Tablo ile program arasındaki fark şudur: Tablo fonksiyonu *numaralandırır*, program ise onu *hesaplar*. AI'nin hedefi, işe yarayan fonksiyonları, düzenliliklerinden yararlanan kısa programlarla yazmaktır.
