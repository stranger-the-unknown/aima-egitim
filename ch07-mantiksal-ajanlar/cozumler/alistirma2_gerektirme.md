# A2 çözümü — Gerektirme

Modeller: `(P,Q)` ∈ {FF, FT, TF, TT}.

KB = {P, P⇒Q} yalnızca **TT** modelinde doğru (P doğru ve Q doğru olmalı; P⇒Q için Q şart).

1. **Evet**, KB ⊨ Q — KB’nin tek modelinde Q doğru.
2. **Evet**, KB ⊨ P∧Q — aynı modelde ikisi de doğru.
3. **Hayır**, KB ⊨ ¬P değil — o modelde P doğru; ¬P yanlış.
