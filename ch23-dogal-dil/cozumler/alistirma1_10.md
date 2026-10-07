# A1–A10 çözümleri

Kodlu kısımlar: `python cozumler/alistirma_kod.py` (bölüm klasöründen).

---

## A1 — Bigram sayımı

Bigramlar (her cümle `<s>` ile başlar): `<s>` ali (2), ali okula (1), okula gitti (2), gitti . (2), `<s>` ayşe (1), ayşe okula (1), ali kitap (1), kitap okudu (1), okudu . (1).
1. P(okula | ali) = 1/2, P(gitti | okula) = 2/2 = **1**, P(ali | `<s>`) = 2/3.
2. P = P(ali | `<s>`) · P(okula | ali) · P(gitti | okula) · P(. | gitti) = 2/3 · 1/2 · 1 · 1 = **1/3**.

## A2 — Laplace düzeltmesi

1. Sözlük: ali, okula, gitti, ., ayşe, kitap, okudu, `<s>` → **8** sözcük. "ayşe" bağlamı 1 kez geçer, "ayşe okudu" hiç: P = (0 + 1)/(1 + 8) = **1/9**.
2. Ardıllık kuralı: 10 kez "6 gelmedi" görülmüş → 6 gelmeme olasılığı (10 + 1)/(10 + 2) ≈ 0.92, 6 gelme 1/12 ≈ 0.083. Zarın altı yüzü olduğunu biliyoruz: Önsel bilgi gerçek olasılığı (1/6) verir; Laplace yalnızca iki sonuçlu bir olay varsayar ve bu bilgiyi kullanmaz.

## A3 — Şaşkınlık

| Model | Şaşkınlık |
|---|---|
| 1-gram (Laplace) | 11.15 |
| 2-gram (Laplace) | 5.24 |
| 3-gram (Laplace) | 6.99 |
| Ara değerleme 0.6/0.3/0.1 | **2.58** |

Bigram unigramdan çok daha iyi (sözcük sırası bilgisi). Laplace'lı trigram bigramdan kötü: Bu küçük derlemde çoğu üçlü görülmemiştir ve Laplace onlara çok fazla olasılık kütlesi dağıtır. Ara değerleme, var olan trigram bilgisini kullanır, yoksa bigram ve unigrama dayanır: en iyisi.

## A4 — Naif Bayes sınıflandırma

Sözlük 11 sözcük; ekonomi sınıfında 8 sözcük (borsa 2, yükseldi 2, faiz 1, düştü 2, dolar 1), hava sınıfında 8 sözcük. Laplace, bilinmeyen sözcük için bir yer daha ayırarak (payda 8 + 11 + 1 = 20):
- Ekonomi: 0.5 · (2+1)/20 · (0+1)/20 · (2+1)/20
- Hava: 0.5 · (0+1)/20 · (0+1)/20 · (0+1)/20
- Oran 9 : 1 → P(ekonomi) ≈ **0.90**, P(hava) ≈ 0.10 (kodla aynı).

"bugün" iki sınıfta da görülmediği için her iki sınıfta aynı çarpanı (1/20) ekler ve oranı değiştirmez. Düzeltme olmasaydı iki sınıfın olasılığı da sıfır olurdu.

## A5 — CYK tablosu

| (i, j) | Kategoriler |
|---|---|
| (0,1) the | Article 0.4 |
| (1,2) wumpus | Noun 0.15, NP 0.015 |
| (2,3) is | Verb 0.1, VP 0.04 |
| (3,4) dead | Adjective 0.05, Adjs 0.04 |
| (0,2) | NP 0.015 |
| (2,4) | VP 0.0001 |
| (1,3) | S 0.00054 |
| (0,3) | S 0.00054 |
| (1,4) | S 1.35 × 10⁻⁶ |
| (0,4) | **S 1.35 × 10⁻⁶** |

