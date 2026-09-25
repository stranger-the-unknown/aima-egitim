# A2 çözümü — Bir adım ileri

`strips_bloklar.py`'deki tanım:

```text
Kaldir(A, Masa):  ÖNKOŞUL On(A,Masa), Clear(A), ElBos
                  SİL     On(A,Masa), ElBos
                  EKLE    Tutuyor(A)          (Y masa olduğu için Clear(Masa) eklenmez)
```

Önkoşullar başlangıçta sağlanıyor. SONUÇ(s, a) = (s − SİL) ∪ EKLE:

| | Atomlar |
|---|---|
| Silinen | `On(A,Masa)`, `ElBos` |
| Eklenen | `Tutuyor(A)` |
| Değişmeyen | `On(B,Masa)`, `Clear(A)`, `Clear(B)` |

**Yeni durum:** `{On(B,Masa), Clear(A), Clear(B), Tutuyor(A)}`

Not: `Clear(A)` durumda kalır, çünkü A'nın üstünde hâlâ hiçbir şey yok. Bu modelde `Clear(X)`, "X'in üstü boş" anlamına gelir; X'in nerede olduğunu söylemez. `ElBos` olmadığı için şimdi başka bir blok kaldırılamaz; yalnızca `Koy(A, B)` ya da `MasayaKoy(A)` uygulanabilir.

Kodla doğrulama:

```python
from strips_bloklar import bloklar_aksiyonlari
s = frozenset({"On(A, Masa)", "On(B, Masa)", "Clear(A)", "Clear(B)", "ElBos"})
a = next(x for x in bloklar_aksiyonlari(["A", "B"]) if x.ad == "Kaldir(A, Masa)")
print(sorted(a.uygula(s)))   # ['Clear(A)', 'Clear(B)', 'On(B, Masa)', 'Tutuyor(A)']
```
