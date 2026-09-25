# A2 çözümü — Birleştirme

1. `f(?x)` ↔ `f(Ankara)` → `{ ?x / Ankara }`
2. `f(?x)` ↔ `g(Ankara)` → **BAŞARISIZ** (functor farklı)
3. `?x` ↔ `f(?x)` → **BAŞARISIZ** (occurs-check: değişken kendi içinde geçen terime bağlanamaz)