Son ağaçta kullanılmayanlar: (1,2)'deki tek başına NP ("wumpus"), (3,4)'teki Adjs, (1,3), (0,3) ve (1,4)'teki S'ler. CYK bütün alt öbekleri hesaplar, çoğu sonunda işe yaramaz. (Not: (0,3)'teki S değeri, aynı olasılığa sahip "wumpus is" ayrıştırmasından gelir; ikisi eşit olduğu için ilk bulunan tutulur.)

## A6 — Chomsky normal biçimi

1. NP → Article X [0.05], X → Adjs Noun [1.0]. Çarpım 0.05 · 1.0 = 0.05: korunur.
2. S → S Y [0.10], Y → Conj S [1.0].
3. Tekli kural NP → Pronoun [0.25] kaldırılıp her Pronoun sözcüğü için NP → sözcük [0.25 · P(sözcük | Pronoun)] eklenir: NP → I [0.025], NP → it [0.025], … Kodumuz bunun yerine her hücrede tekli kural kapanışı uygular; sonuç aynıdır.

## A7 — Edat öbeği nereye?

- VP'ye bağlı: [S [NP I] [VP [VP feel [NP the wumpus]] [PP near 1 3]]]
- NP'ye bağlı: [S [NP I] [VP feel [NP [NP the wumpus] [PP near 1 3]]]]

İkisinin olasılığı da **9.45 × 10⁻¹¹**: VP → VP PP ve NP → NP PP aynı olasılığa (0.10) sahip ve geri kalan kurallar ortak. PCFG bağlamdan bağımsız olduğu için "feel" fiilinin ya da "wumpus" adının edat öbeğiyle ne kadar sık birlikte geçtiğini hesaba katamaz. Çözüm: **sözcükselleştirilmiş** PCFG (olasılıklar başsözcüğe bağlı) ya da sinir ağı tabanlı ayrıştırıcılar.

## A8 — Ağaç bankasından PCFG

S düğümleri 7 kez geçer (5 kök + 2 iç içe); 6'sı NP VP → **6/7 ≈ 0.86**, 1'i S Conj S → 0.14. Görülmeyen kurallar (sıfır olasılık): NP → Digit Digit, NP → NP PP, NP → Article Adjs Noun, VP → VP PP, VP → VP Adjective, RelClause kuralları vb. Gerçek ağaç bankası 100 000'den fazla cümle içerir; yine de seyrek kurallar için düzeltme gerekir.

## A9 — Aritmetik dilbilgisi

2 × (3 + 4) − 5 = **9**; 100 ÷ (2 + 3) ÷ 4 = **5**; ((7)) = **7**.

"12 − 2 − 3": Exp(op(x₁, x₂)) → Exp Operator Exp kuralı iki ağaca izin verir: ((12 − 2) − 3) = 7 ve (12 − (2 − 3)) = 13. Dilbilgisi tek başına belirsizdir; aritmetik geleneği **sola bağlı** okumayı (7) seçer. Kodumuz da işlem önceliği ve sola bağlılık kuralıyla 7 verir.

## A10 — Gerçek dilin zorlukları

1. **Sözcüksel:** "Yüz" (sayı / surat / yüzmek fiili). "Gülü yüz kez kokladı" ile "Yüzü kızardı".
2. **Sözdizimsel:** "Yaşlı adam ve kadın geldi": Kadın da yaşlı mı?
3. **Niceleme:** "Her öğrenci bir kitap okudu": Aynı kitap mı, herkes farklı mı?
4. **Gösterge sözcük:** "Ben yarın burada olacağım": "ben", "yarın" ve "burada" kimin ne zaman nerede söylediğine bağlı.
5. **Düz değişmece:** "Ankara yeni bir açıklama yaptı": Şehir değil, hükümet kastediliyor.

Hepsinde doğru anlamı seçmek için dünya bilgisi, bağlam ve konuşanın niyeti gerekir; yalnızca dilbilgisi yetmez.
