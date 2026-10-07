# Bölüm 23 — Alıştırmalar

Sorular özgündür. Çözümler `cozumler/` klasöründe; önce kendin dene.

Zorluk: ★ kolay · ★★ orta · ★★★ zor

---

## A1 — Bigram sayımı ★

Derlem: "ali okula gitti . ayşe okula gitti . ali kitap okudu ." (her cümle başına `<s>` eklenir).
1. P(okula | ali), P(gitti | okula), P(ali | `<s>`) nedir?
2. P(`<s>` ali okula gitti .) olasılığını bigram modeliyle hesapla.

## A2 — Laplace düzeltmesi ★

1. Yukarıdaki derlemde sözlük `<s>` dahil kaç sözcüktür? Laplace düzeltmesiyle P(okudu | ayşe) nedir?
2. Laplace'ın ardıllık kuralını kullanarak, bir zarın 10 atışında hiç 6 gelmediyse bir sonraki atışta 6 gelmeme olasılığını tahmin et. Bu tahmin neden zar için kötüdür?

## A3 — Şaşkınlık (kod) ★★

"ayşe okulda kitap okudu ." cümlesi için Laplace düzeltmeli 1-, 2-, 3-gram modellerinin ve ara değerlenmiş modelin şaşkınlığını hesapla. Sonuçları yorumla.

## A4 — Naif Bayes sınıflandırma ★★

İki sınıf (ekonomi, hava) ve her birinde ikişer kısa belge var (`dil_modelleri.py`). "borsa bugün yükseldi" cümlesinin sınıf olasılıklarını Laplace düzeltmesiyle elle hesapla. "bugün" sözcüğü hiçbir eğitim belgesinde yoksa ne olur?

## A5 — CYK tablosu (kod) ★★

"the wumpus is dead" için CYK tablosunun bütün dolu hücrelerini (i, j) ve her hücredeki kategorileri, olasılıklarıyla yaz. Hangi hücreler son ayrıştırmada kullanılmıyor?

## A6 — Chomsky normal biçimi ★★

E₀'daki şu kuralları Chomsky normal biçimine çevir:
1. NP → Article Adjs Noun [0.05]
2. S → S Conj S [0.10]
3. NP → Pronoun [0.25] (tekli kural)
Olasılıkların korunduğunu göster.

## A7 — Edat öbeği nereye? (kod) ★★

"I feel the wumpus near 1 3" cümlesinin iki ayrıştırmasının olasılığını E₀ ile hesapla. Hangisi daha olası? Bu sonuç PCFG'lerin hangi zayıflığını gösterir? Nasıl düzeltilir?

## A8 — Ağaç bankasından PCFG (kod) ★★

`ayristirma.py`'deki beş ağaçlık bankadan PCFG'yi çıkar. S → NP VP'nin olasılığı nedir? Bu küçük banka hangi kuralları hiç görmediği için sıfır olasılık verir?

## A9 — Aritmetik dilbilgisi (kod) ★★★

"2 × (3 + 4) − 5", "100 ÷ (2 + 3) ÷ 4" ve "((7))" ifadelerinin anlamını bileşimsel dilbilgisiyle hesapla. "12 − 2 − 3" ifadesi için dilbilgisinin iki ağaç verebileceğini göster; hangisi doğrudur ve kod hangisini seçer?

## A10 — Gerçek dilin zorlukları ★★★

Her biri için bir Türkçe örnek ver ve neden zor olduğunu açıkla:
1. Sözcüksel belirsizlik
2. Sözdizimsel belirsizlik
3. Niceleme belirsizliği
4. Gösterge sözcük
5. Düz değişmece (metonymy)
