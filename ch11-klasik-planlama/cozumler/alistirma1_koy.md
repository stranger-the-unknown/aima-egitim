# A1 çözümü — Koy(X, Y)

```text
Eylem(Koy(X, Y),
   ÖNKOŞUL: Tutuyor(X) ∧ Clear(Y)
   EKLE:    On(X, Y), ElBos, Clear(X)
   SİL:     Tutuyor(X), Clear(Y))
```

| Silinen | Neden? |
|---|---|
| `Tutuyor(X)` | X artık elde değil, Y'nin üstünde. |
| `Clear(Y)` | Y'nin üstünde X var; başka bir blok Y'nin üstüne konamaz. |

| Eklenen | Neden? |
|---|---|
| `On(X, Y)` | Eylemin amacı. |
| `ElBos` | El serbest kaldı; yeni bir blok kaldırılabilir. |
| `Clear(X)` | X en üstte. `Kaldir` Clear(X)'i silmediği için bu atom zaten durumda kalmış olabilir. Eklemek zararsızdır ve modeli açık tutar. |

Masa için ayrı bir `MasayaKoy(X)` eylemi vardır. Masanın üstü hiç dolmaz, bu yüzden `Clear(Masa)` silinmemelidir. Kitaptaki `MoveToTable` şeması da aynı nedenle ayrıdır.
